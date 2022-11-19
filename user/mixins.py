from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    
    def test_func(self):
        return self.request.user.is_staff
    
    def dispatch(self, request, *args, **kwargs):
        is_staff = self.get_test_func()()
        if not is_staff:
            return redirect(reverse('overview'))
        return super().dispatch(request, *args, **kwargs)

