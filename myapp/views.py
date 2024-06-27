from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Cliente, Rol, Empleado, Inventario, CategoriaProducto, Producto

from myapp.carrito import Carrito

""" ----------------------------------------Home Principal------------------------------------- """

def home(request):
    return render(request, 'home.html')

""" ----------------------------------------Logica de login------------------------------------- """

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email.endswith('@ferremas.cl'):
            try:
                empleado = Empleado.objects.get(emp_mail=email, emp_password=password)
                # Autenticar al empleado y redireccionar según su rol
                request.session['user_id'] = empleado.emp_id
                rol_description = empleado.rol.rol_description
                if rol_description == 'Vendedor':
                    return redirect('ven_home')
                elif rol_description == 'Bodeguero':
                    return redirect('bod_home')
                elif rol_description == 'Contador':
                    return redirect('con_home')
                elif rol_description == 'Admin':
                    return redirect('adm_home')
                else:
                    return render(request, 'home.html')
            except Empleado.DoesNotExist:
                # Manejar el caso de usuario o contraseña incorrectos para el empleado
                return render(request, 'home.html')
        else:
            try:
                cliente = Cliente.objects.get(cli_mail=email, cli_password=password)
                # Autenticar al cliente y redireccionar según su rol
                request.session['user_id'] = cliente.cli_id
                rol_description = cliente.rol.rol_description
                if rol_description == 'Cliente':
                    return redirect('cli_home')
                else:
                    return render(request, 'home.html')
            except Cliente.DoesNotExist:
                # Manejar el caso de usuario o contraseña incorrectos para el cliente
                return render(request, 'home.html')

    return render(request, 'home.html')

def crear_cuenta(request):
    if request.method == 'POST':
        cli_rut = request.POST.get('cli_rut')
        cli_name = request.POST.get('cli_name')
        cli_lastname = request.POST.get('cli_lastname')
        cli_password = request.POST.get('cli_password')
        cli_mail = request.POST.get('cli_mail')
        cli_fono = request.POST.get('cli_fono')

        # Obtener el rol por defecto, asumiendo que 'cli' es el rol de Cliente
        rol_cliente = Rol.objects.get(rol_id='cli')

        # Crear el objeto Cliente y asignar el rol
        cliente = Cliente(
            cli_rut=cli_rut,
            cli_name=cli_name,
            cli_lastname=cli_lastname,
            cli_password=cli_password,
            cli_mail=cli_mail,
            cli_fono=cli_fono,
            rol=rol_cliente
        )
        cliente.save()

        # Aquí puedes agregar lógica adicional, como iniciar sesión automáticamente

        return redirect('cli_home')

    return render(request, 'crear_cuenta.html')

""" ----------------------------------------Home de Clientes------------------------------------- """

def cli_home(request):
    try:
        cliente = Cliente.objects.get(cli_id=request.session['user_id'])
        print("Cliente ID from session:", request.session.get('user_id'))
        print("Cliente Profile for current user:", cliente)
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente no encontrado'})
    
    productos= Inventario.objects.all()
    categorias = CategoriaProducto.objects.all()

    categoria_filtro = request.GET.get('categoria')

    if categoria_filtro:
        productos = productos.filter(catProd_nom__catProd_nom=categoria_filtro)

    return render(request, 'cliente/cli_home.html', {'cliente': cliente , 'productos': productos, 'categorias': categorias})

def cli_carrito(request):
    try:
        cliente = Cliente.objects.get(cli_id=request.session['user_id'])
        print("Cliente ID from session:", request.session.get('user_id'))
        print("Cliente Profile for current user:", cliente)
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente no encontrado'})
    
    carrito = Carrito(request)
    productos_en_carrito = carrito.carrito.values()
    total_carrito = carrito.total_carrito()

    return render(request, 'cliente/cli_carrito.html', {'cliente': cliente, 'productos': productos_en_carrito, 'totalCarrito': total_carrito})

"""_____________________ Carrito _____________________"""

def agregarProducto(request, prod_id):
    carrito = Carrito(request)
    try:
        producto = Inventario.objects.get(prod_id=prod_id)
        carrito.agregar(producto)
    except Inventario.DoesNotExist:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def restarProducto(request, prod_id):
    carrito = Carrito(request)
    try:
        producto = Inventario.objects.get(prod_id=prod_id)
        carrito.restar(producto)
    except Inventario.DoesNotExist:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def eliminarProducto(request, prod_id):
    carrito = Carrito(request)
    try:
        producto = Inventario.objects.get(prod_id=prod_id)
        carrito.eliminar(producto)
    except Inventario.DoesNotExist:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def limpiarCarrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

""" ----------------------------------------Home de usuarios Empleados------------------------------------- """

""" ----------------------------------------Vendedores------------------------------------- """

def ven_home(request):
    try:
        empleado = Empleado.objects.get(emp_id=request.session['user_id'])
        print("Empleado ID from session:", request.session.get('user_id'))
        print("Empleado Profile for current user:", empleado)
    except Empleado.DoesNotExist:
        return JsonResponse({'error': 'Empleado no encontrado'})
    
    return render(request, 'empleado/vendedor/ven_home.html', {'empleado': empleado})

""" ----------------------------------------Bodegueros------------------------------------- """

def bod_home(request):
    try:
        empleado = Empleado.objects.get(emp_id=request.session['user_id'])
        print("Empleado ID from session:", request.session.get('user_id'))
        print("Empleado Profile for current user:", empleado)
    except Empleado.DoesNotExist:
        return JsonResponse({'error': 'Empleado no encontrado'})
    
    return render(request, 'empleado/bodeguero/bod_home.html', {'empleado': empleado})

""" ----------------------------------------Contadores------------------------------------- """

def con_home(request):
    try:
        empleado = Empleado.objects.get(emp_id=request.session['user_id'])
        print("Empleado ID from session:", request.session.get('user_id'))
        print("Empleado Profile for current user:", empleado)
    except Empleado.DoesNotExist:
        return JsonResponse({'error': 'Empleado no encontrado'})
    
    return render(request, 'empleado/contador/con_home.html', {'empleado': empleado})

""" ----------------------------------------Admins------------------------------------- """

def adm_home(request):
    try:
        empleado = Empleado.objects.get(emp_id=request.session['user_id'])
        print("Empleado ID from session:", request.session.get('user_id'))
        print("Empleado Profile for current user:", empleado)
    except Empleado.DoesNotExist:
        return JsonResponse({'error': 'Empleado no encontrado'})
    
    return render(request, 'empleado/admin/adm_home.html', {'empleado': empleado})

def adm_usuarios(request):
    try:
        empleado = Empleado.objects.get(emp_id=request.session['user_id'])
        print("Empleado ID from session:", request.session.get('user_id'))
        print("Empleado Profile for current user:", empleado)
    except Empleado.DoesNotExist:
        return JsonResponse({'error': 'Empleado no encontrado'})
    
    clientes = Cliente.objects.all()
    empleados = Empleado.objects.all()
    
    return render(request, 'empleado/admin/adm_usuarios.html', {'empleado': empleado, 'clientes': clientes, 'empleados': empleados})

def adm_inventario(request):
    try:
        empleado = Empleado.objects.get(emp_id=request.session['user_id'])
        print("Empleado ID from session:", request.session.get('user_id'))
        print("Empleado Profile for current user:", empleado)
    except Empleado.DoesNotExist:
        return JsonResponse({'error': 'Empleado no encontrado'})
    
    productos = Inventario.objects.all()
    categorias = CategoriaProducto.objects.all()

    categoria_filtro = request.GET.get('categoria')

    if categoria_filtro:
        productos = productos.filter(catProd_nom__catProd_nom=categoria_filtro)

    return render(request, 'empleado/admin/adm_inventario.html', {'empleado': empleado, 'productos': productos, 'categorias': categorias})

def eliminar_producto(request, prod_id):
    producto = get_object_or_404(Inventario, prod_id=prod_id)
    if request.method == 'POST':
        producto.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))

class EditProductoForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['prod_nom', 'prod_marca', 'prod_prec', 'prod_img', 'catProd_nom', 'inv_cantTotal']

def editar_producto(request, prod_id):
    producto = get_object_or_404(Inventario, prod_id=prod_id)

    if request.method == 'POST':
        form = EditProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('adm_inventario')  
    else:
        form = EditProductoForm(instance=producto)

    return render(request, 'empleado/admin/ediciones/editar_producto.html', {'form': form, 'producto': producto})

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['prod_nom', 'prod_marca', 'prod_prec', 'prod_img', 'prod_cant', 'catProd_nom']
        labels = {
            'prod_nom': 'Nombre del Producto',
            'prod_marca': 'Marca',
            'prod_prec': 'Precio',
            'prod_img': 'Imagen',
            'prod_cant': 'Cantidad',
            'catProd_nom': 'Categoría del Producto',
        }
        widgets = {
            'prod_nom': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'prod_marca': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'prod_prec': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'prod_img': forms.FileInput(attrs={'class': 'form-control-file'}),
            'prod_cant': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'catProd_nom': forms.Select(attrs={'class': 'form-control', 'required': True}),
        }

def adm_productos(request):
    categorias = CategoriaProducto.objects.all()
    productos = Producto.objects.all()

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('adm_productos')
    else:
        form = ProductoForm()

    context = {
        'form': form,
        'productos': productos,
        'categorias': categorias,
    }
    return render(request, 'empleado/admin/adm_productos.html', context)