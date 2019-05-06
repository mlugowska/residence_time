import os
import shutil
from shutil import make_archive
from typing import Any
from wsgiref.util import FileWrapper

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from molecules.excel.resources import ComplexResource
from molecules.excel.update_instance_from_import import update_complex_file
from molecules.excel.utils import binary_excel_to_df, df_to_dataset
from molecules.models import Complex
from molecules.serializers import ComplexSerializer
from utils.get_files import download_file, create_dir_with_structure_files
from utils.media_renderer import PassthroughRenderer


class ComplexViewSet(viewsets.ModelViewSet):
    queryset = Complex.objects.all()
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
    def delete(self, request, **kwargs):
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

    @action(methods=('get',), detail=False, url_path='export-data')
    def export_data(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        dataset = ComplexResource().export(queryset=queryset)
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="complexes.xls"'
        return response

    @action(methods=('post', 'get',), detail=False, url_path='import-data')
    def import_data(self, request, **kwargs):
        if request.method == 'POST':
            excel_data = request.FILES['file'].read()
            df = binary_excel_to_df(excel_data)
            dataset = df_to_dataset(df)

            result = ComplexResource().import_data(dataset, dry_run=True)
            if not result.has_errors():
                ComplexResource().import_data(dataset, dry_run=False)
                update_complex_file()
                return HttpResponseRedirect(redirect_to=reverse('molecules:complex-list'))

        return Response(template_name='import.html')

    @action(methods=('get',), detail=False, url_path='download-zip')
    def download_zip(self, request):
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'structures'), ignore_errors=True)
        create_dir_with_structure_files(queryset=Complex.objects.all())

        files_path = os.path.join(settings.MEDIA_ROOT, 'structures')
        path_to_zip = make_archive(files_path, 'zip', files_path)
        response = HttpResponse(FileWrapper(open(path_to_zip, 'rb')), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="structures.zip"'
        return response
