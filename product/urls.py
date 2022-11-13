from django.urls import path
from product.views import categories_view, products_view


urlpatterns = [
    path('categories/', categories_view),
    path('products/', products_view),

]
