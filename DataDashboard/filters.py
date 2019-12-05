from .models import SIMSStudent, SIMSTeachingGroup
import django_filters

class StudentFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    tg_choices = list(SIMSStudent.objects.all().values_list('tutor_group_id', 'tutor_group_id').distinct().order_by('tutor_group_id'))
    house_choices = list(SIMSStudent.objects.all().values_list('house_id', 'house_id').distinct().order_by('house_id'))
    tutor_group_id = django_filters.MultipleChoiceFilter(choices=tg_choices)
    house_id = django_filters.MultipleChoiceFilter(choices=house_choices)

    class Meta:
        model = SIMSStudent
        fields = ['first_name', 'last_name', 'tutor_group_id', 'house_id']