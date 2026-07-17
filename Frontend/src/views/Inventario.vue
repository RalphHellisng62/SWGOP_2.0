<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue';
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
const refreshInterval = ref<ReturnType<typeof setInterval> | null>(null);

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

  if (filtrosAplicados.value.estado.length > 0) {
    resultado = resultado.filter(libro =>
      filtrosAplicados.value.estado.includes(libro.estado)
    );
  }

  if (filtrosAplicados.value.ejemplares > 0) {
    resultado = resultado.filter(libro =>
      libro.ejemplares >= filtrosAplicados.value.ejemplares
    );
  }

  if (filtrosAplicados.value.categorias.length > 0) {
    resultado = resultado.filter(libro =>
      filtrosAplicados.value.categorias.includes(libro.categoria)
    );
  }

  resultado.sort((a, b) => {
    const tituloA = a.titulo.toLowerCase();
    const tituloB = b.titulo.toLowerCase();
    return filtrosAplicados.value.ordenar === 'A-Z' 
      ? tituloA.localeCompare(tituloB) 
      : tituloB.localeCompare(tituloA);
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
    case 'enInventario': return 'text-[#344F37] bg-green-100';
    case 'prestado': return 'text-[#F27B35] bg-yellow-100';
    case 'sinExistencias': return 'text-[#D9298A] bg-rose-100';
    default: return 'text-gray-600 bg-gray-50';
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
      Swal.fire({ title: 'Error', text: 'No se pudo eliminar el libro', icon: 'error' });
    }
  }
};

const irAgregarLibro = () => {
  mostrarModal.value = true;
};

const libroAgregado = () => {
  cargarLibros();  
  mostrarModal.value = false;
};

const aplicarFiltros = (filtros: FiltrosAplicados) => {
  filtrosAplicados.value = filtros;
  localStorage.setItem('filtrosInventario', JSON.stringify(filtros));
  paginaActual.value = 1;
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
  refreshInterval.value = setInterval(cargarLibros, 5000);
});

onUnmounted(() => {
  if (refreshInterval.value) clearInterval(refreshInterval.value);
});
</script>

<template>
  <div class="flex min-h-screen animate-page">
    <Sidebar />

    <main class="flex-1 overflow-auto">
      <!-- Header -->
      <div class="px-6 pt-6 pb-6">
        <div class="bg-[#344F37] backdrop-blur-sm rounded-3xl px-6 py-4 mb-2">
          <div class="flex justify-between items-start">
            <h1 class="text-4xl font-bold text-white">Panel principal de inventario de libros</h1>
            <div class="bg-white rounded-2xl px-6 py-3 text-right shadow-lg">
              <p class="text-sm text-[#344F37]">Fecha actual</p>
              <p class="font-semibold text-[#344F37]">{{ obtenerFecha() }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Estadísticas -->
      <div class="px-6 mb-6 flex justify-between items-start gap-6">
        <!-- Card Total -->
        <div class="bg-white rounded-3xl px-6 py-5 w-fit shadow-lg flex items-center gap-4 transition-all duration-300 hover:scale-105 hover:-translate-y-1 hover:shadow-xl">
          <RectangleStackIcon class="w-10 h-10 text-[#344F37] transition-transform duration-300 hover:scale-110" />
          <div>
            <p class="text-4xl font-bold text-[#344F37]">{{ totalLibros }}</p>
            <p class="text-[#344F37]">Total de libros registrados</p>
          </div>
        </div>

        <!-- Card Categorías -->
        <div class="bg-white rounded-3xl px-6 py-5 shadow-lg flex items-center gap-6 transition-all duration-300 hover:scale-105 hover:-translate-y-1 hover:shadow-xl flex-1 max-w-md">
          <FolderOpenIcon class="w-10 h-10 text-[#344F37] transition-transform duration-300 hover:scale-110" />
          <div class="flex-1">
            <label class="text-sm text-[#344F37] font-semibold block mb-1">Libros por categoría</label>
            <select 
              v-model="categoriaSeleccionada"
              class="w-full px-4 py-2 border border-[#344F37] rounded-2xl focus:outline-none focus:ring-2 focus:ring-[#98BF45] text-sm font-semibold transition-all duration-300 hover:scale-105"
            >
              <option value="">-- Seleccionar una categoría --</option>
              <option v-for="(cantidad, categoria) in librosPorCategoria" :key="categoria" :value="categoria">
                {{ categoria }} ({{ cantidad }})
              </option>
            </select>
          </div>
          <div class="text-center pl-6 border-l border-gray-200">
            <p class="text-4xl font-bold text-[#344F37]">
              {{ categoriaSeleccionada ? librosPorCategoria[categoriaSeleccionada] : libros.length }}
            </p>
            <p class="text-xs text-[#344F37]">en esta categoría</p>
          </div>
        </div>

        <button 
          @click="mostrarFiltros = true"
          class="bg-[#344F37] hover:bg-[#98BF45] text-white font-semibold px-6 py-3 rounded-3xl transition-all duration-300 hover:scale-105 hover:-translate-y-1 shadow-lg flex items-center gap-2 self-start"
        >
          <ListBulletIcon class="w-5 h-5 transition-transform duration-200" />
          Filtros
        </button>
      </div>

      <!-- Búsqueda y Agregar -->
      <div class="flex gap-4 px-6 pb-6">
        <input
          v-model="busqueda"
          type="text"
          placeholder="Búsqueda por NT, título, y autor"
          class="flex-1 px-5 py-4 rounded-3xl bg-white focus:outline-none focus:ring-2 focus:ring-[#344F37] transition-all duration-300 focus:scale-[1.02]"
        />

        <button
          @click="irAgregarLibro"
          class="bg-[#344F37] hover:bg-[#98BF45] text-white font-semibold px-8 py-4 rounded-3xl transition-all duration-300 hover:scale-105 hover:-translate-y-1 shadow-lg flex items-center gap-3 whitespace-nowrap"
        >
          <FolderPlusIcon class="w-5 h-5 transition-transform duration-200" />
          Agregar libro
        </button>
      </div>

      <!-- Tabla -->
      <div class="px-6 pb-6">
        <div class="bg-white rounded-3xl shadow-lg overflow-hidden">
          <table class="w-full">
            <thead>
              <tr class="bg-[#344F37] text-white">
                <th class="px-6 py-5 text-left font-semibold">No. de registro</th>
                <th class="px-6 py-5 text-left font-semibold">NT</th>
                <th class="px-6 py-5 text-left font-semibold">Título</th>
                <th class="px-6 py-5 text-left font-semibold">Autor</th>
                <th class="px-6 py-5 text-left font-semibold">Categoría</th>
                <th class="px-6 py-5 text-left font-semibold">Estado</th>
                <th class="px-6 py-5 text-center font-semibold">Mostrar</th>
                <th class="px-6 py-5 text-center font-semibold">Eliminar</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr 
                v-for="(libro, index) in librosPaginados" 
                :key="libro.id" 
                class="hover:bg-gray-50 transition-all duration-200 hover:scale-[1.01]"
              >
                <td class="px-6 py-5">{{ (paginaActual - 1) * librosPerPage + index + 1 }}</td>
                <td class="px-6 py-5 font-mono text-sm">{{ libro.nt }}</td>
                <td class="px-6 py-5">{{ libro.titulo }}</td>
                <td class="px-6 py-5">{{ libro.autor }}</td>
                <td class="px-6 py-5">{{ libro.categoria }}</td>
                <td class="px-6 py-5">
                  <span :class="['px-4 py-1.5 rounded-2xl text-sm font-semibold', getEstadoClases(libro.estado)]">
                    {{ libro.estado_display }}
                  </span>
                </td>
                <td class="px-6 py-5 text-center">
                  <button @click="verDetalles(libro.id)" class="hover:scale-125 transition-transform duration-200">
                    <EyeIcon class="w-6 h-6 text-gray-600 hover:text-[#344F37]" />
                  </button>
                </td>
                <td class="px-6 py-5 text-center">
                  <button @click="eliminarLibro(libro.id)" class="hover:scale-125 transition-transform duration-200">
                    <TrashIcon class="w-6 h-6 text-gray-600 hover:text-red-600" />
                  </button>
                </td>
              </tr>
            </tbody>
          </table>

          <div v-if="librosPaginados.length === 0" class="text-center py-16 text-[#344F37]">
            No hay libros para mostrar
          </div>
        </div>

        <!-- Paginación -->
        <div class="flex justify-center gap-3 mt-8">
          <button
            v-for="pagina in totalPaginas"
            :key="pagina"
            @click="paginaActual = pagina"
            class="w-11 h-11 rounded-2xl font-semibold transition-all duration-200 hover:scale-110 active:scale-95"
            :class="[
              paginaActual === pagina
                ? 'bg-[#344F37] text-white shadow-lg'
                : 'bg-white text-gray-700 border border-gray-200 hover:border-[#98BF45] hover:bg-[#98BF45] hover:text-white'
            ]"
          >
            {{ pagina }}
          </button>
        </div>
      </div>
    </main>

    <!-- Modales -->
    <VerLibroModal 
      v-if="libroSeleccionadoId"
      :libro-id="libroSeleccionadoId"
      @cerrar="libroSeleccionadoId = null"
      @libro-actualizado="cargarLibros"
    />

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

<style scoped>
@keyframes pageEnter {
  from {
    opacity: 0;
    transform: translateY(24px) scale(.985);
    filter: blur(3px);
  }

  to {
    opacity: 1;
    transform: translateY(0) scale(1);
    filter: blur(0);
  }
}

.animate-page{
  animation: pageEnter .75s cubic-bezier(.22,1,.36,1);
}
</style>