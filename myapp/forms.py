from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from myapp.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'}))
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter a password'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))        

from  myapp.models import Complaint, WarrantyClaim

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['issue_description', 'purchase_receipt', 'product_image']

class WarrantyClaimForm(forms.ModelForm):
    class Meta:
        model = WarrantyClaim
        fields = ['claim_description', 'purchase_receipt', 'product_image']

# class ComplaintForm(forms.ModelForm):
#     class Meta:
#         model = Complaint
#         fields = ['issue_description', 'purchase_receipt', 'product_image']
#         widgets = {
#             'issue_description': forms.Textarea(attrs={'placeholder': 'Describe your issue', 'class': 'form-control'}),
#             'purchase_receipt': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#             'product_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#         }

# class WarrantyClaimForm(forms.ModelForm):
#     class Meta:
#         model = WarrantyClaim
#         fields = ['claim_description', 'purchase_receipt', 'product_image']
#         widgets = {
#             'claim_description': forms.Textarea(attrs={'placeholder': 'Describe your claim', 'class': 'form-control'}),
#             'purchase_receipt': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#             'product_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#         }