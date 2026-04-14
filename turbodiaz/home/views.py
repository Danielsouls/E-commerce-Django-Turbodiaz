from django.shortcuts import render
from home.models import *
#Centro de ayuda
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from .forms import CentroDeAyudasForm

# Create your views here.

def home_inicio(request):
	#select * from productos where estado_id=1 order by id desc limit 8
	datos=Producto.objects.filter(estado_id=1).order_by('-id').all()[:8]
	return render(request, 'home/home.html', {'datos':datos})

# menu principal.
def menu(request):
    return render(request,'home/menu.html')

# donde estamos principal.
def dondeestamos(request):
    return render(request,'home/dondeestamos.html')

# servicios principal.
def servicios(request):
    return render(request,'home/servicios.html')

#nosotros
def nosotros(request):
     return render(request, 'home/nosotros.html')
#nosotros
def terminos(request):
     return render(request, 'home/Terminos_y_condiciones.html')

#Centro de ayuda
def centro_de_ayudas(request):
    if request.method == 'POST':
        form = CentroDeAyudasForm(request.POST)
        if form.is_valid():
            # Obtener los datos del formulario
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            telefono = form.cleaned_data['telefono']
            email = form.cleaned_data['email']
            patente = form.cleaned_data.get('patente', 'No proporcionado')
            marca_turbo = form.cleaned_data.get('marca_turbo', 'No proporcionado')
            mensaje = form.cleaned_data['mensaje']
            
            # Crear el mensaje de correo
            mensaje_correo = (
                f"Nombre: {nombre} {apellido}\n"
                f"Teléfono: {telefono}\n"
                f"Correo Electrónico: {email}\n"
                f"Patente: {patente}\n"
                f"Marca del Turbo: {marca_turbo}\n\n"
                f"Mensaje:\n{mensaje}"
            )
            
            # Enviar el correo
            send_mail(
                subject='Consulta desde Centro de Ayudas',
                message=mensaje_correo,
                from_email='turbodiaz.cl@gmail.com',
                recipient_list=['turbodiaz.cl@gmail.com'],
                fail_silently=False,
            )
            return HttpResponseRedirect('/gracias/')

    else:
        form = CentroDeAyudasForm()
    
    return render(request, 'home/centro_de_ayudas.html', {'form': form})

def Garantia(request):
    return render(request,'home/Garantia.html')

def Pago_Seguro(request):
    return render(request,'home/Pago_Seguro.html')

#COHERE
import cohere
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Configura tu clave de Cohere
cohere_api_key = '0wXZ7MUWPVoA8OID44YMrPgIKxZa0e4Q7BuH5LBM'
co = cohere.Client(cohere_api_key)

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            if not user_message.strip():
                return JsonResponse({"response": "Por favor, escribe algo para que pueda responder."})

            # Llama a Cohere
            response = co.generate(
                model='command-xlarge-nightly',
                prompt=f"Pregunta sobre turbos: {user_message}",
                max_tokens=150,
                temperature=0.7,
            )

            bot_message = response.generations[0].text.strip()
            return JsonResponse({"response": bot_message})

        except Exception as e:
            print(f"Error al procesar la solicitud: {str(e)}")
            return JsonResponse({"response": "Hubo un error al procesar tu solicitud. Por favor, inténtalo más tarde."}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)