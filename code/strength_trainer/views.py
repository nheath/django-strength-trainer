from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpRequest
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

def update(request, week, workout):
    cur_user = request.user
    new_workout = NewWorkout.objects.get(user_id=cur_user.id)
    workout_weeks = WorkoutWeek.objects.filter(associated_workout=new_workout.id)
    workout_week = workout_weeks.get(name=week)
    if workout == 'bench':        
        WorkoutWeek.objects.filter(pk=workout_week.id).update(bench_done=True)
    if workout == 'squat':        
        WorkoutWeek.objects.filter(pk=workout_week.id).update(squat_done=True)
    if workout == 'deadlift':        
        WorkoutWeek.objects.filter(pk=workout_week.id).update(deadlift_done=True)        
    if workout == 'overhead':        
        WorkoutWeek.objects.filter(pk=workout_week.id).update(overhead_done=True)     
    # check if they have any more unfinished workouts
    weeksdone = 0
    for single_week in workout_weeks:
        if single_week.bench_done and single_week.squat_done and single_week.deadlift_done and single_week.overhead_done:
            weeksdone += 1
    if weeksdone == 4:
        # new_max_squat = new_workout.max_squat + 10
        # NewWorkout.objects.filter(user_id=cur_user.id).update(max_squat=new_max_squat)
        # new_max_bench = new_workout.max_bench + 5
        # NewWorkout.objects.filter(user_id=cur_user.id).update(max_bench=new_max_bench)
        # new_max_deadlift = new_workout.max_deadlift + 10
        # NewWorkout.objects.filter(user_id=cur_user.id).update(max_deadlift=new_max_deadlift)
        # new_max_overhead = new_workout.max_overhead + 5
        # NewWorkout.objects.filter(user_id=cur_user.id).update(max_overhead=new_max_overhead)
        # new_request = HttpRequest()
        # new_request.mode = 'POST'
        # new_request.META = request.META
        return redirect('/new_workout/')
        #make a new workout
    return redirect("/home/")

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

        workout_dict = {}
        workout_dict['workout_weeks'] = []
        user_workout = NewWorkout.objects.get(user_id=cur_user.id)
        user_workout_weeks = WorkoutWeek.objects.filter(associated_workout=user_workout.id)
        for week in user_workout_weeks:
            workout_dict['workout_weeks'] += [{
                "name": week.name,
                "pretty_name": week.prettyName,
                "bench": week.bench,
                "bench_done": week.bench_done,
                "squat": week.squat,
                "squat_done": week.squat_done,
                "deadlift": week.deadlift,
                "deadlift_done": week.deadlift_done,
                "overhead": week.overhead,
                "overhead_done": week.overhead_done,
            }]
        context = {
            "user": request.user.username,
            "hasWorkout": True,
            "workoutWeeks": workout_dict['workout_weeks'],
        }
        print(context)
        return render(request, "home.html", context)
    ## This is when you create a new_workout and new workout_schedule
    if request.method == 'POST':
        # get current user from request
        cur_user = request.user

        # Get the current user profile from db
        cur_user_profile = User_Profile_Model.objects.get(user_id=cur_user.id)

        #Check if user has a workout already if so clean it up.
        has_workout = NewWorkout.objects.filter(user_id=cur_user.id).count()

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
                create_workout_week(request, workout_multiplier, '_week_' + str(i))
                workout_multiplier += .05
            workout_multiplier = .4
            create_workout_week(request, workout_multiplier, '_week_4')
            return redirect('/home/')
        #else:
            # mod_workout = NewWorkout.objects.filter(user_id=cur_user.id)           
            # if has_workout > 0:
            #     new_workout = NewWorkout(
            #         max_squat = mod_workout.max_squat,
            #         max_bench = mod_workout.max_bench,
            #         max_deadlift = mod_workout.max_deadlift,
            #         max_overhead = mod_workout.max_overhead,
            #         user_id=cur_user
            #     )
            #     NewWorkout.objects.filter(user_id=cur_user.id).delete()
            #     cur_user_profile.has_workout = 0
            #     cur_user_profile.save()
            #     new_workout.save()
            #     cur_user_profile.has_workout = 1
            #     cur_user_profile.save()                                
            #     workout_multiplier = .65
            #     for i in range(1, 4):
            #         create_workout_week(request, workout_multiplier, '_week_' + str(i))
            #         workout_multiplier += .05
            #     workout_multiplier = .4
            #     create_workout_week(request, workout_multiplier, '_week_4')
            #     return redirect('/home/')                
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