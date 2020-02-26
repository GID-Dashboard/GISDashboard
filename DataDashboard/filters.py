from .models import Student, TeachingStrategy, LocalTeachingGroup
import django_filters

class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class StudentFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    tg_choices = list(Student.objects.all().values_list('tutor_group_id', 'tutor_group_id').distinct().order_by('tutor_group_id'))
    house_choices = list(Student.objects.all().values_list('house_id', 'house_id').distinct().order_by('house_id'))
#    teaching_group_choices = list(LocalTeachingGroup.objects.all().values_list('name', 'name').distinct().order_by('name'))
    tutor_group_id = django_filters.MultipleChoiceFilter(choices=tg_choices)
    house_id = django_filters.MultipleChoiceFilter(choices=house_choices)
    teachinggroup__teaching_group = django_filters.CharFilter(lookup_expr='icontains')
    student_id = NumberInFilter()

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'tutor_group_id', 'house_id']


class StrategyFilter(django_filters.FilterSet):
    category__name = django_filters.CharFilter(lookup_expr='icontains')
    strategy = django_filters.CharFilter(lookup_expr='icontains')
    created_by__full_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = TeachingStrategy
        fields = ['category', 'strategy', 'created_by']