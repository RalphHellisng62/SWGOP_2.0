from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Libro
from .serializers import LibroSerializer
import logging

logger = logging.getLogger(__name__)


class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def create(self, request, *args, **kwargs):
        logger.info('📨 Datos recibidos:')
        logger.info(f'  Files: {request.FILES.keys()}')
        logger.info(f'  Data keys: {request.data.keys()}')
        
        if 'foto' in request.FILES:
            logger.info(f'  ✅ Foto recibida: {request.FILES["foto"].name}')
        else:
            logger.info('  ❌ No hay foto')
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.info('✅ Libro creado exitosamente')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error(f'❌ Errores: {serializer.errors}')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)