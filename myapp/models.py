from django.db import models

from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.
""" ----------------------------------------Roles y usuarios------------------------------------- """

class Rol(models.Model):
    rol_id = models.CharField(max_length=3, primary_key=True)
    rol_description = models.CharField(max_length=12)
    
    def __str__(self):
        return self.rol_description
    
class Cliente(models.Model):
    cli_id = models.AutoField(primary_key=True)
    cli_name = models.CharField(max_length=15, null=False)
    cli_lastname = models.CharField(max_length=20, null=False)
    cli_password = models.CharField(max_length=20, null=False, default="admin")
    cli_mail = models.EmailField(null=False)
    cli_fono = models.IntegerField(null=False)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    def __str__(self):
        return self.rol.rol_id + ' - ' + self.cli_name +' '+ self.cli_lastname  

class Empleado(models.Model):
    emp_id = models.AutoField(primary_key=True)
    emp_name = models.CharField(max_length=15, null=False)
    emp_lastname = models.CharField(max_length=20, null=False)
    emp_password = models.CharField(max_length=20, null=False, default="admin")
    emp_mail = models.EmailField(null=False)
    emp_fono = models.IntegerField(null=False)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    def __str__(self):
        return self.emp_name +' '+ self.emp_lastname +' - '+ self.rol.rol_id 

""" ----------------------------------------Producto e inventario------------------------------------- """

class CategoriaProducto(models.Model):
    catProd_nom = models.CharField(max_length=100)

    def __str__(self):
        return self.catProd_nom

class Producto(models.Model):
    prod_id = models.AutoField(primary_key=True)
    prod_nom = models.CharField(max_length=50, null=False)
    prod_marca = models.CharField(max_length=25, default='Generica')
    prod_prec= models.IntegerField(default=1, null=False)
    prod_cant= models.IntegerField(default= 1, null=False)
    catProd_nom = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.prod_nom

class Inventario(models.Model):
    prod_nom = models.CharField(max_length=50)
    prod_marca = models.CharField(max_length=25)
    prod_prec= models.IntegerField()
    catProd_nom = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE)
    
    inv_cantTotal = models.IntegerField(default=0)
    
    def __str__(self):
        return self.prod_nom + '-' + self.prod_marca

""" ---------------------------------------Gestion de inventario--------------------------------------------"""

@receiver(post_save, sender=Producto)
def actualizar_inventario(sender, instance, created, **kwargs):
    if created:
        inventario, _ = Inventario.objects.get_or_create(
            prod_nom=instance.prod_nom,
            prod_marca=instance.prod_marca,
            prod_prec=instance.prod_prec,
            catProd_nom=instance.catProd_nom
        )
        inventario.inv_cantTotal += int(instance.prod_cant)
        inventario.save()
        
    else:
        inventario = Inventario.objects.get(
            prod_nom=instance.prod_nom,
            prod_marca=instance.prod_marca,
            prod_prec=instance.prod_prec,
            catProd_nom=instance.catProd_nom
        )
        inventario.inv_cantTotal += int(instance.prod_cant)
        inventario.save()
        
@receiver(post_delete, sender=Producto)
def eliminar_de_inventario(sender, instance, **kwargs):
    try:
        inventario = Inventario.objects.get(
            prod_nom=instance.prod_nom,
            prod_marca=instance.prod_marca,
            prod_prec=instance.prod_prec,
            catProd_nom=instance.catProd_nom
        )
        inventario.inv_cantTotal -= int(instance.prod_cant)
        if inventario.inv_cantTotal <= 0:
            inventario.delete()
        else:
            inventario.save()
    except Inventario.DoesNotExist:
        pass
    
@receiver(post_delete, sender=Inventario)
def eliminar_producto(sender, instance, **kwargs):
    try:
        producto = Producto.objects.filter(
            prod_nom=instance.prod_nom,
            prod_marca=instance.prod_marca,
            prod_prec=instance.prod_prec,
            catProd_nom=instance.catProd_nom
        )
        producto.delete()
    except Producto.DoesNotExist:
        pass