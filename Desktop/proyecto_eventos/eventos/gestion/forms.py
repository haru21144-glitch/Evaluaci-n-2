from django import forms
from .models import Evento, Actividad, Tarea

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ["nombre", "descripcion", "fecha_inicio", "fecha_termino"]
        widgets = {
            "fecha_inicio": forms.DateInput(attrs={"type": "date"}),
            "fecha_termino": forms.DateInput(attrs={"type": "date"}),
        }

class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ["nombre", "descripcion", "fecha_inicio", "fecha_termino", "participantes"]
        widgets = {
            "fecha_inicio": forms.DateInput(attrs={"type": "date"}),
            "fecha_termino": forms.DateInput(attrs={"type": "date"}),
        }

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ["titulo", "descripcion", "responsable", "estado", "fecha_inicio", "fecha_termino"]
        widgets = {
            "fecha_inicio": forms.DateInput(attrs={"type": "date"}),
            "fecha_termino": forms.DateInput(attrs={"type": "date"}),
        }
