from django.shortcuts import render, redirect
from .models import Cat, Toy
from django.views.generic import ListView, DetailView
# import the FeedingForm
from .forms import FeedingForm
# User Imports
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Authorization for function based views
from django.contrib.auth.decorators import login_required
# Authorization for class based views
from django.contrib.auth.mixins import LoginRequiredMixin


# Add the following import
from django.views.generic.edit import CreateView, UpdateView, DeleteView

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def cat_index(request):
    # cats = Cat.objects.order_by('id')
    # * once user model is in play
    cats = Cat.objects.filter(user=request.user)
    # cats = request.user.cat_set.all()
    
    return render(request, 'cats/index.html', { 'cats': cats })

@login_required
def cats_detail(request, cat_id):
    # Get the individual cat
    cat = Cat.objects.get(id=cat_id)
    # instantiate the FeedingForm to be rendered in the template
    feeding_form = FeedingForm()
    
    # Get the Toys the cat doesn't have
    toys_cat_doesnt_have = Toy.objects.exclude(id__in = cat.toys.all())
    
    # Render template, passing the cat data
    return render(
        request, 
        'cats/detail.html', 
        { 
            'cat': cat,
            'feeding_form': feeding_form,
            # Add the toys to be displayed
            'toys': toys_cat_doesnt_have
        }
    )

class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    fields = '__all__'
    # or you can explicitly pick which fields
    # fields = ['name', 'breed', 'description', 'age']
    success_url = '/cats/'
    
    # This inherited method is called when a valid cat form is being submitted
    def form_valid(self, form):
        # assign the logged in user (self.request.user)
        form.instance.user = self.request.user # form.instance is the cat
        # Let the CreateView do its job now
        return super().form_valid(form)
    
class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    # lets disallow renaming the cat
    fields = ['breed', 'description', 'age']
    
class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    success_url = '/cats/'

# FEEDINGS
@login_required
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

class ToyList(LoginRequiredMixin, ListView):
    model = Toy
    
class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy
    
class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'
    
class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['name', 'color']
    
class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'

@login_required
def assoc_toy(request, cat_id, toy_id):
    # Note you can pass a ty's id instead of the whole object
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('detail', cat_id=cat_id)

@login_required
def remove_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.remove(toy_id)
    return redirect('detail', cat_id=cat_id)

def signup(request):
    error_message = ''
    
    if request.method == 'POST':
        # Here we handle the user
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the user to the database
            user = form.save()
            # log the user for quality UX
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    
    # Catch a bad POST OR a GET request
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    
    # render signup.html with an empty form
    return render(request, 'registration/signup.html', context)