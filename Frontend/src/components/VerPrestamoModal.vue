<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { prestamosService } from '../services/prestamosService';

interface PrestamoDetalle {
  id: number;
  libro: number;
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
const guardando = ref(false);
const error = ref('');

// Estado editable
const estadoEditando = ref(false);
const nuevoEstado = ref('');

const estados = ['vigente', 'vencido', 'devuelto'];

onMounted(async () => {
  await cargarPrestamo();
});

const cargarPrestamo = async () => {
  cargando.value = true;
  try {
    const response = await prestamosService.obtenerPrestamo(props.prestamoId);
    prestamo.value = response.data;
    nuevoEstado.value = prestamo.value?.estado || '';
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

const getEstadoColor = (estado: string) => {
  switch (estado) {
    case 'vigente':
      return 'text-green-600 bg-green-50';
    case 'vencido':
      return 'text-red-600 bg-red-50';
    case 'devuelto':
      return 'text-yellow-600 bg-yellow-50';
    default:
      return 'text-gray-600 bg-gray-50';
  }
};

const getEstadoLabel = (estado: string) => {
  switch (estado) {
    case 'vigente':
      return 'Vigente';
    case 'vencido':
      return 'Vencido';
    case 'devuelto':
      return 'Devuelto';
    default:
      return estado;
  }
};

const actualizarEstado = async () => {
  if (!prestamo.value || !nuevoEstado.value) return;

  guardando.value = true;
  try {
    await prestamosService.actualizarPrestamo(props.prestamoId, {
      estado: nuevoEstado.value
    });
    
    prestamo.value.estado = nuevoEstado.value;
    estadoEditando.value = false;
    emit('actualizado');
  } catch (err) {
    console.error('Error al actualizar:', err);
    error.value = 'Error al actualizar el estado';
  } finally {
    guardando.value = false;
  }
};

const marcarDevuelto = async () => {
  if (!prestamo.value) return;

  guardando.value = true;
  try {
    await prestamosService.marcarPrestamoDevuelto(props.prestamoId);
    prestamo.value.estado = 'devuelto';
    emit('actualizado');
  } catch (err) {
    console.error('Error:', err);
    error.value = 'Error al marcar como devuelto';
  } finally {
    guardando.value = false;
  }
};

const cerrar = () => {
  emit('cerrar');
};
</script>

<template>
  <!-- Backdrop -->
  <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
    <!-- Modal -->
    <div v-if="!cargando && prestamo" class="bg-white rounded-lg w-full max-w-3xl shadow-2xl">
      
      <!-- Header -->
      <div class="bg-white px-8 py-6 border-b border-gray-200">
        <h2 class="text-2xl font-bold text-gray-800">Información del préstamo</h2>
        <p class="text-gray-600 text-sm mt-1">Detalles completos del registro</p>
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
              <label class="block text-sm font-semibold text-gray-700 mb-2">ID del Libro</label>
              <input 
                :value="prestamo.libro"
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

            <!-- Estado -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Estado</label>
              <div v-if="!estadoEditando" class="flex items-center justify-between">
                <span :class="['px-4 py-2 rounded font-semibold', getEstadoColor(prestamo.estado)]">
                  {{ getEstadoLabel(prestamo.estado) }}
                </span>
                <button
                  @click="estadoEditando = true"
                  class="text-[#8B3A5C] hover:text-[#6D2D46] font-semibold text-sm transition"
                >
                  Cambiar
                </button>
              </div>
              <div v-else class="flex gap-2">
                <select 
                  v-model="nuevoEstado"
                  class="flex-1 px-4 py-2 bg-white border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[#8B3A5C]"
                >
                  <option v-for="est in estados" :key="est" :value="est">
                    {{ getEstadoLabel(est) }}
                  </option>
                </select>
                <button
                  @click="actualizarEstado"
                  :disabled="guardando"
                  class="px-4 py-2 bg-[#8B3A5C] hover:bg-[#6D2D46] text-white rounded transition disabled:opacity-50"
                >
                  ✓
                </button>
                <button
                  @click="estadoEditando = false"
                  class="px-4 py-2 bg-gray-300 hover:bg-gray-400 text-gray-700 rounded transition"
                >
                  ✕
                </button>
              </div>
            </div>
          </div>

          <!-- Columna derecha - Foto del libro -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Foto del libro</label>
            <div class="border-2 border-dashed border-[#8B3A5C] rounded-lg p-6 h-80 flex flex-col items-center justify-center bg-white">
              
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
        <div class="flex justify-between items-center pt-6 border-t border-gray-200 mt-6">
          <button 
            @click="cerrar"
            class="flex items-center gap-2 text-[#8B3A5C] font-semibold hover:text-[#6D2D46] transition"
          >
            ← Regresar
          </button>
          <div class="flex gap-4">
            <button 
              v-if="prestamo.estado !== 'devuelto'"
              @click="marcarDevuelto"
              :disabled="guardando"
              type="button"
              class="px-6 py-2 bg-green-600 hover:bg-green-700 text-white font-semibold rounded transition disabled:opacity-50"
            >
              {{ guardando ? 'Guardando...' : 'Marcar devuelto' }}
            </button>
            <button 
              @click="cerrar"
              type="button"
              class="px-6 py-2 border border-gray-300 text-gray-700 font-semibold rounded hover:border-[#8B3A5C] transition"
            >
              Cerrar
            </button>
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
