from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('promotions/', views.promotions, name='promotions'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove-single/<int:book_id>/', views.remove_single_from_cart, name='remove_single_from_cart'),
    path('cart/remove/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('favorite/toggle/<int:book_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('checkout/', views.checkout, name='checkout'),
]