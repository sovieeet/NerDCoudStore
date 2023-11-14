import datetime
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import *
#from .models import Categoria, Producto, Subasta, Usuario_subasta, Usuario, ParticiparSubasta, Publicacion
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.db.models import Q
from django.core.mail import send_mass_mail
from random import randrange
from django.db.models import Sum
from datetime import datetime
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

def index(request):
    productos = Producto.objects.all().order_by("-fecha_creacion")[:3]

    data = {
        'productos': productos
    }

    return render(request, 'nerdapp/index.html', data)

def page2(request):
    return render(request, 'nerdapp/page2.html')

def testPaypal(request):
    return render(request, 'payment/testpaypal.html')

def lista_categorias(request):
    categorias = Categoria.objects.all()
    #print(categorias)
    return render(request, 'nerdapp/lista_categorias.html', {'categorias': categorias})

def listForo(request):
    return render(request, 'foro/listForo.html')

def signup(request):
    data = {
        'form': CustomUserCreationForm
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            aux_user = formulario.save()
            usuario = Usuario.objects.create(
                id_usuario = aux_user.id,
                nombre_usuario = aux_user.username,
                nombre = aux_user.first_name,
                apellido = aux_user.last_name,
                correo = aux_user.email,        
            )
            usuario.save()
            user = authenticate(username=formulario.cleaned_data['username'], password=formulario.cleaned_data['password1'])
            login(request, user)
            messages.success(request,"cuenta creada correctamente")
            return redirect(to="index")
        data["form"] = formulario

    return render(request, 'registration/signup.html', data)

def agregarSubasta(request):
    data = {
        'form': SubastaForm()
    }
    if request.method == 'POST':
        formulario = SubastaForm(data=request.POST, files=request.FILES)
        #print("formulario ",formulario)
        if formulario.is_valid:
            subasta = formulario.save()  # Guarda la subasta y obtén la instancia
            usuario = Usuario.objects.get(id_usuario=request.user.id)  # Obtiene el usuario actual
            usuario_subasta = Usuario_subasta.objects.create(
                usuario_id_usuario=usuario,  # Obtiene el id del usuario actual
                subasta_id_subasta=subasta # Usa el id de la subasta recién creada
            )
            usuario_subasta.save()  # Guarda la relación en UsuarioSubasta
            data['mensaje']="guardado correctamente"
        else:
            data["form"] = formulario
    return render(request, 'subasta/agregarSubasta.html',data)

class ListarYParticiparSubastas(View):
    def get(self, request, *args, **kwargs):
        subastas = Subasta.objects.all().order_by('-fecha_inicio')
        form = ParticiparSubastaForm()
        context = {
            'subastas': subastas,
            'form': form,
        }
        return render(request, 'subasta/listSubastas.html', context)
    def post(self, request, *args, **kwargs):
        formulario = ParticiparSubastaForm(data=request.POST, files=request.FILES)
        subastas = Subasta.objects.all().order_by('-fecha_inicio')
        context = {
            'subastas': subastas,
            'form': formulario,
        }
        usuario =request.POST.get('usuario_id')           
        subasta = request.POST.get('subasta_id')
        montoS = request.POST.get('monto')
        subastaClass = Subasta.objects.get(id_subasta=subasta)
        """print("Usuario:", usuario)
        print("Subasta:", subasta)
        print("precio_inicial:", subastaClass.precio_inicial)
        print("precio_mas_alto:", subastaClass.precio_mas_alto)
        print("Monto:", montoS)"""
        if formulario.is_valid and int(montoS) > int(subastaClass.precio_inicial) and int(montoS) >  int(subastaClass.precio_mas_alto) :
            usuarioClass = Usuario.objects.get(id_usuario=request.user.id)      
            participarSubastaUsuario = ParticiparSubasta.objects.create(
                usuario_id_usuario_id=usuarioClass,
                subasta_id_subasta_id=subastaClass,
                monto=montoS
            )
            participarSubastaUsuario.save()
            subastaClass.precio_mas_alto = montoS
            subastaClass.save()
            return redirect(reverse('participacionSubasta', args=[subasta, montoS]))
        elif  int(montoS) < int(subastaClass.precio_inicial) :
            context['mensaje'] = 'El monto ingresado es menor a la oferta mas alta'
        else:
            context['mensaje'] = 'Hubo un error al procesar el formulario. Por favor, inténtelo de nuevo.'

        return render(request, 'subasta/listSubastas.html', context)

def participacionSubasta(request, subasta_id, monto):
    #print("Subasta:", subasta_id)
    #print("Monto:", monto)
    try:
        subasta = Subasta.objects.get(id_subasta=subasta_id)
        context = {
            'subasta': subasta,
            'descripcion' : subasta.descripcion,
            'fecha_termino' : subasta.fecha_termino,
            'hora_termino' : subasta.hora_termino,
            'monto': monto,
        }
        return render(request, 'subasta/participacionSubasta.html', context)
    except Subasta.DoesNotExist:
        return HttpResponse("Subasta no encontrada.")

def ProductView(request):

    get_productos = Producto.objects.all()

    return render(request, 'product.html', {'productos': get_productos})

def CheckOut(request, id_producto):

    productos = Producto.objects.get(id_producto=id_producto)

    clp_a_usd = 0.0011
    
    precio_clp = float(productos.precio)

    monto_usd = precio_clp * clp_a_usd

    host = request.get_host()

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': monto_usd,
        'item_name': productos.nombre,
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('payment-success', kwargs = {'id_producto': productos.id_producto})}",
        'cancel_url': f"http://{host}{reverse('payment-failed', kwargs = {'id_producto': productos.id_producto})}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        'productos': productos,
        'paypal': paypal_payment
    }

    return render(request, 'producto/checkout.html', context)

def PaymentSuccessful(request, id_producto):

    productos = Producto.objects.get(id_producto=id_producto)

    return render(request, 'nerdapp/payment-success.html', {'productos': productos})

def paymentFailed(request, id_producto):

    productos = Producto.objects.get(id_producto=id_producto)

    return render(request, 'nerdapp/payment-failed.html', {'productos': productos})

class listarYComentarForo(View):
    def get(self, request, *args, **kwargs):
        publicaciones = Publicacion.objects.all().order_by('-fecha_publicacion')
        comentarios = Comentario.objects.all().order_by('-fecha_comentario')
        context = {
                'publicaciones': publicaciones,
                'comentarios': comentarios
            }
        return render(request, 'foro/listForo.html', context)
    def post(self, request, *args, **kwargs):
        formulario = ComentarForo(data=request.POST, files=request.FILES)
        foro= request.POST.get('publicacion_id_publicacion')
        #print(foro)
        if formulario.is_valid():
            formulario.save()
            return redirect(reverse('participacionForo', args=[foro]))
        
def participacionForo(request, id_publicacion):
    #print("Foro:", id_publicacion)
    try:
        foro = Publicacion.objects.get(id_publicacion=id_publicacion)
        context = {
            'foro': foro.titulo_publicacion,
        }
        return render(request, 'foro/participacionForo.html', context)
    except Publicacion.DoesNotExist:
        return HttpResponse("Foro no encontrado.")

def agregarForo(request):
    data = {'form': ForoForm()}
    if request.method =="POST":
        formulario = ForoForm(data=request.POST, files=request.FILES)
        #print(formulario)
        if formulario.is_valid():
            #print("formulario valido")
            formulario.save()
            #usuario = Usuario.objects.get(id_usuario=request.user.id)  # Obtiene el usuario actual
            data['mensaje']="guardado correctamente"
        else:
            #print("formulario no valido")
            data["form"] = formulario
    return render(request, 'foro/agregarForo.html',data)

def vistaVenta(request):
    diccAlias, diccNombre = diccProductos()
    diccIdNombreCant = [(str(id), nombre, cantidad) for id, nombre, cantidad in diccNombre]

    context = {
        'diccIdNombreCant': diccIdNombreCant,
    }

    return render(request, 'informe/vistaVenta.html', context)

def get_chart(request):
    diccAlias,diccNombre = diccProductos()
    diccionario_ordenado=diccAlias
    now = datetime.now()
    current_month = now.month
    current_year = now.year
    nombres_productos = list(diccionario_ordenado.keys())
    cantidad_prodcutos = list(diccionario_ordenado.values())
    #print(cantidad_prodcutos)
    #print(nombres_productos)
    series = cantidad_prodcutos

    chart={
        'xAxis':[
            {
                'type' : "category",
                'data' : nombres_productos,
                'name': 'Productos',  # Título del eje X
                'axisLabel': {
                    'rotate': 45,  # Rotar etiquetas del eje X para mejor legibilidad
                },
            }
        ],
        'yAxis':[
            {
                'type' : "value",
                'name': 'Cantidad Vendida en '+str(current_month)+'/'+str(current_year),
            }
        ],
        'series':[
            {
            'data':series,
            'type': 'bar',
            'showBackground': 'true',
            'backgroundStyle': {
                'color': '#6264eb21'
            }
            }
        ]
    }
    return JsonResponse(chart)

def diccProductos():
    productos = Producto.objects.all().values()
    carritoUsuarios = Carrito.objects.filter(
            estado_pago="pagado"
        ).values()
    cont=0
    lisCarritoProductos =[]
    while(cont<len(carritoUsuarios)):
        carritosProductos = CarritoProducto.objects.filter(
            id_carrito_id=carritoUsuarios[cont]['id_carrito']
        ).values()
        lisCarritoProductos.extend(carritosProductos)
        cont+=1
    now = datetime.now()
    current_month = now.month
    current_year = now.year
    ventas_por_mes = Venta.objects.filter(
        fecha_venta__month =current_month,
        fecha_venta__year =current_year
    ).values()
    diccProductos ={str(producto['id_producto'])+"-"+producto['nombre'][:5]: 0 for producto in productos}
    diccNombres = {str(producto['id_producto'])+"|"+producto['nombre']: 0 for producto in productos}
    #diccNombres=[]
    for venta in ventas_por_mes:
        for carpro in lisCarritoProductos:
            if venta['id_carrito_id_id'] == carpro['id_carrito_id_id']:
                producto = Producto.objects.filter(
                    id_producto=carpro['id_producto_id_id']
                ).values()[0]
                diccProductos.update({str(producto['id_producto'])+"-"+producto['nombre'][:5]:diccProductos[str(producto['id_producto'])+"-"+producto['nombre'][:5]]+int(carpro['cantidad_producto'])})
                #diccNombres.append(producto['id_producto'],producto['nombre'],)
                diccNombres.update({str(producto['id_producto'])+"|"+producto['nombre']:diccNombres[str(producto['id_producto'])+"|"+producto['nombre']]+int(carpro['cantidad_producto'])})
        #diccNombres.append([producto['id_producto'],producto['nombre'],diccProductos[producto['nombre']]])
    #print(diccNombres)
    diccionario_ordenado = dict(sorted(diccProductos.items(), key=lambda item: item[1], reverse=True))
    MatAux=[] 
    for key,value in diccionario_ordenado.items():
        id,alias=key.split("-", 1)
        producto = Producto.objects.get(id_producto=id)
        #print('producto ',producto)
        MatAux.append([id,producto.nombre,value])
    #print(MatAux)
    diccionario_Nombres=MatAux
    #diccionario_Nombres = dict(sorted(diccNombres.items(), key=lambda item: item[1], reverse=True))
    #diccionario_Nombres = diccNombres
    #print(diccionario_Nombres)
    #{'3-Cojín': 2, '6-Manta': 1, '2-Tazón': 0, '4-Nicke': 0}
    return (diccionario_ordenado,diccionario_Nombres)

def descargar_pdf(request):
    diccAlias, diccNombre = diccProductos()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="informe_ventas.pdf"'

    # Crear el objeto PDF usando reportlab
    p = canvas.Canvas(response)
    p.drawString(100, 800, "Informe de Ventas")
    p.drawString(100, 780, "ID | Nombre | Cantidad")

    y = 760
    for id, nombre, cantidad in diccNombre:
        p.drawString(100, y, f"{id} | {nombre} | {cantidad}")
        y -= 20

    p.showPage()
    p.save()

    return response

def descargar_excel(request):
    diccAlias, diccNombre = diccProductos()
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="informe_ventas.xlsx"'

    # Crear el objeto Excel usando openpyxl
    wb = Workbook()
    ws = wb.active

    # Agregar encabezados
    ws.append(['ID', 'Nombre', 'Cantidad'])

    # Agregar datos
    for id, nombre, cantidad in diccNombre:
        ws.append([id, nombre, cantidad])

    # Guardar el libro de trabajo
    wb.save(response)

    return response