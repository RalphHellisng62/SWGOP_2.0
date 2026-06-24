<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { librosService } from '../services/librosService';

const emit = defineEmits<{
  cerrar: [];
  'prestamo-registrado': [];
}>();

const libros = ref<any[]>([]);
const libroSeleccionado = ref<number | null>(null);
const nombreLector = ref('');
const fechaDevolucion = ref('');
const cargando = ref(false);
const error = ref('');
const exito = ref(false);

onMounted(async () => {
  // Cargar libros disponibles
  try {
    const response = await librosService.obtenerLibros();
    libros.value = response.data.results || response.data;
  } catch (err) {
    console.error('Error al cargar libros:', err);
  }
});

const registrarPrestamo = async () => {
  error.value = '';

  if (!libroSeleccionado.value || !nombreLector.value || !fechaDevolucion.value) {
    error.value = 'Completa todos los campos';
    return;
  }

  cargando.value = true;

  try {
    const datos = {
      libro: libroSeleccionado.value,
      nombre_lector: nombreLector.value,
      fecha_devolucion: fechaDevolucion.value,
    };

    
    await (librosService as any).registrarPrestamo?.(datos);

    exito.value = true;
    setTimeout(() => {
      emit('prestamo-registrado');
      cerrar();
    }, 1500);
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Error al registrar préstamo';
  } finally {
    cargando.value = false;
  }
};

const cerrar = () => {
  libroSeleccionado.value = null;
  nombreLector.value = '';
  fechaDevolucion.value = '';
  error.value = '';
  exito.value = false;
  emit('cerrar');
};

const obtenerFechaMinima = () => {
  const hoy = new Date();
  hoy.setDate(hoy.getDate() + 1);
  return hoy.toISOString().split('T')[0];
};
</script>

<template>
  <!-- Backdrop -->
  <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
    <!-- Modal -->
    <div class="bg-white rounded-lg w-full max-w-md shadow-2xl">
      
      <!-- Header -->
      <div class="bg-[#8B3A5C] px-6 py-6 rounded-t-lg">
        <h2 class="text-2xl font-bold text-white">Registrar nuevo préstamo</h2>
      </div>

      <!-- Contenido -->
      <div class="p-6">
        <!-- Mensaje de error -->
        <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4 text-sm">
          {{ error }}
        </div>

        <!-- Mensaje de éxito -->
        <transition name="fade">
          <div v-if="exito" class="fixed bottom-8 right-8 bg-green-100 border border-green-400 text-green-700 px-6 py-4 rounded-lg shadow-lg flex items-center gap-3 z-50">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
            <div>
              <p class="font-semibold">Préstamo registrado</p>
              <p class="text-sm">exitosamente</p>
            </div>
          </div>
        </transition>

        <!-- Formulario -->
        <form @submit.prevent="registrarPrestamo" class="space-y-4">
          
          <!-- Seleccionar libro -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Libro</label>
            <select 
              v-model.number="libroSeleccionado"
              class="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[#8B3A5C]"
            >
              <option value="">Selecciona un libro...</option>
              <option v-for="libro in libros" :key="libro.id" :value="libro.id">
                {{ libro.titulo }} - {{ libro.autor }}
              </option>
            </select>
          </div>

          <!-- Nombre del lector -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Nombre del lector</label>
            <input 
              v-model="nombreLector"
              type="text"
              placeholder="Ejemplo: Juan Pérez"
              class="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[#8B3A5C]"
            />
          </div>

          <!-- Fecha de devolución -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Fecha de devolución</label>
            <input 
              v-model="fechaDevolucion"
              type="date"
              :min="obtenerFechaMinima()"
              class="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[#8B3A5C]"
            />
          </div>

          <!-- Botones -->
          <div class="flex gap-3 mt-6">
            <button 
              @click="cerrar"
              type="button"
              class="flex-1 px-4 py-2 border border-gray-300 text-gray-700 font-semibold rounded hover:border-[#8B3A5C] transition"
            >
              Cancelar
            </button>
            <button 
              @click="registrarPrestamo"
              :disabled="cargando"
              type="button"
              class="flex-1 px-4 py-2 bg-[#8B3A5C] hover:bg-[#6D2D46] text-white font-semibold rounded transition disabled:opacity-50"
            >
              {{ cargando ? 'Registrando...' : 'Registrar' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
