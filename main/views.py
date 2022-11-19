from django.views.generic import TemplateView 
from customer.models import Customer
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin



class HomeView(LoginRequiredMixin, ListView):
    template_name = "main/overview.html"
    model = Customer
    context_object_name = "customers"