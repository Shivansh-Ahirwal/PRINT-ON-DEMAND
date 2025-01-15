from django.urls import path
from .views import (
    add_product, 
    cart_view, 
    add_to_cart, 
    remove_from_cart, 
    product_detail_view, 
    signup_view, 
    signin_view,
    signout_view,home,
    update_cart_quantity,
    products_by_category_view,
    trending_products_view,
    my_products_view
)
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', home, name='home'),

    # Product URLs
    path('product/<int:pk>/', product_detail_view, name='product_detail'),  # View product details
    path('add-product/', add_product, name='add_product'),  # Add a new product
    path('category/<slug:category_slug>/', products_by_category_view, name='products_by_category'),
    path('trending/', trending_products_view, name='trending_view'),
    path('my-stuff/', my_products_view, name='my_product'),
    
    # Cart URLs
    path('cart/', cart_view, name='view_cart'),  # View cart
    path('product/<int:pk>/add-to-cart/', add_to_cart, name='add_to_cart'),  # Add product to cart
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),  # Remove product from cart
    path('update_cart_quantity/<int:product_id>/', update_cart_quantity, name='update_cart_quantity'),

    # Authentication URLs
    path('signup/', signup_view, name='signup'),  # Signup page
    path('signin/', signin_view, name='signin'),  # Signin page
    path('signout/', signout_view, name='signout'),  # Signout page
]

if settings.DEBUG:  # Only for development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)