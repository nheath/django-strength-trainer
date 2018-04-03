from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import registration_form, NewWorkoutForm
from .models import NewWorkout, User_Profile_Model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

def new_workout(request):
    form = NewWorkoutForm()
    context = {
        "form":form
    }
    return render(request, "new_workout.html", context)

def index(request):
    if request.user.is_authenticated:
        username = request.user.username
        return render(request, "home.html")
    else:
        return render(request, "index.html")

@login_required(login_url="/")
def home(request):
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
    return render(request, "home.html")

def register(request):
    if request.method == 'POST':
        form = registration_form(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect("/")
    else:
        form = registration_form()
    context = {
        "form":form
        }
    return render(request,"registration/register.html",context)