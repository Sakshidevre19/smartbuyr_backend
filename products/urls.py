from django.urls import path
from .views import product_list, recommend_products, product_detail, search_products

urlpatterns = [
    path('', product_list),  # ← IMPORTANT
    path('search/', search_products),
    path('<int:product_id>/', product_detail),
    path('<int:product_id>/recommendations/', recommend_products),
]
