from DataDashboard.views import *
from django.urls import path

app_name = "DataDashboard"
urlpatterns = [
    path('students', students, name='students'),
    path('filter', StudentList),
    path("student_listing/", StudentListing.as_view(), name = 'listing'),
    path("ajax/tutor_groups/", getTutorGRoups, name = 'get_tutor_groups'),
    path("student_list/", search, name='student_search'),
    path("add_intervention/", add_intervention, name='add_intervention'),
    path('student_search', StudentAutocomplete.as_view(), name='student_autocomplete'),
    path('strategies/<int:teaching_strategy_pk>', view_strategy, name='view_strategy'),
    path('strategies/', find_strategies, name='find_strategies')
]