from django.shortcuts import render
from home.models import *
from django.contrib.auth.decorators import login_required
from datos.forms import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password


@login_required
def mis_productos(request):
    user_metadata = UsersMetadata.objects.get(user=request.user)

    # Filtrar órdenes relacionadas con el usuario
    ordenes = OrdenDeCompra.objects.filter(users_metadata=user_metadata).order_by('-fecha_emision')

    # Crear una lista para los productos pedidos con los datos necesarios
    productos_pedidos = []
    for orden in ordenes:
        detalles = OrdenDeCompraDetalle.objects.filter(orden_de_compra=orden)
        for detalle in detalles:
            productos_pedidos.append({
                'orden_id': orden.id,
                'producto': detalle.producto.nombre,
                'cantidad': detalle.cantidad,
                'fecha_emision': orden.fecha_emision,
                'comuna': orden.comuna.nombre,
                'direccion': f"{orden.direccion} {orden.observaciones}",
                'token_ws': orden.token_ws,
                'envio_a_regiones': orden.envio_a_regiones or "No envío",
                'rut': orden.rut or "Sin especificar",
                'total': detalle.cantidad * detalle.producto.precio  # Total = Cantidad * Precio Unitario
            })


    return render(request, 'datos/mis_productos.html', {'productos_pedidos': productos_pedidos})


@login_required
def cambiar_password(request):
    if request.method == 'POST':
        form = Formulario_Restore(request.POST)
        if form.is_valid():
            password_actual = form.cleaned_data['password_actual']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            # Verificar si la contraseña actual es correcta
            if not check_password(password_actual, request.user.password):
                mensaje = "La contraseña actual es incorrecta."
                messages.add_message(request, messages.WARNING, mensaje)
            elif password1 != password2:
                mensaje = "Las contraseñas ingresadas no coinciden."
                messages.add_message(request, messages.WARNING, mensaje)
            else:
                # Actualizar la contraseña del usuario
                user = request.user
                user.password = make_password(password1)
                user.save()

                mensaje = "Tu contraseña ha sido actualizada exitosamente."
                messages.add_message(request, messages.SUCCESS, mensaje)
                return redirect('acceso_login')  # Redirige al login o página principal
    else:
        form = Formulario_Restore()

    return render(request, 'datos/restore.html', {'form': form})

#ver datos
# views.py


@login_required
def ver_y_editar_datos(request):
    # Obtener los datos del usuario logueado y su metadata
    user = request.user
    user_metadata = UsersMetadata.objects.get(user=user)
    
    if request.method == 'POST':
        # Si el formulario es enviado, actualizamos los datos
        form = DatosForm(request.POST, instance=user_metadata, user=user)
        if form.is_valid():
            form.save(user=user)
            return redirect('datos')  # Redirigir a la vista de datos después de actualizar
    else:
        # Si es un GET, mostramos el formulario con los datos actuales
        form = DatosForm(instance=user_metadata, user=user)
    
    return render(request, 'datos/editar_datos.html', {'form': form, 'user_metadata': user_metadata})
