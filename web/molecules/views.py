import os
import shutil
from shutil import make_archive
from wsgiref.util import FileWrapper

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from typing import Any

from molecules.excel.resources import ComplexResource
from molecules.excel.utils import binary_excel_to_df, df_to_dataset, collect_excel_import_errors
from molecules.models import Complex
from molecules.serializers import ComplexSerializer
from pdbs.create_protein_ligand_files import split_complex_file
from pdbs.update_complex_pdb_file import update_complex_file
from utils.get_files_to_zip import download_file, create_dir_with_structure_files
from utils.media_renderer import PassthroughRenderer


class ComplexViewSet(viewsets.ModelViewSet):
    queryset = Complex.objects.all().order_by('pdb_id')
    serializer_class = ComplexSerializer
    renderer_classes = (TemplateHTMLRenderer,)
    parser_classes = (MultiPartParser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('pdb_id', 'protein__name', 'ligand__name', 'residence_time',)
    lookup_field = 'pdb_id'

    def list(self, request: Request, *args: Any, **kwargs: Any):
        response = super().list(request, *args, **kwargs)
        return Response({'object_list': response.data}, template_name='main.html', status=status.HTTP_200_OK)

    @action(methods=('get', 'post',), detail=False)
    def add(self, request: Request, *args: Any, **kwargs: Any):
        if request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return HttpResponseRedirect(redirect_to=reverse('molecules:complex-list'))
        serializer = self.get_serializer()
        return Response({'serializer': serializer}, template_name='add_complex.html', status=status.HTTP_201_CREATED)

    def retrieve(self, request: Request, *args: Any, **kwargs: Any):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'object': instance, 'data': serializer.data}, template_name='complex_detail.html')

    @action(methods=('post', 'get',), detail=True)
    def delete(self, request: Request, **kwargs: Any):
        instance = self.get_object()
        if request.method == 'POST':
            self.perform_destroy(instance=instance)
            return HttpResponseRedirect(redirect_to=reverse('molecules:complex-list'))
        return Response({'object': instance}, template_name='confirm_delete.html')

    @action(methods=('get',), detail=True, renderer_classes=(PassthroughRenderer,),
            url_path='download/(?P<obj_type>[a-z]+)')
    def download(self, request: Request, obj_type: str, *args: Any, **kwargs: Any):
        instance = self.get_object()

        if obj_type == 'complex' and instance.file:
            return download_file(instance=instance)
        elif obj_type == 'ligand' and instance.ligand.file:
            return download_file(instance=instance.ligand)
        elif obj_type == 'protein' and instance.protein.file:
            return download_file(instance=instance.protein)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=('post', 'get',), detail=False, url_path='export-data')
    def export_data(self, request: Request):
        if request.method == 'POST':
            file_format = request.POST['file-format']
            employee_resource = ComplexResource()
            dataset = employee_resource.export()
            if file_format == 'CSV':
                response = HttpResponse(dataset.csv, content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="residence_time_data.csv"'
                return response
            elif file_format == 'JSON':
                response = HttpResponse(dataset.json, content_type='application/json')
                response['Content-Disposition'] = 'attachment; filename="residence_time_data.json"'
                return response
            elif file_format == 'XLSX (Excel)':
                response = HttpResponse(dataset.xlsx,
                                        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename="residence_time_data.xlsx"'
                return response
        return render(request, 'export.html')

    @action(methods=('post', 'get',), detail=False, url_path='import-data')
    def import_data(self, request: Request, **kwargs: Any):

        if request.method == 'POST':
            excel_data = request.FILES['file'].read()
            df = binary_excel_to_df(excel_data)
            dataset = df_to_dataset(df)

            result = ComplexResource().import_data(dataset, dry_run=True)

            errors = collect_excel_import_errors(result)
            print(errors)

            if not errors:
                ComplexResource().import_data(dataset, dry_run=False)
                update_complex_file()
                split_complex_file()
                return HttpResponseRedirect(redirect_to=reverse('molecules:complex-list'))

        return Response(template_name='import.html')

    @action(methods=('get',), detail=False, url_path='download-zip/(?P<mode>[a-zA-Z0-9]+)')
    def download_zip(self, request: Request, mode, *args: Any, **kwargs: Any):
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'structures'), ignore_errors=True)

        if mode == 'all':
            create_dir_with_structure_files(queryset=Complex.objects.all())
            files_path = os.path.join(settings.MEDIA_ROOT, 'structures')
            filename = 'structures'
        else:
            queryset = Complex.objects.filter(pdb_id=mode)
            create_dir_with_structure_files(queryset=queryset)
            filename = queryset[0].pdb_id
            files_path = os.path.join(settings.MEDIA_ROOT, 'structures', filename)

        path_to_zip = make_archive(files_path, 'zip', files_path)
        response = HttpResponse(FileWrapper(open(path_to_zip, 'rb')), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{filename}.zip"'
        return response
