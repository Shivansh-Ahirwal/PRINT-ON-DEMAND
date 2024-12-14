from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/seller/', views.seller_register, name='seller_register'),
    path('register/customer/', views.customer_register, name='customer_register'),
    path('login/', views.user_login, name='user_login'),
    path('seller-login/', views.seller_login, name='seller_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('profile/', views.profile_view, name='profile'),
    path('upload-product/', views.upload_product, name='upload_product'),
]
