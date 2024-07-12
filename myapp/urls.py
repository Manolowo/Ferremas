from django.urls import path
from . import views
from myapp.views import agregarProducto,eliminarProducto,restarProducto,limpiarCarrito
from myapp.pdf import generar_factura

urlpatterns = [
    path('', views.home, name="home"),
    path('login_view/', views.login_view, name='login_view'),
    path('crear_cuenta/', views.crear_cuenta, name='crear_cuenta'),
    
    path('cli_home/', views.cli_home, name='cli_home'),
    path('cli_carrito/', views.cli_carrito, name='cli_carrito'),
    path('registrarPedido/', views.registrarPedido, name='registrarPedido'),
    path('cli_pedidos/', views.cli_pedidos, name='cli_pedidos'),
    path('cli_cuenta/<int:cli_id>/', views.cli_cuenta, name='cli_cuenta'),

    path('generar_factura/<int:pedido_id>/', generar_factura, name='generar_factura'),
    path('agregar/<int:prod_id>/', agregarProducto, name="Add"),
    path('restar/<int:prod_id>/', restarProducto, name="Sub"),
    path('eliminar/<int:prod_id>/', eliminarProducto, name="Del"),
    path('limpiar/', limpiarCarrito, name="CLS"),
    path('actualizar_tipo_pedido/', views.actualizarTipoPedido, name='actualizar_tipo_pedido'),
    
    path('ven_home/', views.ven_home, name='ven_home'),
    path('ven_pedidos/', views.ven_pedidos, name='ven_pedidos'),
    path('ven_estado_pedido/<int:ped_id>/', views.ven_estado_pedido, name='ven_estado_pedido'),
    path('ven_inventario/', views.ven_inventario, name='ven_inventario'),
    
    path('bod_home/', views.bod_home, name='bod_home'),
    
    path('con_home/', views.con_home, name='con_home'),
    
    path('adm_home/', views.adm_home, name='adm_home'),
    path('adm_usuarios/', views.adm_usuarios, name='adm_usuarios'),
    path('eliminar_cliente/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('eliminar_empleado/<int:empleado_id>/', views.eliminar_empleado, name='eliminar_empleado'),
    path('editar_cliente/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('editar_empleado/<int:empleado_id>/', views.editar_empleado, name='editar_empleado'),
    path('adm_inventario/', views.adm_inventario, name='adm_inventario'),
    path('eliminar_producto/<int:prod_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('editar_producto/<int:prod_id>/', views.editar_producto, name='editar_producto'),
    path('adm_productos/', views.adm_productos, name='adm_productos'),
    path('adm_pedidos/', views.adm_pedidos, name='adm_pedidos'),
    path('estado_pedido/<int:ped_id>/', views.estado_pedido, name='estado_pedido'),
    
]
