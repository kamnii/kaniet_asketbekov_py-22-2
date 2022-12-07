from django.shortcuts import render, redirect
from product.models import Category, Product, Review
from product.forms import ProductCreateForm, ReviewCreateForm
from users.utils import get_user_from_request
from django.views.generic import ListView, CreateView, DetailView

# Create your views here.

PAGINATION_LIMIT = 2


class CategoriesView(ListView):
    model = Category
    template_name = 'categories/categories.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'user': get_user_from_request(self.request),
            'categories': self.get_queryset()
        }


# def categories_view(request, **kwargs):
#     if request.method == 'GET':
#         categories = Category.objects.all()
#
#         data = {
#             'categories': categories,
#             'user': get_user_from_request(request)
#         }
#
#         return render(request, 'categories/categories.html', context=data)


class ProductsView(ListView):
    model = Product
    template_name = 'products/products.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'products': kwargs['products'],
            'user': get_user_from_request(self.request),
            'max_page': range(1, kwargs['max_page'] + 1),
            'category_id': kwargs['category_id']
        }

    def get(self, request, *args, **kwargs):
        category_id = request.GET.get('category_id')
        search_text = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        if category_id:
            products = Product.objects.filter(category__in=[category_id])
        else:
            products = Product.objects.all()

        if search_text:
            products = products.filter(title__icontains=search_text)

        products = [{
            'id': product.id,
            'title': product.title,
            'description': product.description,
            'image': product.image,
            'price': product.price,
            'categories': product.category.all(),
        } for product in products]

        max_page = round(products.__len__() / PAGINATION_LIMIT)
        products = products[PAGINATION_LIMIT * (page - 1):PAGINATION_LIMIT * page]

        return render(request, 'products/products.html', context=self.get_context_data(
            products=products,
            max_page=max_page,
            category_id=category_id
        ))


# def products_view(request):
#     if request.method == 'GET':
#         category_id = request.GET.get('category_id')
#         search_text = request.GET.get('search')
#         page = int(request.GET.get('page', 1))
#
#         if category_id:
#             products = Product.objects.filter(category__in=[category_id])
#         else:
#             products = Product.objects.all()
#
#         if search_text:
#             products = products.filter(title__icontains=search_text)
#
#         products = [{
#             'id': product.id,
#             'title': product.title,
#             'description': product.description,
#             'image': product.image,
#             'price': product.price,
#             'categories': product.category.all(),
#         } for product in products]
#
#         max_page = round(products.__len__() / PAGINATION_LIMIT)
#         products = products[PAGINATION_LIMIT * (page - 1):PAGINATION_LIMIT * page]
#
#         data = {
#             'products': products,
#             'user': get_user_from_request(request),
#             'category_id': category_id,
#             'max_page': range(1, max_page + 1)
#         }
#
#         return render(request, 'products/products.html', context=data)


class ProductDetailView(DetailView, CreateView):
    model = Product
    form_class = ReviewCreateForm
    template_name = 'products/detail.html'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        return {
            'user': get_user_from_request(self.request),
            'form': kwargs['form'] if kwargs.get('form') else self.form_class,
            'product': self.get_object(),
            'reviews': kwargs['reviews'],
            'categories': kwargs['categories']
        }

    def get(self, request, *args, **kwargs):
        product_id = self.model.objects.get(id=kwargs['id'])
        reviews = Review.objects.filter(product_id=product_id)
        categories = product_id.category.all()

        return render(request, self.template_name, context=self.get_context_data(
            reviews=reviews,
            categories=categories
        ))

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            Review.objects.create(
                author_id=request.user.id,
                product_id=kwargs['id'],
                text=form.cleaned_data.get('text')
            )
            return redirect(f"/products/{kwargs['id']}/")

        else:
            return render(request, self.template_name, context=self.get_context_data(form=form))


# def product_detail_view(request, id):
#     if request.method == 'GET':
#         product = Product.objects.get(id=id)
#         reviews = Review.objects.filter(product_id=id)
#
#         data = {
#             'product': product,
#             'categories': product.category.all(),
#             'reviews': reviews,
#             'form': ReviewCreateForm,
#             'user': get_user_from_request(request)
#         }
#
#         return render(request, 'products/detail.html', context=data)
#
#     if request.method == 'POST':
#         form = ReviewCreateForm(data=request.POST)
#
#         if form.is_valid():
#             Review.objects.create(
#                 author_id=request.user.id,
#                 text=form.cleaned_data.get('text'),
#                 product_id=id
#             )
#             return redirect(f'/products/{id}/')
#         else:
#             product = Product.objects.get(id=id)
#             reviews = Review.objects.filter(product_id=id)
#
#             data = {
#                 'product': product,
#                 'categories': product.category.all(),
#                 'reviews': reviews,
#                 'form': form,
#                 'user': get_user_from_request(request)
#             }
#             return render(request, 'products/detail.html', context=data)


class ProductCreateView(CreateView):
    form_class = ProductCreateForm
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        return {
            'form': kwargs['form'] if kwargs.get('form') else self.form_class,
            'user': get_user_from_request(self.request)
        }

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            Product.objects.create(
                author_id=request.user.id,
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                price=form.cleaned_data.get('price')
            )
            return redirect('/products')

        else:
            return render(request, self.template_name, context=self.get_context_data(form=form))


# def product_create_view(request):
#     if request.method == 'GET':
#         data = {
#             'form': ProductCreateForm,
#             'user': get_user_from_request(request)
#         }
#
#         return render(request, 'products/create.html', context=data)
#
#     if request.method == 'POST':
#         form = ProductCreateForm(data=request.POST)
#
#         if form.is_valid():
#             Product.objects.create(
#                 author_id=request.user.id,
#                 title=form.cleaned_data.get('title'),
#                 description=form.cleaned_data.get('description'),
#                 price=form.cleaned_data.get('price'),
#             )
#             return redirect('/products')
#         else:
#             data = {
#                 'form': form,
#                 'user': get_user_from_request(request)
#             }
#             return render(request, 'products/create.html', context=data)
