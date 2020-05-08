# Generated by Django 2.2.5 on 2020-05-07 23:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DataDashboard', '0011_auto_20200430_0726'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('order', models.IntegerField()),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='DataDashboard.Subject')),
            ],
        ),
        migrations.CreateModel(
            name='CoverSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('national_curriculum_links', models.TextField(blank=True, null=True)),
                ('prior_learning', models.TextField(blank=True, null=True)),
                ('common_misconceptions', models.TextField(blank=True, null=True)),
                ('sow', models.URLField(blank=True, null=True)),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataDashboard.Term')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataDashboard.Topic')),
            ],
            options={
                'unique_together': {('topic', 'term')},
            },
        ),
    ]