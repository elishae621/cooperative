from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from customer.models import Customer, Deposit, Withdrawal


@receiver(post_save, sender=Deposit)
def update_balance_after_adding_deposit(sender, instance, created, **kwargs):
    if created:
        instance.customer.balance += instance.amount
        instance.customer.save()


@receiver(post_save, sender=Withdrawal)
def update_balance_after_adding_withdrawal(sender, instance, created, **kwargs):
    if created:
        instance.customer.balance -= instance.amount
        instance.customer.save()
     