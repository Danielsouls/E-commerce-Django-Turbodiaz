from django import forms

#centro de ayuda
class CentroDeAyudasForm(forms.Form):
    nombre = forms.CharField(
        max_length=100, 
        label="Nombre", 
        widget=forms.TextInput(attrs={
            'placeholder': 'Tu nombre',
            'class': 'form-control'
        })
    )
    apellido = forms.CharField(
        max_length=100, 
        label="Apellido", 
        widget=forms.TextInput(attrs={
            'placeholder': 'Tu apellido',
            'class': 'form-control'
        })
    )
    telefono = forms.CharField(
        max_length=15, 
        label="Teléfono", 
        widget=forms.TextInput(attrs={
            'placeholder': 'Teléfono de contacto',
            'class': 'form-control'
        })
    )
    email = forms.EmailField(
        label="Correo Electrónico", 
        widget=forms.EmailInput(attrs={
            'placeholder': 'Tu correo electrónico',
            'class': 'form-control'
        })
    )
    patente = forms.CharField(
        max_length=10, 
        label="Patente del auto (Opcional)", 
        required=False, 
        widget=forms.TextInput(attrs={
            'placeholder': 'Patente del vehículo',
            'class': 'form-control'
        })
    )
    marca_turbo = forms.CharField(
        max_length=100, 
        label="Marca del turbo (Opcional)", 
        required=False, 
        widget=forms.TextInput(attrs={
            'placeholder': 'Marca del turbo',
            'class': 'form-control'
        })
    )
    mensaje = forms.CharField(
        label="Mensaje", 
        widget=forms.Textarea(attrs={
            'placeholder': 'Escribe tu mensaje aquí...',
            'class': 'form-control',
            'rows': 5
        })
    )
