from django.urls import path
from product.views import CategoriesView, ProductsView, ProductDetailView, ProductCreateView


urlpatterns = [
    path('categories/', CategoriesView.as_view()),
    path('products/', ProductsView.as_view()),
    path('products/<int:id>/', ProductDetailView.as_view()),
    path('products/create/', ProductCreateView.as_view())
]
