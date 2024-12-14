from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.http import HttpResponse,HttpResponseForbidden
from .models import Product, User, Category


# Home view
def home(request):
    if request.user.is_authenticated:
        products = Product.objects.all()
        return render(request,'home.html',{'products': products})
    else:
        return render(request, 'landing_page.html')


# Seller registration view
def seller_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # Create user as seller
        user = User.objects.create_user(
            username=username, email=email, password=password, is_seller=True)
        user.save()
        return redirect('seller_login')
    return render(request, 'register_seller.html')


# Customer registration view
def customer_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # Create user as a regular customer
        user = User.objects.create_user(
            username=username, email=email, password=password, is_seller=False)
        user.save()
        return HttpResponse("Customer registered successfully! You can now log in.")
    return render(request, 'register_customer.html')


# Login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('profile')
        return HttpResponse("Invalid username or password!")
    return render(request, 'login.html')

def seller_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('profile')
        return HttpResponse("Invalid username or password!")
    return render(request, 'seller_login.html')

# Logout view
def user_logout(request):
    logout(request)
    return redirect('user_login')


# Profile view
@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})


# Product listing for all users
def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'product_list.html', {'categories': categories, 'products': products})

@login_required
def upload_product(request):
    if not request.user.is_seller:  # Check if the user is a seller
        return HttpResponseForbidden("You are not authorized to upload products.")

    if request.method == "POST":
        # Extract data from the POST request
        category_id = request.POST.get('category')
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')

        # Validate the required fields
        if not (category_id and name and slug and description and price and stock):
            return render(request, 'upload_product.html', {'error': "All fields are required!"})

        # Get the category object
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return render(request, 'upload_product.html', {'error': "Invalid category!"})

        # Create and save the product
        product = Product.objects.create(
            category=category,
            name=name,
            slug=slug,
            description=description,
            price=price,
            stock=stock,
            seller=request.user,
        )
        return redirect('seller_home')  # Redirect to the seller's home page

    categories = Category.objects.all()  # Get all categories for the dropdown
    return render(request, 'upload_product.html', {'categories': categories})
