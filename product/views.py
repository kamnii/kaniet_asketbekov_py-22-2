from django.shortcuts import render, redirect
from product.models import Category, Product, Review
from product.forms import ProductCreateForm, ReviewCreateForm
from users.utils import get_user_from_request


# Create your views here.

def categories_view(request, **kwargs):
    if request.method == 'GET':
        categories = Category.objects.all()

        data = {
            'categories': categories,
            'user': get_user_from_request(request)
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
            'products': products,
            'user': get_user_from_request(request)
        }

        return render(request, 'products/products.html', context=data)


def product_detail_view(request, id):
    if request.method == 'GET':
        product = Product.objects.get(id=id)
        reviews = Review.objects.filter(product_id=id)

        data = {
            'product': product,
            'categories': product.category.all(),
            'reviews': reviews,
            'form': ReviewCreateForm,
            'user': get_user_from_request(request)
        }

        return render(request, 'products/detail.html', context=data)

    if request.method == 'POST':
        form = ReviewCreateForm(data=request.POST)

        if form.is_valid():
            Review.objects.create(
                author_id=2,
                text=form.cleaned_data.get('text'),
                product_id=id
            )
            return redirect(f'/products/{id}/')
        else:
            product = Product.objects.get(id=id)
            reviews = Review.objects.filter(product_id=id)

            data = {
                'product': product,
                'categories': product.category.all(),
                'reviews': reviews,
                'form': form,
                'user': get_user_from_request(request)
            }
            return render(request, 'products/detail.html', context=data)


def product_create_view(request):
    if request.method == 'GET':
        data = {
            'form': ProductCreateForm,
            'user': get_user_from_request(request)
        }

        return render(request, 'products/create.html', context=data)

    if request.method == 'POST':
        form = ProductCreateForm(data=request.POST)

        if form.is_valid():
            Product.objects.create(
                author_id=1,
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                price=form.cleaned_data.get('price'),
            )
            return redirect('/products')
        else:
            data = {
                'form': form,
                'user': get_user_from_request(request)
            }
            return render(request, 'products/create.html', context=data)
