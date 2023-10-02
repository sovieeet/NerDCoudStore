from django.db import models

class Categoria(models.Model):
    id_categoria = models.IntegerField(default=100)
    nombre_categoria = models.CharField(max_length=200)
    
class Inventario(models.Model):
    id_inventario = models.PositiveSmallIntegerField(primary_key=True)
    cantidad_producto = models.PositiveIntegerField()
    fecha = models.CharField(max_length=100)

class Producto(models.Model):
    id_producto = models.PositiveSmallIntegerField(primary_key=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    categoria_id_categoria = models.ForeignKey(Categoria, null=False,  blank=False, on_delete=models.CASCADE)
    inventario_id_inventario = models.ForeignKey(Inventario, null=False,  blank=False, on_delete=models.CASCADE)
    
    def nombreProducto():
        txt = "{0} , {1}"
        return txt.format(self.nombre, self.descripcion)