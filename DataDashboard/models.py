from django.db import models
from django.contrib.auth.models import User
import datetime


class House(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    head_of_house = models.ForeignKey('Teacher', blank=True, null=True, on_delete=models.SET_NULL, related_name='hoh')


class Teacher(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    house = models.ForeignKey(House, blank=True, null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(blank=False, null=False, max_length=100)
    last_name = models.CharField(blank=False, null=False, max_length=100)
    salutation = models.CharField(blank=False, null=False, max_length=20)
    staff_code = models.CharField(blank=False, null=False, max_length=5)
    email = models.EmailField(blank=True, null=True)
    position = models.CharField(blank=False, null=False, max_length=5)


class TutorGroup(models.Model):
    group_name = models.CharField(blank=False, null=False, max_length=100)
    tutor = models.ForeignKey('Teacher', blank=True, null=True, on_delete=models.SET_NULL)
    year_group = models.IntegerField(blank=False, null=True)


class Student(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    student_id = models.IntegerField(blank=True, null=True, unique=True)
    first_name = models.CharField(blank=False, null=False, max_length=100)
    last_name = models.CharField(blank=False, null=False, max_length=100)
    preferred_forename = models.CharField(blank=True, null=True, max_length=100)
    gender = models.CharField(blank=True, null=True, max_length=20)
    tutor_group = models.ForeignKey(TutorGroup, blank=True, null=True, on_delete=models.SET_NULL)
    sen_status = models.CharField(blank=True, null=True, max_length=100)
    eal_status = models.CharField(blank=True, null=True, max_length=100)
    exam_candidate_number = models.CharField(blank=True, null=True, max_length=20)
    house = models.ForeignKey(House, blank=True, null=True, on_delete=models.SET_NULL)
    parent_email = models.EmailField(blank=True, null=True)
    parent_salutation = models.CharField(blank=True, null=True, max_length=150)
    student_email = models.EmailField(blank=True, null=True)


class AttendanceSession(models.Model):
    date = models.DateField(blank=False, null=False)
    period = models.IntegerField(blank=False, null=False)
    phase = models.CharField(blank=False, null=False, max_length=20)


class TeachingGroup(models.Model):
    name = models.CharField(blank=False, null=False, max_length=20)
    teachers = models.ManyToManyField(Teacher, blank=True)
    students = models.ManyToManyField(Student, blank=True)


class ClassAtttenanceSession(models.Model):
    attendance_session = models.ForeignKey(AttendanceSession, blank=False, null=False, on_delete=models.CASCADE)
    # teaching_group
    tutor_group = models.ForeignKey(TutorGroup, blank=True, null=True, on_delete=models.CASCADE)


class ConductReport(models.Model):
    student = models.ForeignKey(Student, blank=False, null=False, on_delete=models.CASCADE)
    teacher_assigning = models.ForeignKey(Teacher, blank=True, null=True, on_delete=models.SET_NULL)
    date = models.DateField(blank=False, null=False)
    type = models.CharField(blank=False, null=False, max_length=100)
    comments = models.TextField(blank=True, null=True)
    points = models.FloatField(blank=False, null=False, default=0)


class AttiudinalData(models.Model):
    student = models.ForeignKey(Student, blank=False, null=False, on_delete=models.CASCADE)
    date = models.DateField(blank=False, null=False)
    pass1 = models.IntegerField(blank=True, null=True)
    pass2 = models.IntegerField(blank=True, null=True)
    pass3 = models.IntegerField(blank=True, null=True)
    pass4 = models.IntegerField(blank=True, null=True)
    pass5 = models.IntegerField(blank=True, null=True)
    pass6 = models.IntegerField(blank=True, null=True)
    pass7 = models.IntegerField(blank=True, null=True)
    pass8 = models.IntegerField(blank=True, null=True)
    pass9 = models.IntegerField(blank=True, null=True)


class AptitudinalData(models.Model):
    student = models.ForeignKey(Student, blank=False, null=False, on_delete=models.CASCADE)
    date = models.DateField(blank=False, null=False)
    verbal = models.IntegerField(blank=True, null=True)
    non_verbal = models.IntegerField(blank=True, null=True)
    quantitative = models.IntegerField(blank=True, null=True)
    spatial = models.IntegerField(blank=True, null=True)


class SummativeScheme(models.Model):
    name = models.CharField(blank=False, null=False, max_length=100)


class SummativeDefinition(models.Model):
scheme = models.ForeignKey(SummativeScheme, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(blank=False, null=False, max_length=100)
    max_score = models.IntegerField(blank=False, null=True)
    min_score = models.IntegerField(blank=False, null=True)
    increment = models.FloatField(blank=False, null=True)


class SummativeData(models.Model):
    data = models.ForeignKey(SummativeDefinition, blank=False, null=False, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, blank=False, null=False, on_delete=models.CASCADE)
    date = models.DateField(blank=False, null=False, default=datetime.date.today)
    value = models.FloatField(blank=False, null=False)


class Faculty(models.Model):
    name = models.CharField(blank=False, null=False, max_length=100)
    hof = models.ManyToManyField(Teacher, blank=True, related_name='hof')
    staff = models.ManyToManyField(Teacher, blank=True)


class Department(models.Model):
    name = models.CharField(blank=False, null=False, max_length=100)
    faculty = models.ForeignKey(Faculty, blank=True, null=True, on_delete=models.SET_NULL)
    hod = models.ManyToManyField(Teacher, blank=True, related_name='hod')
    staff = models.ManyToManyField(Teacher, blank=True)


class Marksheet(models.Model):
    name = models.CharField(blank=False, null=False, max_length=100)
    factulty = models.ForeignKey(Faculty, blank=True, null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(Department, blank=True, null=True, on_delete=models.SET_NULL)
    classgroups = models.ManyToManyField(TeachingGroup, blank=True)


class MarksheetFields(models.Model):
    marksheet = models.ForeignKey(Marksheet, blank=False, null=False, on_delete=models.CASCADE)
    name = models.CharField(blank=False, null=False, max_length=100)
    type = models.CharField(blank=False, null=False, max_length=100)
    max_score = models.IntegerField(blank=True, null=True)
    min_score = models.IntegerField(blank=True, null=True)
    increment = models.FloatField(blank=False, null=False, default=1)

class MarksheetData(models.Model):
    field = models.ForeignKey(MarksheetFields, on_delete=models.CASCADE, blank=False, null=False)
    student = models.ForeignKey(Student, blank=False, null=False, on_delete=models.CASCADE)
    date = models.DateField(blank=False, null=False)
    numerical_value = models.FloatField(blank=True, null=True)
    text_value = models.TextField(blank=True, null=True)


class CSVDoc(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
