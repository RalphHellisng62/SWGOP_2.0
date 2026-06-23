from rest_framework import serializers
from .models import Libro

class LibroSerializer(serializers.ModelSerializer):
    foto = serializers.SerializerMethodField()

    class Meta:
        model = Libro
        fields = ['id', 'nt', 'etiqueta', 'titulo', 'autor', 'categoria', 'ejemplares', 'foto', 'estado', 'registrado_en']

    def get_foto(self, obj):
        if obj.foto:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.foto.url)
            return obj.foto.url
        return None
