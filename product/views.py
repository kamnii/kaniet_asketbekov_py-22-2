from django.shortcuts import render
from product.models import Category, Product, Review


# Create your views here.

def categories_view(request, **kwargs):
    if request.method == 'GET':
        categories = Category.objects.all()

        data = {
            'categories': categories
        }

        return render(request, 'categories/categories.html', context=data)


def products_view(request):
    if request.method == 'GET':
        categories_id = request.GET.get('category_id')

        if categories_id:
            products = Product.objects.filter(category__in=[categories_id])
        else:
            products = Product.objects.all()

        products = [{
            'id': product.id,
            'title': product.title,
            'description': product.description,
            'image': product.image,
            'price': product.price,
            'categories': product.category.all(),
        } for product in products]

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
