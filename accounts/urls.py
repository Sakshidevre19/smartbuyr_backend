from django.urls import path
from .views import signup, signin, add_to_cart, get_cart, remove_from_cart, add_to_wishlist, get_wishlist, remove_from_wishlist

urlpatterns = [
    path('signup/', signup),
    path('signin/', signin),
    path('cart/add/', add_to_cart),
    path('cart/', get_cart),
    path('cart/remove/<int:item_id>/', remove_from_cart),
    path('wishlist/add/', add_to_wishlist),
    path('wishlist/', get_wishlist),
    path('wishlist/remove/<int:item_id>/', remove_from_wishlist),
]