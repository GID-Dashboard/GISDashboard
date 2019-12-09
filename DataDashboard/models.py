from django.db import models
from django.contrib.auth.models import User, Group
import datetime


class House(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    head_of_house = models.ForeignKey('Teacher', blank=True, null=True, on_delete=models.SET_NULL, related_name='hoh')


class Teacher(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    title_des = models.CharField(max_length= 100, blank=True, null=True)
    firstname = models.CharField(max_length= 500, blank=True, null=True)
    lastname = models.CharField(max_length= 500, blank=True, null=True)
    full_name = models.CharField(max_length= 500, blank=True, null=True)
    staff_code = models.CharField(max_length= 10, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['staff_code']


class YearGroup(models.Model):

    year = models.CharField(max_length=10, blank=False, null=False)
    integer_year = models.IntegerField(blank=False, null=True)
    heads_of_year = models.ManyToManyField(Teacher, blank=True)

    def set_integer_year(self):
        try:
            self.integer_year = int(self.year)

        except ValueError:
            self.integer_year = 0

        self.save()

    def __str__(self):
        return self.year


class TutorGroup(models.Model):
    group_name = models.CharField(blank=False, null=False, max_length=100)
    tutor = models.ForeignKey('Teacher', blank=True, null=True, on_delete=models.SET_NULL)
    year_group = models.ForeignKey(YearGroup, blank=False, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.group_name


class Student(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.SET_NULL)
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

    def full_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.first_name + " " + self.last_name + " (" + str(self.tutor_group) + ")"

    class Meta:
        ordering = ['student_id']


class AttendanceSession(models.Model):
    date = models.DateField(blank=False, null=False)
    period = models.IntegerField(blank=False, null=False)
    phase = models.CharField(blank=False, null=False, max_length=20)


class TeachingGroup(models.Model):
    name = models.CharField(blank=False, null=False, max_length=20)
    teachers = models.ManyToManyField(Teacher, blank=True)
    students = models.ManyToManyField(Student, blank=True)

    def __str__(self):
        return saelf.name

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
    value = models.FloatField(blank=False, null=True)
    letter_value = models.CharField(max_length=20, blank=True, null=True)
    raw_value = models.TextField(blank=True, null=True)

    def value_from_raw(self):
        if self.raw_value:
            from .functions import is_number
            if is_number(self.raw_value):
                self.value = self.raw_value

            elif len(self.raw_value) < 20:
                self.letter_value = self.raw_value

                # TODO: Add code here to convert letter grades to numerical
                raw = self.raw_value
                if raw == ('S' or 'A*' or 'SS' or 'A*A*'):
                    self.value = 9
                if raw == ('A' or 'AA' or 'aa' or 'a'):
                    self.value = 8
                if raw == ('B' or 'BB' or 'b' or 'bb'):
                    self.value = 7
                if raw == ('C' or 'CC' or 'c' or 'cc'):
                    self.value = 6
                if raw == ('D' or 'DD' or 'd' or 'dd'):
                    self.value = 5
                if raw == ('E' or 'EE' or 'e' or 'ee'):
                    self.value = 4
                if raw == ('F' or 'FF' or 'f' or 'ff'):
                    self.value = 3
                if raw == ('G' or 'GG' or 'g' or 'gg'):
                    self.value = 2
                if raw == ('U' or 'UU' or 'u' or 'uu'):
                    self.value = 1
            self.save()


class Faculty(models.Model):
    name = models.CharField(blank=False, null=False, max_length=100)
    hof = models.ManyToManyField(Teacher, blank=True, related_name='hof')
    staff = models.ManyToManyField(Teacher, blank=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(blank=False, null=False, max_length=100)
    faculty = models.ForeignKey(Faculty, blank=True, null=True, on_delete=models.SET_NULL)
    hod = models.ManyToManyField(Teacher, blank=True, related_name='hod')
    staff = models.ManyToManyField(Teacher, blank=True)

    def __str__(self):
        return self.name


class Marksheet(models.Model):
    name = models.CharField(blank=False, null=False, max_length=100)
    factulty = models.ForeignKey(Faculty, blank=True, null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(Department, blank=True, null=True, on_delete=models.SET_NULL)
    classgroups = models.ManyToManyField(TeachingGroup, blank=True)

    def __str__(self):
        return self.name


class MarksheetFields(models.Model):
    marksheet = models.ForeignKey(Marksheet, blank=False, null=False, on_delete=models.CASCADE)
    name = models.CharField(blank=False, null=False, max_length=100)
    type = models.CharField(blank=False, null=False, max_length=100)
    max_score = models.IntegerField(blank=True, null=True)
    min_score = models.IntegerField(blank=True, null=True)
    increment = models.FloatField(blank=False, null=False, default=1)

    def __str__(self):
        return self.name

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


class SIMSStudent(models.Model):

    id = models.IntegerField(primary_key=True, null=False)
    student_id=models.IntegerField()
    first_name=models.CharField(max_length=1000)
    last_name=models.CharField(max_length=1000)
    preferred_forename=models.CharField(max_length=1000)
    gender=models.CharField(max_length=1000)
    parent_email=models.EmailField(max_length=1000)
    parent_salutation=models.CharField(max_length=1000)
    student_email=models.EmailField(max_length=1000)
    house_id=models.CharField(max_length=1000)
    tutor_group_id=models.CharField(max_length=1000)
    full_name=models.CharField(max_length=1000)
    EAL_status=models.CharField(max_length=1000)
    SEN_status=models.CharField(max_length=1000)
    exam_candidate_number=models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'sims].[DataDashboard_student'

    def __str__(self):
        return self.full_name + " (" + self.tutor_group_id + ")"


class SIMSSubject(models.Model):
    id = models.IntegerField(primary_key=True)
    Subject = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'sims].[DataDashboard_subject'


class SIMSTeachingGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    teaching_group = models.CharField(max_length=1000)
    subject_code = models.ForeignKey('SIMSSubject', on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sims].[DataDashboard_teachinggroup'


class SIMSTeacher(models.Model):
    id = models.IntegerField(blank=False, null=False, primary_key=True)
    title_des = models.CharField(max_length= 100, blank=True, null=True)
    firstname = models.CharField(max_length= 500, blank=True, null=True)
    lastname = models.CharField(max_length= 500, blank=True, null=True)
    full_name = models.CharField(max_length= 500, blank=True, null=True)
    staff_code = models.CharField(max_length= 10, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.full_name

    class Meta:
        managed = False
        db_table = 'sims].[DataDashboard_teachers'
        ordering = ['staff_code']


class TeachingStrategyCategory(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name

class TeachingStrategy(models.Model):
    students = models.ManyToManyField(Student)
    category = models.ForeignKey(TeachingStrategyCategory, on_delete=models.SET_NULL, blank=False, null=True)
    strategy = models.TextField(blank=False, null=True)
    created_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateField(blank=False, null=False, default=datetime.date.today)

    def __str__(self):
        if self.category:
            return str(self.category)+ str(self.pk)
        else:
            return str(self.pk)

class TeachingStrategyResources(models.Model):
    strategy = models.ForeignKey(TeachingStrategy, on_delete=models.CASCADE)
    link = models.URLField(blank=False, null=False)
    title = models.CharField(max_length=260, blank=False, null=False)

    def __str__(self):
        return self.title


class TeachingStrategyComment(models.Model):
    VOTE_CHOICES = [
        (1, 'Upvote'),
        (-1, 'Downvote'),
    ]
    strategy = models.ForeignKey(TeachingStrategy, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)
    comment = models.TextField(blank=True, null=True)
    vote = models.IntegerField(blank=True, null=True, choices=VOTE_CHOICES)
    date = models.DateField(blank=False, null=False, default=datetime.date.today)
    author = models.ForeignKey(Teacher, blank=False, null=True, on_delete=models.SET)

    def __str__(self):
        return "strategy" + str(self.pk)
