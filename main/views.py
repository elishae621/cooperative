from django.views.generic import TemplateView 
from customer.models import Customer
from django.views.generic.list import ListView
from user.mixins import StaffRequiredMixin


class HomeView(StaffRequiredMixin, ListView):
    template_name = "main/overview.html"
    model = Customer
    context_object_name = "customers"
    ordering = ["name", "balance",]