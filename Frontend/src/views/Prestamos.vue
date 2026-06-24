<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import Sidebar from '../components/SideBar.vue';
import { EyeIcon, TrashIcon, IdentificationIcon, NewspaperIcon, CheckCircleIcon, ExclamationCircleIcon } from '@heroicons/vue/24/solid';
import RegistrarPrestamoModal from '../components/RegistrarPrestamoModal.vue';
import { prestamosService } from '../services/prestamosService';
import VerPrestamoModal from '../components/VerPrestamoModal.vue';
import { librosService } from '../services/librosService.ts';
import Swal from 'sweetalert2';

interface Prestamo {
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

const prestamoSeleccionadoId = ref<number | null>(null);

const obtenerFotoPreview = (prestamo: Prestamo) => {
  if (!prestamo.libro_foto) {
    return '';
  }
  
  if (prestamo.libro_foto.startsWith('http')) {
    return prestamo.libro_foto;
  }
  
  return `http://localhost:8000${prestamo.libro_foto}`;
};

// Verificar si un préstamo está vencido
const estaVencido = (fechaDevolucion: string): boolean => {
  try {
    const hoy = new Date();
    hoy.setHours(0, 0, 0, 0);
    
    const fechaDev = new Date(fechaDevolucion);
    fechaDev.setHours(0, 0, 0, 0);
    
    return fechaDev < hoy;
  } catch (e) {
    console.error('Error al parsear fecha:', fechaDevolucion, e);
    return false;
  }
};

const filtroActual = ref<'vigentes' | 'vencidos' | 'devueltos'>('vigentes');
const paginaActual = ref(1);
const prestamosPerPage = 4;
const mostrarModal = ref(false);
const prestamos = ref<Prestamo[]>([]);
const cargando = ref(false);

const verDetalles = (id: number) => {
  prestamoSeleccionadoId.value = id;
};

const obtenerFecha = () => {
  const hoy = new Date();
  const opciones: Intl.DateTimeFormatOptions = { weekday: 'long', day: 'numeric', month: 'long' };
  return hoy.toLocaleDateString('es-ES', opciones).charAt(0).toUpperCase() + hoy.toLocaleDateString('es-ES', opciones).slice(1);
};

// Cargar préstamos con actualización automática de vencidos
const cargarPrestamos = async () => {
  cargando.value = true;
  try {
    const response = await prestamosService.obtenerPrestamos();
    let prestamosCargados = response.data.results || response.data;

    // Actualizar automáticamente préstamos vencidos
    for (let prestamo of prestamosCargados) {
      if (prestamo.estado === 'vigente' && estaVencido(prestamo.fecha_devolucion)) {
        console.log(`Actualizando préstamo ${prestamo.id} a vencido...`);
        
        try {
          // Intentar actualizar en el backend
          await prestamosService.actualizarPrestamo(prestamo.id, { estado: 'vencido' });
          prestamo.estado = 'vencido';
          console.log(`✓ Préstamo ${prestamo.id} actualizado en backend`);
        } catch (err) {
          // Si falla, actualizar localmente al menos
          console.warn(`No se pudo actualizar en backend, actualizando localmente:`, err);
          prestamo.estado = 'vencido';
        }
      }
    }

    prestamos.value = prestamosCargados;
  } catch (err) {
    console.error('Error al cargar préstamos:', err);
    prestamos.value = [];
  } finally {
    cargando.value = false;
  }
};

const prestamosFiltrados = computed(() => {
  return prestamos.value.filter(prestamo => {
    if (filtroActual.value === 'vigentes') {
      return prestamo.estado === 'vigente';
    } else if (filtroActual.value === 'vencidos') {
      return prestamo.estado === 'vencido';
    } else {
      return prestamo.estado === 'devuelto';
    }
  });
});

const prestamosPaginados = computed(() => {
  const inicio = (paginaActual.value - 1) * prestamosPerPage;
  const fin = inicio + prestamosPerPage;
  return prestamosFiltrados.value.slice(inicio, fin);
});

const totalPaginas = computed(() => {
  return Math.ceil(prestamosFiltrados.value.length / prestamosPerPage);
});

const getEstadoColor = (estado: string) => {
  switch (estado) {
    case 'vigente':
      return 'text-[#F2B035]';
    case 'vencido':
      return 'text-[#D9298A]';
    case 'devuelto':
      return 'text-[#344F37]';
    default:
      return 'text-gray-600';
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

const formatearFecha = (fecha: string) => {
  const date = new Date(fecha);
  return date.toLocaleDateString('es-ES', { day: 'numeric', month: 'long', year: 'numeric' });
};

const irRegistrarPrestamo = () => {
  mostrarModal.value = true;
};

const marcarComoDevuelto = async (id: number, libroId: number) => {
  try {
    await prestamosService.marcarPrestamoDevuelto(id);
    await librosService.cambiarEstado(libroId, 'enInventario');
    cargarPrestamos();
  } catch (err) {
    console.error('Error al marcar como devuelto:', err);
  }
};

const eliminarPrestamo = async (id: number) => {
  const result = await Swal.fire({
    title: '¿Eliminar préstamo?',
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
      await prestamosService.eliminarPrestamo(id);

      await Swal.fire({
        title: 'Eliminado',
        text: 'El préstamo fue eliminado correctamente',
        icon: 'success',
        timer: 1500,
        showConfirmButton: false,
      });

      cargarPrestamos();

    } catch (err) {
      console.error('Error al eliminar:', err);

      Swal.fire({
        title: 'Error',
        text: 'No se pudo eliminar el préstamo',
        icon: 'error',
      });
    }
  }
};

const prestamoRegistrado = () => {
  mostrarModal.value = false;
  cargarPrestamos();
};

onMounted(() => {
  cargarPrestamos();
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
            <h1 class="text-4xl font-bold text-white">Panel principal de libros prestados</h1>
            <div class="bg-white rounded-lg px-6 py-2 text-right shadow-lg">
              <p class="text-sm text-[#344F37]">Fecha actual</p>
              <p class="font-semibold text-[#344F37]">{{ obtenerFecha() }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Estadísticas -->
      <div class="px-6 mb-6 flex flex-col md:flex-row md:justify-between md:items-center gap-6">
  
        <div class="bg-white rounded-lg px-6 py-2 w-fit shadow-lg flex items-center gap-3">
          <IdentificationIcon class="icono" />
          <div class="text-left flex flex-col gap-1">
            <p class="text-3xl font-bold text-[#344F37]">{{ prestamos.length }}</p>
            <p class="text-[#344F37] mb-0">Libros prestados</p>
          </div>
        </div>

        <div class="flex flex-col sm:flex-row items-start sm:items-center gap-4 flex-1 md:justify-end">
          
          <div class="flex gap-3 flex-wrap">
            <button
              @click="filtroActual = 'vigentes'; paginaActual = 1"
              :class="[
                'px-6 py-2 rounded-full font-semibold transition',
                filtroActual === 'vigentes'
                  ? 'bg-[#F2B035] text-white shadow-lg'
                  : 'bg-white text-gray-700 border'
              ]"
            >
              Vigentes
            </button>
            <button
              @click="filtroActual = 'vencidos'; paginaActual = 1"
              :class="[
                'px-6 py-2 rounded-full font-semibold transition',
                filtroActual === 'vencidos'
                  ? 'bg-[#D9298A] text-white shadow-lg'
                  : 'bg-white text-gray-700 border'
              ]"
            >
              Vencidos
            </button>
            <button
              @click="filtroActual = 'devueltos'; paginaActual = 1"
              :class="[
                'px-6 py-2 rounded-full font-semibold transition',
                filtroActual === 'devueltos'
                  ? 'bg-[#344F37] text-white shadow-lg'
                  : 'bg-white text-gray-700 border'
              ]"
            >
              Devueltos
            </button>
          </div>

          <button
            @click="irRegistrarPrestamo"
            class="bg-[#344F37] hover:bg-[#98BF45] text-white font-semibold px-6 py-3 rounded-lg transition flex items-center gap-2 shadow-lg whitespace-nowrap"
          >
            <NewspaperIcon class="icono2" />
            <span>Registrar préstamo</span> 
          </button>

        </div>
      </div>

      <!-- Grid de tarjetas -->
      <div class="px-6 pb-12">
        <!-- Cargando -->
        <div v-if="cargando" class="text-center py-12 text-gray-500">
          <svg class="w-12 h-12 mx-auto mb-4 text-gray-400 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
          </svg>
          <p class="text-lg">Cargando préstamos...</p>
        </div>

        <!-- Tarjetas -->
        <div v-else-if="prestamosPaginados.length > 0"
            class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 justify-items-center">
          <div
            v-for="prestamo in prestamosPaginados"
            :key="prestamo.id"
           class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition w-72"
          >
            <!-- Foto del libro -->
            <div class="relative h-50 bg-gray-200 overflow-hidden">
                <img
                v-if="obtenerFotoPreview(prestamo)"
                :src="obtenerFotoPreview(prestamo)"
                :alt="prestamo.libro_titulo"
                class="w-full h-full object-cover"
              />
              <div v-else class="w-full h-full flex items-center justify-center bg-gray-300">
                <svg class="w-12 h-12 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M5 3a2 2 0 012-2h6a2 2 0 012 2v2H5V3z"/>
                  <path fill-rule="evenodd" d="M5 5h10a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2zm0 2v9h10V7H5z"/>
                </svg>
              </div>
            </div>

            <!-- Contenido -->
            <div class="p-4">
              <!-- Título -->
              <h3 class="text-lg font-semibold text-gray-800 line-clamp-2 mb-1">{{ prestamo.libro_titulo }}</h3>
              <p class="text-sm text-gray-600 mb-4">{{ prestamo.libro_autor }}</p>

              <!-- Información del préstamo -->
              <p class="text-sm text-gray-700 mb-1">
                <span class="font-semibold">Lector:</span> {{ prestamo.nombre_lector }}
              </p>
              <p class="text-sm text-gray-600 mb-4">
                Libro prestado: {{ formatearFecha(prestamo.fecha_prestamo) }}
              </p>

              <!-- Estado y fecha de devolución -->
              <div class="flex items-center justify-between pb-4 border-b border-gray-200">
                <span :class="['text-sm font-semibold', getEstadoColor(prestamo.estado)]">
                  {{ getEstadoLabel(prestamo.estado) }}
                </span>
                <span class="text-xs text-gray-500">
                  Vence: {{ formatearFecha(prestamo.fecha_devolucion) }}
                </span>
              </div>

              <!-- Acciones -->
              <div class="flex gap-2 justify-end mt-4">
                <!-- Marcar como devuelto -->
                <button
                  v-if="prestamo.estado !== 'devuelto'"
                  @click="marcarComoDevuelto(prestamo.id, prestamo.libro)"
                  class="p-2 text-green-600 hover:bg-green-50 rounded transition"
                  title="Marcar como devuelto"
                >
                  <CheckCircleIcon class="icono" />
                </button>

                <!-- Ver detalles -->
                <button 
                  @click="verDetalles(prestamo.id)"
                  class="p-2 hover:bg-blue-50 rounded transition"
                  title="Ver detalles"
                >
                  <EyeIcon class="icono" />
                </button>

                <!-- Eliminar -->
                <button
                  @click="eliminarPrestamo(prestamo.id)"
                  class="p-2 text-red-600 hover:bg-red-50 rounded transition"
                  title="Eliminar"
                >
                  <TrashIcon class="icono" />
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Sin resultados -->
        <div v-else class="bg-[#011956] rounded-2xl mx-auto max-w-2xl w-70% text-center py-6 text-white hover:bg-[#4EBFD9] transition">
          <ExclamationCircleIcon class="w-12 h-12 mx-auto mb-4" />
          <p class="text-lg">No hay préstamos en esta categoría</p>
        </div>

        <!-- Paginación -->
        <div v-if="totalPaginas > 1" class="flex justify-center gap-2 mt-8">
          <button
            v-for="pagina in totalPaginas"
            :key="pagina"
            @click="paginaActual = pagina"
            :class="['w-10 h-10 rounded-lg font-semibold transition', paginaActual === pagina ? 'bg-[#344F37] text-white shadow-lg' : 'bg-white text-[#344F37] border border-gray-300 hover:border-[#344F37]']"
          >
            {{ pagina }}
          </button>
        </div>
      </div>
    </main>

    <VerPrestamoModal
      v-if="prestamoSeleccionadoId"
      :prestamo-id="prestamoSeleccionadoId"
      @cerrar="prestamoSeleccionadoId = null"
      @actualizado="cargarPrestamos"
    />

    <!-- Modal registrar préstamo -->
    <RegistrarPrestamoModal
      v-if="mostrarModal"
      @cerrar="mostrarModal = false"
      @prestamo-registrado="prestamoRegistrado"
    />

  </div>
</template>