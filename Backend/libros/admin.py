from django.contrib import admin
from .models import Libro

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'nt', 'categoria', 'estado', 'ejemplares']
    list_filter = ['estado', 'categoria']
    search_fields = ['titulo', 'autor', 'nt']