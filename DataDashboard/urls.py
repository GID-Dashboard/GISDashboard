from DataDashboard import views
from django.urls import path

app_name = "DataDashboard"
urlpatterns = [
    path('import', views.import_students, name='import_students'),
]