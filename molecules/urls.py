from django.urls import path
from rest_framework.routers import DefaultRouter

from molecules.views import ComplexViewSet, LigandViewSet, ProteinViewSet

router = DefaultRouter()
router.register('complex', ComplexViewSet, basename='complex')
router.register('ligand', LigandViewSet, basename='ligand')
router.register('protein', ProteinViewSet, basename='protein')
urlpatterns = router.urls