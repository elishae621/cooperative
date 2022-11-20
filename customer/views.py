from django.views.generic.edit import FormView, CreateView
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http.response import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from customer.forms import EntryForm, CustomerCreateForm
from customer.models import Customer, Deposit, Withdrawal
from itertools import chain
from django.contrib.auth.mixins import LoginRequiredMixin


class AddEntryView(LoginRequiredMixin, FormView):
    template_name = 'customer/add_entry.html'
    form_class = EntryForm
    success_url = reverse_lazy('overview')
    
    def form_valid(self, form):
        form.save(self.request.user)
        return HttpResponseRedirect(self.get_success_url())
    

class AjaxReturnCustomerID(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        customer_id = request.GET.get("customer_id", 0)
        data = {'ok': True}
        try:
            customer = Customer.objects.get(id=int(customer_id))
            data['name'] = customer.name
        except Customer.DoesNotExist:
            data['ok'] = False
        return JsonResponse(data=data)
    
    
    
class CustomerCreateView(LoginRequiredMixin, CreateView):
    template_name = "customer/add_customer.html"
    model = Customer 
    form_class = CustomerCreateForm
    success_url = reverse_lazy("customers")
    
    
class CustomerDetailView(LoginRequiredMixin, DetailView):
    template_name = "customer/customer.html"
    model = Customer 
    context_object_name = "customer"
    query_pk_and_slug = True
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entries = sorted(chain(list(self.object.deposit_set.all()), list(self.object.withdrawal_set.all())), key=lambda instance: instance.date_created) 
        context["entries"] = entries
        total_deposit = 0
        for deposit in self.object.deposit_set.all():
            total_deposit += deposit.amount
        context['total_deposit'] = total_deposit
        total_withdrawal = 0
        for withdrawal in self.object.withdrawal_set.all():
            total_withdrawal += withdrawal.amount
        context['total_withdrawal'] = total_withdrawal
        self.object.balance = total_deposit - total_withdrawal
        self.object.save()
        return context
    
    
    
class CustomerListView(LoginRequiredMixin, ListView):
    template_name = "customer/customers.html"
    model = Customer
    context_object_name = "customers"
    

class DepositListView(LoginRequiredMixin, ListView):
    template_name = "customer/deposits.html"
    model = Deposit 
    context_object_name = "deposits"
    

class WithdrawalListView(LoginRequiredMixin, ListView):
    template_name = "customer/withdrawals.html"
    model = Withdrawal 
    context_object_name = "withdrawals"
    