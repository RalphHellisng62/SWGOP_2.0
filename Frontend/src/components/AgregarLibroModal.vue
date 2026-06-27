<script setup lang="ts">
import { ref } from 'vue';
import { librosService } from '../services/librosService';
import { ArrowLeftCircleIcon, FolderArrowDownIcon, PhotoIcon } from '@heroicons/vue/24/solid';


const emit = defineEmits<{
  cerrar: [];
  'libro-agregado': [];
}>();

const nt = ref('');
const etiqueta = ref('');
const titulo = ref('');
const autor = ref('');
const categoria = ref('000-Generalidades');
const estado = ref('enInventario');
const ejemplares = ref(1);
const fotoFile = ref<File | null>(null);
const fotoUrl = ref('');
const fotoPreview = ref('');
const cargando = ref(false);
const error = ref('');
const exito = ref(false);
const mostrarDialogUrl = ref(false);

const categorias = [
  '000-Generalidades',
  '300-Ciencias Sociales',
  '400-Lenguas',
  '500-Ciencias naturales y matemáticas',
  '600-Tecnología (Ciencia aplicadas)',
  '700-Bellas artes',
  '800-Literatura y retórica',
  '900-Geografía e Historia',
  'Préstamo a domicilio',
];

const validarFormato = (url: string): boolean => {
  const extension = url.toLowerCase().split('?')[0].split('.').pop();
  return extension === 'png' || extension === 'jpg' || extension === 'jpeg';
};

const handleFotoArchivo = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  
  if (!file) return;
  
  error.value = '';
  
  if (!['image/png', 'image/jpeg'].includes(file.type)) {
    error.value = 'Solo PNG y JPG permitidos';
    return;
  }
  
  fotoFile.value = file;
  fotoUrl.value = '';
  const reader = new FileReader();
  reader.onload = (e) => {
    fotoPreview.value = e.target?.result as string;
  };
  reader.readAsDataURL(file);
};


const cerrarDialogUrl = () => {
  mostrarDialogUrl.value = false;
};

const handleFotoUrl = () => {
  if (!fotoUrl.value) {
    error.value = 'Ingresa una URL';
    return;
  }
  
  if (!validarFormato(fotoUrl.value)) {
    error.value = 'Solo PNG y JPG permitidos';
    return;
  }
  
  error.value = '';
  fotoFile.value = null;
  fotoPreview.value = fotoUrl.value;
  cerrarDialogUrl();
};

const agregarLibro = async () => {
  error.value = '';
  
  if (!nt.value || !titulo.value || !autor.value) {
    error.value = 'Completa los campos obligatorios (NT, Título, Autor)';
    return;
  }
  
  if (ejemplares.value < 1) {
    error.value = 'La cantidad debe ser mayor a 0';
    return;
  }
  
  cargando.value = true;
  
  try {
    
    // Si hay foto (archivo o URL), usar FormData
    if (fotoFile.value instanceof File || fotoUrl.value) {
      const formData = new FormData();
      formData.append('nt', nt.value);
      formData.append('etiqueta', etiqueta.value);
      formData.append('titulo', titulo.value);
      formData.append('autor', autor.value);
      formData.append('categoria', categoria.value);
      formData.append('estado', estado.value);
      formData.append('ejemplares', String(ejemplares.value));
      // DEBUG: Ver qué está en FormData
  console.log('📋 FormData entries:');
  for (let [key, value] of formData.entries()) {
    console.log(`  ${key}:`, value);
  }
  
      

      if (fotoFile.value instanceof File) {
        formData.append('foto', fotoFile.value);
        console.log('📸 Agregando foto al FormData:', fotoFile.value.name);
      } else if (fotoUrl.value) {
        formData.append('foto_url', fotoUrl.value);
      }
      
      await librosService.crearLibro(formData);
    } else {
      // Sin foto, enviar como JSON
      const datos = {
        nt: nt.value,
        etiqueta: etiqueta.value,
        titulo: titulo.value,
        autor: autor.value,
        categoria: categoria.value,
        estado: estado.value,
        ejemplares: Number(ejemplares.value),
      };
      
      console.log('📤 Enviando JSON:', datos);
      await librosService.crearLibro(datos);
    }
    
    exito.value = true;
    setTimeout(() => {
      emit('libro-agregado');
      cerrar();
    }, 1500);
  } catch (err: any) {
    console.error('❌ Error al agregar libro:', err.response?.data);
    error.value = err.response?.data?.detail || JSON.stringify(err.response?.data) || 'Error al agregar libro';
  } finally {
    cargando.value = false;
  }
};

const cerrar = () => {
  nt.value = '';
  etiqueta.value = '';
  titulo.value = '';
  autor.value = '';
  categoria.value = '000-Generalidades';
  estado.value = 'enInventario';
  ejemplares.value = 1;
  fotoFile.value = null;
  fotoUrl.value = '';
  fotoPreview.value = '';
  error.value = '';
  exito.value = false;
  mostrarDialogUrl.value = false;
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
    <div class="bg-white rounded-3xl w-full max-w-4xl max-h-[95vh] overflow-y-auto shadow-2xl">
      
      <!-- Header -->
      <div class="backdrop-blur-sm bg-[#344F37] px-8 py-6 sticky top-0 border-b border-[#344F37]">
        <h2 class="text-4xl font-bold text-white">Registrar un nuevo libro</h2>
      </div>

      <!-- Contenido -->
      <div class="p-8">
        <h1 class="text-center text-2xl text-black font-bold mb-6">Conteste el formulario con los datos del libro</h1>

        <!-- Mensaje de error -->
        <div v-if="error" class="bg-red-100 border border-red-700 text-[#F27B35] px-4 py-3 rounded mb-4 text-sm">
          {{ error }}
        </div>

        <!-- Mensaje de éxito (Toast) -->
        <transition name="fade">
          <div v-if="exito" class="fixed bottom-8 right-8 bg-green-100 border border-green-400 text-[#344F37] px-8 py-8 rounded-3xl shadow-lg flex items-center gap-3 z-50">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
            <div>
              <p class="font-semibold">Registro del libro</p>
              <p class="text-sm">exitosamente</p>
            </div>
          </div>
        </transition>

        <!-- Formulario -->
        <form @submit.prevent="agregarLibro" class="grid grid-cols-2 gap-6 mb-6">
          
          <!-- Columna izquierda -->
          <div class="space-y-4">
            <!-- NT -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">NT</label>
              <input 
                v-model="nt"
                type="text"
                placeholder="Ejemplo: 729023"
                class="w-full px-4 py-2 bg-gray-100 text-gray-800 placeholder-gray-500 rounded focus:outline-none focus:ring-2 focus:ring-[#F27B35]"
              />
            </div>

            <!-- Etiqueta -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Datos de etiqueta</label>
              <input 
                v-model="etiqueta"
                type="text"
                placeholder="Ejemplo: 839.73-L37-M542"
                class="w-full px-4 py-2 bg-gray-100 text-gray-800 placeholder-gray-500 rounded focus:outline-none focus:ring-2 focus:ring-[#F27B35]"
              />
            </div>

            <!-- Título -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Título</label>
              <input 
                v-model="titulo"
                type="text"
                placeholder="Ejemplo: Las grandes aventuras"
                class="w-full px-4 py-2 bg-gray-100 text-gray-800 placeholder-gray-500 rounded focus:outline-none focus:ring-2 focus:ring-[#F27B35]"
              />
            </div>

            <!-- Autor -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Autor</label>
              <input 
                v-model="autor"
                type="text"
                placeholder="Ejemplo: Stefan Zweig"
                class="w-full px-4 py-2 bg-gray-100 text-gray-800 placeholder-gray-500 rounded focus:outline-none focus:ring-2 focus:ring-[#F27B35]"
              />
            </div>

            <!-- Categoría -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Categoría</label>
              <select 
                v-model="categoria"
                class="w-full px-4 py-2 bg-white border border-gray-300 text-gray-800 rounded focus:outline-none focus:ring-2 focus:ring-[#F27B35]"
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
                  class="w-full px-4 py-2 bg-white border border-gray-300 text-gray-800 rounded focus:outline-none focus:ring-2 focus:ring-[#F27B35]"
                >
                  <option value="enInventario">En inventario</option>
                  <option value="prestado">Prestado</option>
                  <option value="sinExistencias">Sin existencias</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Ejemplares</label>
                <div class="flex items-center gap-2">
                  <button 
                    type="button"
                    @click="decrementar"
                    class="bg-[#F27B35] hover:bg-[#F2B035] text-white w-8 h-8 rounded flex items-center justify-center font-bold"
                  >
                    −
                  </button>
                  <span class="text-center w-8 text-gray-800 font-semibold">{{ ejemplares }}</span>
                  <button 
                    type="button"
                    @click="incrementar"
                    class="bg-[#F27B35] hover:bg-[#F2B035] text-white w-8 h-8 rounded flex items-center justify-center font-bold"
                  >
                    +
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Columna derecha - Foto -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Foto del libro</label>
            <div class="border-2 border-dashed border-[#8B3A5C] rounded-lg p-0 h-130 flex flex-col items-center justify-center bg-white">
              
              <!-- Preview de foto -->
              <img v-if="fotoPreview" :src="fotoPreview" alt="Preview" class="w-full h-full max-h-115 object-contain mb-4" />
              
              <!-- Sin foto -->
              <div v-else class="text-center">
              <div class="flex justify-center items-center w-full">
              <photo-icon class="icono" />
              </div>
                <p class="text-gray-700 font-semibold mb-1">Suba la imagen del libro</p>
                <p class="text-gray-500 text-sm mb-3">Acepta formato: PNG, JPG</p>
              </div>

              <!-- Botones de carga -->
              <div class="flex gap-3 justify-center w-full flex-wrap">
                <!-- Cargar desde archivo -->
                <label class="flex items-center gap-2 font-semibold transition cursor-pointer">
                  <FolderArrowDownIcon class="icono" />
                  Explorador
                  <input 
                    type="file"
                    accept="image/png,image/jpeg"
                    @change="handleFotoArchivo"
                    class="hidden"
                  />
                </label>
                <button
                  type="button"
                  @click="mostrarDialogUrl = true"
                  class="flex items-center gap-2 font-semibold px-4 py-2 border border-gray-300 rounded hover:bg-gray-100 transition"
                >
                  URL
                </button>
              </div>
            </div>
          </div>

        </form>

        <div v-if="mostrarDialogUrl" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <div class="bg-white rounded-3xl w-full max-w-md p-6 shadow-2xl">
            <h3 class="text-xl font-semibold mb-4">Ingresar URL de la imagen</h3>
            <input
              v-model="fotoUrl"
              type="text"
              placeholder="https://example.com/imagen.jpg"
              class="w-full px-4 py-3 border border-gray-300 rounded mb-4 focus:outline-none focus:ring-2 focus:ring-[#F27B35]"
            />
            <div class="flex justify-end gap-3">
              <button
                type="button"
                @click="cerrarDialogUrl"
                class="px-5 py-2 border border-gray-300 rounded hover:bg-gray-100 transition"
              >
                Cancelar
              </button>
              <button
                type="button"
                @click="handleFotoUrl"
                class="px-5 py-2 bg-[#344F37] text-white rounded hover:bg-[#98BF45] transition"
              >
                Aceptar
              </button>
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
            class="flex items-center gap-2 text-[#344F37] font-semibold hover:text-[#98BF45] transition underline"
          >
          <arrow-left-circle-icon class="icono" />
          Regresar
          </button>
          <div class="flex gap-4">
            <button 
              @click="cerrar"
              type="button"
              class="px-6 py-2 bg-[#D9298A] font-semibold rounded hover:bg-[#690035] transition text-white"
            >
              Cancelar
            </button>
            <button 
              @click="agregarLibro"
              :disabled="cargando"
              type="button"
              class="px-6 py-2 bg-[#344F37] hover:bg-[#98BF45] text-white font-semibold rounded transition disabled:opacity-50"
            >
              {{ cargando ? 'Agregando...' : 'Agregar' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.9s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>