# Generated by Django 2.0.1 on 2018-04-15 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('strength_trainer', '0005_workoutweek'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workoutweek',
            old_name='sqaut_done',
            new_name='squat_done',
        ),
    ]
