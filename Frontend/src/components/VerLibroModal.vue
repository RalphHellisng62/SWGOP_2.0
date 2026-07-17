<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { librosService } from '../services/librosService';
import { FolderArrowDownIcon, ArrowLeftCircleIcon } from '@heroicons/vue/24/solid';

interface Libro {
  id: number;
  nt: string;
  etiqueta: string;
  titulo: string;
  autor: string;
  categoria: string;
  ejemplares: number;
  estado: string;
  estado_display: string;
  foto?: string;
  creado_en?: string;
  actualizado_en?: string;
}

const props = defineProps<{
  libroId: number;
}>();

const emit = defineEmits<{
  cerrar: [];
  'libro-actualizado': [];
}>();

const libro = ref<Libro | null>(null);
const modoEdicion = ref(false);
const cargando = ref(true);
const guardando = ref(false);
const error = ref('');
const exito = ref(false);

// Campos editables
const nt = ref('');
const etiqueta = ref('');
const titulo = ref('');
const autor = ref('');
const categoria = ref('000-Generalidades');
const ejemplares = ref(1);
const estado = ref('enInventario');
const fotoPreview = ref('');
const fotoFile = ref<File | null>(null);

const categorias = [
  '000-Generalidades',
  '300-Ciencias Sociales',
  '400-Lenguas',
  '500-Ciencias naturales y matemáticas',
  '600-Tegnología (Ciencia aplicadas)',
  '700-Bellas artes',
  '800-Literatura y retorica',
  '900-Geográfia e Historia',
  'Prestamo a domicilio',
];

onMounted(async () => {
  await cargarLibro();
});

const cargarLibro = async () => {
  cargando.value = true;
  try {
    const response = await librosService.obtenerLibro(props.libroId);
    console.log('📸 Respuesta API:', response.data);
    console.log('📸 Campo foto:', response.data.foto);
    libro.value = response.data;
    
    // Llenar campos editables
    if (libro.value) {
      const lb = libro.value;
      nt.value = lb.nt;
      etiqueta.value = lb.etiqueta;
      titulo.value = lb.titulo;
      autor.value = lb.autor;
      categoria.value = lb.categoria;
      ejemplares.value = lb.ejemplares;
      estado.value = lb.estado;
      fotoPreview.value = lb.foto || '';
    }
  } catch (err: any) {
    error.value = 'Error al cargar el libro';
  } finally {
    cargando.value = false;
  }
};

const handleFoto = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  
  if (!file) return;
  
  if (!['image/png', 'image/jpeg'].includes(file.type)) {
    error.value = 'Solo PNG y JPG permitidos';
    return;
  }
  
  fotoFile.value = file;
  
  const reader = new FileReader();
  reader.onload = (e) => {
    fotoPreview.value = e.target?.result as string;
  };
  reader.readAsDataURL(file);
};

const guardarCambios = async () => {
  if (!nt.value || !titulo.value || !autor.value) {
    error.value = 'Completa los campos obligatorios';
    console.log('Campos vacios');
    return;
  }
  
  guardando.value = true;
  error.value = '';
  
  try {
    console.log('Intentando guardar..');
  const datosActualizados = {
  nt: nt.value,
  etiqueta: etiqueta.value,
  titulo: titulo.value,
  autor: autor.value,
  categoria: categoria.value,
  ejemplares: ejemplares.value,
  estado: estado.value,
  foto: fotoFile.value
};

await librosService.actualizarLibro(props.libroId, datosActualizados);
    exito.value = true;
    setTimeout(() => {
      modoEdicion.value = false;
      cargarLibro();
      emit('libro-actualizado');
      setTimeout(() => {
        exito.value = false;
      }, 1000);
    }, 1000);
  } catch (err: any) {
    console.log('Error capturado:', err);
    error.value = err.response?.data?.detail || 'Error al guardar cambios';
  } finally {
    guardando.value = false;
  }
};

const cancelarEdicion = () => {
  modoEdicion.value = false;
  // Restaurar valores originales
  if (libro.value) {
    const lb = libro.value;
    nt.value = lb.nt;
    etiqueta.value = lb.etiqueta;
    titulo.value = lb.titulo;
    autor.value = lb.autor;
    categoria.value = lb.categoria;
    ejemplares.value = lb.ejemplares;
    estado.value = lb.estado;
    fotoPreview.value = lb.foto || '';
    fotoFile.value = null;
  }
};

const cerrar = () => {
  emit('cerrar');
};

const incrementar = () => {
  ejemplares.value++;
};

const decrementar = () => {
  if (ejemplares.value > 1) ejemplares.value--;
};
</script>

<template>
  <!-- Backdrop -->
  <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
    <!-- Modal -->
    <div v-if="!cargando && libro" class="bg-white rounded-3xl w-full max-w-4xl max-h-[95vh] overflow-y-auto shadow-2xl">
      
      <!-- Header -->
      <div class="bg-[#344F37] backdrop-blur-sm px-8 py-6 sticky top-0 border-b border-[#344F37] flex justify-between items-center">
        <h2 class="text-3xl font-bold text-white">Información completa del libro</h2>
        
        <!-- Toggle Modo Edición -->
        <div class="flex items-center gap-3 bg-white rounded-lg px-4 py-2">
          <span class="text-sm text-[#344F37]">Modo edición</span>
          <button
            @click="modoEdicion = !modoEdicion"
            :class="[
              'relative inline-flex h-6 w-11 items-center rounded-full transition-colors',
              modoEdicion ? 'bg-[#011956]' : 'bg-[#4EBFD9]'
            ]"
          >
            <span
              :class="[
                'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                modoEdicion ? 'translate-x-6' : 'translate-x-1'
              ]"
            />
          </button>
        </div>
      </div>

      <!-- Contenido -->
      <div class="p-8">
        
        <!-- Mensajes -->
        <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4 text-sm">
          {{ error }}
        </div>

        <transition name="fade">
          <div v-if="exito" class="fixed bottom-8 right-8 bg-green-100 border border-green-400 text-green-700 px-6 py-4 rounded-lg shadow-lg flex items-center gap-3 z-50">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
            <div>
              <p class="font-semibold">Se guardaron los nuevos</p>
              <p class="text-sm">cambios del libro</p>
            </div>
          </div>
        </transition>

        <!-- Información del libro -->
        <div class="grid grid-cols-2 gap-6">
          
          <!-- Columna izquierda - Datos -->
          <div class="space-y-4">
            <!-- NT -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">NT</label>
              <input 
                v-model="nt"
                type="text"
                :disabled="!modoEdicion"
                :class="[
                  'w-full px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-[#011956]',
                  modoEdicion ? 'bg-gray-200 border border-gray-300' : 'bg-gray-100 text-gray-600 cursor-not-allowed'
                ]"
              />
            </div>

            <!-- Etiqueta -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Datos de etiqueta</label>
              <input 
                v-model="etiqueta"
                type="text"
                :disabled="!modoEdicion"
                :class="[
                  'w-full px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-[#011956]',
                  modoEdicion ? 'bg-gray-200 border border-gray-300' : 'bg-gray-100 text-gray-600 cursor-not-allowed'
                ]"
              />
            </div>

            <!-- Título -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Título</label>
              <input 
                v-model="titulo"
                type="text"
                :disabled="!modoEdicion"
                :class="[
                  'w-full px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-[#011956]',
                  modoEdicion ? 'bg-gray-200 border border-gray-300' : 'bg-gray-100 text-gray-600 cursor-not-allowed'
                ]"
              />
            </div>

            <!-- Autor -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Autor</label>
              <input 
                v-model="autor"
                type="text"
                :disabled="!modoEdicion"
                :class="[
                  'w-full px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-[#011956]',
                  modoEdicion ? 'bg-gray-200 border border-gray-300' : 'bg-gray-100 text-gray-600 cursor-not-allowed'
                ]"
              />
            </div>

            <!-- Categoría -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Categoría</label>
              <select 
                v-model="categoria"
                :disabled="!modoEdicion"
                :class="[
                  'w-full px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-[#011956]',
                  modoEdicion ? 'bg-gray-200 border border-gray-300 cursor-pointer' : 'bg-gray-100 text-gray-600 cursor-not-allowed'
                ]"
              >
                <option v-for="cat in categorias" :key="cat" :value="cat">
                  {{ cat }}
                </option>
              </select>
            </div>

            <!-- Estado y Cantidad -->
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Estado</label>
                <select 
                  v-model="estado"
                  :disabled="!modoEdicion"
                  :class="[
                    'w-full px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-[#011956]',
                    modoEdicion ? 'bg-gray-200 border border-gray-300 cursor-pointer' : 'bg-gray-100 text-gray-600 cursor-not-allowed'
                  ]"
                >
                  <option value="enInventario">En inventario</option>
                  <option value="prestado">Prestado</option>
                  <option value="sinExistencias">Sin existencias</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Cantidad en el inventario</label>
                <div v-if="modoEdicion" class="flex items-center gap-2">
                  <button 
                    type="button"
                    @click="decrementar"
                    class="bg-[#011956] hover:bg-[#4EBFD9] text-white text-4xl w-8 h-8 rounded flex items-center justify-center font-bold"
                  >
                    −
                  </button>
                  <span class="text-center w-8 text-gray-800 font-semibold">{{ ejemplares }}</span>
                  <button 
                    type="button"
                    @click="incrementar"
                    class="bg-[#011956] hover:bg-[#4EBFD9] text-white text-4xl w-8 h-8 rounded flex items-center justify-center font-bold"
                  >
                    +
                  </button>
                </div>
                <div v-else class="px-4 py-2 bg-gray-100 text-gray-600 rounded">
                  {{ ejemplares }}
                </div>
              </div>
            </div>
          </div>

          <!-- Columna derecha - Foto -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Foto del libro</label>
            <div 
              :class="[
                'border-2 border-dashed border-[#D9298A] rounded-lg p-0 h-130 flex flex-col items-center justify-center bg-white',
                modoEdicion ? 'border-[#D9298A] bg-white' : 'border-gray-300 bg-gray-50'
              ]"
            >
              <!-- Foto -->
              <img v-if="fotoPreview" :src="fotoPreview" alt="Libro" class="w-full h-full max-h-115 object-contain mb-0" />
              
              <!-- Sin foto -->
              <div v-else class="text-center">
                <div class="w-16 h-16 bg-[#8B3A5C] rounded-lg flex items-center justify-center mx-auto mb-3">
                  <svg class="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M5 3a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2V5a2 2 0 00-2-2H5zm0 2h10v10H5V5z"/>
                  </svg>
                </div>
                <p class="text-gray-700 font-semibold mb-1">Sin imagen</p>
              </div>

              <!-- Botones de carga (solo en modo edición) -->
              <div v-if="modoEdicion" class="flex gap-3 justify-center w-full flex-wrap mt-4">
                <label class="flex items-center gap-2 font-semibold transition cursor-pointer">
                  <FolderArrowDownIcon class="icono" />
                  Explorador
                  <input 
                    type="file"
                    accept="image/png,image/jpeg"
                    @change="handleFoto"
                    class="hidden"
                  />
                </label>

              </div>
            </div>
          </div>

        </div>

        <!-- Línea decorativa -->
  <div class="relative mb-6 mt-10">
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
        <!-- Botones de acción -->
        <div class="flex justify-between items-center">
          <button 
            @click="cerrar"
            class="flex items-center gap-2 text-[#344F37] hover:text-[#98BF45] transition underline"
          >
          <ArrowLeftCircleIcon class="icono" />
          Regresar
          </button>
          
          <div v-if="modoEdicion" class="flex gap-4">
            <button 
              @click="cancelarEdicion"
              type="button"
              class="px-6 py-2 bg-[#D9298A] font-semibold rounded text-white hover:bg-[#690035] transition"
            >
              Cancelar
            </button>
            <button 
              @click="guardarCambios"
              :disabled="guardando"
              type="button"
              class="px-6 py-2 bg-[#344F37] hover:bg-[#98BF45] text-white font-semibold rounded transition disabled:opacity-50"
            >
              {{ guardando ? 'Guardando...' : 'Guardar cambios' }}
            </button>
          </div>
        </div>

      </div>
    </div>

    <!-- Cargando -->
    <div v-else class="bg-white rounded-lg p-8 text-center">
      <p class="text-gray-600">Cargando información del libro...</p>
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