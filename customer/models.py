from django.db import models
from autoslug import AutoSlugField
from customer.utils import generate_filename
from django.urls import reverse


class Customer(models.Model):
    
    def image_location(self, filename):
        file_format = filename.split('.')[1]
        filename = generate_filename() + '.' + file_format
        return '/'.join(['customer/passports/', self.name, filename])
    
    name = models.CharField(max_length=50, null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    passport = models.ImageField(upload_to=image_location, default='/defaults/profile-picture.png')
    email =  models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=False, unique=True)
    address = models.TextField(null=True, blank=True)
    user = models.ForeignKey("user.User", null=True, blank=False, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('customer', kwargs={"pk": self.id})
    
    
class Deposit(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", null=True, blank=False, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    last_saved = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    balance = models.DecimalField(decimal_places=2, max_digits=12, default=0, help_text="Customer's account balance after deposit entry")
    is_deposit = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.amount} for {self.customer}"
    
    
class Withdrawal(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", null=True, blank=False, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    last_saved = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    balance = models.DecimalField(decimal_places=2, max_digits=12, default=0, help_text="Customer's account balance after deposit entry")
    is_withdrawal = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.amount} for {self.customer}"
    
    
class DailySummary(models.Model):
    date = models.DateField(null=True, blank=False, unique=True)
    total_deposit = models.IntegerField(default=0)
    total_withdrawal = models.IntegerField(default=0)
    no_of_deposits = models.IntegerField(default=0)
    no_of_withdrawals = models.IntegerField(default=0)
    
    def __str__(self):
        return self.date
    
    def reset(self):
        self.total_deposit = 0
        self.total_withdrawal = 0
        self.no_of_deposits = 0
        self.no_of_withdrawals = 0
        return self.save()