from django.db import models
from django.contrib.auth.models import User, Group
import datetime


# KEEP
class House(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    head_of_house = models.ForeignKey('Teacher', blank=True, null=True, on_delete=models.SET_NULL, related_name='hoh')


# KEEP
class Teacher(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    title_des = models.CharField(max_length= 100, blank=True, null=True)
    firstname = models.CharField(max_length= 500, blank=True, null=True)
    lastname = models.CharField(max_length= 500, blank=True, null=True)
    full_name = models.CharField(max_length= 500, blank=True, null=True)
    staff_code = models.CharField(max_length= 10, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)

    def __str__(self):
        if self.full_name:
            return self.full_name

        else:
            return self.staff_code

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


class LocalStudent(models.Model):
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


class LocalTeachingGroup(models.Model):
    name = models.CharField(blank=False, null=False, max_length=20)
    teachers = models.ManyToManyField(Teacher, blank=True)
    students = models.ManyToManyField(LocalStudent, blank=True)

    def __str__(self):
        return self.name


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
    student = models.ForeignKey(LocalStudent, blank=False, null=False, on_delete=models.CASCADE)
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
    classgroups = models.ManyToManyField(LocalTeachingGroup, blank=True)

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
    student = models.ForeignKey(LocalStudent, blank=False, null=False, on_delete=models.CASCADE)
    date = models.DateField(blank=False, null=False)
    numerical_value = models.FloatField(blank=True, null=True)
    text_value = models.TextField(blank=True, null=True)


class CSVDoc(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Student(models.Model):

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
    teachinggroup = models.ManyToManyField('TeachingGroup', db_table='sims].[DataDashboard_students_teachinggroup')

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


class TeachingGroup(models.Model):
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
    teachinggroup = models.ManyToManyField(TeachingGroup)

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
    title = models.CharField(max_length=150, blank=False, null=False)
    students = models.ManyToManyField(LocalStudent)
    category = models.ForeignKey(TeachingStrategyCategory, on_delete=models.SET_NULL, blank=False, null=True)
    strategy = models.TextField(blank=False, null=True)
    created_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateField(blank=False, null=False, default=datetime.date.today)

    def __str__(self):
        return self.title

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
    students = models.ManyToManyField(LocalStudent)
    comment = models.TextField(blank=True, null=True)
    vote = models.IntegerField(blank=True, null=True, choices=VOTE_CHOICES)
    date = models.DateField(blank=False, null=False, default=datetime.date.today)
    author = models.ForeignKey(Teacher, blank=False, null=True, on_delete=models.SET)

    def __str__(self):
        return "strategy" + str(self.pk)


class VerbalSpatialBias(models.Model):
    student_id = models.IntegerField(blank=False, null=False, unique=True)
    bias = models.CharField(max_length=50, blank=True, null=True)

class SIMSSummativeData(models.Model):
    aspect_id = models.IntegerField(blank=True, null=True)
    student = models.ForeignKey(Student, blank=True, null=True, on_delete=models.SET_NULL)
    aspect_name = models.CharField(max_length=200, blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    result_value = models.FloatField(blank=True, null=True)
    result_date = models.DateTimeField(blank=True, null=True)
    aspect_type = models.CharField(max_length=100, blank=True, null=True
                                   )
    class Meta:
        managed = False
        db_table = 'sims].[DataDashboard_summativedata'


class CAT4GradeProbability(models.Model):
    student = models.ForeignKey(LocalStudent, on_delete=models.CASCADE, blank=False, null=False)
    subject = models.CharField(max_length=100, blank=False, null=False)
    qualification = models.CharField(max_length=20, blank=False, null=False)
    grade = models.CharField(max_length=3, blank=False, null=False)
    probability = models.FloatField(blank=False, null=False)
    cumulative_probability = models.FloatField(blank=True, null=True)

    def numerical_grade(self):
        if self.grade == "A*" or self.grade == "S":
            return 9
        if self.grade == "A":
            return 8
        if self.grade == "B":
            return 7
        if self.grade == "C":
            return 6
        if self.grade == "D":
            return 5
        if self.grade =="E":
            return 4
        if self.grade == "F":
            return 3
        if self.grade == "G":
            return 2
        if self.grade == "U":
            return 1
        else:
            return 0


    class Meta:
        unique_together = ('student', 'subject', 'qualification', 'grade')


class OldVSBiases(models.Model):
    student_number = models.IntegerField(blank=False, null=False)
    bias = models.CharField(max_length=100, blank=False, null=False)


class TutorialCategory(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)

    def total_pages(self):
        return TutorialPage.objects.filter(category=self).count()

    def __str(self):
        return self.name


class TutorialPage(models.Model):
    category = models.ForeignKey(TutorialCategory, blank=False, null=True, on_delete=models.SET_NULL)
    order = models.IntegerField(blank=False, null=False)
    name = models.CharField(max_length=250, blank=False, null=False)
    video = models.CharField(max_length=50, blank=True, null=True)
    video_start = models.IntegerField(default=0, blank=False, null=False)
    video_end = models.IntegerField(default=10000, blank=False, null=False)
    dashboard_page = models.URLField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)

    def next_page(self):
        if self.order:
            if self.order < self.category.total_pages():
                return TutorialPage.objects.get(order=self.order+1, category=self.category)

        return False

    def previous_page(self):
        if self.order > 1:
            return TutorialPage.objects.get(order=self.order-1, category=self.category)
        else:
            return False

    class Meta:
        unique_together = ('category', 'order')

    def __str__(self):
        return self.name


# For primary curriculum
class Term(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False, unique=True)
    order = models.IntegerField(blank=False, null=False)

    def save(self, *args, **kwargs):
        super(Term, self).save(*args, **kwargs)
        for topic in Topic.objects.all():
            for year in YearGroup.objects.filter(integer_year__lte=6):
                sheet, created = CoverSheet.objects.get_or_create(topic=topic, term=self, yeargroup=year)
                if created:
                    sheet.name = "Y" + sheet.yeargroup.year+ " " + sheet.term.name + " " + sheet.topic.name
                    sheet.save()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    def __str__(self):
        return self.name

class Topic(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=True)

    def save(self, *args, **kwargs):
        super(Topic, self).save(*args, **kwargs)
        for term in Term.objects.all():
            for year in YearGroup.objects.filter(integer_year__lte=6):

                sheet, created = CoverSheet.objects.get_or_create(topic=self, term=term, yeargroup=year)
                if created:
                    sheet.name = "Y" + sheet.yeargroup.year + " " + sheet.term.name + " " + sheet.topic.name
                    sheet.save()

    def __str__(self):
        return self.name


class CoverSheet(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=False, null=False)
    term = models.ForeignKey(Term, on_delete=models.CASCADE, blank=False, null=False)
    yeargroup = models.ForeignKey(YearGroup, on_delete=models.CASCADE, blank=False, null=True)
    name = models.CharField(max_length=100, blank=False, null=True, help_text="Name of your unit of work", verbose_name='Unit Name')
    national_curriculum_links = models.TextField(blank=True, null=True)
    prior_learning = models.TextField(blank=True, null=True)
    common_misconceptions = models.TextField(blank=True, null=True)
    sow = models.URLField(blank=True, null=True, help_text="This can be a link to <em>Google Drive</em> or any other site", verbose_name='SoW Link')

    class Meta:
        unique_together = ("topic", "term", "yeargroup")

    def __str__(self):
        if self.name:
            return self.name

        return str(self.yeargroup) + " "  + (self.term) + " " + str(self.topic)
