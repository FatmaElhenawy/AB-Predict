from dataclasses import fields
from pyexpat import model
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class UserRegisterForm(UserCreationForm):
	username = forms.CharField(max_length=30, required = True)
	email = forms.EmailField(max_length=250, required=True)
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

          
def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

cdr_validator = RegexValidator(
    regex=r'^[ABCDEFGHIKLMNPQRSTUVWY]+$',
    message='Only capital letters A, B, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y are allowed.'
)
class userInputForm(forms.Form):
    H_CDR1 = forms.CharField(label='H_CDR1', max_length=12)
    H_CDR2 = forms.CharField(label='H_CDR2', max_length=22)
    H_CDR3 = forms.CharField(label='H_CDR3', max_length=31)
    L_CDR1 = forms.CharField(label='L_CDR1', max_length=16)
    L_CDR2 = forms.CharField(label='L_CDR2', max_length=8)
    L_CDR3 = forms.CharField(label='L_CDR3', max_length=18)
    Epitope = forms.CharField(label='Epitope', max_length=515)
    Description = forms.CharField(
        label='Description',
        max_length=500,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
class outputForm(forms.Form):
    result = forms.BooleanField()

class userInputForm2(forms.Form):
    TYPE_CHOICES = [
        ('', 'Select Type'),
        ('H', 'H'),  
        ('L', 'L'),  
	]
    CDR_CHOICES = [
        ('', 'Select CDR'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
	]
    Type = forms.ChoiceField(label='Type', choices=TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    CDR = forms.ChoiceField(label='CDR', choices=CDR_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    BWindow = forms.CharField(label='Antibody Window', max_length=9, widget=forms.TextInput(attrs={'class': 'form-control'}))
    AWindow = forms.CharField(label='Antigen Window', max_length=9, widget=forms.TextInput(attrs={'class': 'form-control'}))
    BSol = forms.CharField(label='Antibody Solvent accessibility', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    ASol = forms.CharField(label='Antigen Solvent accessibility', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    BSec = forms.CharField(label='Antibody Secondary Structure', max_length=17, widget=forms.TextInput(attrs={'class': 'form-control'}))
    ASec = forms.CharField(label='Antigen Secondary Structure', max_length=17, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Description = forms.CharField(
        label='Description',
        max_length=500,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
   
