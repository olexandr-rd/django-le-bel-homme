from django.contrib.auth.models import User
from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Perfume(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField()
    price = models.DecimalField(max_digits=6, decimal_places=0)
    volume = models.DecimalField(max_digits=6, decimal_places=0)
    url_name = models.SlugField(max_length=200, unique=True, default='')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.name



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    perfume = models.ForeignKey(Perfume, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)