from django.contrib import admin

from .models import Rol,Cliente,Empleado,CategoriaProducto,Producto,Inventario

admin.site.register(Rol)
admin.site.register(Cliente)
admin.site.register(Empleado)
admin.site.register(CategoriaProducto)
admin.site.register(Producto)
admin.site.register(Inventario)