# rifa/admin.py
import random # Para elegir al azar
from django.contrib import admin, messages
from django.urls import reverse
from django.utils.html import format_html
from .models import Rifa, Boleta
from django.urls import path
from . import views

# --- Esta es la función que será nuestro "botón" ---
class RifaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activa', 'fecha_sorteo', 'boton_sorteo_visual')
    list_filter = ('activa',)
    
    # --- AÑADE ESTA FUNCIÓN ---
    def get_urls(self):
        # Obtiene las URLs de admin estándar
        urls = super().get_urls()
        
        # Añade nuestra URL personalizada
        custom_urls = [
            path(
                # La ruta es relativa al admin de este modelo
                '<int:rifa_id>/sorteo/', 
                # Envolvemos la vista para protegerla
                self.admin_site.admin_view(views.admin_sorteo_visual), 
                name='admin_sorteo_visual'
            )
        ]
        # Devuelve nuestras URLs personalizadas PRIMERO
        return custom_urls + urls

    def boton_sorteo_visual(self, obj):
        if obj.activa:
            # El 'name' que usamos aquí ahora es 'admin:admin_sorteo_visual'
            # pero como estamos dentro del admin, Django suele resolverlo.
            # Usemos 'admin:admin_sorteo_visual' para estar seguros.
            url = reverse('admin:admin_sorteo_visual', args=[obj.pk])
            return format_html(f'<a href="{url}" class="button" style="background-color: #E67E22;">Realizar Sorteo</a>')
        return "Sorteo Finalizado"
    
    boton_sorteo_visual.short_description = "Acción de Sorteo"

class BoletaAdmin(admin.ModelAdmin):
    # ... (esto no cambia)
    list_display = ('numero', 'nombre_propietario', 'rifa', 'usuario_creador', 'fecha_creacion')
    list_filter = ('rifa', 'usuario_creador')

admin.site.register(Rifa, RifaAdmin)
admin.site.register(Boleta, BoletaAdmin)