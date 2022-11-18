from django.views.generic.edit import FormView, CreateView
from django.views.generic.base import View
from django.http.response import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from customer.forms import EntryForm
from customer.models import Customer


class AddEntryView(FormView):
    template_name = 'customer/add_entry.html'
    form_class = EntryForm
    success_url = reverse_lazy('overview')
    
    def form_valid(self, form):
        form.save(self.request.user)
        return HttpResponseRedirect(self.get_success_url())
    

class AjaxReturnCustomerID(View):
    def get(self, request, *args, **kwargs):
        customer_id = request.GET.get("customer_id", 0)
        data = {'ok': True}
        try:
            customer = Customer.objects.get(id=int(customer_id))
            data['name'] = customer.name
        except Customer.DoesNotExist:
            data['ok'] = False
        return JsonResponse(data=data)