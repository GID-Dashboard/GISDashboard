# Generated by Django 2.2.5 on 2019-10-16 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DataDashboard', '0013_auto_20191016_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='code',
            field=models.CharField(max_length=2, null=True, unique=True),
        ),
    ]