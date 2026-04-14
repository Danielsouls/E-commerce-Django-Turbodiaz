from django.urls import path
from .views import *

urlpatterns = [
    path('mis-productos/', mis_productos, name="mis_productos"),
    path('cambiar_password/', cambiar_password, name='cambiar_password'),
    path('mis-datos/', ver_y_editar_datos, name='datos'),
]
