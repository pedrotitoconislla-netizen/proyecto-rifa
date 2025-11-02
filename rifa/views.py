# rifa/views.py
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Boleta, Rifa
from .forms import BoletaForm
from django.contrib.auth.forms import UserCreationForm # Importa el formulario de registro
from django.urls import reverse_lazy # Para la redirección
from django.views.generic import RedirectView
import random # <-- ASEGÚRATE DE IMPORTAR RANDOM
from django.contrib import messages # <-- Y MESSAGES
from django.shortcuts import get_object_or_404, redirect

# Vista para que un usuario cree una boleta
# LoginRequiredMixin = Obliga al usuario a estar logueado
class CrearBoletaView(LoginRequiredMixin, CreateView):
    model = Boleta
    form_class = BoletaForm
    template_name = 'rifa/crear_boleta.html' # El HTML que usará
    success_url = '/mis-boletas/' # A dónde ir después de crearla
        

    def form_valid(self, form):
        # 1. Asigna el usuario actual como el creador
        form.instance.usuario_creador = self.request.user
        
        # 2. Asigna la rifa que está activa
        # (Esto asume que solo hay una rifa activa a la vez)
        rifa_activa = Rifa.objects.filter(activa=True).first()
        
        if not rifa_activa:
            # Si no hay rifas activas, muestra un error
            form.add_error(None, "No hay ninguna rifa activa en este momento.")
            return self.form_invalid(form)
            
        form.instance.rifa = rifa_activa
        
        # 3. Validar que el número no esté repetido EN ESA rifa
        existe = Boleta.objects.filter(rifa=rifa_activa, numero=form.instance.numero).exists()
        if existe:
            form.add_error('numero', f"El número {form.instance.numero} ya está ocupado en esta rifa.")
            return self.form_invalid(form)

        return super().form_valid(form)
    
    
# Vista para que el usuario vea SOLO las boletas que él creó
class MisBoletasView(LoginRequiredMixin, ListView):
    model = Boleta
    template_name = 'rifa/mis_boletas.html' # El HTML que usará
    context_object_name = 'boletas'

    def get_queryset(self):
        # Filtra las boletas para mostrar solo las del usuario logueado
        return Boleta.objects.filter(usuario_creador=self.request.user).order_by('-fecha_creacion')
# Vista de Registro de Usuario
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login') # Redirige al login después de registrarse

# --- NUEVA VISTA DE ADMIN PARA SORTEO VISUAL ---
def admin_sorteo_visual(request, rifa_id):
    rifa = get_object_or_404(Rifa, pk=rifa_id)
    
    nuevo_ganador = None # Inicializamos esto en None

    # Si el admin hizo clic en "Sacar Siguiente Ganador"
    if request.method == 'POST':
        # Buscamos las boletas que aún participan
        boletas_para_sorteo = rifa.boletas.filter(ganadora=False)
        
        if boletas_para_sorteo:
            # ¡La magia! Seleccionamos un ganador de los ELEGIBLES
            nuevo_ganador = random.choice(list(boletas_para_sorteo))

            # Marcamos la boleta como ganadora
            nuevo_ganador.ganadora = True
            nuevo_ganador.save()
            
            messages.success(request, f"¡Ganador seleccionado: Boleta #{nuevo_ganador.numero}!")
            
            # ¡YA NO REDIRIGIMOS!
            # Dejamos que la función continúe para renderizar la plantilla
            # con el 'nuevo_ganador'
            
        else:
            messages.error(request, "No quedan más boletas participantes para sortear.")
            
    # --- Consultas actualizadas para la plantilla ---
    
    # 1. Obtenemos los ganadores que YA salieron
    #    Si acabamos de sacar uno, lo excluimos de esta lista por ahora
    ganadores_anteriores = rifa.boletas.filter(ganadora=True)
    if nuevo_ganador:
        ganadores_anteriores = ganadores_anteriores.exclude(pk=nuevo_ganador.pk)

    # 2. Obtenemos las boletas que AÚN participan (ya no incluye al nuevo ganador)
    boletas_participantes_restantes = rifa.boletas.filter(ganadora=False)

    context = {
        'title': f'Sorteo de {rifa.nombre}',
        'rifa': rifa,
        'boletas_participantes': boletas_participantes_restantes, # Lista actualizada
        'ganadores_anteriores': ganadores_anteriores,
        'nuevo_ganador': nuevo_ganador, # ¡Pasamos el nuevo ganador a la plantilla!
        'has_permission': True,
        'opts': Rifa._meta,
    }
    
    return render(request, 'admin/sorteo_visual.html', context)