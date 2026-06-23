from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    LoginView, registro, perfil, actualizar_perfil, cambiar_contraseña,
    iniciar_recuperacion, verificar_codigo, cambiar_contraseña_recuperacion
)

urlpatterns = [
    # Login y autenticación
    path('login/', LoginView.as_view(), name='login'),
    path('registro/', registro, name='registro'),
    path('perfil/', perfil, name='perfil'),
    path('perfil/actualizar/', actualizar_perfil, name='actualizar_perfil'),
    path('perfil/cambiar-contraseña/', cambiar_contraseña, name='cambiar_contraseña'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Recuperación de contraseña
    path('recuperacion/iniciar/', iniciar_recuperacion, name='iniciar_recuperacion'),
    path('recuperacion/verificar/', verificar_codigo, name='verificar_codigo'),
    path('recuperacion/cambiar/', cambiar_contraseña_recuperacion, name='cambiar_contraseña_recuperacion'),
]
