from django.utils import timezone
from django.db import models

from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os


# Create your models here.
""" ----------------------------------------Roles y usuarios------------------------------------- """

class Rol(models.Model):
    rol_id = models.CharField(max_length=3, primary_key=True)
    rol_description = models.CharField(max_length=12)
    
    def __str__(self):
        return self.rol_description
    
class Cliente(models.Model):
    cli_id = models.AutoField(primary_key=True)
    cli_rut= models.CharField(max_length=12, null=False, unique=True)
    cli_name = models.CharField(max_length=15, null=False)
    cli_lastname = models.CharField(max_length=20, null=False)
    cli_password = models.CharField(max_length=20, null=False)
    cli_mail = models.EmailField(null=False)
    cli_fono = models.IntegerField(null=False)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    def __str__(self):
        return self.rol.rol_id + ' - ' + self.cli_name +' '+ self.cli_lastname  

class Empleado(models.Model):
    emp_id = models.AutoField(primary_key=True)
    emp_rut= models.CharField(max_length=12, null=False, unique=True)
    emp_name = models.CharField(max_length=15, null=False)
    emp_lastname = models.CharField(max_length=20, null=False)
    emp_password = models.CharField(max_length=20, null=False)
    emp_mail = models.EmailField(null=False)
    emp_fono = models.IntegerField(null=False)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    def __str__(self):
        return self.rol.rol_id +' - '+ self.emp_name +' '+ self.emp_lastname 

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
    prod_img = models.ImageField(upload_to='productos/', null=True, blank=True)
    prod_cant= models.IntegerField(default= 1, null=False)
    catProd_nom = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE)
    prod_ingreso = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.prod_nom
    
def path_and_rename(instance, filename):
    upload_to = 'productos/'
    ext = filename.split('.')[-1]
    filename = f'{instance.prod_id}.{ext}'
    return os.path.join(upload_to, filename)

class Inventario(models.Model):
    prod_id = models.AutoField(primary_key=True)
    prod_nom = models.CharField(max_length=50)
    prod_marca = models.CharField(max_length=25)
    prod_prec= models.IntegerField()
    prod_img = models.ImageField(upload_to=path_and_rename, null=True, blank=True)
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
        if instance.prod_img:
            inventario.prod_img = instance.prod_img
    else:
        try:
            inventario = Inventario.objects.get(
                prod_nom=instance.prod_nom,
                prod_marca=instance.prod_marca,
                prod_prec=instance.prod_prec,
                catProd_nom=instance.catProd_nom
            )
            if not instance.prod_img:
                instance.prod_img = inventario.prod_img
        except Inventario.DoesNotExist:
            pass

    inventario.inv_cantTotal += instance.prod_cant
    inventario.save()
    
