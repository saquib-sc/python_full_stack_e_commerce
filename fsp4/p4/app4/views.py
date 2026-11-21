from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Product


def login_page(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username") or request.POST.get("Username")
        password = request.POST.get("password") or request.POST.get("Password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "accounts/login.html", {"error": "Invalid username or password"})

    return render(request, "accounts/login.html")


def logout_page(request):
    logout(request)
    return redirect("login")


def register_page(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not username or not password:
            return render(
                request,
                "accounts/register.html",
                {"error": "Username and password are required.", "username": username, "email": email},
            )

        if password != confirm_password:
            return render(
                request,
                "accounts/register.html",
                {"error": "Passwords do not match.", "username": username, "email": email},
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "accounts/register.html",
                {"error": "Username already taken.", "username": username, "email": email},
            )

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect("home")

    return render(request, "accounts/register.html")


def home(request):
    products = Product.objects.order_by("-created_at")
    context = {"products": products}

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")

        name = request.POST.get("name", "")
        price_raw = request.POST.get("price", "")
        description = request.POST.get("description", "")
        image = request.FILES.get("image")

        if not name or not price_raw or not description:
            context.update({
                "product_error": "All product fields are required.",
                "name": name,
                "price": price_raw,
                "description": description,
            })
            return render(request, "accounts/home.html", context)

        try:
            price = Decimal(price_raw)
            if price < 0:
                raise InvalidOperation
        except InvalidOperation:
            context.update({
                "product_error": "Enter a valid non-negative price.",
                "name": name,
                "price": price_raw,
                "description": description,
            })
            return render(request, "accounts/home.html", context)

        Product.objects.create(
            name=name,
            price=price,
            description=description,
            image=image,
        )
        return redirect("home")

    return render(request, "accounts/home.html", context)


@login_required(login_url="login")
def delete_product(request, pk):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=pk)
        product.delete()
    return redirect("home")