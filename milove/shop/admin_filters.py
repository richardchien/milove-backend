from django.contrib.admin.filters import (
    AllValuesFieldListFilter,
    RelatedFieldListFilter,
    ChoicesFieldListFilter
)


class AllValuesFieldDropdownFilter(AllValuesFieldListFilter):
    template = 'admin/dropdown_filter.html'


class RelatedFieldDropdownFilter(RelatedFieldListFilter):
    template = 'admin/dropdown_filter.html'


class ChoicesFieldDropdownFilter(ChoicesFieldListFilter):
    template = 'admin/dropdown_filter.html'
