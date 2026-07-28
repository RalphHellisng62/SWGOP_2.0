<script setup lang="ts">
import { ref } from 'vue';
import { authService } from '../services/authService';
import { useRouter } from 'vue-router';
import { LockClosedIcon, UserCircleIcon } from '@heroicons/vue/24/solid';
import TerminosModal from '../components/TerminosModal.vue';
import RecuperacionModal from '../components/RecuperarContraseña.vue';

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

    // DEBUG: Ver qué devuelve el servidor
    console.log('RESPUESTA COMPLETA:', response);
    console.log('response.data:', response.data);
    console.log(' Claves disponibles:', Object.keys(response.data || {}));

    // Validación más segura de la respuesta
    if (!response.data?.access || !response.data?.refresh) {
      console.error('Estructura inesperada. Esperamos access y refresh, pero tenemos:', response.data);
      throw new Error('Respuesta inválida del servidor');
    }

    authService.guardarToken(
      response.data.access,
      response.data.refresh,
      response.data.usuario || response.data.user
    );

    console.log('Tokens guardados correctamente');

    loginExitoso.value = true;
    
    // Pequeño delay para mostrar mensaje de éxito
    setTimeout(() => {
      router.push('/inventario');
    }, 800);

  } catch (err: any) {
    console.error('Error de login:', err);
    console.error('Response status:', err.response?.status);
    console.error('Response data:', err.response?.data);
    
    error.value = err.response?.data?.detail 
      || err.response?.data?.message 
      || err.message
      || 'Credenciales incorrectas. Inténtalo de nuevo.';
  } finally {
    cargando.value = false;
  }
};

const aceptarTerminos = () => {
  mostrarTerminos.value = false;
};

const mostrarRecuperacion = ref(false);
</script>

<template>
  <div class="min-h-screen bg-cover bg-center relative">
    <div class="absolute inset-0"></div>
    
    <div class="relative flex items-center justify-end h-screen px-20 ">
      <!-- Panel izquierdo -->
      <div class="hidden lg:flex items-center justify-between anim-left w-[calc(100%-28rem)] h-[60%] rounded-[26px] bg-black/50 backdrop-blur-[5px] text-white p-8 gap-8 transition-all duration-300 hover:scale-105">

      <!-- LADO IZQUIERDO: Logo (40%) -->
      <div class="w-[40%] flex flex-col items-center justify-center text-center">
        <img
          src="/LOGO SAN JOSE.png"
          alt="Barrio de San José"
          class="w-full max-w-85 object-contain drop-shadow-xl anim-logo"
        />
      </div>

      <!-- LÍNEA DIVISORIA EN MEDIO -->
      <div class="relative h-[95%] w-0.5 shrink-0">
        
        <div class="h-full w-full bg-linear-to-b from-transparent via-[#98BF45] to-transparent"></div>
        <!-- Puntos decorativos en los extremos -->
        <div class="absolute top-0 left-1/2 -translate-x-1/2 w-2 h-2 rounded-full bg-[#98BF45] shadow-[0_0_8px_#98BF45]"></div>
        <div class="absolute bottom-0 left-1/2 -translate-x-1/2 w-2 h-2 rounded-full bg-[#98BF45] shadow-[0_0_8px_#98BF45]"></div>
      </div>

      <!-- LADO DERECHO: Contenido y Textos (60%) -->
      <div class="w-[60%] h-[90%] flex flex-col justify-between py-6">
        

        <!-- Título Principal -->
        <div class="my-auto">
          <h1 class="italic text-3xl xl:text-4xl font-light leading-snug mb-13">
            Sistema Web de Información y Gestión Bibliotecaria 
            <span class="font-bold text-white block mt-1">(S.W.I.G.B)</span>
          </h1>
        </div>

        <!-- Copyright / Botón Términos -->
        <div>
          <button 
            @click="mostrarTerminos = true"
            class="text text-white hover:text-[#98BF45] transition-all duration-300 ease-out hover:scale-105 cursor-pointer text-left group"
          >
          <span class="underline group-hover:text-[#98BF45]">© Presidencia de comunidad del Barrio de San José | 
          Términos de Uso | Aviso Institucional</span>
          </button>
        </div>

      </div>

    </div>
    
      <!-- Formulario de Login -->
      <div class="anim-right bg-white rounded-[26px] shadow-2xl p-8 w-full max-w-md h-[60%] flex flex-col justify-center shrink-0 transition-all duration-300 hover:scale-105">
        <h1 class="text-3xl font-bold text-center mb-1 text-gray-800">Iniciar sesión</h1>
        <!-- Espacio reservado para alertas (altura fija) -->
        <div class="h-16 mb-2">
          <div v-if="loginExitoso" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded h-full flex items-center">
            ¡Login exitoso! Redirigiendo...
          </div>

          <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded h-full flex items-center">
            {{ error }}
          </div>
        </div>

        <form @submit.prevent="iniciarSesion" class="space-y-6">
          <div>
            <label class="block text-gray-700 font-semibold mb-4 mt-3">Usuario</label>
            <div class="relative">
              <UserCircleIcon class="w-5 absolute mt-3 ml-3 icono" />
              <input 
                v-model="usuario"
                type="text" 
                placeholder="Ingresa tu usuario"
                class="w-full px-10 py-3 bg-gray-200 border border-gray-300 rounded-lg focus:outline-none focus:border-[#344F37] transition-all duration-300 ease-out hover:shadow-md"
                required
              />
            </div>
          </div>

          <div>
            <label class="block text-gray-700 font-semibold mb-4 mt-3">Contraseña</label>
            <div class="relative">
              <LockClosedIcon class="w-5 h-5 absolute mt-3 ml-3 icono" />
              <input 
                v-model="contraseña"
                type="password" 
                placeholder="Ingresa tu contraseña"
                  class="w-full px-10 py-3 bg-gray-200 border border-gray-300 rounded-lg transition-all duration-300 focus:outline-none focus:border-[#344F37] focus:shadow-md ease-out hover:shadow-md"
                required
              />
            </div>
          </div>

          <div class="text-right mb-2">
          <button
            type="button"
            @click="mostrarRecuperacion = true"
            class="text-sm text-[#344F37] hover:text-[#98BF45] hover:tracking-wide transition-all duration-300 underline"
          >
            ¿Olvidaste tu contraseña?
          </button>
        </div>

          <button 
            type="submit"
            :disabled="cargando"
            class="w-full bg-[#344F37] hover:bg-[#98BF45] hover:scale-[1.02] active:scale-95 transition-all duration-300 text-white font-bold py-3 rounded-4xl disabled:opacity-50"
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

  <RecuperacionModal
    :isOpen="mostrarRecuperacion"
    @cerrar="mostrarRecuperacion = false"
        />
</template>

<style scoped>
@keyframes fadeLeft {
  from {
    opacity: 0;
    transform: translateX(-40px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeRight {
  from {
    opacity: 0;
    transform: translateX(40px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes logo {
  from {
    opacity: 0;
    transform: scale(.85);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.anim-left{
  animation: fadeLeft .8s ease forwards;
}

.anim-right{
  animation: fadeRight .8s ease forwards;
}

.anim-logo{
  animation: logo .9s ease forwards;
}
</style>