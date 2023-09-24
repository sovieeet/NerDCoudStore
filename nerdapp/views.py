from django.shortcuts import render

# Create your views here.

def hola_mundo(request):
    return render(request, 'nerdapp/index.html')

def page2(request):
    return render(request, 'nerdapp/page2.html')