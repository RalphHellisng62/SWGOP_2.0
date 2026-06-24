<script setup lang="ts">
import { ref } from 'vue';
import { authService } from '../services/authService';
import { useRouter } from 'vue-router';
import { KeyIcon, UserCircleIcon } from '@heroicons/vue/24/solid';
import TerminosModal from '../components/TerminosModal.vue';

const router = useRouter();

const usuario = ref('');
const contraseña = ref('');
const cargando = ref(false);
const error = ref('');
const loginExitoso = ref(false);
const mostrarTerminos = ref(false);

const iniciarSesion = async () => {
  if (!usuario.value || !contraseña.value) {
    error.value = 'Por favor ingresa usuario y contraseña';
    return;
  }

  cargando.value = true;
  error.value = '';

  try {
    const response = await authService.login({
      username: usuario.value,
      password: contraseña.value
    });

    // Validación más segura de la respuesta
    if (!response.data?.access || !response.data?.refresh) {
      throw new Error('Respuesta inválida del servidor');
    }

    authService.guardarToken(
      response.data.access,
      response.data.refresh,
      response.data.usuario || response.data.user
    );

    loginExitoso.value = true;
    
    // Pequeño delay para mostrar mensaje de éxito
    setTimeout(() => {
      router.push('/inventario');
    }, 800);

  } catch (err: any) {
    console.error('Error de login:', err);
    error.value = err.response?.data?.detail 
      || err.response?.data?.message 
      || 'Credenciales incorrectas. Inténtalo de nuevo.';
  } finally {
    cargando.value = false;
  }
};

const aceptarTerminos = () => {
  mostrarTerminos.value = false;
};
</script>

<template>
  <div class="min-h-screen bg-cover bg-center relative">
    <div class="absolute inset-0 bg-black/25"></div>
    
    <div class="relative flex items-center justify-end h-screen pr-20">
      <!-- Panel izquierdo -->
      <div class="hidden lg:flex flex-col justify-end w-[calc(100%-28rem)] h-[60%] rounded-[26px] bg-black/25 backdrop-blur-[5px] text-white px-10 py-8">
        <h1 class="text-6xl font-light leading-tight max-w-4xl">
          Sistema Web de Gestión Operativa Presidencial
        </h1>
        <p class="mt-8 text-2xl">Presidencia del Barrio de San José</p>
        
        <button 
          @click="mostrarTerminos = true"
          class="mt-10 text-sm text-white hover:text-[#4EBFD9] font-semibold transition underline"
        >
          Términos y Condiciones
        </button>
      </div>

      <!-- Formulario de Login -->
      <div class="bg-white rounded-[26px] shadow-2xl p-8 w-full max-w-md h-[60%] flex flex-col justify-center shrink-0">
        <h1 class="text-3xl font-bold text-center mb-8 text-gray-800">Iniciar sesión</h1>

        <div v-if="loginExitoso" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
          ¡Login exitoso! Redirigiendo...
        </div>

        <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {{ error }}
        </div>

        <form @submit.prevent="iniciarSesion" class="space-y-6">
          <div>
            <label class="block text-gray-700 font-semibold mb-2">Usuario</label>
            <div class="relative">
              <UserCircleIcon class="w-5 absolute mt-3 ml-3 icono" />
              <input 
                v-model="usuario"
                type="text" 
                placeholder="Ingresa tu usuario"
                class="w-full px-10 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-[#344F37]"
                required
              />
            </div>
          </div>

          <div>
            <label class="block text-gray-700 font-semibold mb-2">Contraseña</label>
            <div class="relative">
              <KeyIcon class="w-5 h-5 absolute mt-3 ml-3 icono" />
              <input 
                v-model="contraseña"
                type="password" 
                placeholder="Ingresa tu contraseña"
                class="w-full px-10 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-[#344F37]"
                required
              />
            </div>
          </div>

          <div class="text-right">
            <router-link
              to="/recuperar-contraseña"
              class="text-sm text-[#344F37] hover:text-[#98BF45] font-semibold transition underline"
            >
              ¿Olvidaste tu contraseña?
            </router-link>
          </div>

          <button 
            type="submit"
            :disabled="cargando"
            class="w-full bg-[#344F37] hover:bg-[#98BF45] text-white font-bold py-3 rounded-lg transition disabled:opacity-50"
          >
            {{ cargando ? 'Iniciando sesión...' : 'Iniciar sesión' }}
          </button>
        </form>
      </div>
    </div>
  </div>

  <TerminosModal 
    :isOpen="mostrarTerminos" 
    :onAceptar="aceptarTerminos" 
    :onCerrar="() => (mostrarTerminos = false)" 
  />
</template>