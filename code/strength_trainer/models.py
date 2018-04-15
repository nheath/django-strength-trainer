from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from .forms import NewWorkoutForm

# Adapted from https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
class User_Profile_Model(models.Model):

    has_workout = models.BooleanField(default=False)
    gender = models.CharField(null=True, blank = True, max_length=1)
    age = models.IntegerField(null=True, blank = True, default=0)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    user_id = models.OneToOneField(        
                        User,
                        on_delete=models.CASCADE
                )
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            User_Profile_Model.objects.create(user_id=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.user_profile_model.save()

    def __str__(self):
        return "user_profile " + str(self.user_id)

class NewWorkout(models.Model):
    max_squat = models.PositiveIntegerField(default=None)
    max_bench = models.PositiveIntegerField(default=None)
    max_deadlift = models.PositiveIntegerField(default=None)
    max_overhead = models.PositiveIntegerField(default=None)
    user_id = models.OneToOneField(        
                        User,
                        on_delete=models.CASCADE
                )    
    def __str__(self):
        return "workout " + str(self.user_id)

class WorkoutWeek(models.Model):
    length = 250
    name = models.CharField(max_length=length)
    bench = models.CharField(max_length=length)
    bench_done = models.BooleanField(default=False)
    squat = models.CharField(max_length=length)
    squat_done = models.BooleanField(default=False)
    deadlift = models.CharField(max_length=length)
    deadlift_done = models.BooleanField(default=False)
    overhead = models.CharField(max_length=length)
    overhead_done = models.BooleanField(default=False)
    associated_workout = models.ForeignKey(
        NewWorkout,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.associated_workout)  + str(self.name)
# class Workout(models.Model):

#     squat_max = models.IntegerField(required=False)
#     bench_max = models.IntegerField(required=False)
#     deadlift_max = models.IntegerField(required=False)
#     overhead_max = models.IntegerField(required=False)
#     created_on = models.DateTimeField(auto_now_add=True, blank=True)
#     user_profile_id = models.OneToOne(        
#                         User_Profile_Model,
#                         on_delete=models.CASCADE
#                 )

#     def __str__(self):
#     return " " + str(self.created_on)