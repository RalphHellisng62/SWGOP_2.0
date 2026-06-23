from django.contrib import admin
from .models import PerfilUsuario, RecuperacionContraseña

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario']
    search_fields = ['usuario__username']

@admin.register(RecuperacionContraseña)
class RecuperacionContraseñaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tipo', 'creado_en', 'usado']
    list_filter = ['tipo', 'usado']
    search_fields = ['usuario__username']