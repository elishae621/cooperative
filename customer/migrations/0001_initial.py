# Generated by Django 4.1.3 on 2022-11-16 16:21

import customer.models
import customer.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                (
                    "balance",
                    models.DecimalField(decimal_places=2, default=0, max_digits=12),
                ),
                (
                    "slug",
                    models.CharField(
                        default=customer.utils.generate_slug, max_length=10
                    ),
                ),
                (
                    "passport",
                    models.ImageField(
                        default="/defaults/profile-picture.png",
                        upload_to=customer.models.Customer.image_location,
                    ),
                ),
                ("phone", models.CharField(blank=True, max_length=20, null=True)),
                ("address", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Withdrawal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("last_saved", models.DateTimeField(auto_now=True)),
                (
                    "amount",
                    models.DecimalField(decimal_places=2, default=0, max_digits=12),
                ),
                (
                    "balance",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        help_text="Customer's account balance after deposit entry",
                        max_digits=12,
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="customer.customer",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Deposit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("last_saved", models.DateTimeField(auto_now=True)),
                (
                    "amount",
                    models.DecimalField(decimal_places=2, default=0, max_digits=12),
                ),
                (
                    "balance",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        help_text="Customer's account balance after deposit entry",
                        max_digits=12,
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="customer.customer",
                    ),
                ),
            ],
        ),
    ]