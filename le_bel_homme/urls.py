from django.urls import path
# from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shop/', views.shop, name='shop'),
    path('info/', views.info, name='info'),
    path('cart/', views.cart, name='cart'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('item/', views.item, name='item'),
]