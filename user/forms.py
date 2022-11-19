from django import forms
from django.forms.utils import ErrorList
from django.forms import ValidationError
from user.models import User

class MyErrorList(ErrorList):
    def __init__(self, initlist=None, error_class='invalid-feedback'):
        super().__init__(initlist=initlist, error_class=error_class)


class MyBaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs_new = {**kwargs, 'error_class': MyErrorList,
                      'label_suffix': ''}
        super().__init__(*args, **kwargs_new)
        

class MyBaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs_new = {**kwargs, 'error_class': MyErrorList,
                      'label_suffix': ''}
        super().__init__(*args, **kwargs_new)


class LoginForm(MyBaseForm):
    email = forms.CharField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
            return email
        except User.DoesNotExist:
            raise ValidationError('incorrect email')

    def clean_password(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email != None:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return password
            raise ValidationError('incorrect password')
        return password
    



class UserCreateForm(MyBaseModelForm):
    class Meta:
        model = User 
        fields = ("name", "email", "access_code", "phone", "address")