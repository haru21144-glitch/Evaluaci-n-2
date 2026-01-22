from django.urls import path
from . import views

urlpatterns = [
    path("", views.evento_list, name="evento_list"),
    path("eventos/crear/", views.evento_create, name="evento_create"),
    path("eventos/<int:pk>/", views.evento_detail, name="evento_detail"),
    path("eventos/<int:pk>/editar/", views.evento_edit, name="evento_edit"),
    path("eventos/<int:evento_pk>/actividades/crear/", views.create_actividad, name="actividad_create"),
    path("eventos/<int:evento_pk>/actividades/<int:actividad_pk>/editar/", views.edit_actividad, name="actividad_edit"),
    path("eventos/<int:evento_pk>/actividades/<int:actividad_pk>/eliminar/", views.delete_actividad, name="actividad_delete"),
    path("eventos/<int:evento_pk>/actividades/<int:actividad_pk>/tareas/crear/", views.create_tarea, name="tarea_create"),
    path("eventos/<int:evento_pk>/actividades/<int:actividad_pk>/tareas/<int:tarea_pk>/editar/", views.edit_tarea, name="tarea_edit"),
    path("eventos/<int:evento_pk>/actividades/<int:actividad_pk>/tareas/<int:tarea_pk>/eliminar/", views.delete_tarea, name="tarea_delete"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]