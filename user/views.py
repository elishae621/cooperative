from django.views.generic.edit import FormView, CreateView
from django.views.generic.list import ListView
from django.views.generic.base import View
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from user.forms import LoginForm, UserCreateForm
from user.models import User
from user.mixins import StaffRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from customer.models import Deposit, Withdrawal
from customer.models import DailySummary
from itertools import chain


class LoginView(FormView):
    template_name = 'user/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('add-entry')
    
    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET['next']
        return self.success_url

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            logout(self.request)
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')        
        user = authenticate(email=email, password=password)
        login(self.request, user)
        user.access_code = password
        user.save()
        return super().form_valid(form)



class LogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('login'))
    

class UserListView(StaffRequiredMixin, ListView):
    template_name = "user/users.html"
    model = User 
    context_object_name = "users"
    ordering = ["name",]
    

class UserCreateView(StaffRequiredMixin, CreateView):
    template_name = "user/add_user.html"
    model = User 
    form_class = UserCreateForm
    success_url = reverse_lazy("users")
    
    def form_valid(self, form):
        user = form.save()
        user.set_password(form.cleaned_data.get('access_code', None))
        user.save()
        return HttpResponseRedirect(self.success_url)
    

class UserEntriesTodayView(LoginRequiredMixin, ListView):
    template_name = "user/entries_today.html"
    context_object_name = "entries"
    
    def get_queryset(self):
        user = self.request.user
        today = datetime.today()
        entries = sorted(chain(list(user.deposit_set.filter(date_created__date=today.date())), list(user.withdrawal_set.filter(date_created__date=today.date()))), key=lambda instance: instance.date_created, reverse=True)
        return entries
    

class DailySummaryView(LoginRequiredMixin, ListView):
    template_name = "user/daily_summary.html"
    context_object_name = "summaries"
    model = DailySummary
    ordering = ["-date",]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entries = list(Deposit.objects.all()) + list(Withdrawal.objects.all())
        total_deposits = 0
        total_withdrawals = 0
        for d in DailySummary.objects.all():
            d.reset()
        for index, entry in enumerate(entries):
            entry_date = entry.date_created.date()
            daily_summary = DailySummary.objects.get_or_create(date=entry_date)[0]
                
            if entry._meta.model_name == "deposit":
                daily_summary.total_deposit += entry.amount 
                daily_summary.no_of_deposits += 1
                total_deposits += 1
            if entry._meta.model_name == "withdrawal":
                daily_summary.total_withdrawal += entry.amount 
                daily_summary.no_of_withdrawals += 1
                total_withdrawals += 1
            daily_summary.save()
        context["total_deposits"] = total_deposits
        context["total_withdrawals"] = total_withdrawals
        return context
    