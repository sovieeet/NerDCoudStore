from django.urls import path
from . import views

urlpatterns = [
    path('', views.hola_mundo, name='hola_mundo'),
    path('page2/', views.page2, name='page2'),  # Agrega esta línea para la página 2
]