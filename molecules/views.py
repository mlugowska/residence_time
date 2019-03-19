from typing import Any

from django.http import FileResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy

from molecules.models import Complex
from molecules.serializers import ComplexSerializer
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
            serializer.save()
            return HttpResponseRedirect(redirect_to=reverse('molecules:complex-list'))
        serializer = self.get_serializer()
        return Response({'serializer': serializer}, template_name='add_complex.html', status=status.HTTP_201_CREATED)

    def retrieve(self, request: Request, *args: Any, **kwargs: Any):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'object': instance, 'data': serializer.data}, template_name='complex_detail.html')

    @action(methods=['get'], detail=True, renderer_classes=(PassthroughRenderer,))
    def download(self, request: Request, *args: Any, **kwargs: Any):
        instance = self.get_object()
        if instance.file:
            file_handle = instance.file.open()
            response = FileResponse(file_handle, content_type='whatever')
            response['Content-Length'] = instance.file.size
            dir, slash, name = instance.file.name.rpartition('/')
            response['Content-Disposition'] = f'attachment; filename={name}'
            return response
        return Response(status=status.HTTP_404_NOT_FOUND)


class ComplexDeleteView(generic.DeleteView):
    model = Complex
    template_name = 'confirm_delete.html'
    slug_field = 'pdb_id'
    slug_url_kwarg = 'pdb_id'
    success_url = reverse_lazy('molecules:complex-list')
