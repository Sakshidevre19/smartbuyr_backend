from django.urls import path
from .views import product_list, recommend_products, product_detail, search_products

urlpatterns = [
    path('products/', product_list),
    path('products/search/', search_products),
    path('products/<int:product_id>/', product_detail),
    path('products/<int:product_id>/recommendations/', recommend_products),
]
