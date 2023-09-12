from django.db.models import Q
import django_filters

from product.models import Product


class ProductFilter(django_filters.FilterSet):

    class Meta:
        model = Product
        fields = ['name', 'category__name', 'brand__name', 'search', 'is_famous']

    search = django_filters.CharFilter(field_name='search',
                                       method='filter_search')

    def filter_search(self, queryset, name, value):
        filter_actions = Q()
        filter_actions &= Q(name__icontains=value)
        filter_actions |= Q(category__name__icontains=value)
        filter_actions |= Q(brand__name__icontains=value)
        return queryset.filter(filter_actions)
