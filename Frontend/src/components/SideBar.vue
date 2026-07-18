<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { authService } from '../services/authService';
import { useUsuario } from '../composables/useUsuario';
import { 
  ArrowRightStartOnRectangleIcon, 
  BookOpenIcon, 
  ChevronDoubleLeftIcon, 
  ChevronDoubleRightIcon,
  ClipboardDocumentListIcon, 
  
} from '@heroicons/vue/24/solid';
import router from '../router';
import { useRoute } from 'vue-router';

const route = useRoute();
const { usuarioGlobal, cargarUsuario, inicializarDesdeLocalStorage, limpiarUsuario } = useUsuario();

const claseBoton = (ruta: string) => {
  return route.path === ruta
    ? 'bg-[#344F37] text-white hover:bg-[#98BF45]'
    : 'bg-white text-[#344F37]';
};

const abierto = ref(true);

const toggleSidebar = () => {
  abierto.value = !abierto.value;
};

onMounted(async () => {
  console.log('🔄 Sidebar onMounted iniciado');

  if (!authService.estaAutenticado()) {
    console.log('⚠️ No hay token, cargando desde localStorage');
    inicializarDesdeLocalStorage();
    return;
  }

  try {
    console.log('📡 Intentando obtener perfil...');
    const response = await authService.obtenerPerfil();
    console.log('✅ Perfil cargado correctamente:', response.data);
    cargarUsuario(response.data);
  } catch (err: any) {
    console.error('❌ Error al cargar perfil:', err.response?.status, err.response?.data || err.message);
    
    if (err.response?.status === 401) {
      console.log('🔑 Token inválido o expirado → Cerrando sesión');
      authService.logout();
      window.location.href = '/login';
    } else {
      console.log('📦 Cargando desde localStorage como fallback');
      inicializarDesdeLocalStorage();
    }
  }
});

const cerrarSesion = () => {
  limpiarUsuario();
  authService.logout();
  window.location.href = '/login';
};

const editarPerfil = () => {
  router.push('/editarPerfil');
};

const irAInventario = () => {
  router.push('/inventario');
};

const irAPrestamos = () => {
  router.push('/prestamos');
};

const obtenerUrlFoto = (foto?: string) => {
  if (!foto) return '';
  if (foto.startsWith('http')) return foto;
  return `http://localhost:8000${foto}`;
};
</script>

<template>
  <div 
    :class="[
      'bg-white shadow-lg flex flex-col rounded-4xl transition-all duration-300',
      abierto ? 'w-64' : 'w-20', 
      'min-h-screen'
    ]"
  >
    <!-- Toggle -->
    <div class="flex justify-end p-4 bg-white rounded-tl-4xl rounded-tr-4xl">
      <button @click="toggleSidebar" class="text-gray-700">
        <ChevronDoubleLeftIcon v-if="abierto" class="icono" />
        <ChevronDoubleRightIcon v-else class="icono" />
      </button>
    </div>

    <!-- Logo -->
    <div class="pt-0 px-6 pb-6">
      <div class="flex justify-center mb-1 -mt-4" v-if="abierto">
        <div class="w-32 h-32 rounded-full flex items-center justify-center">
          <img
            src="/LOGO SAN JOSE.png"
            alt="Logo"
            class="w-full h-full object-contain"
          />
        </div>
      </div>

      <div class="relative mt-3">
        <div class="min-h-0.5 bg-[#98BF45] rounded-full">
          <div class="absolute left-0 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-[#98BF45]"></div>
          <div class="absolute right-0 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-[#98BF45]"></div>
        </div>
      </div>
    </div>

    <!-- Perfil -->
    <div class="p-6 border-b border-green-200">
      <div class="flex justify-center mb-4" v-if="abierto">
        <div class="relative">
          <img
            v-if="usuarioGlobal?.foto"
            :key="usuarioGlobal.foto"
            :src="obtenerUrlFoto(usuarioGlobal.foto)"
            :alt="usuarioGlobal?.username"
            class="w-20 h-20 rounded-full object-cover border-2 border-[#344F37]"
          />
          <div 
            v-else 
            class="w-20 h-20 bg-gradient-to from-pink-300 to-pink-400 rounded-full flex items-center justify-center text-2xl border-4 border-[#344F37]"
          >
            👤
          </div>
        </div>
      </div>

      <div class="text-center mb-4" v-if="abierto">
        <p class="text-gray-600 text-sm">@{{ usuarioGlobal?.username || 'Usuario' }}</p>
      </div>

      <button
        v-if="abierto"
        @click="editarPerfil"
        class="w-full text-center text-[#344F37] font-semibold underline py-2 hover:text-[#98BF45] transition-colors"
      >
        Editar perfil
      </button>

      <div class="relative mt-5">
        <div class="min-h-0.5 bg-[#98BF45]">
          <div class="absolute left-0 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-[#98BF45]"></div>
          <div class="absolute right-0 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-[#98BF45]"></div>
        </div>
      </div>
    </div>

    <!-- Navegación -->
    <div class="flex-1 p-6 space-y-3">
      <button
        @click="irAInventario"
        :class="[
          claseBoton('/inventario'),
          'w-full font-semibold py-3 rounded-4xl flex items-center justify-center gap-2 transition-all duration-300'
        ]"
      >
        <BookOpenIcon class="w-6 h-6" />
        <span v-if="abierto">Inventario</span>
      </button>

      <button
        @click="irAPrestamos"
        :class="[
          claseBoton('/prestamos'),
          'w-full font-semibold py-3 rounded-4xl flex items-center justify-center gap-2 transition-all duration-300'
        ]"
      >
        <ClipboardDocumentListIcon class="w-6 h-6" />
        <span v-if="abierto">Préstamos</span>
      </button>
    </div>

    <!-- Cerrar Sesión -->
    <div class="p-6">
      <div class="relative mb-6">
        <div class="min-h-0.5 bg-[#98BF45]">
          <div class="absolute left-0 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-[#98BF45]"></div>
          <div class="absolute right-0 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-[#98BF45]"></div>
        </div>
      </div>

      <button
        @click="cerrarSesion"
        class="w-full text-[#344F37] font-semibold underline text-center py-2 flex items-center justify-center gap-2 hover:text-[#98BF45] transition-colors"
      >
        <ArrowRightStartOnRectangleIcon class="icono" />
        <span v-if="abierto">Cerrar sesión</span>
      </button>
    </div>
  </div>
</template>