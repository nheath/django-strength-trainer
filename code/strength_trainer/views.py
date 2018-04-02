from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import registration_form
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


def index(request):
    if request.user.is_authenticated:
        username = request.user.username
        return render(request, "home.html")
    else:
        return render(request, "index.html")

@login_required(login_url="/")
def home(request):
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