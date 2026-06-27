from rest_framework import serializers
from .models import Libro

class LibroSerializer(serializers.ModelSerializer):
    foto_url = serializers.SerializerMethodField()
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)

    class Meta:
        model = Libro
        fields = [
            'id', 'nt', 'etiqueta', 'titulo', 'autor', 
            'categoria', 'ejemplares', 'foto', 'foto_url', 'estado', 
            'estado_display', 'registrado_en'
        ]

    def get_foto_url(self, obj):
        """Devuelve la URL completa de la foto"""
        if obj.foto:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.foto.url)
            return obj.foto.url
        return None