from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Product, Category
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from .models import Product, Cart, CartItem, Category,User
from django.contrib import messages
from .forms import *

def home(request):
    category_id = request.GET.get('category_id')
    
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    
    product_data = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": float(product.price),
            "category": product.category.name if product.category else None,
            "added_by": product.added_by_display(),
            "product_image": product.product_image.url if product.product_image else None  # Correct way to get the image URL
        }
        for product in products
    ]
    
    return render(request, 'index.html', {"product_data": product_data})

def product_detail_view(request, pk):
    """
    Display details of a specific product.
    """
    product = get_object_or_404(Product, pk=pk)
    product_data ={
        "id": pk,
        "name": product.name,
        "description": product.description,
        "price": float(product.price),
        "category": product.category.name if product.category else None,
        "added_by": product.added_by_display(),
        "product_image": product.product_image.url if product.product_image else None , # Correct way to get the image URL
        "added_by_admin": product.added_by_admin
    }
    return render(request, 'product_detail.html', {'product': product_data})

# Cart Views 
@login_required(login_url='signin')
def cart_view(request):
    """
    API to view the user's cart.
    """
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()

    cart_data = {
        "id": cart.id,
        "user": cart.user.username,
        "items": [
            {
                "product_name": item.product.name,
                "quantity": item.quantity,
                "price": float(item.product.price),
                "total_price": item.quantity * float(item.product.price),  # Calculate total price for each item
                "product_id": item.product.id,
                "product_image": item.product.product_image.url if item.product.product_image else None ,
            }
            for item in cart_items
        ],
        "total_cart_value": sum(item.quantity * float(item.product.price) for item in cart_items),  # Calculate total cart value
    }

    return render(request, 'cart.html', {"cart_data": cart_data})



@login_required(login_url='signin')
def add_to_cart(request, pk):
    """
    Add a product to the user's cart.
    """
    product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)  # Fetch or create the user's cart
    
    # Check if the product already exists in the cart
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        # If the item already exists, increment the quantity
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"Added another '{product.name}' to your cart.")
    else:
        # If the item is new, it's already added by get_or_create
        messages.success(request, f"'{product.name}' has been added to your cart.")

    return redirect('product_detail', pk=pk)  # Redirect back to the product detail page


@login_required(login_url='signin')
def remove_from_cart(request, product_id):
    """
    Remove a product from the user's cart.
    """
    cart, created = Cart.objects.get_or_create(user=request.user)  # Create the cart if it doesn't exist

    # Get the cart item associated with the product_id
    cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        return redirect('view_cart')
    else:
        if cart_item:
            cart_item.delete()  # Remove the cart item from the cart
            messages.success(request, 'Product has been removed from your cart.')
        else:
            messages.warning(request, 'This product is not in your cart.')

        return redirect('view_cart')  # Ensure 'cart' is correctly configured in urls.py


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Basic validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('signup')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('signin')

    return render(request, 'signup.html')


# SignIn View
def signin_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')  # Redirect to the homepage or dashboard
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('signin')

    return render(request, 'signin.html')


# SignOut View
def signout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('signin')

@login_required
def add_product(request):
    """
    View to add a new product.
    """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # Handle form with image uploads
        if form.is_valid():
            product = form.save(commit=False)
            product.added_by = request.user  # Associate the product with the logged-in user
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('product_detail', pk=product.pk)  # Redirect to the product detail page
        else:
            messages.error(request, 'There was an error with your form.')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})

@login_required(login_url='signin')
def update_cart_quantity(request, product_id):
    """Update the quantity of a product in the cart."""
    new_quantity = request.GET.get('quantity')

    if new_quantity:
        cart = Cart.objects.get(user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        cart_item.quantity = new_quantity
        cart_item.save()

        # Calculate the new total price
        new_total_price = cart_item.quantity * cart_item.product.price

        return JsonResponse({'new_total_price': new_total_price})

    return JsonResponse({'error': 'Invalid quantity'}, status=400)

def products_by_category_view(request, category_slug):
    """
    Display all products under a specific category using the slug.
    """
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    
    product_data = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": float(product.price),
            "category": product.category.name if product.category else None,
            "added_by": product.added_by_display(),
            "product_image": product.product_image.url if product.product_image else None
        }
        for product in products
    ]

    # Pass product data as context
    return render(request, 'products_by_category.html', {
        'category': category,
        'product_data': product_data,
    })

def trending_products_view(request):
    """
    Display all products having is_trending = True.
    """
    
    products = Product.objects.filter(is_trending=True)
    
    product_data = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": float(product.price),
            "category": product.category.name if product.category else None,
            "added_by": product.added_by_display(),
            "product_image": product.product_image.url if product.product_image else None
        }
        for product in products
    ]

    # Pass product data as context
    return render(request, 'trending_view.html', {
        'product_data': product_data,
    })

def my_products_view(request):
    """
    Display all products added by the logged-in user.
    """
    if not request.user.is_authenticated:
        return redirect('signin')  # Redirect to sign-in page if user is not authenticated

    products = Product.objects.filter(added_by=request.user)
    
    product_data = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": float(product.price),
            "category": product.category.name if product.category else None,
            "added_by": product.added_by.username,  # Ensure added_by_display works if a method
            "product_image": product.product_image.url if product.product_image else None
        }
        for product in products
    ]

    # Pass product data as context
    return render(request, 'my_product.html', {
        'product_data': product_data,
    })



