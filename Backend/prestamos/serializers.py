from rest_framework import serializers
from .models import Prestamo
from libros.models import Libro

class PrestamoSerializer(serializers.ModelSerializer):
    libro_nt = serializers.CharField(source='libro.nt', read_only=True)
    libro_titulo = serializers.CharField(source='libro.titulo', read_only=True)
    libro_autor = serializers.CharField(source='libro.autor', read_only=True)
    libro_etiqueta = serializers.CharField(source='libro.etiqueta', read_only=True)
    libro_foto = serializers.SerializerMethodField()

    class Meta:
        model = Prestamo
        fields = [
            'id', 'libro', 'libro_nt', 'libro_titulo', 'libro_autor', 
            'libro_etiqueta', 'libro_foto', 'usuario', 'nombre_lector', 
            'fecha_prestamo', 'fecha_devolucion', 'estado'
        ]

    def get_libro_foto(self, obj):
        if obj.libro.foto:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.libro.foto.url)
            return obj.libro.foto.url
        return None
