from django.shortcuts import render    
from django.http import HttpResponse
from .models import SubRabble

def index(request):
    context = {
        'subrabbles': SubRabble.objects.all()
    }
    return render(request, "rabble/index.html", context)

def profile(request):
    return render(request, "rabble/profile.html")
