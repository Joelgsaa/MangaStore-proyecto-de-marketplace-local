import django_filters
from .models import Producto

class ProductoFilter(django_filters.FilterSet):
    precio_min = django_filters.NumberFilter(field_name='precio', lookup_expr='gte')
    precio_max = django_filters.NumberFilter(field_name='precio', lookup_expr='lte')
    nombre = django_filters.CharFilter(field_name='nombre', lookup_expr='icontains')

    class Meta:
        model = Producto
        fields = ['precio_min', 'precio_max', 'nombre']