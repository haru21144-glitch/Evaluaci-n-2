from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import Evento, Actividad, Tarea
from .forms import EventoForm, ActividadForm, TareaForm

@login_required
@permission_required("gestion.view_evento", raise_exception=True)
def evento_list(request):
    eventos = Evento.objects.all()

    if request.user.groups.filter(name="COLABORADOR").exists():
        eventos = eventos.filter(colaboradores=request.user)

    return render(request, "gestion/evento_list.html", {"eventos": eventos})

@login_required
@permission_required("gestion.add_evento", raise_exception=True)
def evento_create(request):
    if request.method == "POST":
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.responsable = request.user
            evento.save()
            evento.colaboradores.add(request.user)
            return redirect("evento_list")
    else:
        form = EventoForm()

    return render(request, "gestion/evento_form.html", {"form": form})



def login_view(request):
    if request.user.is_authenticated:
        return redirect("evento_list")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("evento_list")
    else:
        form = AuthenticationForm()

    return render(request, "gestion/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
@permission_required("gestion.view_evento", raise_exception=True)
def evento_detail(request, pk):
    evento = Evento.objects.prefetch_related(
        "actividades__tareas"
    ).get(pk=pk)

    actividades = evento.actividades.all()

    return render(request, "gestion/evento_detail.html", {
        "evento": evento,
        "actividades": actividades,
        "actividad_form": ActividadForm(),
        "tarea_form": TareaForm(),
    })

@login_required
@permission_required("gestion.change_evento", raise_exception=True)
def evento_edit(request, pk):
    evento = get_object_or_404(Evento, pk=pk)

    if request.method == "POST":
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect("evento_detail", pk=evento.pk)
    else:
        form = EventoForm(instance=evento)

    return render(request, "gestion/evento_form.html", {
        "form": form,
        "evento": evento
    })

@login_required
@permission_required("gestion.add_evento", raise_exception=True)
def create_actividad(request, evento_pk):
    evento = get_object_or_404(Evento, pk=evento_pk)

    if request.method == "POST":
        form = ActividadForm(request.POST)
        if form.is_valid():
            actividad = form.save(commit=False)
            actividad.evento = evento
            actividad.save()

            return redirect("evento_detail", pk=evento.pk)
    else:
        form = ActividadForm()

    return render(request, "gestion/actividad_form.html", {"form": form, "evento": evento})

@login_required
@permission_required("gestion.change_evento", raise_exception=True)
def edit_actividad(request, evento_pk, actividad_pk):
    evento = get_object_or_404(Evento, pk=evento_pk)
    actividad = get_object_or_404(Actividad, pk=actividad_pk, evento=evento)

    if request.method == "POST":
        form = ActividadForm(request.POST, instance=actividad)
        if form.is_valid():
            form.save()
            return redirect("evento_detail", pk=evento.pk)
    else:
        form = ActividadForm(instance=actividad)

    return render(request, "gestion/actividad_form.html", {
        "form": form,
        "actividad": actividad,
        "evento": evento
    })

@login_required
@permission_required("gestion.delete_evento", raise_exception=True)
def delete_actividad(request, evento_pk, actividad_pk):
    evento = get_object_or_404(Evento, pk=evento_pk)
    actividad = get_object_or_404(Actividad, pk=actividad_pk, evento=evento)

    if request.method == "POST":
        actividad.delete()
        return redirect("evento_detail", pk=evento.pk)

    return render(request, "gestion/confirm_delete.html", {
        "object": actividad,
        "type": "actividad"
    })

@login_required
@permission_required("gestion.add_evento", raise_exception=True)
def create_tarea(request, evento_pk, actividad_pk):
    evento = get_object_or_404(Evento, pk=evento_pk)
    actividad = get_object_or_404(Actividad, pk=actividad_pk, evento=evento)

    if request.method == "POST":
        form = TareaForm(request.POST, instance=Tarea(actividad=actividad))
        if form.is_valid():
            form.save()
            tarea = form.save(commit=False)
            tarea.actividad = actividad
            tarea.responsable = request.user
            tarea.save()
            return redirect("evento_detail", pk=evento.pk)
    else:
        form = TareaForm()

    return render(request, "gestion/tarea_form.html", {"form": form, "evento": evento, "actividad": actividad})


@login_required
@permission_required("gestion.change_evento", raise_exception=True)
def edit_tarea(request, evento_pk, actividad_pk, tarea_pk):
    evento = get_object_or_404(Evento, pk=evento_pk)
    actividad = get_object_or_404(Actividad, pk=actividad_pk, evento=evento)
    tarea = get_object_or_404(Tarea, pk=tarea_pk, actividad=actividad)

    if request.method == "POST":
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect("evento_detail", pk=evento.pk)
    else:
        form = TareaForm(instance=tarea)

    return render(request, "gestion/tarea_form.html", {
        "form": form,
        "tarea": tarea,
        "evento": evento
    })

@login_required
@permission_required("gestion.delete_evento", raise_exception=True)
def delete_tarea(request, evento_pk, actividad_pk, tarea_pk):
    evento = get_object_or_404(Evento, pk=evento_pk)
    actividad = get_object_or_404(Actividad, pk=actividad_pk, evento=evento)
    tarea = get_object_or_404(Tarea, pk=tarea_pk, actividad=actividad)

    if request.method == "POST":
        tarea.delete()
        return redirect("evento_detail", pk=evento.pk)

    return render(request, "gestion/confirm_delete.html", {
        "object": tarea,
        "type": "tarea"
    })

