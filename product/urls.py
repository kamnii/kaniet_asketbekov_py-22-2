from django.urls import path
from product.views import categories_view, products_view, product_detail_view


urlpatterns = [
    path('categories/', categories_view),
    path('products/', products_view),
    path('products/<int:id>/', product_detail_view)
]
