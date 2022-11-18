"""cooperative URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
from django.contrib import admin
from django.urls import path

from main import views as main 
from user import views as user
from customer import views as customer

urlpatterns = [
    path("admin/", admin.site.urls),
    
    path("", main.HomeView.as_view(), name="overview"),
    
    path("add-entry/", customer.AddEntryView.as_view(), name="add-entry"),
    path("get-customer-name/", customer.AjaxReturnCustomerID.as_view(), name="get-customer-name"),
    
    path("login/", user.LoginView.as_view(), name="login"),
    path("logout/", user.LogoutView.as_view(), name="logout")
]
