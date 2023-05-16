from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Categoria(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='Id de categoria')
    descripcion = models.CharField(max_length=200, null=True)

    def __str__(self) -> str:
        return f"Id: {self.id} | Descripcion: {self.descripcion}"


class Producto(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='Id de producto')
    titulo = models.CharField(max_length=50, null=False)
    # Imagen
    imagen = models.FileField(upload_to='productos/')
    descripcion = models.CharField(max_length=200, null=False)
    precio = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    # FK
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE, related_name="productos")

    def __str__(self) -> str:
        return f"Id: {self.id} | Titulo: {self.titulo} | Imagen: {self.imagen} | Descripcion: {self.descripcion} | Precio: {self.precio} || Categoria_id: {self.categoria.id} "


class Carrito(models.Model):
    
    id = models.IntegerField(primary_key=True, verbose_name='Id de carrito')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carrito")
    total = models.DecimalField(null=False, max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"Id: {self.id} | Usuario_id: {self.usuario.id} | Usuario: {self.usuario.username} | Total: {self.total}"


class Carrito_item(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='Id de Item carrito')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE) 
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="items")

    def __str__(self) -> str:
        return f"Id: {self.id} | Producto: {self.producto.titulo} | Carrito_id: {self.carrito.id}"