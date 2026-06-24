<script setup lang="ts">
import { ref, onMounted } from 'vue';
import Sidebar from '../components/SideBar.vue';
import { authService } from '../services/authService';
import { useUsuario } from '../composables/useUsuario';
import { AtSymbolIcon, FolderArrowDownIcon, UserCircleIcon,
        EyeIcon, EyeSlashIcon 
} from '@heroicons/vue/24/solid';
import router from '../router';

const { usuarioGlobal, cargarUsuario, actualizarUsuario } = useUsuario();

const cargando = ref(true);
const guardando = ref(false);
const error = ref('');
const exito = ref(false);


// Campos del formulario
const username = ref('');
const email = ref('');
const fotoFile = ref<File | null>(null);
const fotoPreview = ref('');

// Campos de contraseña
const contraseñaActual = ref('');
const contraseñaNueva = ref('');
const contraseñaConfirmar = ref('');
const verActual = ref(false);
const verNueva = ref(false);
const verConfirmar = ref(false);

onMounted(async () => {
  await cargarPerfil();
});

const cargarPerfil = async () => {
  cargando.value = true;
  try {
    const response = await authService.obtenerPerfil();
    cargarUsuario(response.data);
    
    if (usuarioGlobal.value) {
      username.value = usuarioGlobal.value.username;
      email.value = usuarioGlobal.value.email;
      if (usuarioGlobal.value.foto) {
        fotoPreview.value = usuarioGlobal.value.foto;
      }
    }
  } catch (err) {
    console.error('Error al cargar perfil:', err);
    error.value = 'Error al cargar el perfil';
  } finally {
    cargando.value = false;
  }
};

const handleFoto = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  
  if (!file) return;
  
  error.value = '';
  
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

const guardarPerfil = async () => {
  error.value = '';

  if (!username.value.trim()) {
    error.value = 'El nombre de usuario es obligatorio';
    return;
  }

  if (
    contraseñaActual.value ||
    contraseñaNueva.value ||
    contraseñaConfirmar.value
  ) {
    if (!contraseñaActual.value) {
      error.value = 'Ingrese la contraseña actual';
      return;
    }

    if (contraseñaNueva.value.length < 6) {
      error.value = 'La nueva contraseña debe tener mínimo 6 caracteres';
      return;
    }

    if (contraseñaNueva.value !== contraseñaConfirmar.value) {
      error.value = 'Las contraseñas no coinciden';
      return;
    }
  }

  guardando.value = true;

  try {
    const datos: any = {
      username: username.value,
      email: email.value,
    };

    if (fotoFile.value) {
      datos.foto = fotoFile.value;
    }

    const response = await authService.actualizarPerfil(datos);
    actualizarUsuario(response.data);

    if (contraseñaNueva.value) {
      await authService.cambiarContraseña(
        contraseñaActual.value,
        contraseñaNueva.value
      );
    }

    exito.value = true;

    contraseñaActual.value = '';
    contraseñaNueva.value = '';
    contraseñaConfirmar.value = '';

    setTimeout(() => {
      exito.value = false;
    }, 2000);
  } catch (err: any) {
    error.value =
      err.response?.data?.detail ||
      err.response?.data?.error ||
      'Error al guardar';
  } finally {
    guardando.value = false;
  }
};

const obtenerUrlFoto = (foto?: string) => {
  if (!foto) return '';
  if (foto.startsWith('http')) return foto;
  return `http://localhost:8000${foto}`;
};
</script>

<template>
 <div class="flex min-h-screen">
    <Sidebar />

    <main class="flex-1 overflow-auto flex flex-col items-center justify-center p-6">
      

      <!-- Card centrada -->
      <div v-if="!cargando" class="w-full max-w-2xl mt-1 rounded-2xl overflow-hidden shadow-lg">
        <!-- Header verde -->
        <div class="bg-[#344F37] px-8 py-8 rounded-t-2xl">
          <h2 class="text-2xl font-bold text-white mb-2">Edición de perfil</h2>
          <p class="text-green-100 text-sm">Complete los siguientes datos para el cambio de perfil</p>
        </div>

        <!-- Card blanca -->
      <div class="bg-white rounded-b-2xl p-8">
        <!-- Mensaje de error -->
        <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4 text-sm">
          {{ error }}
        </div>

        <!-- Mensaje de éxito -->
        <transition name="fade">
          <div v-if="exito" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4 text-sm">
            ✓ Perfil actualizado exitosamente
          </div>
        </transition>

        <!-- Foto de perfil -->
        <div class="flex flex-col items-center mb-8">
          <h3 class="text-lg font-bold text-gray-800 mb-4">Cambiar foto de perfil</h3>

          <div class="relative">
            <img 
              v-if="fotoPreview"
              :src="obtenerUrlFoto(fotoPreview)"
              :alt="username"
              class="w-32 h-32 rounded-full object-cover border-4 border-[#344F37]"
            />
            

            <!-- Botón cambiar foto -->
            <label class="absolute bottom-0 right-0 p-2 rounded-full cursor-pointer transition shadow-lg">
              <FolderArrowDownIcon class="icono" />
              <input 
                type="file"
                accept="image/png,image/jpeg"
                @change="handleFoto"
                class="hidden"
              />
            </label>
          </div>
        </div>

        <!-- Formulario -->
        <form @submit.prevent="guardarPerfil" class="space-y-4">
          
          <!-- Username -->
          <div>
            <label class="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
              <UserCircleIcon class="icono" />
              Ingrese su nuevo nombre de usuario
            </label>
            <input 
              v-model="username"
              type="text"
              placeholder="Ejemplo: presidentsanJose"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#344F37]"
            />
          </div>

          <!-- Email -->
          <div>
            <label class="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
              <AtSymbolIcon class="icono" />
              Correo
            </label>
            <input 
              v-model="email"
              type="email"
              placeholder="Ejemplo: presidentsanJose"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#344F37]"
            />
          </div>

          <!-- CONTRASEÑAS -->

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

          <div class="pt-4 border-t">

            <h3 class="font-bold text-lg mb-4 text-gray-800">
              Cambiar contraseña
            </h3>

            <!-- ACTUAL -->
            <div class="relative mb-4">
              <input
                v-model="contraseñaActual"
                :type="verActual ? 'text':'password'"
                placeholder="Contraseña actual"
                class="w-full border border-gray-300 rounded-lg px-4 py-2 pr-12 focus:outline-none focus:ring-2 focus:ring-[#F2B035]"
              />
              <button
                type="button"
                @click="verActual=!verActual"
                class="absolute right-4 top-2.5 text-xl"
              >
                <EyeIcon
                v-if="!verActual"
                class="icono"
              />

              <EyeSlashIcon
                v-else
                class="icono"
              />
              </button>
            </div>

            <!-- NUEVA -->
            <div class="relative mb-4">
              <input
                v-model="contraseñaNueva"
                :type="verNueva ? 'text':'password'"
                placeholder="Nueva contraseña"
                class="w-full border border-gray-300 rounded-lg px-4 py-2 pr-12 focus:outline-none focus:ring-2 focus:ring-[#F2B035]"
              />
              <button
                type="button"
                @click="verNueva=!verNueva"
                class="absolute right-4 top-2.5 text-xl"
              >
                <EyeIcon
                v-if="!verNueva"
                class="icono"
              />

              <EyeSlashIcon
                v-else
                class="icono"
              />
              </button>
            </div>

            <!-- CONFIRMAR -->
            <div class="relative mb-4">
              <input
                v-model="contraseñaConfirmar"
                :type="verConfirmar ? 'text':'password'"
                placeholder="Confirmar contraseña"
                class="w-full border border-gray-300 rounded-lg px-4 py-2 pr-12 focus:outline-none focus:ring-2 focus:ring-[#F2B035]"
              />
              <button
                type="button"
                @click="verConfirmar=!verConfirmar"
                class="absolute right-4 top-2.5 text-xl"
              >
                <EyeIcon
                v-if="!verConfirmar"
                class="icono"
              />

              <EyeSlashIcon
                v-else
                class="icono"
              />
              </button>
            </div>
          </div>

          <!-- Botones -->
          <div class="flex gap-4 pt-6">
            <button 
              type="button"
              @click="() => router.back()"
              class="flex-1 px-6 py-2 bg-[#D9298A] hover:bg-[#690035] text-white font-bold rounded-lg transition"
            >
              Cancelar
            </button>
            <button 
              @click="guardarPerfil"
              :disabled="guardando"
              type="button"
              class="flex-1 px-6 py-2 bg-[#344F37] hover:bg-[#98BF45] text-white font-bold rounded-lg transition disabled:opacity-50"
            >
              {{ guardando ? 'Guardando...' : 'Guardar cambios' }}
            </button>
          </div>
        </form>
      </div>
    </div>

      <!-- Cargando -->
      <div v-else class="text-center mt-24">
        <p class="text-gray-600">Cargando perfil...</p>
      </div>
    </main>
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