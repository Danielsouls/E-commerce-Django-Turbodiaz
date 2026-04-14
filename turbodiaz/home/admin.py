from django.contrib import admin
from django.contrib.admin import AdminSite
from home.models import *
from utilidades import formularios

# Register your models here.
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('id', 'nombre')


class GeneroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('id', 'nombre')


class PaisAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('id', 'nombre')


class PerfilesAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('id', 'nombre')


class UsersMetadataAdmin(admin.ModelAdmin):
    list_display = ('id', 'correo', 'telefono', 'direccion', formularios.set_estado, formularios.set_genero, formularios.set_pais, formularios.set_perfiles, formularios.set_user, formularios.set_correo)
    search_fields = ('id', 'pasaporte', 'correo', 'telefono', 'direccion', 'avatar', 'fecha_nacimiento')
    list_per_page = 20


class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('id', 'nombre')


class ProductoCategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('id', 'nombre', 'slug')


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', formularios.set_producto_categoria, formularios.set_estado, 'nombre', formularios.get_descripcion, formularios.get_foto_producto, 'stock', 'precio')
    search_fields = ('id', 'nombre, descripcion')
    list_per_page = 20


class ProductoFotosAdmin(admin.ModelAdmin):
    list_display = ('id', formularios.set_producto, formularios.get_foto_producto_galeria)
    list_per_page = 20


class CarritoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cantidad', formularios.set_users_metadata, formularios.set_producto, 'fecha')


class MetadataAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'keyword', 'description', 'correo', 'telefono')
    search_fields = ('id', 'nombre')


class OrdenDeCompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'users_metadata', 'estado', 'comuna', 'fecha', 'suma', 'direccion')
    search_fields = ('id', 'users_metadata__correo', 'direccion', 'token_ws')
    list_filter = ('estado', 'fecha')


class OrdenDeCompraDetalleAdmin(admin.ModelAdmin):
    list_display = ('id', 'orden_de_compra', 'producto', 'cantidad')
    search_fields = ('id', 'orden_de_compra__id', 'producto__nombre')
    list_filter = ('producto',)


admin.site.register(Estado, EstadoAdmin)
admin.site.register(Genero, GeneroAdmin)
admin.site.register(Pais, PaisAdmin)
admin.site.register(Perfiles, PerfilesAdmin)
admin.site.register(UsersMetadata, UsersMetadataAdmin)
admin.site.register(ProductoCategoria, ProductoCategoriaAdmin)
admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Carrito, CarritoAdmin)
admin.site.register(Metadata, MetadataAdmin)
admin.site.register(ProductoFotos, ProductoFotosAdmin)
admin.site.register(OrdenDeCompra, OrdenDeCompraAdmin)
admin.site.register(OrdenDeCompraDetalle, OrdenDeCompraDetalleAdmin)

admin.site.site_header = 'Administración Tienda'
admin.site.index_title = 'Administración Tienda'
admin.site.site_title = 'Administración Tienda'
