from autoslug import AutoSlugField
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import AnonymousUser as DjangoAnonymousUser
from django.urls import reverse


class CustomAccountManager(BaseUserManager):

    def _create_user(self, name, email, password, **other_fields):
        """create and saves the user with the given info"""

        if not email:
            raise ValueError('You must provide an email address')
        
        if not name:
            raise ValueError('You must add a name')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name, email, password=None, **other_fields):
        other_fields.setdefault('is_superuser', False)
        other_fields.setdefault('is_staff', False)
        other_fields.setdefault('is_active', True)

        return self._create_user(name, email, password, **other_fields)

    def create_superuser(self, name, email, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self._create_user(name, email, password, **other_fields)

# holiday, apartments, short stay, vacation

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50, unique=False, null=True, blank=True)
    slug = AutoSlugField(populate_from='email', unique_with=['id', 'name'])
    access_code = models.CharField(max_length=30, unique=False, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True, unique=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]

    def __str__(self):
        return self.name

class CustomAnonymousUser(DjangoAnonymousUser):
    ip = None

    def __init__(self, request):
        self.ip = request.META.get('REMOTE_ADDR')
        super().__init__()
        
    def get_absolute_url(self):
        return reverse('user:login')
