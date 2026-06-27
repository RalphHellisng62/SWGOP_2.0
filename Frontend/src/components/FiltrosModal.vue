<script setup lang="ts">
import { MinusIcon, PlusIcon } from '@heroicons/vue/24/solid';
import { ref } from 'vue';

interface Filtros {
  ordenar: 'A-Z' | 'Z-A';
  estado: string[];
  ejemplares: number;
  categorias: string[];
}

const props = defineProps<{
  modelValue: boolean;
}>();

const emit = defineEmits<{
  'update:modelValue': [value: boolean];
  aplicar: [filtros: Filtros];
}>();

const filtrosGuardados = localStorage.getItem('filtrosInventario');

const filtrosIniciales: Filtros = filtrosGuardados
  ? JSON.parse(filtrosGuardados)
  : {
      ordenar: 'A-Z',
      estado: [],
      ejemplares: 0,
      categorias: [],
    };

const ordenar = ref<'A-Z' | 'Z-A'>(
  filtrosIniciales.ordenar
);

const estadoSeleccionados = ref<string[]>(
  filtrosIniciales.estado
);

const ejemplares = ref(
  filtrosIniciales.ejemplares
);

const categoriasSeleccionadas = ref<string[]>(
  filtrosIniciales.categorias
);

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

const estados = ['enInventario', 'prestado', 'sinExistencias'];
const estadoLabels: Record<string, string> = {
  enInventario: 'En inventario',
  prestado: 'Prestado',
  sinExistencias: 'Sin existencias',
};

const toggleEstado = (estado: string) => {
  const index = estadoSeleccionados.value.indexOf(estado);
  if (index > -1) {
    estadoSeleccionados.value.splice(index, 1);
  } else {
    estadoSeleccionados.value.push(estado);
  }
};

const toggleCategoria = (categoria: string) => {
  const index = categoriasSeleccionadas.value.indexOf(categoria);
  if (index > -1) {
    categoriasSeleccionadas.value.splice(index, 1);
  } else {
    categoriasSeleccionadas.value.push(categoria);
  }
};

const aplicarFiltros = () => {
  emit('aplicar', {
    ordenar: ordenar.value,
    estado: estadoSeleccionados.value,
    ejemplares: ejemplares.value,
    categorias: categoriasSeleccionadas.value,
  });
  cerrar();
};

const cerrar = () => {
  emit('update:modelValue', false);
};

const incrementar = () => {
  ejemplares.value++;
};

const decrementar = () => {
  if (ejemplares.value > 0) ejemplares.value--;
};
</script>

<template>
  <!-- Backdrop -->
  <div v-if="modelValue" class="fixed inset-0 bg-black/50 z-50 flex items-start justify-end">
    <!-- Panel lateral -->
    <div class="bg-white w-full max-w-sm h-full overflow-y-auto shadow-lg rounded-2xl">
      
      <!-- Header -->
      <div class="bg-[#344F37] px-6 py-4 flex justify-between items-center sticky top-0 z-20">
        <h2 class="text-lg font-bold text-white">Búsqueda por filtros</h2>
        <button 
          @click="cerrar"
          class="text-white hover:text-gray-200 transition"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Contenido -->
      <div class="p-6 space-y-6">
        
        <!-- Ordenar por -->
        <div>
          <h3 class="font-semibold text-black mb-3">Ordenar por...</h3>
          <div class="space-y-2">
            <label class="flex items-center cursor-pointer">
              <input 
                v-model="ordenar"
                type="radio"
                value="A-Z"
                class="w-4 h-4 accent-[#011956] cursor-pointer"
              />
              <span class="ml-3 text-gray-700">A-Z</span>
            </label>
            <label class="flex items-center cursor-pointer">
              <input 
                v-model="ordenar"
                type="radio"
                value="Z-A"
                class="w-4 h-4 accent-[#011956] cursor-pointer"
              />
              <span class="ml-3 text-gray-700">Z-A</span>
            </label>
          </div>
           <div class="relative mt-3">
        <div class="min-h-0.5 bg-[#F27B35] rounded-full">
          <div class="absolute left-0 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-[#F27B35]"></div>
          <div class="absolute right-0 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-[#F27B35]"></div>
        </div>
      </div>
        </div>

        <!-- Estado -->
        <div>
          <h3 class="font-semibold text-gray-800 mb-3">Estado</h3>
          <div class="space-y-2">
            <label v-for="estado in estados" :key="estado" class="flex items-center cursor-pointer">
              <input 
                :checked="estadoSeleccionados.includes(estado)"
                @change="toggleEstado(estado)"
                type="checkbox"
                class="w-4 h-4 accent-[#011956] rounded cursor-pointer"
              />
              <span class="ml-3 text-gray-700">{{ estadoLabels[estado] }}</span>
            </label>
          </div>
           <div class="relative mt-3">
        <div class="min-h-0.5 bg-[#F27B35] rounded-full">
          <div class="absolute left-0 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-[#F27B35]"></div>
          <div class="absolute right-0 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-[#F27B35]"></div>
        </div>
      </div>
        </div>

        <!-- Ejemplares -->
        <div>
          <h3 class="font-semibold text-gray-800 mb-3">Ejemplares</h3>
          <div class="flex items-center justify-center gap-8">
            <button 
              @click="decrementar"
              class="bg-[#011956] hover:bg-[#4EBFD9] text-white w-10 h-10 rounded flex items-center justify-center font-bold transition"
            >
            <MinusIcon class="w-5 h-5 text-white" />
            </button>
            <span class="text-center w-12 text-gray-800 font-semibold text-lg">{{ ejemplares }}</span>
            <button 
              @click="incrementar"
              class="bg-[#011956] hover:bg-[#4EBFD9] text-white w-10 h-10 rounded flex items-center justify-center font-bold transition"
            >
            <PlusIcon class="w-5 h-5 text-white" />

            </button>
          </div>
           <div class="relative mt-3">
        <div class="min-h-0.5 bg-[#F27B35] rounded-full">
          <div class="absolute left-0 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-[#F27B35]"></div>
          <div class="absolute right-0 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-[#F27B35]"></div>
        </div>
      </div>
        </div>

        <!-- Categoría -->
        <div>
          <h3 class="font-semibold text-gray-800 mb-3">Categoría</h3>
          <div class="space-y-2">
            <label v-for="cat in categorias" :key="cat" class="flex items-center cursor-pointer">
              <input 
                :checked="categoriasSeleccionadas.includes(cat)"
                @change="toggleCategoria(cat)"
                type="checkbox"
                class="w-4 h-4 border-2 border-[#011956] accent-[#011956] rounded cursor-pointer"
              />
              <span class="ml-3 text-gray-700 text-sm">{{ cat }}</span>
            </label>
          </div>
          <div class="relative mt-3">
        <div class="min-h-0.5 bg-[#F27B35] rounded-full">
          <div class="absolute left-0 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-[#F27B35]"></div>
          <div class="absolute right-0 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-[#F27B35]"></div>
        </div>
      </div>
        </div>

        <!-- Botón Aplicar -->
        <button 
          @click="aplicarFiltros"
          class="w-full bg-[#344F37] hover:bg-[#98BF45] text-white font-semibold py-3 rounded transition"
        >
          Aplicar
        </button>

      </div>
    </div>
  </div>
</template>