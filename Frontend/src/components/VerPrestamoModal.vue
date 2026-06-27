<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { prestamosService } from '../services/prestamosService';


interface PrestamoDetalle {
  id: number;
  libro: number;
  libro_nt: string;
  libro_titulo: string;
  libro_autor: string;
  libro_etiqueta: string;
  libro_foto?: string;
  nombre_lector: string;
  fecha_prestamo: string;
  fecha_devolucion: string;
  estado: string;
}

const props = defineProps<{
  prestamoId: number;
}>();

const emit = defineEmits<{
  cerrar: [];
  'actualizado': [];
}>();

const prestamo = ref<PrestamoDetalle | null>(null);
const cargando = ref(true);

const error = ref('');

onMounted(async () => {
  await cargarPrestamo();
});

const cargarPrestamo = async () => {
  cargando.value = true;
  try {
    const response = await prestamosService.obtenerPrestamo(props.prestamoId);
    prestamo.value = response.data;
  } catch (err) {
    console.error('Error al cargar préstamo:', err);
    error.value = 'Error al cargar el préstamo';
  } finally {
    cargando.value = false;
  }
};

const formatearFecha = (fecha: string) => {
  const date = new Date(fecha);
  return date.toLocaleDateString('es-ES', { day: 'numeric', month: 'long', year: 'numeric' });
};

const obtenerUrlFoto = (foto?: string) => {
  if (!foto) return '';
  if (foto.startsWith('http')) return foto;
  return `http://localhost:8000${foto}`;
};





const cerrar = () => {
  emit('cerrar');
};
</script>

<template>
  <!-- Backdrop -->
  <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
    <!-- Modal -->
    <div v-if="!cargando && prestamo" class="bg-white rounded-3xl w-full max-w-4xl max-h-[110vh] overflow-y-auto shadow-2xl">
      
      <!-- Header -->
      <div class="bg-[#344F37] px-8 py-6 border-b border-gray-200">
        <h2 class="text-2xl font-bold text-white">Información del préstamo</h2>
        <p class="text-gray-200 text-sm mt-1">Detalles completos del registro</p>
      </div>

      <!-- Contenido -->
      <div class="p-8 max-h-[80vh] overflow-y-auto">
        
        <!-- Mensaje de error -->
        <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4 text-sm">
          {{ error }}
        </div>

        <!-- Formulario -->
        <div class="grid grid-cols-2 gap-6">
          
          <!-- Columna izquierda -->
          <div class="space-y-4">
            
            <!-- NT del libro -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">NT del Libro</label>
              <input 
                :value="prestamo.libro_nt"
                type="text"
                disabled
                class="w-full px-4 py-2 bg-gray-100 text-gray-800 rounded cursor-not-allowed"
              />
            </div>

            <!-- Datos de etiqueta -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Datos de etiqueta</label>
              <input 
                :value="prestamo.libro_etiqueta"
                type="text"
                disabled
                class="w-full px-4 py-2 bg-gray-100 text-gray-800 rounded cursor-not-allowed"
              />
            </div>

            <!-- Título -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Título</label>
              <input 
                :value="prestamo.libro_titulo"
                type="text"
                disabled
                class="w-full px-4 py-2 bg-gray-100 text-gray-800 rounded cursor-not-allowed"
              />
            </div>

            <!-- Autor -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Autor</label>
              <input 
                :value="prestamo.libro_autor"
                type="text"
                disabled
                class="w-full px-4 py-2 bg-gray-100 text-gray-800 rounded cursor-not-allowed"
              />
            </div>

            <!-- Nombre del lector -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Nombre del lector</label>
              <input 
                :value="prestamo.nombre_lector"
                type="text"
                disabled
                class="w-full px-4 py-2 bg-gray-100 text-gray-800 rounded cursor-not-allowed"
              />
            </div>

            <!-- Fechas -->
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Fecha de préstamo</label>
                <input 
                  :value="formatearFecha(prestamo.fecha_prestamo)"
                  type="text"
                  disabled
                  class="w-full px-4 py-2 bg-gray-100 text-gray-800 rounded cursor-not-allowed"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Fecha de devolución</label>
                <input 
                  :value="formatearFecha(prestamo.fecha_devolucion)"
                  type="text"
                  disabled
                  class="w-full px-4 py-2 bg-gray-100 text-gray-800 rounded cursor-not-allowed"
                />
              </div>
            </div>


           

          </div>

          <!-- Columna derecha - Foto del libro -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Foto del libro</label>
            <div class="border-2 border-dashed border-[#8B3A5C] rounded-lg p-0 h-130 flex flex-col items-center justify-center bg-white">
              
              <!-- Foto -->
              <img v-if="obtenerUrlFoto(prestamo.libro_foto)" :src="obtenerUrlFoto(prestamo.libro_foto)" alt="Libro" class="w-full h-full object-contain" />
              
              <!-- Sin foto -->
              <div v-else class="text-center">
                <div class="w-16 h-16 bg-[#8B3A5C] rounded-lg flex items-center justify-center mx-auto mb-3">
                  <svg class="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M5 3a2 2 0 012-2h6a2 2 0 012 2v2H5V3z"/>
                    <path fill-rule="evenodd" d="M5 5h10a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2zm0 2v9h10V7H5z"/>
                  </svg>
                </div>
                <p class="text-gray-700 font-semibold mb-1">Sin foto</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Botones de acción -->

        <div class="mt-6 pt-6">

  <!-- Línea decorativa -->
  <div class="relative mb-6">
    <div class="min-h-0.5 bg-[#344F37] relative">

      <!-- Punto izquierdo -->
      <div
        class="absolute left-0 top-1/2 -translate-x-1/2 -translate-y-1/2
              w-2 h-2 rounded-full bg-[#344F37]">
      </div>

      <!-- Punto derecho -->
      <div
        class="absolute right-0 top-1/2 translate-x-1/2 -translate-y-1/2
              w-2 h-2 rounded-full bg-[#344F37]">
      </div>

    </div>
  </div>

  <!-- Contenido -->
  <div class="flex justify-between items-center">
    <button
      @click="cerrar"
      class="flex items-center gap-2 text-[#344F37] font-semibold hover:text-[#98BF45] transition"
    >
      ← Regresar
    </button>

    <div class="flex gap-4">
      <!-- botones -->
    </div>
  </div>

</div>

      </div>
    </div>

    <!-- Cargando -->
    <div v-else class="bg-white rounded-lg p-8 text-center">
      <p class="text-gray-600">Cargando información del préstamo...</p>
    </div>
  </div>
</template>