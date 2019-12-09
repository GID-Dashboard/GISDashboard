from django.shortcuts import render, redirect, reverse
from .models import Student
from .forms import *
from .filters import *
from .functions import processstudent
import os
# Create your views here.
from django.contrib import messages

from django.http import JsonResponse
from django.shortcuts import render, resolve_url
from rest_framework.generics import ListAPIView
from .serializers import StudentSerializers
from .pagination import StandardResultsSetPagination


def StudentList(request):
    return render(request, "DataDashboard/students_filterable.html", {})


class StudentListing(ListAPIView):
    # set the pagination and serializer class

    pagination_class = StandardResultsSetPagination
    serializer_class = StudentSerializers

    def get_queryset(self):
        # filter the queryset based on the filters applied

        queryList = Student.objects.all().order_by('student_id')
        tutor_group = self.request.query_params.get('tutor_group', None)
        sort_by = self.request.query_params.get('sort_by', None)


        if tutor_group:
            queryList = queryList.filter(tutor_group=tutor_group)

            # sort it if applied on based on price/points

        if sort_by == "name":
            queryList = queryList.order_by("name")
        elif sort_by == "student_id":
            queryList = queryList.order_by("student_id")
        return queryList


def getTutorGRoups(request):
    # get all the countreis from the database excluding
    # null and blank values

    if request.method == "GET" and request.is_ajax():
        groups = Student.objects.exclude(tutor_group__isnull=True)\
            .order_by('tutor_group').values_list('tutor_group').distinct()
        groups = [i[0] for i in list(groups)]
        data = {
            "groups": groups,
        }
        return JsonResponse(data, status=200)




def students(request):
    students = Student.objects.all()

    return render(request, 'DataDashboard/students.html', {'students': students})


def search(request):
    student_list = Student.objects.all()
    user_filter = StudentFilter(request.GET, queryset=student_list)
    if request.method=='POST':
        pass
    return render(request, 'DataDashboard/student_list.html', {'filter': user_filter})


def add_intervention(request):
    teacher = Teacher.objects.get(user=request.user)

    student_pks = []
    for key, value in request.POST.items():
        if 'student_id' in key:
            student_pks.append(value)

    # Todo; add logic if no students are selected
    # Todo: add logic for if student is in SIMS but not our DB

    students = LocalStudent.objects.filter(student_id__in=student_pks)

    if (request.method == 'POST') and ('searchform' not in request.POST):
            intervention_form = InterventionForm(request.POST)
            if intervention_form.is_valid():
                intervention = intervention_form.save()
                intervention.created_by = teacher
                intervention.save()

                if 'save' in request.POST.items():
                    # Redirect to intervention overview page
                    pass

                if 'add_resource' in request.POST.items():
                    # Redirect to resource page
                    pass

    else:
        intervention_form = InterventionForm(initial={'students': students})

    return render(request, 'DataDashboard/add_intervention.html', {'students': students,
                                                                   'form': intervention_form})

def add_resource(request, teaching_strategy_pk):

    strategy = TeachingStrategy.objects.get(pk=teaching_strategy_pk)
    pass


def view_strategy(request, teaching_strategy_pk):
    strategy = TeachingStrategy.objects.get(pk=teaching_strategy_pk)

    comment_form = InterventionCommentForm()

    if request.method == 'POST':
        comment_form = InterventionCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.strategy = strategy
            comment.author = Teacher.objects.get(user=request.user)
            comment.save()
            comment_form = InterventionCommentForm()

    comments = TeachingStrategyComment.objects.filter(strategy=strategy)
    resources = TeachingStrategyResources.objects.filter(strategy=strategy)

    return render(request, 'DataDashboard/view_strategies.html', {'strategy': strategy,
                                                                  'comments': comments,
                                                                  'resources': resources,
                                                                  'form': comment_form})


def find_strategies(request):
    strategy_list = TeachingStrategy.objects.all()
    strategy_filter = StrategyFilter(request.GET, queryset=strategy_list)
    if request.method == 'POST':
        pass
    return render(request, 'DataDashboard/strategy_list.html', {'filter': strategy_filter})


def delete_strategy(request, teaching_strategy_pk):
    strategy = TeachingStrategy.objects.get(pk=teaching_strategy_pk)

    if (request.user == strategy.created_by.user) | request.user.is_superuser:
        return render(request, "DataDashboard/delete_strategy.html", {'strategy': strategy})

    else:
        messages.add_message(request, messages.ERROR, "You must be the creator of a strategy to delete it.")
        return redirect(reverse("DataDashboard:permission_error"))


def confirmed_delete_strategy(request, teaching_strategy_pk):
    strategy = TeachingStrategy.objects.get(pk=teaching_strategy_pk)

    if (request.user == strategy.created_by.user) | request.user.is_superuser:
        strategy.delete()
        messages.add_message(request, messages.SUCCESS, "Strategy deleted successfully")
        return redirect(reverse("DataDashboard:find_strategies"))

    else:
        return redirect(reverse("DataDashboard:permission_error"))


def permission_error(request):
    return render(request, "DataDashboard/permission_error.html")


def report_dashboard(request):
    return render(request, "DataDashboard/report_dashboard.html")


