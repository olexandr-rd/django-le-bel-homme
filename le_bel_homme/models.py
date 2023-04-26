from django.db import models

# Create your models here.
class Perfume(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField()
    price = models.DecimalField(max_digits=6, decimal_places=0)
    volume = models.DecimalField(max_digits=6, decimal_places=0)