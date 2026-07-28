<script setup lang="ts">
import { ref, watch } from 'vue';
import { prestamosService } from '../services/prestamosService';
import { librosService } from '../services/librosService';
import { BookmarkIcon, ArrowLeftCircleIcon } from '@heroicons/vue/24/solid';

const emit = defineEmits<{
  cerrar: [];
  'prestamo-registrado': [];
}>();

const nt = ref('');
const nombreLector = ref('');
const fechaPrestamo = ref('');
const fechaDevolucion = ref('');

// Datos del libro que se completarán automáticamente
const libroId = ref<number | null>(null);
const etiqueta = ref('');
const titulo = ref('');
const autor = ref('');
const categoria = ref('');
const foto = ref('');

const cargando = ref(false);
const cargandoLibro = ref(false);
const error = ref('');
const exito = ref(false);
const libroEncontrado = ref(false);

// Función para buscar el libro por NT
const buscarLibroPorNT = async (ntValue: string) => {
  if (!ntValue || ntValue.trim().length === 0) {
    libroEncontrado.value = false;
    libroId.value = null;
    etiqueta.value = '';
    titulo.value = '';
    autor.value = '';
    categoria.value = '';
    foto.value = '';
    return;
  }

  cargandoLibro.value = true;
  try {
    const response = await prestamosService.obtenerLibrosDisponibles();
    const librosData = response.data.results || response.data;
    
    // Buscar el libro por NT
    const libroEncontradoData = librosData.find((libro: any) => libro.nt === ntValue.trim());
    
    if (libroEncontradoData) {
      libroId.value = libroEncontradoData.id;
      etiqueta.value = libroEncontradoData.etiqueta || '';
      titulo.value = libroEncontradoData.titulo || '';
      autor.value = libroEncontradoData.autor || '';
      categoria.value = libroEncontradoData.categoria || '';
      foto.value = libroEncontradoData.foto || '';
      libroEncontrado.value = true;
      error.value = '';
    } else {
      libroEncontrado.value = false;
      libroId.value = null;
      etiqueta.value = '';
      titulo.value = '';
      autor.value = '';
      categoria.value = '';
      foto.value = '';
      error.value = 'No se encontró el libro con el Número de Topografía (NT) proporcionado, por favor registre el libro o verifique que el NT sea correcto.';
    }
  } catch (err) {
    console.error('Error al buscar libro:', err);
    error.value = 'Error al buscar el libro';
    libroEncontrado.value = false;
  } finally {
    cargandoLibro.value = false;
  }
};

// Watch para buscar automáticamente cuando cambia el NT
watch(nt, (newValue) => {
  buscarLibroPorNT(newValue);
});

const registrarPrestamo = async () => {
  error.value = '';

  if (!libroId.value) {
    error.value = 'Debe seleccionar un libro válido';
    return;
  }

  if (!nombreLector.value.trim()) {
    error.value = 'Ingrese el nombre del lector';
    return;
  }

  if (!fechaPrestamo.value) {
    error.value = 'Ingrese la fecha de préstamo';
    return;
  }

  if (!fechaDevolucion.value) {
    error.value = 'Ingrese la fecha de devolución';
    return;
  }

  if (new Date(fechaDevolucion.value) <= new Date(fechaPrestamo.value)) {
    error.value = 'La fecha de devolución debe ser posterior a la de préstamo';
    return;
  }

  cargando.value = true;

  try {
    const ajustarFecha = (fecha: string) => {
      const date = new Date(fecha + 'T12:00:00');
      return date.toISOString().split('T')[0];
    };

    const datos = {
      libro: libroId.value,
      nombre_lector: nombreLector.value,
      fecha_prestamo: ajustarFecha(fechaPrestamo.value),
      fecha_devolucion: ajustarFecha(fechaDevolucion.value),
    };

    await prestamosService.registrarPrestamo(datos);
    
    // Cambiar estado del libro a "prestado"
    await librosService.cambiarEstado(libroId.value, 'prestado');

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
  nt.value = '';
  nombreLector.value = '';
  fechaPrestamo.value = '';
  fechaDevolucion.value = '';
  libroId.value = null;
  etiqueta.value = '';
  titulo.value = '';
  autor.value = '';
  categoria.value = '';
  foto.value = '';
  error.value = '';
  exito.value = false;
  libroEncontrado.value = false;
  emit('cerrar');
};

const obtenerFechaHoy = () => {
  const hoy = new Date();
  return hoy.toISOString().split('T')[0];
};

const obtenerFechaMinima = () => {
  const hoy = new Date();
  hoy.setDate(hoy.getDate() + 1);
  return hoy.toISOString().split('T')[0];
};
</script>

<template>
  <Transition name="modal-prestamo" appear>
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-black/25 backdrop-blur-xs flex items-center justify-center z-50 p-4">
      
      <!-- Container Modal con Flexbox Layout y Recorte Estricto -->
      <div class="bg-white rounded-3xl w-full max-w-4xl max-h-[90vh] flex flex-col overflow-hidden shadow-2xl relative">
        
        <!-- Header Verde Fijo -->
        <div class="bg-[#344F37] px-8 py-5 flex flex-col gap-1 shrink-0">
          <h2 class="text-3xl font-bold text-white">Registrar préstamo</h2>
          <p class="text-sm font-normal text-gray-300">Ingrese el Número de Topografía (NT) del libro y automáticamente se completarán los datos</p>
        </div>

        <!-- Cuerpo Con Scroll Exclusivo -->
        <div class="p-8 overflow-y-auto flex-1">
          
          <!-- Mensaje de error -->
          <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4 text-sm">
            {{ error }}
          </div>

          <!-- Mensaje de éxito (Toast) -->
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
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            <!-- Columna izquierda -->
            <div class="space-y-4">
              
              <!-- NT del libro -->
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Número de Topografía (NT)</label>
                <div class="relative">
                  <input 
                    v-model="nt"
                    type="text"
                    placeholder="Ejemplo: 729023"
                    class="w-full px-4 py-2 bg-gray-200 text-gray-800 placeholder-gray-500 rounded transition-all duration-300 ease-out hover:shadow-md focus:outline-none focus:ring-2 focus:ring-[#8B3A5C]"
                  />
                  <div v-if="cargandoLibro" class="absolute right-3 top-2.5">
                    <svg class="w-5 h-5 animate-spin text-[#D9298A]" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
                    </svg>
                  </div>
                </div>
              </div>

              <!-- Datos de etiqueta (auto) -->
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Clave de ubicación en el estante (signatura topográfica)</label>
                <input 
                  v-model="etiqueta"
                  type="text"
                  disabled
                  :class="[
                    'w-full px-4 py-2 rounded text-gray-800 cursor-not-allowed transition-all duration-300 ease-out hover:shadow-md',
                    libroEncontrado ? 'bg-gray-200 border border-gray-300' : 'bg-gray-100'
                  ]"
                />
              </div>

              <!-- Título (auto) -->
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Título</label>
                <input 
                  v-model="titulo"
                  type="text"
                  disabled
                  :class="[
                    'w-full px-4 py-2 rounded text-gray-800 cursor-not-allowed transition-all duration-300 ease-out hover:shadow-md',
                    libroEncontrado ? 'bg-gray-200 border border-gray-300' : 'bg-gray-100'
                  ]"
                />
              </div>

              <!-- Autor (auto) -->
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Autor</label>
                <input 
                  v-model="autor"
                  type="text"
                  disabled
                  :class="[
                    'w-full px-4 py-2 rounded text-gray-800 cursor-not-allowed transition-all duration-300 ease-out hover:shadow-md',
                    libroEncontrado ? 'bg-gray-200 border border-gray-300' : 'bg-gray-100'
                  ]"
                />
              </div>

              <!-- Categoría (auto) -->
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Categoría</label>
                <input 
                  v-model="categoria"
                  type="text"
                  disabled
                  :class="[
                    'w-full px-4 py-2 rounded text-gray-800 cursor-not-allowed transition-all duration-300 ease-out hover:shadow-md',
                    libroEncontrado ? 'bg-gray-200 border border-gray-300' : 'bg-gray-100'
                  ]"
                />
              </div>

              <!-- Nombre del lector -->
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Nombre del lector</label>
                <input 
                  v-model="nombreLector"
                  type="text"
                  placeholder="Ejemplo: José Luis Hernández"
                  class="w-full px-4 py-2 bg-gray-200 text-gray-800 placeholder-gray-500 rounded transition-all duration-300 ease-out hover:shadow-md focus:outline-none focus:ring-2 focus:ring-[#D9298A]"
                />
              </div>

              <!-- Fechas -->
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Fecha de préstamo</label>
                  <input 
                    v-model="fechaPrestamo"
                    type="date"
                    :max="obtenerFechaHoy()"
                    class="w-full px-4 py-2 bg-gray-200 text-gray-800 rounded transition-all duration-300 ease-out hover:shadow-md focus:outline-none focus:ring-2 focus:ring-[#D9298A]"
                  />
                </div>
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Fecha de devolución</label>
                  <input 
                    v-model="fechaDevolucion"
                    type="date"
                    :min="obtenerFechaMinima()"
                    class="w-full px-4 py-2 bg-gray-200 text-gray-800 rounded  transition-all duration-300 ease-out hover:shadow-md focus:outline-none focus:ring-2 focus:ring-[#D9298A]"
                  />
                </div>
              </div>
            </div>

            <!-- Columna derecha - Foto del libro -->
            <div class="flex flex-col">
              <label class="block text-sm font-semibold text-gray-700 mb-2">Foto del libro</label>
              <div class="border-2 border-dashed border-[#D9298A] rounded-3xl p-4 h-130 flex flex-col items-center justify-center bg-white transition-all duration-300 hover:scale-105 overflow-hidden">
                
                <!-- Foto -->
                <img 
                  v-if="foto" 
                  :src="foto" 
                  alt="Libro" 
                  class="w-full h-full max-h-115 object-contain rounded-xl" 
                />
                
                <!-- Sin foto -->
                <div v-else class="text-center">
                  <div class="w-16 h-16 bg-[#D9298A] rounded-lg flex items-center justify-center mx-auto mb-3">
                    <BookmarkIcon class="w-8 h-8 text-white"/>
                  </div>
                  <p class="text-gray-700 font-semibold mb-1">Foto del libro</p>
                  <p class="text-gray-500 text-sm">Se cargará automáticamente</p>
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

          <!-- Botones de acción -->
          <div class="flex justify-between items-center">
            <button 
              @click="cerrar"
              class="flex items-center gap-2 text-[#344F37] font-semibold hover:text-[#98BF45] transition-all duration-300 ease-out hover:scale-105 active:scale-95 underline"
            >
              <ArrowLeftCircleIcon class="w-5 h-5" />
              Regresar
            </button>
            <div class="flex gap-4">
              <button 
                @click="cerrar"
                type="button"
                class="px-6 py-2 bg-[#D9298A] hover:bg-[#690035] text-white font-bold rounded-4xl transition-all duration-300 ease-out hover:scale-105 active:scale-95"
              >
                Cancelar
              </button>
              <button 
                @click="registrarPrestamo"
                :disabled="cargando || !libroEncontrado"
                type="button"
                class="px-6 py-2 bg-[#344F37] hover:bg-[#98BF45] disabled:opacity-50 disabled:hover:bg-[#344F37] disabled:hover:scale-100 text-white font-bold rounded-4xl transition-all duration-300 ease-out hover:scale-105 active:scale-95"
              >
                {{ cargando ? 'Registrando...' : 'Agregar' }}
              </button>
            </div>
          </div>

        </div>
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

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>