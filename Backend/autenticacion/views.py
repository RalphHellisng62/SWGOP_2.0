from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .serializers import (
    LoginSerializer, RegistroSerializer, UsuarioSerializer,
    IniciarRecuperacionSerializer, VerificarCodigoSerializer,
    CambiarContraseñaRecuperacionSerializer
)
from .models import PerfilUsuario, RecuperacionContraseña
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


@api_view(['POST'])
def registro(request):
    serializer = RegistroSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'mensaje': 'Usuario creado exitosamente'}, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil(request):
    serializer = UsuarioSerializer(request.user, context={'request': request})
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_perfil(request):
    usuario = request.user
    
    if 'username' in request.data:
        usuario.username = request.data['username']
    if 'email' in request.data:
        usuario.email = request.data['email']
    
    usuario.save()
    
    try:
        perfil = usuario.perfil
    except PerfilUsuario.DoesNotExist:
        perfil = PerfilUsuario.objects.create(usuario=usuario)
    
    if 'foto' in request.FILES:
        perfil.foto = request.FILES['foto']
    
    perfil.save()
    
    serializer = UsuarioSerializer(usuario, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cambiar_contraseña(request):
    usuario = request.user
    contraseña_actual = request.data.get('contraseña_actual')
    contraseña_nueva = request.data.get('contraseña_nueva')
    
    if not usuario.check_password(contraseña_actual):
        return Response({'error': 'Contraseña actual incorrecta'}, status=400)
    
    usuario.set_password(contraseña_nueva)
    usuario.save()
    return Response({'mensaje': 'Contraseña actualizada'})


# ========== RECUPERACIÓN DE CONTRASEÑA ==========

@api_view(['POST'])
def iniciar_recuperacion(request):
    """Inicia proceso de recuperación por email"""
    serializer = IniciarRecuperacionSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    email_o_telefono = serializer.validated_data['email_o_telefono']
    tipo = serializer.validated_data['tipo']
    
    if tipo != 'email':
        return Response(
            {'error': 'Solo recuperación por email es permitida'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    codigo = RecuperacionContraseña.generar_codigo()
    
    usuario = User.objects.filter(email=email_o_telefono).first()
    
    if not usuario:
        return Response(
            {'error': 'No se encontró usuario con ese email'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    RecuperacionContraseña.objects.create(
        usuario=usuario,
        tipo='email',
        codigo=codigo,
        email_o_telefono=email_o_telefono
    )
    
    asunto = 'Código de recuperación de contraseña'
    mensaje = f'Tu código de recuperación es: {codigo}\n\nEste código es válido por 5 minutos.'
    
    try:
        send_mail(
            asunto,
            mensaje,
            settings.DEFAULT_FROM_EMAIL,
            [email_o_telefono],
            fail_silently=False,
        )
        return Response({
            'mensaje': 'Código enviado al email',
            'tipo': 'email'
        })
    except Exception as e:
        return Response(
            {'error': f'Error al enviar email: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def verificar_codigo(request):
    """Verifica si el código es válido"""
    serializer = VerificarCodigoSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    email_o_telefono = serializer.validated_data['email_o_telefono']
    codigo = serializer.validated_data['codigo']
    
    recuperacion = RecuperacionContraseña.objects.filter(
        email_o_telefono=email_o_telefono,
        codigo=codigo,
        usado=False
    ).first()
    
    if not recuperacion:
        return Response(
            {'error': 'Código inválido'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    if not recuperacion.es_valido():
        return Response(
            {'error': 'Código expirado (válido solo 5 minutos)'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    return Response({'mensaje': 'Código válido'})


@api_view(['POST'])
def cambiar_contraseña_recuperacion(request):
    """Cambia la contraseña con código válido"""
    serializer = CambiarContraseñaRecuperacionSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    email_o_telefono = serializer.validated_data['email_o_telefono']
    codigo = serializer.validated_data['codigo']
    nueva_contraseña = serializer.validated_data['nueva_contraseña']
    
    recuperacion = RecuperacionContraseña.objects.filter(
        email_o_telefono=email_o_telefono,
        codigo=codigo,
        usado=False
    ).first()
    
    if not recuperacion:
        return Response(
            {'error': 'Código inválido'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    if not recuperacion.es_valido():
        return Response(
            {'error': 'Código expirado'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    usuario = recuperacion.usuario
    usuario.set_password(nueva_contraseña)
    usuario.save()
    
    recuperacion.usado = True
    recuperacion.save()
    
    return Response({'mensaje': 'Contraseña cambiada exitosamente'})
