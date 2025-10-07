from django.forms import forms
from .models import CustomUser

#no utilizado por ahora

# class RegisterForm(forms.ModelForm):

#     class Meta:
#         model = CustomUser
#         fields = ['username','email','password','checkbox']

#     def clean_username(self):
#         username = self.cleaned_data['username']
#         if CustomUser.objects.filter(username=username).exists():
#             raise forms.ValidationError("Este nombre de usuario ya fue registrado")
#         return username
    
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if CustomUser.objects.filter(email=email).exists():
#             raise forms.ValidationError("Este correo electronico ya fue registrado")
#         return email
    
        