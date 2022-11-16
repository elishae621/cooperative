from django.db import models

from customer.utils import generate_slug, generate_filename


class Customer(models.Model):
    
    def image_location(self, filename):
        file_format = filename.split('.')[1]
        filename = generate_filename() + '.' + file_format
        return '/'.join(['customer/passports/', self.slug, filename])

    name = models.CharField(max_length=50, null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    slug = models.CharField(max_length=10, default=generate_slug)
    passport = models.ImageField(upload_to=image_location, default='/defaults/profile-picture.png')
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField()
    
    
class Deposit(models.Model):
    customer = models.ForeignKey(Customer, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", null=False, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    last_saved = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    balance = models.DecimalField(decimal_places=2, max_digits=12, default=0, help_text="Customer's account balance after deposit entry")
    
    
class Withdrawal(models.Model):
    customer = models.ForeignKey(Customer, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", null=False, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    last_saved = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    balance = models.DecimalField(decimal_places=2, max_digits=12, default=0, help_text="Customer's account balance after deposit entry")