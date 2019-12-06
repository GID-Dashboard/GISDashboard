# Generated by Django 2.2.5 on 2019-12-06 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DataDashboard', '0021_teachingstrategycomment_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teachingstrategycomment',
            name='downvote',
        ),
        migrations.RemoveField(
            model_name='teachingstrategycomment',
            name='upvote',
        ),
        migrations.AlterField(
            model_name='teachingstrategycomment',
            name='vote',
            field=models.IntegerField(blank=True, choices=[(1, 'Upvote'), (2, 'Downvote')], null=True),
        ),
    ]
