from django.shortcuts import render, redirect, reverse
from .models import Teacher
from .forms import *
from .functions import processstudent
import os
# Create your views here.

def splash(request):
    pass


def markbook(request):

    teacher = Teacher.objects.get(user=request.user)
    return render(request, 'DataDashboard/markbook.html', {'teacher': teacher})


def import_students(request):
    # Deal with getting a CSV file

    if request.method == 'POST':
        csvform = CSVDocForm(request.POST, request.FILES)
        if csvform.is_valid():
            file = csvform.save()
            path = file.document.path
            processstudent(path)
            os.remove(path)
            file.delete()
            return redirect(reverse('school:list_students'))
    else:
        csvform = CSVDocForm()
    return render(request, 'DataDashboard/model_form_upload.html', {'csvform': csvform})
