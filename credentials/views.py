from django.contrib import auth, messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from productapp.models import Shop
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def home(request):
    if request.method == "POST":
        try:
            username = request.POST.get("username", "").strip()
            password = request.POST.get("password", "").strip()

            if not username or not password:
                return JsonResponse(
                    {"success": False, "message": "Username and password are required"},
                    status=400,
                )

            logger.info(f"Login attempt for user: {username}")
            user = authenticate(username=username, password=password)

            if user is not None:
                auth_login(request, user)
                logger.info(f"Login successful for user: {username}")
                return JsonResponse({"success": True, "redirect_url": "/"})
            else:
                logger.warning(f"Login failed for user: {username}")
                return JsonResponse(
                    {"success": False, "message": "Invalid credentials"}
                )

        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return JsonResponse(
                {"success": False, "message": f"Server error: {str(e)}"}, status=500
            )

    # GET request - show trending products
    try:
        trending_products = Shop.objects.filter(cat="trending").order_by("-created_at")[
            :6
        ]
    except Exception as e:
        logger.error(f"Error fetching trending products: {str(e)}")
        trending_products = []

    return render(request, "home.html", {"trending_products": trending_products})


def demo(request):
    return render(request, "demo.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        cpassword = request.POST["password1"]

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username taken")
                return redirect("credentials:register")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already taken")
                return redirect("credentials:register")
            else:
                user = User.objects.create_user(
                    username=username, password=password, email=email
                )
                user.save()
                print("User created")
                return redirect("credentials:home")
        else:
            messages.info(request, "Passwords do not match")
            return redirect("credentials:register")
    return render(request, "register.html")


def logout_view(request):
    auth.logout(request)
    return redirect("credentials:home")


def index(request):
    return render(request, "index.html")


def test_api(request):
    """Test endpoint to check if backend is working"""
    return JsonResponse(
        {
            "status": "working",
            "database": "connected",
            "user_count": User.objects.count(),
            "shop_count": Shop.objects.count(),
        }
    )
