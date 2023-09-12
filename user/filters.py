import django_filters

from user.models import District


class DistrictFilter(django_filters.FilterSet):
    class Meta:
        model = District
        fields = ("region",)