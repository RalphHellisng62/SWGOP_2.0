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

// Validar formato de email
const validarEmail = (emailValue: string): boolean => {
  const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regexEmail.test(emailValue);
};

const guardarPerfil = async () => {
  error.value = '';

  if (!username.value.trim()) {
    error.value = 'El nombre de usuario es obligatorio';
    return;
  }

  if (!email.value.trim()) {
    error.value = 'El correo es obligatorio';
    return;
  }

  if (!validarEmail(email.value)) {
    error.value = 'Ingrese un correo válido (ej: usuario@gmail.com, usuario@outlook.com)';
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
  <div class="flex min-h-screen animate-page">
    <Sidebar />

    <main class="flex-1 overflow-auto flex flex-col items-center justify-center p-6">
      <!-- Card centrada -->
      <div v-if="!cargando" class="w-full max-w-2xl mt-2 rounded-4xl overflow-hidden shadow-lg transition-transform duration-300 hover:scale-[1.02]">
        
        <!-- Header verde -->
        <div class="bg-[#344F37] px-8 py-8 rounded-t-2xl">
          <h2 class="text-2xl font-bold text-white mb-2">Edición de perfil</h2>
          <p class="text-green-100 text-sm">Complete los siguientes datos para el cambio de perfil</p>
        </div>

        <!-- Card blanca -->
        <div class="bg-white rounded-b-2xl p-8">
          <!-- ... mensajes de error y éxito igual ... -->

          <!-- Foto de perfil -->
          <div class="flex flex-col items-center mb-8">
            <h3 class="text-lg font-bold text-gray-800 mb-4">Cambiar foto de perfil</h3>

            <div class="relative group">
              <img 
                v-if="fotoPreview"
                :src="obtenerUrlFoto(fotoPreview)"
                :alt="username"
                class="w-32 h-32 rounded-full object-cover border-4 border-[#344F37] transition-all duration-300 group-hover:scale-110 group-hover:shadow-2xl"
              />
              
              <!-- Botón cambiar foto -->
              <label class="absolute bottom-0 right-0 p-2 rounded-full cursor-pointer transition-all duration-300 hover:scale-125 bg-white shadow-lg hover:shadow-xl">
                <FolderArrowDownIcon class="w-6 h-6 text-[#98BF45] transition-transform" />
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
                <UserCircleIcon class="icono transition-transform hover:scale-110" />
                Ingrese su nuevo nombre de usuario
              </label>
              <input 
                v-model="username"
                type="text"
                placeholder="Ejemplo: presidentsanJose"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#344F37] transition-all duration-300 hover:scale-[1.02] focus:scale-[1.02]"
              />
            </div>

            <!-- Email -->
            <div>
              <label class="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                <AtSymbolIcon class="icono transition-transform hover:scale-110" />
                Correo
              </label>
              <input 
                v-model="email"
                type="email"
                placeholder="Ejemplo: usuario@gmail.com"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#344F37] transition-all duration-300 hover:scale-[1.02] focus:scale-[1.02]"
              />
              <p class="text-xs text-gray-500 mt-1">Aceptamos: Gmail, Outlook, Yahoo, Hotmail, etc.</p>
            </div>

            <!-- Contraseñas (mantengo igual la estructura) -->
            <div class="pt-1">
              <h3 class="font-bold text-lg mb-4 text-gray-800">Cambiar contraseña</h3>

              <!-- ACTUAL, NUEVA y CONFIRMAR con hover en inputs e iconos -->
              <div class="relative mb-4">
                <input
                  v-model="contraseñaActual"
                  :type="verActual ? 'text':'password'"
                  placeholder="Contraseña actual"
                  class="w-full border border-gray-300 rounded-lg px-4 py-2 pr-12 focus:outline-none focus:ring-2 focus:ring-[#F2B035] transition-all duration-300 hover:scale-[1.02]"
                />
                <button
                  type="button"
                  @click="verActual=!verActual"
                  class="absolute right-4 top-2.5 text-xl transition-transform hover:scale-125"
                >
                  <EyeIcon v-if="!verActual" class="icono" />
                  <EyeSlashIcon v-else class="icono" />
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
                <EyeIcon v-if="!verNueva" class="icono" />
                <EyeSlashIcon v-else class="icono" />
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
                <EyeIcon v-if="!verConfirmar" class="icono" />
                <EyeSlashIcon v-else class="icono" />
              </button>
            </div>
          </div>

            <!-- Botones -->
            <div class="flex gap-4 pt-6">
              <button 
                type="button"
                @click="() => router.back()"
                class="flex-1 px-6 py-2 bg-[#D9298A] hover:bg-[#690035] text-white font-bold rounded-4xl transition-all duration-300 hover:scale-105 active:scale-95"
              >
                Cancelar
              </button>
              <button 
                @click="guardarPerfil"
                :disabled="guardando"
                type="button"
                class="flex-1 px-6 py-2 bg-[#344F37] hover:bg-[#98BF45] text-white font-bold rounded-4xl transition-all duration-300 hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ guardando ? 'Guardando...' : 'Guardar cambios' }}
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Cargando ... -->
    </main>
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



.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}


input, button, label {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.icono {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Efecto suave extra en la card completa */
.shadow-lg {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}
</style>