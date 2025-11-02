# rifa/models.py
from django.db import models
from django.contrib.auth.models import User # Para el "usuario que lo creo"

class Rifa(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    fecha_sorteo = models.DateTimeField(blank=True, null=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Boleta(models.Model):
    # La rifa a la que pertenece esta boleta
    rifa = models.ForeignKey(Rifa, on_delete=models.CASCADE, related_name="boletas")
    
    # El número de la boleta
    numero = models.PositiveIntegerField()
    
    # El usuario que registró la boleta (tu requisito)
    usuario_creador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # El nombre del comprador (tu requisito)
    nombre_propietario = models.CharField(max_length=255)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ganadora = models.BooleanField(default=False, verbose_name="¿Es ganadora?")

    class Meta:
        # Asegura que no haya dos números iguales en la MISMA rifa
        unique_together = ('rifa', 'numero')

    def __str__(self):
        return f"Boleta #{self.numero} ({self.nombre_propietario})"