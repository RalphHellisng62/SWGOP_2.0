# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import secrets

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    foto = models.ImageField(upload_to='perfiles/', null=True, blank=True)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"


class RecuperacionContraseña(models.Model):
    TIPO_CHOICES = [('email', 'Email')]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    codigo = models.CharField(max_length=6)
    email_o_telefono = models.CharField(max_length=100)
    creado_en = models.DateTimeField(auto_now_add=True)
    usado = models.BooleanField(default=False)

    def es_valido(self):
        desde_creacion = timezone.now() - self.creado_en
        return desde_creacion.total_seconds() < 300 and not self.usado

    @staticmethod
    def generar_codigo():
        return ''.join([str(secrets.randbelow(10)) for _ in range(6)])

    def __str__(self):
        return f"Recuperación para {self.usuario.username}"