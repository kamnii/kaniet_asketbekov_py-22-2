from django.db import models


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=100)


class Product(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField()
    price = models.IntegerField()
    description = models.TextField()
    category = models.ManyToManyField(Category)
