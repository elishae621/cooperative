from django import forms
from user.forms import MyBaseForm
from customer.models import Deposit, Withdrawal, Customer

class EntryForm(MyBaseForm):
    entry_type = forms.ChoiceField(choices=[(1, 'DEPOSIT'), (2, "WITHDRAWAL")], required=True)
    customer_id = forms.CharField(required=True)
    amount = forms.IntegerField(required=True, min_value=1)

    def save(self, user):
        customer = Customer.objects.get(id=self.cleaned_data["customer_id"])
        amount = self.cleaned_data['amount']
        entry_type = self.cleaned_data["entry_type"]
        if entry_type == "1":
            Deposit.objects.create(
                customer=customer,
                user=user,
                amount=amount,
                balance=customer.balance + amount
            )
            customer.balance += amount
        if entry_type == "2": 
            Withdrawal.objects.create(
                customer=customer,
                user=user,
                amount=amount,
                balance=customer.balance - amount
            )
            customer.balance -= amount
        customer.save()
        return customer
    
