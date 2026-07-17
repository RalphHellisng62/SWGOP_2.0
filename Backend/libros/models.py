from django.db import models
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


def imagen_path(instance, filename):
    """
    Guarda la imagen en: media/libros/CATEGORIA/NOMBRE.jpg
    Ejemplo: media/libros/700-Bellas-artes/001_Picasso.jpg
    """
    # Limpia el nombre de la categoría para la carpeta
    categoria_folder = instance.categoria.replace(' ', '-')
    return f'libros/{categoria_folder}/{instance.nt}_{instance.titulo[:30].replace(" ", "_")}.jpg'


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
    foto = models.ImageField(
        upload_to=imagen_path,  # ← Guarda en carpeta por categoría automáticamente
        null=True,
        blank=True
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='enInventario')
    registrado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-registrado_en']

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        # 🖼️ COMPRIMIR IMAGEN AUTOMÁTICAMENTE
        if self.foto:
            try:
                img = Image.open(self.foto)
                
                # Convertir a RGB si es PNG con transparencia
                if img.mode in ('RGBA', 'LA', 'P'):
                    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                    rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = rgb_img
                
                # Redimensionar si es muy grande (máx 1200x1200)
                max_size = (1200, 1200)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Guardar como JPG optimizado
                output = BytesIO()
                img.save(output, format='JPEG', quality=95, optimize=True)
                output.seek(0)
                
                # Reemplazar con versión comprimida
                self.foto.file = output
                
            except Exception as e:
                print(f"⚠️ Error comprimiendo imagen: {e}")
        
        self.actualizado_en = timezone.now()
        super().save(*args, **kwargs)