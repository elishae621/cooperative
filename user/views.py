from django.views.generic.edit import FormView, CreateView
from django.views.generic.list import ListView
from django.views.generic.base import View
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from user.forms import LoginForm, UserCreateForm
from user.models import User


class LoginView(FormView):
    template_name = 'user/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('overview')
    
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
        user.raw_password = password
        user.save()
        return super().form_valid(form)



class LogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('login'))
    

class UserListView(ListView):
    template_name = "user/users.html"
    model = User 
    context_object_name = "users"
    

class UserCreateView(CreateView):
    template_name = "user/add_user.html"
    model = User 
    form_class = UserCreateForm
    success_url = reverse_lazy("users")