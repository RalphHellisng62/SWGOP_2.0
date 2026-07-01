from django.db import models
from django.contrib.auth.models import User
from libros.models import Libro

class Prestamo(models.Model):
    ESTADO_CHOICES = [
        ('vigente', 'Vigente'),
        ('vencido', 'Vencido'),
        ('devuelto', 'Devuelto'),
    ]

    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='prestamos')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prestamos_otorgados')
    nombre_lector = models.CharField(max_length=150)
    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='vigente')
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado_en']

    def __str__(self):
        return f"{self.libro.titulo} - {self.nombre_lector}"