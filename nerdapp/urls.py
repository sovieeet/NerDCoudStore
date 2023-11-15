from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('vistaVenta/', views.vistaVenta, name='vistaVenta'),
    path('get_chart/', views.get_chart, name='get_chart'),
    path('descargar-pdf/', views.descargar_pdf, name='descargar_pdf'),
    path('descargar-excel/', views.descargar_excel, name='descargar_excel'),
    path('signup/', views.signup, name='signup'),
    path('listSubastas/', views.ListarYParticiparSubastas.as_view(), name='listSubastas'),
    path('agregarSubasta/', views.agregarSubasta, name='agregarSubasta'),
    path('participacionSubasta/<int:subasta_id>/<int:monto>/', views.participacionSubasta, name='participacionSubasta'),
    path('participacionForo/<int:id_publicacion>/', views.participacionForo, name='participacionForo'),
    path('checkout/<int:id_producto>/', views.CheckOut, name='checkout'),
    path('payment-success/<int:id_producto>/', views.PaymentSuccessful, name='payment-success'),
    path('payment-failed/<int:id_producto>/', views.paymentFailed, name='payment-failed'),
    path('products/', views.ProductView, name='products'),
    path('listForo/', views.listarYComentarForo.as_view(), name='listForo'),
    path('agregarForo/', views.agregarForo, name='agregarForo'),
     path('agregar_al_carrito/<int:id_producto>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('ver_carrito/', views.ver_carrito, name='ver_carrito'),
    path('ver_carrito/', views.ver_carrito, name='ver_carrito'),
    path('eliminar_del_carrito/<int:id_carrito_producto>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),



]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)