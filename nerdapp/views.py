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
from django.core.mail import send_mail
from nerdcoudstore.settings import EMAIL_HOST_USER

def index(request):
    productos = Producto.objects.all()[:3]

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
            
            subject = "Usuario/a Creado" 
            message = "Estimado/a usuario/a" + " " + aux_user.username + ", su cuenta de NerdCoudStore ha sido creada."
            email = aux_user.email
            recipient_list = [email]
            send_mail(subject, message, EMAIL_HOST_USER, recipient_list, fail_silently=True) 
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

            subject = "Subasta Creada" 
            message = "Estimado/a " + usuario.nombre_usuario + ", su subasta '" + subasta.nombre + "' ha sido creada con un valor inicial de " + "$" + str(subasta.precio_inicial) + " CLP."
            email = usuario.correo
            recipient_list = [email]
            html_message = f"""<p>{message}</p><img src="https://i.imgur.com/wSs6Cnr.png" title="source: imgur.com" />
            <p>Encuéntranos en Avenida Concha Y Toro, Av. San Carlos 1340</p>"""
            send_mail(subject, message, EMAIL_HOST_USER, recipient_list, fail_silently=True, html_message=html_message)

            usuario_subasta.save()  # Guarda la relación en UsuarioSubasta
            data['mensaje']="guardado correctamente"
            return redirect('listSubastas')
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

            subject = "Participación en Subasta Exitosa"
            message = f"Estimado/a {usuarioClass.nombre_usuario}, su participación en la subasta '{subastaClass.nombre}' ha sido exitosa."
            email = usuarioClass.correo
            recipient_list = [email]

            html_message = f"""
            <p>{message}</p>
            <p>Ha ofertado con éxito en la subasta. El monto de su oferta es de ${montoS} CLP.</p>
            <img src="https://i.imgur.com/wSs6Cnr.png" alt="Firma">
            <p>Encuéntranos en Avenida Concha Y Toro, Av. San Carlos 1340</p>
            """

            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=True, html_message=html_message)
            
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

    producto = Producto.objects.get(id_producto=id_producto)
    usuario = request.user

    subject = "Compra Exitosa"
    message = f"Estimado/a {usuario.nombre_usuario}, ¡su compra de {producto.nombre} ha sido exitosa!"
    email = usuario.correo
    recipient_list = [email]

    html_message = f"""<p>{message}</p><img src="https://i.imgur.com/wSs6Cnr.png" alt="Firma">
    <p>Encuéntranos en Avenida Concha Y Toro, Av. San Carlos 1340</p>"""

    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=True, html_message=html_message)

    return render(request, 'nerdapp/payment-success.html', {'productos': producto})

def paymentFailed(request, id_producto):

    producto = Producto.objects.get(id_producto=id_producto)
    usuario = request.user

    subject = "Compra fallida"
    message = f"Estimado/a {usuario.nombre_usuario}, su compra de {producto.nombre} no se ha completado"
    email = usuario.correo
    recipient_list = [email]

    html_message = f"""<p>{message}</p><img src="https://i.imgur.com/wSs6Cnr.png" alt="Firma">
    <p>Encuéntranos en Avenida Concha Y Toro, Av. San Carlos 1340</p>"""

    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=True, html_message=html_message)

    return render(request, 'nerdapp/payment-failed.html', {'productos': producto})
"""
def enviar_correo(subasta):
    subject = 'Subasta finalizada'
    message = f'La subasta {subasta.nombre} ha finalizado. ¡Felicidades! Tu oferta de ${subasta.precio_mas_alto} ha ganado.'
    from_email = 'your-email@example.com'
    recipient_list = [subasta.usuario_id_usuario_id.correo]  # Dirección de correo del usuario que ganó la subasta

    send_mail(subject, message, from_email, recipient_list)


def listForo(request):
    publicaciones = Publicacion.objects.all()
    comentarios = Comentario.objects.all()
    context = {
            'publicaciones': publicaciones,
            'comentarios': comentarios
        }
    return render(request, 'foro/listForo.html', context)
    """

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
        print(foro)
        if formulario.is_valid():
            formulario.save()
            return redirect(reverse('participacionForo', args=[foro]))
        
def participacionForo(request, id_publicacion):
    print("Foro:", id_publicacion)
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
        print(formulario)
        if formulario.is_valid():
            print("formulario valido")

            # Obtener el usuario actual
            usuario = request.user

            # Envía un correo de confirmación
            subject = "Foro Agregado Exitosamente"
            message = f"Estimado/a {usuario.username}, su foro ha sido agregado exitosamente." 
            email = usuario.email
            recipient_list = [email]

            html_message = f"""
            <p>{message}</p>
            <img src="https://i.imgur.com/wSs6Cnr.png" alt="Firma" style="width: 100%">
            <p>Encuéntranos en Avenida Concha Y Toro, Av. San Carlos 1340</p>
            """

            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=True, html_message=html_message)

            data['mensaje'] = "Guardado correctamente"

            formulario.save()
        #usuario = Usuario.objects.get(id_usuario=request.user.id)  # Obtiene el usuario actual
            data['mensaje']="guardado correctamente"
        else:
            print("formulario no valido")
        data["form"] = formulario
        return render(request, 'foro/agregarForo.html',data)
