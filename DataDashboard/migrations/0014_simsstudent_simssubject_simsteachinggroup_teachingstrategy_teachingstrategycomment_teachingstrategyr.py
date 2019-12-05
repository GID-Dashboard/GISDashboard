# Generated by Django 2.2.5 on 2019-12-05 05:04

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DataDashboard', '0013_auto_20191110_0540'),
    ]

    operations = [
        migrations.CreateModel(
            name='SIMSStudent',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('student_id', models.IntegerField()),
                ('first_name', models.CharField(max_length=1000)),
                ('last_name', models.CharField(max_length=1000)),
                ('preferred_forename', models.CharField(max_length=1000)),
                ('gender', models.CharField(max_length=1000)),
                ('parent_email', models.EmailField(max_length=1000)),
                ('parent_salutation', models.CharField(max_length=1000)),
                ('student_email', models.EmailField(max_length=1000)),
                ('house_id', models.CharField(max_length=1000)),
                ('tutor_group_id', models.CharField(max_length=1000)),
                ('full_name', models.CharField(max_length=1000)),
                ('EAL_status', models.CharField(max_length=1000)),
                ('SEN_status', models.CharField(max_length=1000)),
                ('exam_candidate_number', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'sims].[DataDashboard_student',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SIMSSubject',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('Subject', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'sims].[DataDashboard_subject',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SIMSTeachingGroup',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('teaching_group', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'sims].[DataDashboard_teachinggroup',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TeachingStrategy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strategy', models.TextField(null=True)),
                ('created', models.DateField(default=datetime.date.today)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='DataDashboard.Teacher')),
                ('students', models.ManyToManyField(to='DataDashboard.Student')),
            ],
        ),
        migrations.CreateModel(
            name='TeachingStrategyResources',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('title', models.CharField(max_length=260)),
                ('strategy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataDashboard.TeachingStrategy')),
            ],
        ),
        migrations.CreateModel(
            name='TeachingStrategyComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, null=True)),
                ('vote', models.IntegerField(blank=True, null=True)),
                ('strategy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataDashboard.TeachingStrategy')),
                ('students', models.ManyToManyField(to='DataDashboard.Student')),
            ],
        ),
    ]