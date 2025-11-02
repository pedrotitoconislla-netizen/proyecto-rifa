# rifa/urls.py (Archivo nuevo)
from django.urls import path
from django.views.generic import RedirectView
from .views import CrearBoletaView, MisBoletasView, RegisterView
from . import views 

urlpatterns = [
    path('', RedirectView.as_view(url='/mis-boletas/', permanent=False), name='home'),
    path('crear/', CrearBoletaView.as_view(), name='crear_boleta'),    
    path('mis-boletas/', MisBoletasView.as_view(), name='mis_boletas'),    
    path('registro/', RegisterView.as_view(), name='register'),

]