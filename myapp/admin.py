from django.contrib import admin

from .models import Rol,Cliente,Empleado,CategoriaProducto,Producto,Inventario,Pedido,PedidoItem,Factura,FacturaItem

admin.site.register(Rol)
admin.site.register(Cliente)
admin.site.register(Empleado)
admin.site.register(CategoriaProducto)
admin.site.register(Producto)
admin.site.register(Inventario)
admin.site.register(Pedido)
admin.site.register(PedidoItem)
admin.site.register(Factura)
admin.site.register(FacturaItem)