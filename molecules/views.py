from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer, BrowsableAPIRenderer

from molecules.models import Complex, Protein, Ligand
from molecules.serializers import ComplexSerializer, ProteinSerializer, LigandSerializer

from rest_framework.renderers import TemplateHTMLRenderer


# class MyTemplateHTMLRenderer(TemplateHTMLRenderer):
#     def get_template_context(self, data, renderer_context):
#         response = renderer_context['response']
#         if response.exception:
#             data['status_code'] = response.status_code
#         return {'data': data}


class ComplexViewSet(viewsets.ModelViewSet):
    serializer_class = ComplexSerializer
    queryset = Complex.objects.all()


class ProteinViewSet(viewsets.ModelViewSet):
    serializer_class = ProteinSerializer
    queryset = Protein.objects.all()


class LigandViewSet(viewsets.ModelViewSet):
    serializer_class = LigandSerializer
    queryset = Ligand.objects.all()
