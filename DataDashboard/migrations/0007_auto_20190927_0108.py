# Generated by Django 2.2.5 on 2019-09-27 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DataDashboard', '0006_auto_20190924_0759'),
    ]

    operations = [
        migrations.AddField(
            model_name='summativedata',
            name='letter_value',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='summativedata',
            name='value',
            field=models.FloatField(null=True),
        ),
    ]
