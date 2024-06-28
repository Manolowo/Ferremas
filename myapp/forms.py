from django import forms
from .models import Cliente, Empleado, Inventario, Producto

class EditProductoForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['prod_nom', 'prod_marca', 'prod_prec', 'prod_img', 'catProd_nom', 'inv_cantTotal']
        
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

class EditClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cli_rut', 'cli_name', 'cli_lastname', 'cli_password', 'cli_mail', 'cli_fono', 'rol']
        labels = {
            'cli_rut': 'RUT',
            'cli_name': 'Nombre',
            'cli_lastname': 'Apellido',
            'cli_password': 'Contraseña',
            'cli_mail': 'Correo',
            'cli_fono': 'Teléfono',
            'rol': 'Rol',
        }
        widgets = {
            'cli_rut': forms.TextInput(attrs={'class': 'form-control'}),
            'cli_name': forms.TextInput(attrs={'class': 'form-control'}),
            'cli_lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'cli_password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'cli_mail': forms.EmailInput(attrs={'class': 'form-control'}),
            'cli_fono': forms.NumberInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
        }

class EditEmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['emp_rut', 'emp_name', 'emp_lastname', 'emp_password', 'emp_mail', 'emp_fono', 'rol']
        labels = {
            'emp_rut': 'RUT',
            'emp_name': 'Nombre',
            'emp_lastname': 'Apellido',
            'emp_password': 'Contraseña',
            'emp_mail': 'Correo',
            'emp_fono': 'Teléfono',
            'rol': 'Rol',
        }
        widgets = {
            'emp_rut': forms.TextInput(attrs={'class': 'form-control'}),
            'emp_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emp_lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'emp_password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'emp_mail': forms.EmailInput(attrs={'class': 'form-control'}),
            'emp_fono': forms.NumberInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
        }

