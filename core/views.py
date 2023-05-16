from django.contrib.auth.models import User
from django.views import View
from core.forms import FormProducto
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http.response import HttpResponse
from django.http import JsonResponse

from core.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            usuario_logeado = User.objects.last()
            carrito = Carrito()
            carrito.usuario = usuario_logeado
            carrito.total = 0
            carrito.save()
            messages.success(request, "El usuario ha sido registrado exitosamente! ahora puede iniciar sesion.")
            return redirect('CORE:producto_index')
            
        else:
            messages.success(request, "No se pudo registrar el usuario, vuelva a intenarlo rellenando los campos correctamente!")

    return render(request, 'registration/register.html')

def producto_index(request):
    productos = Producto.objects.all().order_by("-id")
    
    return render(request, "core/producto/index.html", {
        'categorias' : Categoria.objects.all(),
        #'productos' : productos[3:10] codigo para obtener solo algunos
        'productos' : productos
    })

def producto_create(request):
    categorias = Categoria.objects.all()
    if request.method == "POST":
        categoria_del_producto = Categoria.objects.get(id=request.POST["categoria"])
        form = FormProducto(request.POST, request.FILES, instance=Producto(imagen=request.FILES['imagen'], categoria=categoria_del_producto))   
        if form.is_valid():
            form.save()
            return redirect("CORE:producto_index")
        else:
            return render(request, 'core/producto/create.html', {
                'categorias' : categorias,
                'error_message' : 'Ingreso un campo incorrecto, vuelva a intentar'
            })
    else:
        return render(request, 'core/producto/create.html', {
            'categorias' : categorias
        })

def producto_show(request, producto_id):
    producto =  get_object_or_404(Producto, id=producto_id)

    return render(request, 'core/producto/show.html',{
        'categorias' : Categoria.objects.all(),
        'producto' : producto
    })

def producto_edit(request, producto_id):
    categorias = Categoria.objects.all()
    producto = Producto.objects.get(id=producto_id)

    if request.method == "POST":
        categoria_del_producto = Categoria.objects.get(id=request.POST["categoria"])
        form = FormProducto(request.POST, request.FILES, instance=Producto(imagen=request.FILES['imagen'], categoria=categoria_del_producto))   
        if form.is_valid():
            producto.titulo = request.POST['titulo']
            producto.categoria = categoria_del_producto
            producto.descripcion = request.POST['descripcion']
            producto.imagen = request.FILES['imagen']
            producto.precio = request.POST['precio']
            producto.save()
            return redirect("CORE:producto_index")
        else:
            return render(request, 'core/producto/edit.html', {
                'categorias' : categorias,
                'error_message' : 'Ingreso un campo incorrecto, vuelva a intentar'
            })
    else:
        return render(request, 'core/producto/edit.html',{
            'categorias' : categorias,
            'producto' : producto
        })

def producto_delete(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    producto.delete()
    return redirect('CORE:producto_index')

def producto_search(request):
    texto_de_busqueda = request.GET["texto"]
    productosPorTitulo = Producto.objects.filter(titulo__icontains = texto_de_busqueda).all()
    productosPorDescripcion = Producto.objects.filter(descripcion__icontains = texto_de_busqueda).all()
    productos = productosPorTitulo | productosPorDescripcion
    return render(request, 'core/producto/search.html',
    {
        'categorias' : Categoria.objects.all(),
        'productos' : productos
    })
  
def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id = categoria_id)
    productos = categoria.productos.all()
    return render(request, 'core/producto/search.html',
    {
        'categorias' : Categoria.objects.all(),
        'productos' : productos,
        'categoria' : categoria.descripcion,
    })

def carrito_index(request):
    categorias = Categoria.objects.all()
    usuario_logeado = User.objects.get(username=request.user)
    productos = Carrito.objects.get(usuario=usuario_logeado.id).items.all()

    carrito = Carrito.objects.get(usuario=usuario_logeado.id)
    nuevo_precio_Carrito = 0
    for item in carrito.items.all():
        #validar si es que tiene descuento
        nuevo_precio_Carrito += item.producto.precio

    carrito.total = nuevo_precio_Carrito
    carrito.save()

    return render(request, 'core/carrito/index.html', {
        'categorias' : categorias,
        'usuario' : usuario_logeado,
        'items_carrito' : productos
    })

def carrito_save(request):

    if request.method == 'POST':
        producto = Producto.objects.get(id=request.POST['producto_id'])
        usuario_logeado = User.objects.get(username=request.user)

        #Agregamos el producto
        carrito = Carrito.objects.get(usuario=usuario_logeado.id)
        item_carrito = Carrito_item()
        item_carrito.carrito = carrito
        item_carrito.producto = producto
        item_carrito.save()

        #Sumamos el precio
        carrito.total = producto.precio + carrito.total
        carrito.save()
        messages.success(request, f"El producto {producto.titulo} fue agregado al carrito")
        return redirect("CORE:carrito_index")

    else:
        return redirect("CORE:carrito_index")

def carrito_clean(request):
    usuario_logeado = User.objects.get(username=request.user)
    carrito = Carrito.objects.get(usuario=usuario_logeado.id)
    carrito.items.all().delete()
    carrito.total = 0
    carrito.save()
    return redirect('CORE:carrito_index')

def item_carrito_delete(request, item_carrito_id):
    item_carrito = Carrito_item.objects.get(id=item_carrito_id)
    carrito = item_carrito.carrito
    
    nuevo_precio_Carrito = 0 - item_carrito.producto.precio
    for item in carrito.items.all():
        nuevo_precio_Carrito += item.producto.precio

    carrito.total = nuevo_precio_Carrito
    item_carrito.delete()
    carrito.save()
    return redirect("CORE:carrito_index")


class ConvertCurrencyView(View):
    def post(self, request):
        exchange_rate = 0.0012  # Tasa de cambio de pesos a dólares (ejemplo)
        peso_amount = request.POST.get('peso_amount')
        dollar_amount = float(peso_amount) * exchange_rate
        return JsonResponse({'dollar_amount': dollar_amount})



