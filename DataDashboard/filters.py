from .models import SIMSStudent, TeachingStrategy, TeachingGroup
import django_filters

class StudentFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    tg_choices = list(SIMSStudent.objects.all().values_list('tutor_group_id', 'tutor_group_id').distinct().order_by('tutor_group_id'))
    house_choices = list(SIMSStudent.objects.all().values_list('house_id', 'house_id').distinct().order_by('house_id'))
    teaching_group_choices = list(TeachingGroup.objects.all().values_list('name', 'name').distinct().order_by('name'))
    tutor_group_id = django_filters.MultipleChoiceFilter(choices=tg_choices)
    house_id = django_filters.MultipleChoiceFilter(choices=house_choices)
    teaching_group = django_filters.ChoiceFilter(choices=teaching_group_choices)

    class Meta:
        model = SIMSStudent
        fields = ['first_name', 'last_name', 'tutor_group_id', 'house_id']


class StrategyFilter(django_filters.FilterSet):
    category__name = django_filters.CharFilter(lookup_expr='icontains')
    strategy = django_filters.CharFilter(lookup_expr='icontains')
    created_by__full_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = TeachingStrategy
        fields = ['category', 'strategy', 'created_by']