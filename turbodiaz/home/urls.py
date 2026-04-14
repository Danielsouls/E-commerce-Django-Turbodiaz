from django.urls import  path
from .views import *

urlpatterns = [
    #menu**********************
    path('', menu, name="menu"),
    path('dondeestamos', dondeestamos, name="dondeestamos"),
    path('servicios', servicios, name="servicios"),
    path('nosotros', nosotros, name="nosotros"),
    path('terminos', terminos, name="terminos"),
    path('Garantia',Garantia,name="Garantia"),
    path('Pago_Seguro',Pago_Seguro,name="Pago_Seguro"),

    #COHERE
    path('api/chatbot/', chatbot_response, name='chatbot_response'),
   
    #centro de ayuda
    path('centro-de-ayudas/', centro_de_ayudas, name='centro_de_ayudas'),
    
    #***************************
    path('home_inicio', home_inicio, name="home_inicio"),
    
]