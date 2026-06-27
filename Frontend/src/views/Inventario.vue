<script setup lang="ts">

import { ref, onMounted, computed } from 'vue';
import { EyeIcon, TrashIcon, ListBulletIcon, FolderPlusIcon, RectangleStackIcon, FolderOpenIcon } from '@heroicons/vue/24/solid';
import { librosService } from '../services/librosService';
import Sidebar from '../components/SideBar.vue';
import AgregarLibroModal from '../components/AgregarLibroModal.vue';
import VerLibroModal from '../components/VerLibroModal.vue';  
import FiltrosModal from '../components/FiltrosModal.vue';
import Swal from 'sweetalert2';

interface FiltrosAplicados {
  ordenar: 'A-Z' | 'Z-A';
  estado: string[];
  ejemplares: number;
  categorias: string[];
}

interface Libro {
  id: number;
  nt: string;
  titulo: string;
  autor: string;
  categoria: string;
  estado: string;
  estado_display: string;
  ejemplares: number;
}

const mostrarFiltros = ref(false);
const mostrarModal = ref(false);
const libros = ref<Libro[]>([]);
const busqueda = ref('');
const paginaActual = ref(1);
const librosPerPage = 30;
const totalLibros = ref(0);
const cargando = ref(false);
const libroSeleccionadoId = ref<number | null>(null);

const filtrosGuardados = localStorage.getItem('filtrosInventario');

const filtrosAplicados = ref<FiltrosAplicados>(
  filtrosGuardados
    ? JSON.parse(filtrosGuardados)
    : {
        ordenar: 'A-Z',
        estado: [],
        ejemplares: 0,
        categorias: [],
      }
);
const obtenerFecha = () => {
  const hoy = new Date();
  const opciones: Intl.DateTimeFormatOptions = { weekday: 'long', day: 'numeric', month: 'long' };
  return hoy.toLocaleDateString('es-ES', opciones).charAt(0).toUpperCase() + hoy.toLocaleDateString('es-ES', opciones).slice(1);
};

const cargarLibros = async () => {
  cargando.value = true;
  try {
    const response = await librosService.obtenerLibros();
    libros.value = response.data.results || response.data;
    totalLibros.value = response.data.count || response.data.length || 0;
  } catch (err) {
    console.error('Error al cargar libros:', err);
  } finally {
    cargando.value = false;
  }
};

// Filtrar por búsqueda
const librosFiltradosPorBusqueda = computed(() => {
  if (!busqueda.value) return libros.value;
  
  return libros.value.filter(libro =>
    libro.nt.toLowerCase().includes(busqueda.value.toLowerCase()) ||
    libro.titulo.toLowerCase().includes(busqueda.value.toLowerCase()) ||
    libro.autor.toLowerCase().includes(busqueda.value.toLowerCase()) ||
    libro.categoria.toLowerCase().includes(busqueda.value.toLowerCase())
  );
});

// Filtrar por los filtros avanzados
const librosFiltrados = computed(() => {
  let resultado = librosFiltradosPorBusqueda.value;

  // Filtrar por estado
  if (filtrosAplicados.value.estado.length > 0) {
    resultado = resultado.filter(libro =>
      filtrosAplicados.value.estado.includes(libro.estado)
    );
  }

  // Filtrar por ejemplares (mayor o igual)
  if (filtrosAplicados.value.ejemplares > 0) {
    resultado = resultado.filter(libro =>
      libro.ejemplares >= filtrosAplicados.value.ejemplares
    );
  }

  // Filtrar por categorías
  if (filtrosAplicados.value.categorias.length > 0) {
    resultado = resultado.filter(libro =>
      filtrosAplicados.value.categorias.includes(libro.categoria)
    );
  }

  // Ordenar
  resultado.sort((a, b) => {
    const tituloA = a.titulo.toLowerCase();
    const tituloB = b.titulo.toLowerCase();
    
    if (filtrosAplicados.value.ordenar === 'A-Z') {
      return tituloA.localeCompare(tituloB);
    } else {
      return tituloB.localeCompare(tituloA);
    }
  });

  return resultado;
});

const librosPaginados = computed(() => {
  const inicio = (paginaActual.value - 1) * librosPerPage;
  const fin = inicio + librosPerPage;
  return librosFiltrados.value.slice(inicio, fin);
});

const totalPaginas = computed(() => {
  return Math.ceil(librosFiltrados.value.length / librosPerPage);
});

const getEstadoClases = (estado: string) => {
  switch (estado) {
    case 'enInventario':
      return 'text-[#344F37] bg-green-100';
    case 'prestado':
      return 'text-[#F27B35] bg-yellow-100';
    case 'sinExistencias':
      return 'text-[#D9298A] bg-rose-100';
    default:
      return 'text-gray-600 bg-gray-50';
  }
};

const verDetalles = (id: number) => {
  libroSeleccionadoId.value = id;
};

const eliminarLibro = async (id: number) => {
  const result = await Swal.fire({
    title: '¿Eliminar libro?',
    text: 'Esta acción no se puede deshacer.',
    icon: 'warning',

    showCancelButton: true,

    confirmButtonColor: '#344F37',
    cancelButtonColor: '#D9298A',

    confirmButtonText: 'Sí, eliminar',
    cancelButtonText: 'Cancelar',
  });

  if (result.isConfirmed) {
    try {
      await librosService.eliminarLibro(id);

      await Swal.fire({
        title: 'Eliminado',
        text: 'El libro fue eliminado correctamente',
        icon: 'success',
        timer: 1500,
        showConfirmButton: false,
      });

      cargarLibros();

    } catch (err) {
      console.error(err);

      Swal.fire({
        title: 'Error',
        text: 'No se pudo eliminar el libro',
        icon: 'error',
      });
    }
  }
};

const irAgregarLibro = () => {
  mostrarModal.value = true;
};

const libroAgregado = () => {
  console.log('Libro agregado, recargando...');
  cargarLibros();  
  mostrarModal.value = false;
};

const aplicarFiltros = (filtros: FiltrosAplicados) => {

  filtrosAplicados.value = filtros;

  // Guardar filtros
  localStorage.setItem(
    'filtrosInventario',
    JSON.stringify(filtros)
  );

  paginaActual.value = 1;

  console.log('Filtros aplicados:', filtros);
};

const categoriaSeleccionada = ref('');
const librosPorCategoria = computed(() => {
  const categorias: { [key: string]: number } = {};
  
  libros.value.forEach(libro => {
    const cat = libro.categoria || 'Sin categoría';
    categorias[cat] = (categorias[cat] || 0) + 1;
  });
  
  return categorias;
});

onMounted(() => {
  cargarLibros();
});
</script>


<template>

    <div class="flex min-h-screen">
        <Sidebar />
   

  <main class="flex-1 overflow-auto">
    <!-- Header -->
     <div class="px-6 pt-6 pb-6">
        <div class="bg-[#344F37] backdrop-blur-sm rounded-4xl px-6 py-3 mb-2">
          <div class="flex justify-between items-start">
            <h1 class="text-4xl font-bold text-white">Panel principal de inventario de libros</h1>
            <div class="bg-white rounded-lg px-6 py-2 text-right shadow-lg">
              <p class="text-sm text-[#344F37]">Fecha actual</p>
              <p class="font-semibold text-[#344F37]">{{ obtenerFecha() }}</p>
            </div>
          </div>
        </div>
      </div>
    
      <!-- Estadísticas -->
      <div class="px-6 mb-6 flex justify-between items-start">
        <div class="bg-white rounded-lg px-6 py-2 w-fit shadow-lg flex items-center gap-3">
          <RectangleStackIcon class="icono" />
          <div class="text-left flex flex-col gap-1">
            <p class="text-3xl font-bold text-[#344F37]">{{ totalLibros }}</p>
            <p class="text-[#344F37]">Total de libros registrados</p>
          </div>
        </div>
       
      <!-- Card Categorías -->
    <div class="bg-white rounded-lg px-6 py-3 shadow-lg flex items-center gap-6">
      
      <FolderOpenIcon class="icono" />
      <div class="flex flex-col gap-2">
        <label class="text-sm text-[#344F37] font-semibold">Libros por categoría</label>
        <select 
          v-model="categoriaSeleccionada"
          class="px-3 py-1 border border-[#344F37] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#98BF45] text-sm font-semibold text-[#344F37]"
        >
          <option value="">-- Seleccionar una categoría --</option>
          <option 
            v-for="(cantidad, categoria) in librosPorCategoria" 
            :key="categoria"
            :value="categoria"
          >
            {{ categoria }} ({{ cantidad }})
          </option>
        </select>
      </div>
    
      <!-- Número grande -->
      <div class="text-center pl-4 border-l border-gray-300">
        <p class="text-3xl font-bold text-[#344F37]">
          {{ categoriaSeleccionada ? librosPorCategoria[categoriaSeleccionada] : libros.length }}
        </p>
        <p class="text-xs text-[#344F37]">libros registrados en esta categoria</p>
      </div>
    </div>
            <div class="flex-rigth gap-4 mb-6">
          <button 
              @click="mostrarFiltros = true"
              class="bg-[#344F37] hover:bg-[#98BF45] text-white font-semibold px-6 py-3 rounded-lg transition flex items-center gap-2 shadow-lg"
            >
              <ListBulletIcon class="icono2" />
              Filtros
            </button>
          </div>
          </div>
          
          <!-- Búsqueda y botón -->
          <div class="flex gap-4 px-6 py-6">
            <input
              v-model="busqueda"
              type="text"
              placeholder="Búsqueda por NT, título, y autor"
              class="flex-1 px-4 py-3 rounded-lg bg-white text-black placeholder-[#344F37] focus:outline-none focus:ring-2 focus:ring-[#344F37]"
            />

        <button
          @click="irAgregarLibro"
          class="bg-[#344F37] hover:bg-[#98BF45] text-white font-semibold px-6 py-3 rounded-lg transition flex items-center gap-2 shadow-lg"
        >
          <FolderPlusIcon class="icono2" />
          <span>Agregar libro</span>
        </button>
      </div>
   

    <!-- Tabla -->
    <div class="px-6 py-6">
      <div class="bg-white rounded-lg shadow-lg overflow-hidden">
        <table class="w-full">
          <thead>
            <tr class="bg-[#344F37] text-white">
              <th class="px-6 py-4 text-left font-semibold">No. de registro</th>
              <th class="px-6 py-4 text-left font-semibold">NT</th>
              <th class="px-6 py-4 text-left font-semibold">Título</th>
              <th class="px-6 py-4 text-left font-semibold">Autor</th>
              <th class="px-6 py-4 text-left font-semibold">Categoría</th>
              <th class="px-6 py-4 text-left font-semibold">Estado</th>
              <th class="px-6 py-4 text-center font-semibold">Mostrar más</th>
              <th class="px-6 py-4 text-center font-semibold">Eliminar</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-[#344F37]/20">
            <tr v-for="(libro, index) in librosPaginados" :key="libro.id" class="hover:bg-gray-50 transition">
              <td class="px-6 py-4 text-black">{{ (paginaActual - 1) * librosPerPage + index + 1 }}</td>
              <td class="px-6 py-4 text-black font-mono text-sm">{{ libro.nt }}</td>
              <td class="px-6 py-4 text-black">{{ libro.titulo }}</td>
              <td class="px-6 py-4 text-black">{{ libro.autor }}</td>
              <td class="px-6 py-4 text-black">{{ libro.categoria }}</td>
              <td class="px-6 py-4">
                <span :class="['px-3 py-1 rounded-full text-sm font-semibold', getEstadoClases(libro.estado)]">
                  {{ libro.estado_display }}
                </span>
              </td>
              <td class="px-6 py-4 text-center">
                <button
                  @click="verDetalles(libro.id)"
                 
                >
                  <EyeIcon class="icono" />
                </button>
              </td>
              <td class="px-6 py-4 text-center">
                <button
                  @click="eliminarLibro(libro.id)"
                  
                >
                  <TrashIcon class="icono" />
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Sin resultados -->
        <div v-if="librosPaginados.length === 0" class="text-center py-12 text-[#344F37]">
          No hay libros para mostrar
        </div>
      </div>

      <!-- Paginación -->
      <div class="flex justify-center gap-2 mt-6">
        <button
          v-for="pagina in totalPaginas"
          :key="pagina"
          @click="paginaActual = pagina"
          :class="[
            'w-10 h-10 rounded-lg font-semibold transition',
            paginaActual === pagina
              ? 'bg-[#344F37] text-white shadow-lg'
              : 'bg-white text-gray-700 border border-gray-300 hover:border-[#98BF45]'
          ]"
        >
          {{ pagina }}
        </button>
      </div>
    </div>
  </main>
 <!-- Modal de ver libro -->
  <VerLibroModal 
  v-if="libroSeleccionadoId"
  :libro-id="libroSeleccionadoId"
  @cerrar="libroSeleccionadoId = null"
  @libro-actualizado="cargarLibros"
/>
  <!-- Modal agregar libro -->
<AgregarLibroModal 
  v-if="mostrarModal"
  @cerrar="mostrarModal = false"
  @libro-agregado="libroAgregado"
/>

<FiltrosModal 
  v-model="mostrarFiltros"
  @aplicar="aplicarFiltros"
/>
  </div>
</template>