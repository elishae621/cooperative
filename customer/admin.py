from django.contrib import admin
from customer.models import Customer, Deposit, Withdrawal


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "balance"]
    
    
@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ["customer", "user", "date_created", "amount"]
    readonly_fields = ("balance",)
    

@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ["customer", "user", "date_created", "amount"]
    readonly_fields = ("balance",)
