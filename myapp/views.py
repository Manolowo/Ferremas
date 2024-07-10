from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Cliente, Rol, Empleado, Inventario, CategoriaProducto, Producto, Pedido, PedidoItem

from myapp.carrito import Carrito
from .forms import EditProductoForm, ProductoForm, EditClienteForm, EditEmpleadoForm, EmpleadoForm

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

        return redirect('home')

    return render(request, 'crear_cuenta.html')

""" ----------------------------------------Home de Clientes------------------------------------- """

def cli_home(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('home')  
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
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('home')  
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

def registrarPedido(request):
    carrito = Carrito(request)
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('home')
    
    try:
        cliente = Cliente.objects.get(cli_id=user_id)
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente no encontrado'})
    
    total = carrito.total_carrito()
    
    if not carrito.carrito:
        return redirect('cli_carrito')
    
    # Crear el pedido
    pedido = Pedido.objects.create(cliente=cliente, total=total)
    
    # Crear los items del pedido
    for item in carrito.carrito.values():
        producto = Inventario.objects.get(prod_id=item['id_prod'])
        PedidoItem.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=item['cantidad'],
            precio=item['precio']
        )
    
    carrito.limpiar()
    
    return render(request, 'cliente/registrarPedido.html', {'pedido': pedido})

def cli_pedidos(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('home')  
    try:
        cliente = Cliente.objects.get(cli_id=request.session['user_id'])
        print("Cliente ID from session:", request.session.get('user_id'))
        print("Cliente Profile for current user:", cliente)
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente no encontrado'})

    # Obtener todos los pedidos del cliente y sus items asociados
    pedidos = Pedido.objects.filter(cliente=cliente.cli_id)

    return render(request, 'cliente/cli_pedidos.html', {'cliente': cliente, 'pedidos': pedidos})

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
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('home')  
    try:
        empleado = Empleado.objects.get(emp_id=request.session['user_id'])
        print("Empleado ID from session:", request.session.get('user_id'))
        print("Empleado Profile for current user:", empleado)
    except Empleado.DoesNotExist:
        return JsonResponse({'error': 'Empleado no encontrado'})
    
    return render(request, 'empleado/vendedor/ven_home.html', {'empleado': empleado})

""" ----------------------------------------Bodegueros------------------------------------- """

def bod_home(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('home')  
    try:
        empleado = Empleado.objects.get(emp_id=request.session['user_id'])
        print("Empleado ID from session:", request.session.get('user_id'))
        print("Empleado Profile for current user:", empleado)
    except Empleado.DoesNotExist:
        return JsonResponse({'error': 'Empleado no encontrado'})
    
    return render(request, 'empleado/bodeguero/bod_home.html', {'empleado': empleado})

""" ----------------------------------------Contadores------------------------------------- """

def con_home(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('home')  
    try:
        empleado = Empleado.objects.get(emp_id=request.session['user_id'])
        print("Empleado ID from session:", request.session.get('user_id'))
        print("Empleado Profile for current user:", empleado)
    except Empleado.DoesNotExist:
        return JsonResponse({'error': 'Empleado no encontrado'})
    
    return render(request, 'empleado/contador/con_home.html', {'empleado': empleado})

""" ----------------------------------------Admins------------------------------------- """

def adm_home(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('home')  
    try:
        empleado = Empleado.objects.get(emp_id=user_id)
        print("Empleado ID from session:", user_id)
        print("Empleado Profile for current user:", empleado)
    except Empleado.DoesNotExist:
        return JsonResponse({'error': 'Empleado no encontrado'})

    return render(request, 'empleado/admin/adm_home.html', {'empleado': empleado})

def adm_usuarios(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('home')  
    try:
        empleado = Empleado.objects.get(emp_id=request.session['user_id'])
        print("Empleado ID from session:", request.session.get('user_id'))
        print("Empleado Profile for current user:", empleado)
    except Empleado.DoesNotExist:
        return JsonResponse({'error': 'Empleado no encontrado'})
    
    clientes = Cliente.objects.all()
    empleados = Empleado.objects.all()

    if request.method == 'POST':
        form = EmpleadoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado añadido correctamente.')
            return redirect('adm_usuarios')
    else:
        form = EmpleadoForm()

    return render(request, 'empleado/admin/adm_usuarios.html', {'empleado': empleado, 'clientes': clientes, 'empleados': empleados, 'form': form})

def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, cli_id=cliente_id)
    cliente.delete()
    messages.success(request, 'Cliente eliminado correctamente.')
    return redirect('adm_usuarios')

def eliminar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, emp_id=empleado_id)
    empleado.delete()
    messages.success(request, 'Empleado eliminado correctamente.')
    return redirect('adm_usuarios')

def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, cli_id=cliente_id)
    form_class = EditClienteForm
    
    if request.method == 'POST':
        form = form_class(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado correctamente.')
            return redirect('adm_usuarios')
    else:
        form = form_class(instance=cliente)

    context = {
        'form': form,
        'usuario': cliente,
    }
    return render(request, 'empleado/admin/ediciones/editar_usuario.html', context)

def editar_empleado(request, empleado_id): 
    empleado = get_object_or_404(Empleado, emp_id=empleado_id)
    form_class = EditEmpleadoForm
    
    if request.method == 'POST':
        form = form_class(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado actualizado correctamente.')
            return redirect('adm_usuarios')
    else:
        form = form_class(instance=empleado)

    context = {
        'form': form,
        'usuario': empleado,
    }
    return render(request, 'empleado/admin/ediciones/editar_usuario.html', context)

def adm_inventario(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('home')  
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
        messages.success(request, 'Producto eliminado correctamente.')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))

def editar_producto(request, prod_id):    
    producto = get_object_or_404(Inventario, prod_id=prod_id)

    if request.method == 'POST':
        form = EditProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto editado correctamente.')
            return redirect('adm_inventario')  
    else:
        form = EditProductoForm(instance=producto)

    return render(request, 'empleado/admin/ediciones/editar_producto.html', {'form': form, 'producto': producto})

def adm_productos(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('home')  
    try:
        empleado = Empleado.objects.get(emp_id=request.session['user_id'])
        print("Empleado ID from session:", request.session.get('user_id'))
        print("Empleado Profile for current user:", empleado)
    except Empleado.DoesNotExist:
        return JsonResponse({'error': 'Empleado no encontrado'})
    
    categorias = CategoriaProducto.objects.all()
    productos = Producto.objects.all()

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto añadido correctamente.')
            return redirect('adm_productos')
    else:
        form = ProductoForm()

    context = {
        'form': form,
        'productos': productos,
        'categorias': categorias,
        'empleado': empleado,
    }
    return render(request, 'empleado/admin/adm_productos.html', context)

def adm_pedidos(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('home')  
    
    try:
        empleado = Empleado.objects.get(emp_id=user_id)
        print("Empleado ID from session:", user_id)
        print("Empleado Profile for current user:", empleado)
    except Empleado.DoesNotExist:
        return JsonResponse({'error': 'Empleado no encontrado'})

    # Obtener todos los pedidos y sus items asociados
    pedidos = Pedido.objects.all()

    return render(request, 'empleado/admin/adm_pedidos.html', {'empleado': empleado, 'pedidos': pedidos})