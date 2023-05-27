from django.contrib.auth.views import LogoutView
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shop/', views.shop, name='shop'),
    path('info/', views.info, name='info'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:perfume_id>', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove_one_from_cart/<int:cart_item_id>/', views.remove_one_from_cart, name='remove_one_from_cart'),
    path('clear_cart', views.clear_cart, name='clear_cart'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('register/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('<slug:slug>/', views.perfume_detail, name='perfume_detail'),

]