from django.shortcuts import render
from product.models import Category, Product, Review


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


def product_detail_view(request, id):
    if request.method == 'GET':
        product = Product.objects.get(id=id)
        comments = Review.objects.filter(product__id=id)

        data = {
            'product': product,
            'comments': comments,
            'categories': product.category.all()
        }

        return render(request, 'products/detail.html', context=data)
