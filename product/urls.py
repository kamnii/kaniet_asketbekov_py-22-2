from django.urls import path
from product.views import categories_view, products_view, product_detail_view, product_create_view


urlpatterns = [
    path('categories/', categories_view),
    path('products/', products_view),
    path('products/<int:id>/', product_detail_view),
    path('products/create/', product_create_view)
]
