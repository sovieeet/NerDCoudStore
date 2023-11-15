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
    path('vistaBoleta/', views.vistaBoleta, name='vistaBoleta'),
    path('descargar_boleta_pdf/<int:boleta_id>/', views.descargarBoleta_pdf, name='descargar_boleta_pdf'),
    path('descargar_boletas_excel/', views.descargarExcelBoletas, name='descargar_boletas_excel'),
    path('videojuegos/', views.videojuegos, name='videojuegos'),
    path('mangas/', views.mangas, name='mangas'),
    path('animes/', views.animes, name='animes'),
    path('accesorios/', views.accesorios, name='accesorios'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)