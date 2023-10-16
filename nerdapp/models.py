from django.db import models

class Categoria(models.Model):
    id_categoria = models.IntegerField(primary_key=True, default=100)
    nombre_categoria = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre_categoria
    
class Inventario(models.Model):
    id_inventario = models.IntegerField(primary_key=True, default=100)
    cantidad_producto = models.PositiveIntegerField()
    fecha = models.CharField(max_length=100)

    def __str__(self):
        return f"Inventario {self.id_inventario}: Fecha - {self.fecha}, Cantidad - {self.cantidad_producto}"

class Producto(models.Model):
    id_producto = models.IntegerField(primary_key=True, default=100)
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    categoria_id_categoria = models.ForeignKey(Categoria, null=False,  blank=False, on_delete=models.CASCADE)
    inventario_id_inventario = models.ForeignKey(Inventario, null=False,  blank=False, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre
     
class Region(models.Model):
    id_region = models.IntegerField(primary_key=True, default=100)
    region = models.CharField(max_length=200)

    def __str__(self):
        return self.region
class Comuna(models.Model):
    id_comuna = models.IntegerField(primary_key=True, default=100)
    comuna = models.CharField(max_length=200)
    region_id_region = models.ForeignKey(Region, null=False,  blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.comuna
    
class Rol(models.Model):
    id_rol = models.IntegerField(primary_key=True, default=100)
    nombre_rol = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre_rol
    
class Usuario(models.Model):
    id_usuario = models.IntegerField(primary_key=True, default=100)
    rut = models.IntegerField(max_length=200)
    nombre = models.CharField(max_length=200)
    apellido_paterno = models.CharField(max_length=200)
    apellido_materno = models.CharField(max_length=200)
    telefono = models.IntegerField(max_length=200)
    correo = models.EmailField()
    direccion = models.CharField(max_length=200)
    rol_id_rol = models.ForeignKey(Rol, null=False,  blank=False, on_delete=models.CASCADE)
    comuna = models.ForeignKey(Comuna, null=False,  blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"
    
class Subasta(models.Model):
    id_subasta = models.IntegerField(primary_key=True, default=100)
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    precio_inicial = models.IntegerField(max_length=200)
    precio_mas_alto = models.IntegerField(max_length=200)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    hora_inicio = models.TimeField()
    hora_termino = models.TimeField()

    def __str__(self):
        return self.nombre
    
class Comentario(models.Model):
    id_comentario = models.IntegerField(primary_key=True, default=100)
    comentario = models.CharField(max_length=200)
    fecha_comentario = models.DateField()
    estado_comentario = models.CharField(max_length=200)
    usuario_id_usuario = models.ForeignKey(Usuario, null=False, blank=False, on_delete=models.CASCADE)

class Carrito(models.Model):
    id_carrito = models.IntegerField(primary_key=True, default=100)
    fecha_compra = models.DateField()
    total_venta = models.IntegerField(max_length=200)
    iva = models.IntegerField(max_length=200)
    usuario_id_usuario = models.ForeignKey(Usuario, null=False, blank=False, on_delete=models.CASCADE)

class Usuario_subasta(models.Model):
    id_usuario_subasta = models.IntegerField(primary_key=True, default=100)
    usuario_id_usuario = models.ForeignKey(Usuario, null=False, blank=False, on_delete=models.CASCADE)
    subasta_id_subasta = models.ForeignKey(Subasta, null=False, blank=False, on_delete=models.CASCADE)

class Publicacion(models.Model):
    id_publicacion = models.IntegerField(primary_key=True, default=100)
    titulo_publicacion = models.CharField(max_length=200)
    descripcion_publicacion = models.IntegerField(max_length=200) 
    fecha_publicacion = models.DateField()
    estado_publicacion = models.CharField(max_length=200)
    usuario_id_usuario = models.ForeignKey(Usuario, null=False, blank=False, on_delete=models.CASCADE)

class Foto(models.Model):
    id_foto = models.IntegerField(primary_key=True, default=100)
    foto = models.CharField(max_length=200)
    subasta_id_subasta = models.ForeignKey(Subasta, null=False, blank=False, on_delete=models.CASCADE)
    producto_id_producto = models.ForeignKey(Producto, null=False, blank=False, on_delete=models.CASCADE)