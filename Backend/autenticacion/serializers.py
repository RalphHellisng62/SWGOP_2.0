from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from .models import PerfilUsuario, RecuperacionContraseña


class UsuarioSerializer(serializers.ModelSerializer):
    foto = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'foto']

    def get_foto(self, obj):
        try:
            if obj.perfil.foto:
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(obj.perfil.foto.url)
                return obj.perfil.foto.url
        except PerfilUsuario.DoesNotExist:
            return None
        return None


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
        return data


class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        PerfilUsuario.objects.create(usuario=user)
        return user


class IniciarRecuperacionSerializer(serializers.Serializer):
    email_o_telefono = serializers.EmailField()
    tipo = serializers.CharField()


class VerificarCodigoSerializer(serializers.Serializer):
    email_o_telefono = serializers.EmailField()
    codigo = serializers.CharField(max_length=6)


class CambiarContraseñaRecuperacionSerializer(serializers.Serializer):
    email_o_telefono = serializers.EmailField()
    codigo = serializers.CharField(max_length=6)
    nueva_contraseña = serializers.CharField()
    confirmar_contraseña = serializers.CharField()