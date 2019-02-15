from .models import Complex
import django_filters


class DatabaseFilter(django_filters.FilterSet):
    pdb_id = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Complex
        fields = ['pdb_id', 'residence_time', 'release_year', ]
