from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from myapp.models import User

# Registration Form
class RegisterForm(UserCreationForm):
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
