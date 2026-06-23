from django.db import models

# Create your models here.
from django.db import models

class Libro(models.Model):
    ESTADO_CHOICES = [
        ('enInventario', 'En Inventario'),
        ('prestado', 'Prestado'),
        ('sinExistencias', 'Sin Existencias')
    ]
    CATEGORIA_CHOICES = [
        ('000-Generalidades', '000-Generalidades'),
        ('300-Ciencias Sociales', '300-Ciencias Sociales'),
        ('400-Lenguas', '400-Lenguas'),
        ('500-Ciencias naturales y matemáticas', '500-Ciencias naturales y matemáticas'),
        ('600-Tecnología (Ciencia aplicadas)', '600-Tecnología (Ciencia aplicadas)'),
        ('700-Bellas artes', '700-Bellas artes'),
        ('800-Literatura y retórica', '800-Literatura y retórica'),
        ('900-Geografía e Historia', '900-Geografía e Historia'),
        ('Préstamo a domicilio', 'Préstamo a domicilio'),
    ]

    nt = models.CharField(max_length=20, unique=True)
    etiqueta = models.CharField(max_length=50)
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES, default='000-Generalidades')
    ejemplares = models.IntegerField(default=1)
    foto = models.ImageField(upload_to='libros/', null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='enInventario')
    registrado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-registrado_en']

    def __str__(self):
        return self.titulo
