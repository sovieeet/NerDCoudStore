from django.urls import path
from . import views
from .views import CustomLoginView

urlpatterns = [
    path('', views.hola_mundo, name='hola_mundo'),
    path('page2/', views.page2, name='page2'),  # Agrega esta línea para la página 2
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('dashboard/', views.dashboard, name='dashboard'),
]