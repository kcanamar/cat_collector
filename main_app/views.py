from django.shortcuts import render

# Add the following import
from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>Hello Cats</h1>')

def about(request):
    return render(request, 'about.html')
