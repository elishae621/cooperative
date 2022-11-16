from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from user.forms import LoginForm


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
