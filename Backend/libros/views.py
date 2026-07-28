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
        logger.info('📨 Datos recibidos para crear libro:')
        logger.info(f'  Data: {request.data}')
        
        # ✅ Leemos la URL recibida en request.data
        foto_url = request.data.get('foto')
        if foto_url:
            logger.info(f'  ✅ URL de foto recibida: {foto_url}')
        else:
            logger.info('  ℹ️ No se envió URL de foto')
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            logger.info('✅ Libro creado exitosamente')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error(f'❌ Errores en creación: {serializer.errors}')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        logger.info(f'📝 Actualizando libro {kwargs.get("pk")}:')
        logger.info(f'  Data: {request.data}')
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            logger.info('✅ Libro actualizado exitosamente')
            return Response(serializer.data)
        else:
            logger.error(f'❌ Errores en actualización: {serializer.errors}')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)