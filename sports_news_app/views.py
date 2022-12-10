from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # render(request)
    return HttpResponse("Hello from sports news!")
