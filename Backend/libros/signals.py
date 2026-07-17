from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from .models import Libro
import os


@receiver(pre_delete, sender=Libro)
def eliminar_foto_libro(sender, instance, using, **kwargs):
    """
    Cuando se elimina un libro, elimina su foto de media/
    """
    print(f"\n⚠️  Eliminando libro: {instance.titulo}")
    
    if instance.foto:
        try:
            # Eliminar archivo
            if hasattr(instance.foto, 'path') and os.path.exists(instance.foto.path):
                os.remove(instance.foto.path)
                print(f"✅ Imagen eliminada: {instance.foto.path}")
        except Exception as e:
            print(f"❌ Error al eliminar imagen: {e}")