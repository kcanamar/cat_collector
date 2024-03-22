from django.shortcuts import render
from .models import Cat

# Add the following import

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def cat_index(request):
    cats = Cat.objects.order_by('id')
    return render(request, 'cats/index.html', { 'cats': cats })

def cats_detail(request, cat_id):
    # Get the individual cat
    cat = Cat.objects.get(id=cat_id)
    # Render template, passing the cat data
    return render(request, 'cats/detail.html', { 'cat': cat })

