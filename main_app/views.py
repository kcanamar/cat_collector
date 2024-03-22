from django.shortcuts import render, redirect
from .models import Cat

# import the FeedingForm
from .forms import FeedingForm

# Add the following import
from django.views.generic.edit import CreateView, UpdateView, DeleteView

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
    # instantiate the FeedingForm to be rendered in the template
    feeding_form = FeedingForm()
    # Render template, passing the cat data
    return render(
        request, 
        'cats/detail.html', 
        { 
            'cat': cat,
            'feeding_form': feeding_form
        }
    )

class CatCreate(CreateView):
    model = Cat
    fields = '__all__'
    # or you can explicitly pick which fields
    # fields = ['name', 'breed', 'description', 'age']
    success_url = '/cats/'
    
class CatUpdate(UpdateView):
    model = Cat
    # lets disallow renaming the cat
    fields = ['breed', 'description', 'age']
    
class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats/'

# FEEDINGS

def add_feeding(request, cat_id):
    # create the ModelForm using the data in request.POST
    form = FeedingForm(request.POST)
    # validate the form
    if form.is_valid():
        # wait to save the cat in the db unit is has the cat_id assigned
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()
        
    return redirect('detail', cat_id=cat_id)