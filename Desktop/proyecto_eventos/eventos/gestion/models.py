from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Evento(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()

    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="eventos_responsable",
    )

    colaboradores = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="eventos",
        blank=True,
    )
    def clean(self):
        if self.fecha_termino < self.fecha_inicio:
            raise ValidationError(
                "La fecha de término del evento no puede ser menor que la fecha de inicio."
            )

    def __str__(self):
        return self.nombre
    
class Actividad(models.Model):
    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
        related_name="actividades",
    )
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()

    participantes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="actividades",
        blank=True,
    )

    def clean(self):
        if self.fecha_termino < self.fecha_inicio:
            raise ValidationError(
                "La fecha de término de la actividad no puede ser menor que la fecha de inicio."
            )

        if self.evento_id:
            if (
                self.fecha_inicio < self.evento.fecha_inicio
                or self.fecha_termino > self.evento.fecha_termino
            ):
                raise ValidationError(
                    "La actividad debe estar dentro del rango de fechas del evento."
                )

    def __str__(self):
        return f"{self.evento.nombre} - {self.nombre}"

class Tarea(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("en_progreso", "En progreso"),
        ("completada", "Completada"),
    ]

    actividad = models.ForeignKey(
        Actividad,
        on_delete=models.CASCADE,
        related_name="tareas",
    )
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)

    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="tareas_responsable",
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="pendiente",
    )

    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()

    def clean(self):
        if self.fecha_termino < self.fecha_inicio:
            raise ValidationError(
                "La fecha de término de la tarea no puede ser menor que la fecha de inicio."
            )

        if self.actividad_id:
            if (
                self.fecha_inicio < self.actividad.fecha_inicio
                or self.fecha_termino > self.actividad.fecha_termino
            ):
                raise ValidationError(
                    "La tarea debe estar dentro del rango de fechas de la actividad."
                )

    def __str__(self):
        return f"{self.actividad.nombre} - {self.titulo}"
