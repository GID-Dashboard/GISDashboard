# Generated by Django 2.2.5 on 2020-03-25 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DataDashboard', '0006_cat4gradeprobability'),
    ]

    operations = [
        migrations.CreateModel(
            name='OldVSBiases',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_number', models.IntegerField()),
                ('bias', models.CharField(max_length=100)),
            ],
        ),
    ]
