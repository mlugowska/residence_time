from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter

from molecules.views import ComplexViewSet, ComplexDeleteView

app_name = 'molecules'

router = DefaultRouter()
router.register('', ComplexViewSet, basename='complex')
urlpatterns = router.urls + [
    path('<pdb_id>/delete/', ComplexDeleteView.as_view(), name='delete'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
