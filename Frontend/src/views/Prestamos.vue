<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue';
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
  if (!prestamo.libro_foto) return '';
  
  if (prestamo.libro_foto.startsWith('http')) {
    return prestamo.libro_foto;
  }
  return `http://localhost:8000${prestamo.libro_foto}`;
};

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
const refreshInterval = ref<number | null>(null);

const verDetalles = (id: number) => {
  prestamoSeleccionadoId.value = id;
};

const obtenerFecha = () => {
  const hoy = new Date();
  const opciones: Intl.DateTimeFormatOptions = { weekday: 'long', day: 'numeric', month: 'long' };
  return hoy.toLocaleDateString('es-ES', opciones).charAt(0).toUpperCase() + hoy.toLocaleDateString('es-ES', opciones).slice(1);
};

const cargarPrestamos = async () => {
  cargando.value = true;
  try {
    const response = await prestamosService.obtenerPrestamos();
    let prestamosCargados = response.data.results || response.data;

    for (let prestamo of prestamosCargados) {
      if (prestamo.estado === 'vigente' && estaVencido(prestamo.fecha_devolucion)) {
        try {
          await prestamosService.actualizarPrestamo(prestamo.id, { estado: 'vencido' });
          prestamo.estado = 'vencido';
        } catch (err) {
          console.warn(`No se pudo actualizar en backend:`, err);
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
    if (filtroActual.value === 'vigentes') return prestamo.estado === 'vigente';
    if (filtroActual.value === 'vencidos') return prestamo.estado === 'vencido';
    return prestamo.estado === 'devuelto';
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
    case 'vigente': return 'text-[#F2B035]';
    case 'vencido': return 'text-[#D9298A]';
    case 'devuelto': return 'text-[#344F37]';
    default: return 'text-gray-600';
  }
};

const getEstadoLabel = (estado: string) => {
  switch (estado) {
    case 'vigente': return 'Vigente';
    case 'vencido': return 'Vencido';
    case 'devuelto': return 'Devuelto';
    default: return estado;
  }
};

const formatearFecha = (fecha: string) => {
  const [year, month, day] = fecha.split('T')[0].split('-').map(Number);
  const date = new Date(year, month - 1, day);
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
      Swal.fire({ title: 'Error', text: 'No se pudo eliminar el préstamo', icon: 'error' });
    }
  }
};

const prestamoRegistrado = () => {
  mostrarModal.value = false;
  cargarPrestamos();
};

onMounted(() => {
  cargarPrestamos();
  refreshInterval.value = setInterval(cargarPrestamos, 5000);
});

onUnmounted(() => {
  if (refreshInterval.value) clearInterval(refreshInterval.value);
});
</script>

<template>
  <div class="flex min-h-screen animate-page">
    <Sidebar />

    <div class="flex-1 overflow-auto">
      <main>
      <!-- Header -->
      <div class="px-6 pt-6 pb-6" >
        <div class="bg-[#344F37] backdrop-blur-sm rounded-4xl px-6 py-4 mb-2 transition-all duration-300 ease-out hover:scale-105 hover:shadow-lg active:scale-90">
          <div class="flex justify-between items-start">
            <h1 class="text-4xl font-bold text-white">Panel principal de libros prestados</h1>
            <div class="bg-white rounded-4xl px-6 py-3 text-right shadow-lg">
              <p class="text-sm text-[#344F37]">Fecha actual</p>
              <p class="font-semibold text-[#344F37]">{{ obtenerFecha() }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Estadísticas y Filtros -->
      <div class="px-6 mb-8 flex flex-col md:flex-row md:justify-between md:items-center gap-6">
        <!-- Total Prestados -->
        <div class="bg-white rounded-4xl px-6 py-5 w-fit shadow-lg flex items-center gap-4 transition-all duration-300 hover:scale-105 hover:-translate-y-1 hover:shadow-xl">
          <IdentificationIcon class="w-10 h-10 text-[#344F37] transition-transform duration-200 hover:scale-110" />
          <div>
            <p class="text-4xl font-bold text-[#344F37]">{{ prestamos.length }}</p>
            <p class="text-[#344F37]">Libros prestados</p>
          </div>
        </div>

        <div class="flex flex-col sm:flex-row items-start sm:items-center gap-4 flex-1 md:justify-end">
          <div class="flex gap-3 flex-wrap">
            <button
              @click="filtroActual = 'vigentes'; paginaActual = 1"
              :class="[
                'px-6 py-3 rounded-4xl font-semibold transition-all duration-300 hover:scale-105',
                filtroActual === 'vigentes'
                  ? 'bg-[#F27B35] text-white shadow-lg'
                  : 'bg-white text-[#F27B35] border border-[#F27B35] hover:bg-[#F27B35] hover:text-white'
              ]"
            >
              Vigentes
            </button>
            <button
              @click="filtroActual = 'vencidos'; paginaActual = 1"
              :class="[
                'px-6 py-3 rounded-4xl font-semibold transition-all duration-300 hover:scale-105',
                filtroActual === 'vencidos'
                  ? 'bg-[#D9298A] text-white shadow-lg'
                  : 'bg-white text-[#D9298A] border border-[#D9298A] hover:bg-[#D9298A] hover:text-white'
              ]"
            >
              Vencidos
            </button>
            <button
              @click="filtroActual = 'devueltos'; paginaActual = 1"
              :class="[
                'px-6 py-3 rounded-3xl font-semibold transition-all duration-300 hover:scale-105',
                filtroActual === 'devueltos'
                  ? 'bg-[#98BF45] text-white shadow-lg'
                  : 'bg-white text-[#344F37] border border-[#98BF45] hover:bg-[#98BF45] hover:text-white'
              ]"
            >
              Devueltos
            </button>
          </div>

          <button
            @click="irRegistrarPrestamo"
            class="bg-[#344F37] hover:bg-[#98BF45] text-white font-semibold px-6 py-3 rounded-3xl transition-all duration-300 hover:scale-105 hover:-translate-y-1 shadow-lg flex items-center gap-2 whitespace-nowrap"
          >
            <NewspaperIcon class="w-5 h-5 transition-transform duration-200" />
            Registrar préstamo
          </button>
        </div>
      </div>

      <!-- Contenido Principal -->
      <div class="px-6 pb-12">
        <!-- Cargando -->
        <div v-if="cargando" class="text-center py-20">
          <svg class="w-12 h-12 mx-auto mb-4 text-gray-400 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
          </svg>
          <p class="text-lg text-gray-500">Cargando préstamos...</p>
        </div>

        <!-- Grid de Tarjetas -->
        <div v-else-if="prestamosPaginados.length > 0" 
            class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
          <div
            v-for="prestamo in prestamosPaginados"
            :key="prestamo.id"
            class="bg-white rounded-4xl shadow-lg overflow-hidden transition-all duration-300 hover:scale-105 hover:shadow-2xl group w-full"
          >
            <!-- Imagen -->
            <div class="relative h-52 bg-gray-100 overflow-hidden">
              <img
                v-if="obtenerFotoPreview(prestamo)"
                :src="obtenerFotoPreview(prestamo)"
                :alt="prestamo.libro_titulo"
                class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
              />
              <div v-else class="w-full h-full flex items-center justify-center bg-gray-200">
                <svg class="w-16 h-16 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M5 3a2 2 0 012-2h6a2 2 0 012 2v2H5V3z"/>
                  <path fill-rule="evenodd" d="M5 5h10a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2zm0 2v9h10V7H5z"/>
                </svg>
              </div>
            </div>

            <!-- Contenido -->
            <div class="p-5">
              <h3 class="text-lg font-semibold text-gray-800 line-clamp-2 mb-1">{{ prestamo.libro_titulo }}</h3>
              <p class="text-sm text-gray-600 mb-4">{{ prestamo.libro_autor }}</p>

              <p class="text-sm text-gray-700 mb-1">
                <span class="font-semibold">Lector:</span> {{ prestamo.nombre_lector }}
              </p>
              <p class="text-sm text-gray-600 mb-4">
                Prestado: {{ formatearFecha(prestamo.fecha_prestamo) }}
              </p>

              <div class="flex items-center justify-between mb-4">
                <span :class="['text-sm font-semibold', getEstadoColor(prestamo.estado)]">
                  {{ getEstadoLabel(prestamo.estado) }}
                </span>
                <span class="text-xs text-gray-500">
                  Vence: {{ formatearFecha(prestamo.fecha_devolucion) }}
                </span>
              </div>

              <!-- Acciones -->
              <div class="flex gap-2 justify-end pt-2 border-t">
                <button
                  v-if="prestamo.estado !== 'devuelto'"
                  @click="marcarComoDevuelto(prestamo.id, prestamo.libro)"
                  class="p-3 text-green-600 hover:bg-green-50 rounded-2xl transition-all hover:scale-110"
                  title="Marcar como devuelto"
                >
                  <CheckCircleIcon class="w-6 h-6" />
                </button>

                <button 
                  @click="verDetalles(prestamo.id)"
                  class="p-3 hover:bg-blue-50 rounded-2xl transition-all hover:scale-110"
                  title="Ver detalles"
                >
                  <EyeIcon class="w-6 h-6 text-gray-700" />
                </button>

                <button
                  @click="eliminarPrestamo(prestamo.id)"
                  class="p-3 text-red-600 hover:bg-red-50 rounded-2xl transition-all hover:scale-110"
                  title="Eliminar"
                >
                  <TrashIcon class="w-6 h-6" />
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Sin resultados -->
        <div v-else class="bg-white rounded-4xl py-16 text-center max-w-md mx-auto transition-all duration-300 ease-out hover:scale-105 hover:shadow-lg active:scale-90">
          <ExclamationCircleIcon class="w-16 h-16 mx-auto mb-6 text-gray-300" />
          <p class="text-xl text-gray-600">No hay préstamos en esta categoría</p>
        </div>

        <!-- Paginación -->
        <div v-if="totalPaginas > 1" class="flex justify-center gap-3 mt-10">
          <button
            v-for="pagina in totalPaginas"
            :key="pagina"
            @click="paginaActual = pagina"
            class="w-11 h-11 rounded-2xl font-semibold transition-all duration-200 hover:scale-110 active:scale-95"
            :class="[
              paginaActual === pagina 
                ? 'bg-[#344F37] text-white shadow-lg' 
                : 'bg-white border border-gray-300 hover:border-[#344F37] hover:text-[#344F37]'
            ]"
          >
            {{ pagina }}
          </button>
        </div>
      </div>
      </main>
    </div>

    <!-- Modales -->
    <VerPrestamoModal
      v-if="prestamoSeleccionadoId"
      :prestamo-id="prestamoSeleccionadoId"
      @cerrar="prestamoSeleccionadoId = null"
      @actualizado="cargarPrestamos"
    />

    <RegistrarPrestamoModal
      v-if="mostrarModal"
      @cerrar="mostrarModal = false"
      @prestamo-registrado="prestamoRegistrado"
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



.prestamos-move,
.prestamos-enter-active,
.prestamos-leave-active{
    transition: all .45s cubic-bezier(.22,1,.36,1);
}

.prestamos-enter-from{
    opacity:0;
    transform:translateY(25px) scale(.95);
}

.prestamos-enter-to{
    opacity:1;
    transform:translateY(0) scale(1);
}

.prestamos-leave-from{
    opacity:1;
    transform:scale(1);
}

.prestamos-leave-to{
    opacity:0;
    transform:translateY(-20px) scale(.95);
}

.prestamos-leave-active{
    position:absolute;
}


</style>