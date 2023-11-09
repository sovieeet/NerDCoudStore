from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Categoria, Producto, Subasta, Usuario_subasta, Usuario, ParticiparSubasta, Publicacion
from .forms import CustomUserCreationForm, SubastaForm, ParticiparSubastaForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.db.models import Q

def index(request):
    productos = Producto.objects.all()

    data = {
        'productos': productos
    }

    return render(request, 'nerdapp/index.html', data)

def dashboard(request):
    return render(request, 'nerdapp/dashboard.html')

def page2(request):
    return render(request, 'nerdapp/page2.html')

def testPaypal(request):
    return render(request, 'payment/testpaypal.html')

def lista_categorias(request):
    categorias = Categoria.objects.all()
    print(categorias)
    return render(request, 'nerdapp/lista_categorias.html', {'categorias': categorias})

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

def participacionSubasta(request):
    return render(request, 'subasta/participacionSubasta.html')

"""def listSubastas(request):
    subastas = Subasta.objects.all()
    data = {
        "subastas" : subastas,
    }
    return render(request, 'subasta/listSubastas.html', data)


def participarSubasta(request):
    print("La función participarSubasta se está ejecutando.")
    data = {
        'form': ParticiparSubastaForm()
    }
    if request.method == 'POST':
        formulario = ParticiparSubastaForm(data=request.POST, files=request.FILES)
        if formulario.is_valid:
            usuario = Usuario.objects.get(id_usuario=request.usuario_id)             
            subasta = Subasta.objects.get(subasta_id = request.subasta_id)
            montoS = request.POST.get('monto')
            print("Usuario:", usuario)
            print("Subasta:", subasta)
            print("Monto:", montoS)
            participarSubastaUsuario = ParticiparSubasta.objects.create(
                usuario_id_usuario_id=usuario,
                subasta_id_subasta_id=subasta,
                monto=montoS
            )
            participarSubastaUsuario.save()
            data['mensaje']="guardado correctamente"
        else:
            data["form"] = formulario
    #return render(request, 'subasta/agregarSubasta.html')
"""

class ListarYParticiparSubastas(View):
    def get(self, request, *args, **kwargs):
        subastas = Subasta.objects.all()
        form = ParticiparSubastaForm()
        context = {
            'subastas': subastas,
            'form': form,
        }
        return render(request, 'subasta/listSubastas.html', context)
    def post(self, request, *args, **kwargs):
        formulario = ParticiparSubastaForm(data=request.POST, files=request.FILES)
        subastas = Subasta.objects.all()
        context = {
            'subastas': subastas,
            'form': formulario,
        }
        usuario =request.POST.get('usuario_id')           
        subasta = request.POST.get('subasta_id')
        montoS = request.POST.get('monto')
        subastaClass = Subasta.objects.get(id_subasta=subasta)
        print("Usuario:", usuario)
        print("Subasta:", subasta)
        print("precio_inicial:", subastaClass.precio_inicial)
        print("precio_mas_alto:", subastaClass.precio_mas_alto)
        print("Monto:", montoS)
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
    print("Subasta:", subasta_id)
    print("Monto:", monto)
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
        # Manejar el caso cuando la subasta no existe
        return HttpResponse("Subasta no encontrada.")

"""def participarSubasta(request):
    if request.method == 'POST':
        subasta_id = request.POST.get('subasta_id')
        usuario_id = request.POST.get('usuario_id')
        monto = request.POST.get('monto')
        participacion = ParticiparSubasta.objects.create(
            usuario_id_usuario_id= usuario_id,
            subasta_id_subasta_id = subasta_id,
            monto=monto,
        )
        participacion.save()
        messages.success(request,"participacion creada correctamente")
        return HttpResponse('Participación guardada exitosamente')
        
    else:
        return HttpResponse('Método no permitido')"""


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

    return render(request, 'nerdapp/checkout.html', context)

def PaymentSuccessful(request, id_producto):

    productos = Producto.objects.get(id_producto=id_producto)

    return render(request, 'nerdapp/payment-success.html', {'productos': productos})

def paymentFailed(request, id_producto):

    productos = Producto.objects.get(id_producto=id_producto)

    return render(request, 'nerdapp/payment-failed.html', {'productos': productos})

def listForo(request):
    publicaciones = Publicacion.objects.all()
    context = {
            'publicaciones': publicaciones,
        }
    return render(request, 'foro/listForo.html', context)