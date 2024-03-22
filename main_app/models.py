from django.db import models
# import the reverse function
from django.urls import reverse

MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner'),
)

# Create your models here.
class Cat(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    age = models.IntegerField()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        # Dont for get to import reverse
        return reverse("detail", kwargs={"cat_id": self.id})
    
    
class Feeding(models.Model):
    date = models.DateField('feeding date')
    meal  = models.CharField(
        max_length=1,
        # Add 'choices' field option
        choices=MEALS,
        # set default value for a meal to 'B'
        default=MEALS[0][0]
    )
    
    # Create a cat_id FK
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE) 
    
    def __str__(self):
        # Nice method for obtaining the friendly value of a Field.choice
        return f"{ self.get_meal_display() } on { self.date }"
    
    # change the default sort
    class Meta:
        ordering = ['-date']