from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    page_message = "CINS465"
    context={
        "page_message":page_message
    }
    return render(request, 'index.html', context)

