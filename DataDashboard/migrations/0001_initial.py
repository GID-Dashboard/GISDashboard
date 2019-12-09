# Generated by Django 2.2.5 on 2019-09-11 05:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('period', models.IntegerField()),
                ('phase', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Marksheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.IntegerField(blank=True, null=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('preferred_forename', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(blank=True, max_length=20, null=True)),
                ('sen_status', models.CharField(blank=True, max_length=20, null=True)),
                ('eal_status', models.CharField(blank=True, max_length=20, null=True)),
                ('exam_candidate_number', models.CharField(blank=True, max_length=20, null=True)),
                ('parent_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('parent_salutation', models.CharField(blank=True, max_length=150, null=True)),
                ('student_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('house', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='DataDashboard.House')),
            ],
        ),
        migrations.CreateModel(
            name='SummativeScheme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('salutation', models.CharField(max_length=20)),
                ('staff_code', models.CharField(max_length=5)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('position', models.CharField(max_length=5)),
                ('house', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='DataDashboard.House')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TutorGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=100)),
                ('year_group', models.IntegerField()),
                ('tutor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='DataDashboard.Teacher')),
            ],
        ),
        migrations.CreateModel(
            name='TeachingGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('students', models.ManyToManyField(blank=True, to='DataDashboard.Student')),
                ('teachers', models.ManyToManyField(blank=True, to='DataDashboard.Teacher')),
            ],
        ),
        migrations.CreateModel(
            name='SummativeDefinition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('max_score', models.IntegerField()),
                ('min_score', models.IntegerField()),
                ('increment', models.FloatField()),
                ('scheme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataDashboard.SummativeScheme')),
            ],
        ),
        migrations.CreateModel(
            name='SummativeData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('value', models.FloatField()),
                ('data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataDashboard.SummativeDefinition')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataDashboard.Student')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='tutor_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='DataDashboard.TutorGroup'),
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='MarksheetFields',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('max_score', models.IntegerField(blank=True, null=True)),
                ('min_score', models.IntegerField(blank=True, null=True)),
                ('increment', models.FloatField(default=1)),
                ('marksheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataDashboard.Marksheet')),
            ],
        ),
        migrations.CreateModel(
            name='MarksheetData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('numerical_value', models.FloatField(blank=True, null=True)),
                ('text_value', models.TextField(blank=True, null=True)),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataDashboard.MarksheetFields')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataDashboard.Student')),
            ],
        ),
        migrations.AddField(
            model_name='marksheet',
            name='classgroups',
            field=models.ManyToManyField(blank=True, to='DataDashboard.TeachingGroup'),
        ),
        migrations.AddField(
            model_name='marksheet',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='DataDashboard.Department'),
        ),
        migrations.AddField(
            model_name='marksheet',
            name='factulty',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='DataDashboard.Faculty'),
        ),
        migrations.AddField(
            model_name='house',
            name='head_of_house',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hoh', to='DataDashboard.Teacher'),
        ),
        migrations.AddField(
            model_name='faculty',
            name='hof',
            field=models.ManyToManyField(blank=True, related_name='hof', to='DataDashboard.Teacher'),
        ),
        migrations.AddField(
            model_name='faculty',
            name='staff',
            field=models.ManyToManyField(blank=True, to='DataDashboard.Teacher'),
        ),
        migrations.AddField(
            model_name='department',
            name='faculty',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='DataDashboard.Faculty'),
        ),
        migrations.AddField(
            model_name='department',
            name='hod',
            field=models.ManyToManyField(blank=True, related_name='hod', to='DataDashboard.Teacher'),
        ),
        migrations.AddField(
            model_name='department',
            name='staff',
            field=models.ManyToManyField(blank=True, to='DataDashboard.Teacher'),
        ),
        migrations.CreateModel(
            name='ConductReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('type', models.CharField(max_length=100)),
                ('comments', models.TextField(blank=True, null=True)),
                ('points', models.FloatField(default=0)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataDashboard.Student')),
                ('teacher_assigning', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='DataDashboard.Teacher')),
            ],
        ),
        migrations.CreateModel(
            name='ClassAtttenanceSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataDashboard.AttendanceSession')),
                ('tutor_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='DataDashboard.TutorGroup')),
            ],
        ),
        migrations.CreateModel(
            name='AttiudinalData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('pass1', models.IntegerField(blank=True, null=True)),
                ('pass2', models.IntegerField(blank=True, null=True)),
                ('pass3', models.IntegerField(blank=True, null=True)),
                ('pass4', models.IntegerField(blank=True, null=True)),
                ('pass5', models.IntegerField(blank=True, null=True)),
                ('pass6', models.IntegerField(blank=True, null=True)),
                ('pass7', models.IntegerField(blank=True, null=True)),
                ('pass8', models.IntegerField(blank=True, null=True)),
                ('pass9', models.IntegerField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataDashboard.Student')),
            ],
        ),
        migrations.CreateModel(
            name='AptitudinalData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('verbal', models.IntegerField(blank=True, null=True)),
                ('non_verbal', models.IntegerField(blank=True, null=True)),
                ('quantitative', models.IntegerField(blank=True, null=True)),
                ('spatial', models.IntegerField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataDashboard.Student')),
            ],
        ),
    ]
