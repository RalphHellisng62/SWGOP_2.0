from django.contrib import admin
from .models import Prestamo

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ['nombre_lector', 'libro', 'fecha_prestamo', 'fecha_devolucion', 'estado']
    list_filter = ['estado', 'fecha_prestamo']
    search_fields = ['nombre_lector', 'libro__titulo']