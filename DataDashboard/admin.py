from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(TeachingStrategy)
admin.site.register(TeachingStrategyCategory)
admin.site.register(Teacher)
admin.site.register(LocalStudent)
admin.site.register(TeachingStrategyComment)
admin.site.register(TutorialCategory)
admin.site.register(TutorialPage)
admin.site.register(Topic)
admin.site.register(Subject)
admin.site.register(Term)
admin.site.register(YearGroup)

class CoverSheetAdmin(admin.ModelAdmin):
    fields = ('name', 'sow', 'national_curriculum_links', 'prior_learning', 'common_misconceptions')

admin.site.register(CoverSheet, CoverSheetAdmin)
