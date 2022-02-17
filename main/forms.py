from django.forms import ModelForm
from .models import Products, User, Orders
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, TextInput, EmailInput, FileInput, NumberInput


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email']


class CheckoutForm(ModelForm):
    class Meta:
        model = Orders
        fields = ['owner', 'email', 'phone','address', 'country', 'city', 'zip_code',]

        widgets = {
            'owner': TextInput(attrs={
                'class': "input",
                'placeholder': 'Your full name'
            }),
            'address': TextInput(attrs={
                'class': "input",
                'placeholder': 'Address'
            }),
            'country': TextInput(attrs={
                'class': "input",
                'placeholder': 'Country'
            }),
            'city': TextInput(attrs={
                'class': "input",
                'placeholder': 'City'
            }),
            'zip_code': TextInput(attrs={
                'class': "input",
                'placeholder': 'Zip code'
            }),
            'phone': TextInput(attrs={
                'class': "input",
                'placeholder': 'Phone',
                'type': 'tel'
            }),
            'email': EmailInput(attrs={
                'class': "input",
                'placeholder': 'Email',
                'type': 'email'
            }),
        }


