import re
from django.db import models
from django import forms
from django.forms import ModelForm, PasswordInput
#seguridad
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate
from django.forms import PasswordInput

from django import forms
from home.models import *


#Restuarar Contraseña
class Formulario_Restore(forms.Form):
    password_actual = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña Actual'}))
    password1 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nueva Contraseña'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repetir Contraseña'}))



class DatosForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Nombre"
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Apellido"
    )

    class Meta:
        model = UsersMetadata
        fields = ['correo', 'telefono', 'direccion']  # Los campos de UsersMetadata
        widgets = {
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Recibimos el usuario como parámetro
        super().__init__(*args, **kwargs)
        if user:
            # Prellenar los campos first_name y last_name con los valores actuales
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

    def save(self, user=None, commit=True):
        # Guardar los campos de UsersMetadata
        metadata = super().save(commit=False)
        if user:
            # Guardar los campos del modelo User
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            if commit:
                user.save()
        if commit:
            metadata.save()
        return metadata