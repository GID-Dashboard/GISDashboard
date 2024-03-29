from django import forms
from .models import *
from dal import autocomplete
from django.db.models import Q


class CSVDocForm(forms.ModelForm):
    class Meta:
        model = CSVDoc
        fields = ('description', 'document', )


class InterventionForm(forms.ModelForm):

    class Meta:
        model = TeachingStrategy
        exclude = ('created_by',)
        widgets = {
            'students': autocomplete.ModelSelect2Multiple(url='DataDashboard:student_autocomplete')
        }


class InterventionResourceForm(forms.ModelForm):

    class Meta:
        model = TeachingStrategyResources
        fields = {'title', 'link'}


class InterventionCommentForm(forms.ModelForm):
    field_order = ['comment', 'vote']
    class Meta:
        model = TeachingStrategyComment
        fields = {'comment', 'vote'}
        widgets = {'vote': forms.RadioSelect,
                   }



class StudentAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated():
        #     return Student.objects.none()
        #
        qs = LocalStudent.objects.all()

        if self.q:
            qs = qs.filter(Q(first_name__icontains=self.q)|Q(last_name__icontains=self.q))

        return qs