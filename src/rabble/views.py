from django.shortcuts import render    
from django.http import HttpResponse

def index(request):
    return render(request, "rabble/index.html")

def profile(request):
    return render(request, "rabble/profile.html")
