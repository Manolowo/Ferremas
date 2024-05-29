from django.urls import path
from . import views
from myapp.views import agregarProducto,eliminarProducto,restarProducto,limpiarCarrito

urlpatterns = [
    path('', views.home, name="home"),
    path('login_view/', views.login_view, name='login_view'),
    path('crear_cuenta/', views.crear_cuenta, name='crear_cuenta'),
    
    path('cli_home/', views.cli_home, name='cli_home'),
    path('cli_carrito/', views.cli_carrito, name='cli_carrito'),
    
    path('agregar/<int:prod_id>/', agregarProducto, name="Add"),
    path('restar/<int:prod_id>/', restarProducto, name="Sub"),
    path('eliminar/<int:prod_id>/', eliminarProducto, name="Del"),
    path('limpiar/', limpiarCarrito, name="CLS"),
        
    path('ven_home/', views.ven_home, name='ven_home'),
    
    path('bod_home/', views.bod_home, name='bod_home'),
    
    path('con_home/', views.con_home, name='con_home'),
    
    path('adm_home/', views.adm_home, name='adm_home'),
]
