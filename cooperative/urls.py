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
from django.conf.urls.static import static
from django.conf import settings
from main import views as main 
from user import views as user
from customer import views as customer

urlpatterns = [
    path("admin/", admin.site.urls),
    
    path("", customer.AddEntryView.as_view(), name="add-entry"),
    
    path("overview/", main.HomeView.as_view(), name="overview"),
    path("get-customer-name/", customer.AjaxReturnCustomerID.as_view(), name="get-customer-name"),
    path("customer/<int:pk>/", customer.CustomerDetailView.as_view(), name="customer"),
    path("add-customer/", customer.CustomerCreateView.as_view(), name="add-customer"),
    path("customers/", customer.CustomerListView.as_view(), name="customers"),
    path("entries/", customer.EntryListView.as_view(), name="entries"),
    
    path("users/", user.UserListView.as_view(), name="users"),
    path("add-user/", user.UserCreateView.as_view(), name="add-user"),
    path("today/", user.UserEntriesTodayView.as_view(), name="entries-today"),
    path("summaries/", user.DailySummaryView.as_view(), name="summaries"),
    
    path("login/", user.LoginView.as_view(), name="login"),
    path("logout/", user.LogoutView.as_view(), name="logout")
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
