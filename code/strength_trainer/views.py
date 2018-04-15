from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import registration_form, NewWorkoutForm
from .models import NewWorkout, User_Profile_Model, WorkoutWeek
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from .utils import create_workout_week

def new_workout(request):
    form = NewWorkoutForm()
    context = {
        "form":form
    }
    return render(request, "new_workout.html", context)

def index(request):
    if request.user.is_authenticated:
        return redirect("/home/")
    else:
        return render(request, "index.html")

@login_required(login_url="/")
def home(request):
    if request.method == "GET":
        cur_user = request.user
        has_workout = NewWorkout.objects.filter(user_id=cur_user.id).count()
        if has_workout == 0:
            context = {
                "user": request.user.username,
                "hasWorkout": False,
                "message": "The gym is empty and so is your training plan! Not much to do here if you dont have a workout, you should go create a new workout."
            }
            return render(request, "home.html", context)
        context = {
            "user": request.user.username,
            "hasWorkout": True,
        }      
        return render(request, "home.html", context)
    ## This is when you create a new_workout and new workout_schedule
    if request.method == 'POST':
        # get current user from request
        cur_user = request.user
        has_workout = NewWorkout.objects.filter(user_id=cur_user.id).count()

        # Get the current user profile from db
        cur_user_profile = User_Profile_Model.objects.get(user_id=cur_user.id)

        #Check if user has a workout already if so clean it up.
        has_workout = NewWorkout.objects.filter(user_id=cur_user.id).count()

        if has_workout == 1:
            associated_workout = NewWorkout.objects.get(user_id=cur_user.id)
            has_calculated_workout = WorkoutWeek.objects.filter(associated_workout=associated_workout.id).count()
            if has_calculated_workout > 0:
                return HttpResponseRedirect('/home/')

        form = NewWorkoutForm(request.POST)
        if form.is_valid():
            if has_workout > 0:
                NewWorkout.objects.filter(user_id=cur_user.id).delete()
                cur_user_profile.has_workout = 0
                cur_user_profile.save()

            new_workout = NewWorkout(
                max_squat=form.cleaned_data['max_squat'],
                max_bench=form.cleaned_data['max_bench'],
                max_deadlift=form.cleaned_data['max_deadlift'],
                max_overhead=form.cleaned_data['max_overhead'],            
                user_id=cur_user
            )
            new_workout.save()
            cur_user_profile.has_workout = 1
            cur_user_profile.save()
            workout_multiplier = .65
            for i in range(1, 4):
                create_workout_week(request, workout_multiplier, ' week ' + str(i))
                workout_multiplier += .05
            workout_multiplier = .4
            create_workout_week(request, workout_multiplier, ' week 4')
        return render(request, "home.html")


# auto login adapted from https://stackoverflow.com/questions/3222549/how-to-automatically-login-a-user-after-registration-in-django
def register(request):
    if request.method == 'POST':
        form = registration_form(request.POST)
        if form.is_valid():
            form.save(commit=True)
            newUser = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(request, newUser)
            return redirect("/home/")
    else:
        form = registration_form()
    context = {
        "form":form
        }
    return render(request,"registration/register.html",context)