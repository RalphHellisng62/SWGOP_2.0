from rest_framework import serializers
from .models import Libro


class LibroSerializer(serializers.ModelSerializer):
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)

    class Meta:
        model = Libro
        fields = [
            'id', 'nt', 'etiqueta', 'titulo', 'autor', 'foto',
            'categoria', 'ejemplares', 'estado', 
            'estado_display', 'registrado_en'
        ]