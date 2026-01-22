from django.contrib import admin
from .models import Evento, Actividad, Tarea

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "responsable", "fecha_inicio", "fecha_termino")
    search_fields = ("nombre",)
    fields = ("nombre", "descripcion", "responsable", "colaboradores", "fecha_inicio", "fecha_termino")

@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "evento", "fecha_inicio", "fecha_termino")
    list_filter = ("evento",)

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "actividad", "responsable", "fecha_inicio", "fecha_termino", "estado")
    list_filter = ("actividad", "responsable", "estado",)
