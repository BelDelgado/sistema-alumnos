from django.contrib import admin
from .models import Alumno

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'email', 'telefono', 'fecha_nacimiento', 'usuario', 'fecha_registro']
    list_filter = ['fecha_registro', 'usuario']
    search_fields = ['nombre', 'apellido', 'email']
    date_hierarchy = 'fecha_registro'
    ordering = ['-fecha_registro']