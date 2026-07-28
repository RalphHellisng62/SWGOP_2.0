<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { prestamosService } from '../services/prestamosService';
import { ArrowLeftCircleIcon } from '@heroicons/vue/24/solid';

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
  if (!fecha) return '';
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
  <Transition name="modal-prestamo" appear>
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-black/25 backdrop-blur-xs flex items-center justify-center z-50 p-4">
      
      <!-- Container Modal con Scroll Controlado -->
      <div v-if="!cargando && prestamo" class="bg-white rounded-3xl w-full max-w-4xl max-h-[90vh] flex flex-col overflow-hidden shadow-2xl relative">
        
        <!-- Header Verde Fijo -->
        <div class="bg-[#344F37] px-8 py-5 flex flex-col gap-1 shrink-0">
          <h1 class="text-3xl font-bold text-white">Información del préstamo</h1>
          <h2 class="text-sm font-normal text-gray-300">Detalles completos del registro</h2>
        </div>

        <!-- Cuerpo Con Scroll -->
        <div class="p-8 overflow-y-auto flex-1">
          
          <!-- Mensaje de error -->
          <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4 text-sm">
            {{ error }}
          </div>

          <!-- Formulario / Datos -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            <!-- Columna izquierda -->
            <div class="space-y-4">
              
              <!-- NT -->
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Número de Topografía (NT)</label>
                <input 
                  :value="prestamo.libro_nt"
                  type="text"
                  disabled
                  class="w-full px-4 py-2 bg-gray-100 text-gray-800 rounded cursor-not-allowed transition-all duration-300 ease-out hover:shadow-md"
                />
              </div>

              <!-- Signatura Topográfica -->
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Clave de ubicación en el estante (signatura topográfica)</label>
                <input 
                  :value="prestamo.libro_etiqueta"
                  type="text"
                  disabled
                  class="w-full px-4 py-2 bg-gray-100 text-gray-800 rounded cursor-not-allowed transition-all duration-300 ease-out hover:shadow-md"
                />
              </div>

              <!-- Título -->
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Título</label>
                <input 
                  :value="prestamo.libro_titulo"
                  type="text"
                  disabled
                  class="w-full px-4 py-2 bg-gray-100 text-gray-800 rounded cursor-not-allowed transition-all duration-300 ease-out hover:shadow-md"
                />
              </div>

              <!-- Autor -->
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Autor</label>
                <input 
                  :value="prestamo.libro_autor"
                  type="text"
                  disabled
                  class="w-full px-4 py-2 bg-gray-100 text-gray-800 rounded cursor-not-allowed transition-all duration-300 ease-out hover:shadow-md"
                />
              </div>

              <!-- Nombre del lector -->
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Nombre del lector</label>
                <input 
                  :value="prestamo.nombre_lector"
                  type="text"
                  disabled
                  class="w-full px-4 py-2 bg-gray-100 text-gray-800 rounded cursor-not-allowed transition-all duration-300 ease-out hover:shadow-md"
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
                    class="w-full px-4 py-2 bg-gray-100 text-gray-800 rounded cursor-not-allowed transition-all duration-300 ease-out hover:shadow-md"
                  />
                </div>
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Fecha de devolución</label>
                  <input 
                    :value="formatearFecha(prestamo.fecha_devolucion)"
                    type="text"
                    disabled
                    class="w-full px-4 py-2 bg-gray-100 text-gray-800 rounded cursor-not-allowed transition-all duration-300 ease-out hover:shadow-md"
                  />
                </div>
              </div>

            </div>

            <!-- Columna derecha - Foto del libro -->
            <div class="flex flex-col">
              <label class="block text-sm font-semibold text-gray-700 mb-2">Foto del libro</label>
              <div class="border-2 border-dashed border-[#D9298A] rounded-4xl p-0 h-130 flex flex-col items-center justify-center bg-white transition-all duration-300 hover:scale-105 overflow-hidden">
                
                <!-- Foto -->
                <img v-if="obtenerUrlFoto(prestamo.libro_foto)" :src="obtenerUrlFoto(prestamo.libro_foto)" alt="Libro" class="w-full h-full max-h-115 object-contain rounded-xl" />
                
                <!-- Sin foto -->
                <div v-else class="text-center">
                  <div class="w-16 h-16 bg-[#D9298A] rounded-lg flex items-center justify-center mx-auto mb-3">
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

          <!-- Línea decorativa -->
          <div class="relative mb-6 mt-8">
            <div class="min-h-0.5 bg-[#344F37] relative">
              <div class="absolute left-0 top-1/2 -translate-x-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-[#344F37]"></div>
              <div class="absolute right-0 top-1/2 translate-x-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-[#344F37]"></div>
            </div>
          </div>

          <!-- Botón de acción -->
          <div class="flex justify-between items-center">
            <button
              @click="cerrar"
              class="flex items-center gap-2 text-[#344F37] font-semibold hover:text-[#98BF45] transition-all duration-300 ease-out hover:scale-105 active:scale-90 underline"
            >
              <ArrowLeftCircleIcon class="w-5 h-5" />
              Regresar
            </button>
          </div>

        </div>
      </div>

      <!-- Spinner Cargando -->
      <div v-else class="bg-white rounded-2xl p-8 text-center shadow-xl">
        <p class="text-gray-600 font-semibold">Cargando información del préstamo...</p>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.modal-prestamo-enter-active,
.modal-prestamo-leave-active {
  transition: opacity .35s ease;
}

.modal-prestamo-enter-from,
.modal-prestamo-leave-to {
  opacity: 0;
}

.modal-prestamo-enter-active .bg-white,
.modal-prestamo-leave-active .bg-white {
  transition: transform .40s cubic-bezier(.22,1,.36,1), opacity .35s ease;
}

.modal-prestamo-enter-from .bg-white {
  transform: translateY(40px) scale(.95);
  opacity: 0;
}

.modal-prestamo-leave-to .bg-white {
  transform: translateY(30px) scale(.95);
  opacity: 0;
}
</style>