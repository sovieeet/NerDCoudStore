from django.shortcuts import render
from .models import Categoria  # Asegúrate de importar tu modelo Producto

# Create your views here.

def hola_mundo(request):
    return render(request, 'nerdapp/index.html')

def page2(request):
    return render(request, 'nerdapp/page2.html')

#def lista_categorias(request):
#   categorias = Categoria.objects.all()  # Consultar todos los productos de la base de datos
#   return render(request, 'lista_categorias.html', {'categorias': categorias})

def lista_categorias(request):
    categorias = Categoria.objects.all()
    print(categorias)  # Muestra las categorías en la consola
    return render(request, 'nerdapp/lista_categorias.html', {'categorias': categorias})
