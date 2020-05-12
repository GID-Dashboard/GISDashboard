from DataDashboard.views import *
from django.urls import path

app_name = "DataDashboard"
urlpatterns = [
    # path('students', students, name='students'),
    # path('filter', StudentList),
    #path("student_listing/", StudentListing.as_view(), name = 'listing'),
    # path("ajax/tutor_groups/", getTutorGRoups, name = 'get_tutor_groups'),
    path("student_list/", search, name='student_search'),
    path("add_intervention/", add_intervention, name='add_intervention'),
    path('student_search', StudentAutocomplete.as_view(), name='student_autocomplete'),
    path('strategies/<int:teaching_strategy_pk>', view_strategy, name='view_strategy'),
    path('strategies/', find_strategies, name='find_strategies'),
    path('denied/', permission_error, name='permission_error'),
    path('strategies/<int:teaching_strategy_pk>/delete', delete_strategy, name='delete_strategy'),
    path('strategies/<int:teaching_strategy_pk>/confirm_delete', confirmed_delete_strategy, name='confirm_delete_strategy'),
    path('reportdashboard/', report_dashboard, name='report_dashboard'),
    path('curriculum/', curriculum_dashboard, name='curriculum_dashboard'),
    path('master/', master_dashboard, name='master_dashboard'),
    path('tutorial/<int:page_pk>', tutorial, name='tutorial'),
    path('', splash, name='splash'),
]