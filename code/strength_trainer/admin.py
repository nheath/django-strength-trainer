from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.User_Profile_Model)
admin.site.register(models.NewWorkout)
admin.site.register(models.WorkoutWeek)
