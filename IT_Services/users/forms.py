from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Service

from django.shortcuts import render, redirect, get_object_or_404


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        
        
class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )




class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['service_name', 'payment_terms', 'service_price', 'service_package', 'service_tax', 'service_image', 'active']
        widgets = {
                    'service_name': forms.TextInput(attrs={'class': 'form-control'}),
                    'payment_terms': forms.Textarea(attrs={'class': 'form-control'}),
                    'service_price': forms.NumberInput(attrs={'class': 'form-control'}),
                    'service_package': forms.TextInput(attrs={'class': 'form-control'}),
                    'service_tax': forms.NumberInput(attrs={'class': 'form-control'}),
                    'service_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class SubscriptionForm(forms.Form):
    address = forms.CharField(widget=forms.Textarea, label="Address")

def subscribe(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            # Here you would handle the subscription process
            # For now, we'll just redirect to a thank you page or similar
            return redirect('thank_you')  # Redirect to a thank you or confirmation page
    else:
        form = SubscriptionForm()

    net_price = service.service_price + service.service_tax
    return render(request, 'subscribe.html', {'form': form, 'service': service, 'net_price': net_price})
