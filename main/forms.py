from django.forms import ModelForm
from .models import Products, User, Orders
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput, CharField
from django import forms


class MyUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'input', 'type':'password', 'align':'center', 'placeholder':'Your password'}),
        )
    password2 = forms.CharField(
            label="Confirm password",
            widget=forms.PasswordInput(attrs={'class':'input', 'type':'password', 'align':'center', 'placeholder':'Repeat your password'}),
    )
    class Meta:
        
        model = User
        fields = ['first_name', 'username', 'email']
        widgets = {
            'first_name': TextInput(attrs={
                'class': "input",
                'placeholder': 'Your full name'
            }),
            'username': TextInput(attrs={
                'class': "input",
                'placeholder': 'Your username'
            }),
            'email': EmailInput(attrs={
                'class': "input",
                'placeholder': 'Email',
                'type': 'email'
            })
        }




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


