from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Category(models.Model):
    icon = models.ImageField(null=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Product(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    image = models.ImageField()
    price = models.IntegerField()
    description = models.TextField()
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.title


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author}_{self.product}'

