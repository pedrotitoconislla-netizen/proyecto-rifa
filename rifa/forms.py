# rifa/forms.py
from django import forms
from .models import Boleta

class BoletaForm(forms.ModelForm):
    class Meta:
        model = Boleta
        
        # El usuario solo debe ingresar el número y el propietario
        # La 'rifa' y 'usuario_creador' se asignarán automáticamente en la vista
        fields = ['numero', 'nombre_propietario']
        
        widgets = {
            'numero': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 123'}),
            'nombre_propietario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Juan Pérez'}),
        }