from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from home.models import *
from acceso.decorators import logueado
from utilidades import utilidades, webpay
import json
from django.conf import settings
from django.utils.timezone import localtime


@logueado()
def carro_inicio(request):
    cuantos=Carrito.objects.filter(users_metadata_id=request.session['users_metadata_id']).count()
    datos=Carrito.objects.filter(users_metadata_id=request.session['users_metadata_id']).order_by('-id').all()
    suma=0
    for dato in datos:
        valor=dato.cantidad*dato.producto.precio
        suma=suma+valor
    return render(request, 'carro/home.html', {'datos': datos, 'suma': suma, 'cuantos': cuantos})


@logueado()
def carro_crear(request):
    if request.method =='POST':
        try:
            datos=Producto.objects.filter(pk=request.POST['id']).get()
        except Producto.DoesNotExist:
            raise Http404
        Carrito.objects.create(cantidad=request.POST['cantidad'], producto_id=request.POST['id'], users_metadata_id=request.session['users_metadata_id'])
        return HttpResponseRedirect("/carro")
    else:
        raise Http404


@logueado()
def carro_vaciar(request):
    Carrito.objects.filter(users_metadata_id=request.session['users_metadata_id']).delete()
    OrdenDeCompra.objects.filter(users_metadata_id=request.session['users_metadata_id']).filter(estado_id=3).delete()
    
    messages.add_message(request, messages.SUCCESS, f'Se vació tu carrito exitosamente!!!.')
    return HttpResponseRedirect('/carro')


@logueado()
def carro_quitar(request, id):
    try:
        datos=Producto.objects.filter(pk=id).get()
    except Producto.DoesNotExist:
        raise Http404
    Carrito.objects.filter(users_metadata_id=request.session['users_metadata_id']).filter(producto_id=id).delete()
    messages.add_message(request, messages.SUCCESS, f'Se quitó el producto del carrito exitosamente!!!.')
    return HttpResponseRedirect('/carro')


@logueado()
def carro_modificar_cantidad(request, id, cantidad):
    try:
        datos=Carrito.objects.filter(pk=id).get()
    except Carrito.DoesNotExist:
        raise Http404
    Carrito.objects.filter(id=id).update(cantidad=cantidad)
    messages.add_message(request, messages.SUCCESS, f'Se modificó la cantidad del producto {datos.producto.nombre} exitosamente!!!.')
    return HttpResponseRedirect('/carro')


@logueado()
def carro_pagar(request):
    cuantos=Carrito.objects.filter(users_metadata_id=request.session['users_metadata_id']).count()
    if cuantos==0:
        return HttpResponseRedirect('/carro')
    datos=Carrito.objects.filter(users_metadata_id=request.session['users_metadata_id']).order_by('-id').all()
    
    suma=0
    for dato in datos:
        valor=dato.cantidad*dato.producto.precio
        suma=suma+valor
    usuario=UsersMetadata.objects.filter(id=request.session['users_metadata_id']).get()
    comunas=Comuna.objects.all()
    return render(request, 'carro/pagar.html', {'datos': datos, 'suma': suma, 'usuario': usuario, 'comunas': comunas, 'cuantos': cuantos})

#paso 3 opcional
@logueado()
def carro_webpay(request):
    if request.method =='POST':
        cuantos=Carrito.objects.filter(users_metadata_id=request.session['users_metadata_id']).count()
        if cuantos==0:
            return HttpResponseRedirect('/carro')
        direccion=f"{request.POST['direccion']} {request.POST['indicaciones']}"
        envio_a_regiones = request.POST.get('envio_a_regiones', '')
        rut = request.POST.get('rut', '')
        result=webpay.crearTransaccion(request.session['users_metadata_id'], direccion, request.POST['comuna'])

        OrdenDeCompra.objects.filter(users_metadata_id=request.session['users_metadata_id'], estado_id=3).update(
            envio_a_regiones=envio_a_regiones, rut=rut
        )
        return render(request, 'carro/webpay.html', {'url': result['url'], 'token': result['token']})


@logueado()
def carro_webpay_respuesta(request):
    # Verificar que el token_ws esté presente
    token = request.GET.get('token_ws')
    if not token:
        raise Http404

    # Verificar la transacción con Transbank
    result = webpay.verificarTransaccion(token)
    if result[0] == 'vacio':
        raise Http404

    # Manejar transacciones autorizadas
    if result[0] == 'AUTHORIZED':
        try:
            # Buscar la orden de compra asociada al usuario
            orden = OrdenDeCompra.objects.filter(
                users_metadata_id=request.session['users_metadata_id'],
                estado_id=3
            ).get()
        except OrdenDeCompra.DoesNotExist:
            raise Http404

        # Actualizar información de la orden en la base de datos
        OrdenDeCompra.objects.filter(
            users_metadata_id=request.session['users_metadata_id'],
            estado_transbank=0
        ).update(
            token_ws=token,
            estado_transbank=result[0],
            fecha_transbank=result[2],
            tarjeta=result[1],
            estado_id=6
        )

        #hora y fecha local
        fecha_emision_local = localtime(orden.fecha_emision)

        # Generar detalles de la compra
        suma = 0
        datos = Carrito.objects.filter(users_metadata_id=request.session['users_metadata_id']).all()
        detalle = ""

        for dato in datos:
            valor = dato.cantidad * dato.producto.precio
            suma += valor
            detalle += f"""
            <tr>
                <td style="border: 1px solid black;">
                    <p>transbank</p>
                </td>
                <td style="border: 1px solid black;"><p>Emitido el: {fecha_emision_local.strftime('%d/%m/%Y %H:%M:%S')}</p></td>
                <td style="border: 1px solid black;">{dato.producto.nombre}</td>
                <td style="border: 1px solid black;">{dato.cantidad}</td>
                <td style="border: 1px solid black;">${utilidades.numberFormat(dato.producto.precio)}</td>
            </tr>
            """
            # Crear detalles en la base de datos
            OrdenDeCompraDetalle.objects.create(
                orden_de_compra_id=orden.id,
                producto_id=dato.producto_id,
                cantidad=dato.cantidad
            )

        # Limpiar el carrito después de la compra
        Carrito.objects.filter(users_metadata_id=request.session['users_metadata_id']).delete()

        # Obtener datos del usuario
        usuario = UsersMetadata.objects.filter(id=request.session['users_metadata_id']).get()

        # Obtenemos los datos de envío y rut de la orden
        envio_a_regiones = orden.envio_a_regiones or "No envio"
        rut = orden.rut or "Sin espeficicar"

        # Construir el correo de confirmación
        html = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8" />
                <title>Confirmación de Pedido</title>
            </head>
            <body>
                <div class="container">
                    <div class="row">
                        <h1 style="color: red;">TURBO DIAZ</h1>
                        <h1>Hola {usuario}, tu pedido ha sido ingresado al sistema con el N°{orden.id}</h1>
                        <table style="border-collapse: collapse;">
                            <thead>
                                <tr>
                                    <th>Pago</th>
                                    <th>Fecha de emision</th>
                                    <th>Producto</th>
                                    <th>Cantidad</th>
                                    <th>Precio</th>
                                </tr>
                            </thead>
                            <tbody>
                                {detalle}
                                <tr>
                                    <td colspan="5" style="border: 1px solid black;">Total de tu compra</td>
                                </tr>
                                <tr>
                                    <td colspan="5" style="border: 1px solid black;">${utilidades.numberFormat(suma)}</td>

                                </tr>

                                <tr>
                                    <td colspan="5" style="border: 1px solid black;">COMUNA: {orden.comuna.nombre}</td>
                                </tr>
                                <tr>
                                    <td colspan="5" style="border: 1px solid black;">DIRECCIÓN: {orden.direccion}</td>
                                </tr>

                                <tr>
                                    <td colspan="5" style="border: 1px solid black;"><strong>Envío por:</strong>{envio_a_regiones}<br>***RECUERDE QUE TURBODIAZ NO SE HACE RESPONSABLE POR DAÑOS, PÉRDIDAS O DEMORAS UNA VEZ<br>QUE EL PRODUCTO HA SIDO ENTREGADO A LA EMPRESA DE TRANSPORTE***</td>
                                </tr>
                                <tr>
                                    <td colspan="5" style="border: 1px solid black;">{rut}</td>
                                </tr>
                                <tr>
                                    <td colspan="5" style="border: 1px solid black;">NÚMERO DE TRANSACCIÓN DE TRANSBANK: {token}</td>
                                </tr>
                                <tr>
                                    <td colspan="5" style="border: 1px solid black;">LOCAL:Turbo Diaz. Carr. Panamericana Sur, Km 681.5, Araucania, Chile</td>
                                </tr>
                                <tr>
                                    <td colspan="5" style="border: 1px solid black;">TELEFONO DEL LOCAL: +569 99463203</td>
                                </tr>
                                <tr>
                                    <td colspan="5" style="border: 1px solid black;">NUESTRO SITIO WEB: www.turbodiaz.cl </td>
                                </tr>
                                <tr>
                                    <td colspan="5" style="border: 1px solid black;">10 días hábiles pueden tardar los envios a regiones <br> 3 dias hábiles pueden tardar los envios en la zona regional</td>
                                </tr>
                                <tr>
                                    <td colspan="5" style="border: 1px solid black;">COPIA CLIENTE</td>
                                </tr>
                                <tr>
                                    <td colspan="5" style="border: 1px solid black;">*********************************************************GRACIAS POR SU COMPRA*********************************************************</td>
                                </tr>
                                
                            </tbody>
                        </table>
                    </div>
                </div>
            </body>
        </html>
        """

        # Enviar correos
        utilidades.sendMail(html, 'Tienda', usuario.correo)
        utilidades.sendMail(html, 'Tienda', 'info@tamila.cl')

        # Mostrar mensaje de éxito
        messages.add_message(
            request,
            messages.SUCCESS,
            f'La orden de compra N° {orden.id} ha sido generada exitosamente. '
            f'Tu número de transacción de Transbank es {token}. '
            'Nos pondremos en contacto contigo a la brevedad para coordinar el envío de los productos. ¡Gracias por tu compra!'
        )
        return HttpResponseRedirect('/carro')

    # Manejar transacciones fallidas
    if result[0] == 'FAILED':
        OrdenDeCompra.objects.filter(
            users_metadata_id=request.session['users_metadata_id'],
            estado_transbank=0
        ).update(
            token_ws=token,
            fecha_transbank=result[2],
            tarjeta=result[1],
            estado_id=5
        )
        messages.add_message(
            request,
            messages.WARNING,
            'No fue posible procesar el pago, por favor vuelva a intentarlo.'
        )
        return HttpResponseRedirect('/carro')