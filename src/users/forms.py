from django import forms 
from django.db import models

from users.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'bio', 'profile_pic']

class EditProfileForm(forms.ModelForm):
    bio     = forms.CharField(max_length=280)

    class Meta:
        model = User
        fields = ['bio']

        widgets={
            'bio' : forms.TextInput(attrs={'class':'form-control'}),
        }