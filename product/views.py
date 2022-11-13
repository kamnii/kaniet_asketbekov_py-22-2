from django.shortcuts import render
from product.models import Category, Product


# Create your views here.

def categories_view(request):
    if request.method == 'GET':
        categories = [{
            'id': category.id,
            'title': category.title
        } for category in Category.objects.all()]

        data = {
            'categories': categories
        }

        return render(request, 'categories/categories.html', context=data)


def products_view(request):
    if request.method == 'GET':
        products = [{
            'id': product.id,
            'title': product.title,
            'description': product.description,
            'image': product.image,
            'price': product.price,
            'categories': product.category.all(),

        } for product in Product.objects.all()]

        data = {
            'products': products
        }

        return render(request, 'products/products.html', context=data)
