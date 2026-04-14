import re
from django.db import models
from django import forms
from django.forms import ModelForm, PasswordInput



class Formulario_Login(forms.Form):
    correo = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E-Mail', 'autocomplete':'off'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña', 'autocomplete':'off'}))


class Formulario_Registro(forms.Form):
    nombre = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre', 'autocomplete':'off'}))
    apellido = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido', 'autocomplete':'off'}))
    telefono = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono', 'autocomplete':'off'}))
    correo = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E-Mail', 'autocomplete':'off'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña', 'autocomplete':'off'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repetir Contraseña', 'autocomplete':'off'}))
    
        #condición para el telefono
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit():
            raise forms.ValidationError("El campo Teléfono solo debe contener números.")
        return telefono

    def clean_password(self):
        password = self.cleaned_data.get('password')
        # Regex para validar la contraseña
        regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$#*])[A-Za-z\d@$#*]{8,16}$'
        if not re.match(regex, password):
            raise forms.ValidationError(
                "La contraseña debe contener entre 8 y 16 caracteres, al menos 1 letra mayúscula, una minúscula, un carácter especial (@$#*) y al menos 1 número."
            )
        return password


class Formulario_Reset(forms.Form):
    correo = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E-Mail', 'autocomplete':'off'}))


class Formulario_Restore(forms.Form):
    password1 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repetir Contraseña'}))



