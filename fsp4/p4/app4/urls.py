from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_page, name="register_page"),
    path("", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    path("home/", views.home, name="home"),
    path("products/<int:pk>/delete/", views.delete_product, name="delete_product"),
]