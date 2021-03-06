from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from models import *

class CesiumUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    def save(self, commit=True):
        user = super(CesiumUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class CesiumUserUpdateForm(CesiumUserCreationForm):
    pass 

class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        exclude = ('last_testrun',)
