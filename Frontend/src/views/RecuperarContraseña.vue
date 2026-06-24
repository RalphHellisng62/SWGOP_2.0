<script setup lang="ts">
import { ref } from 'vue';
import { recuperacionService } from '../services/recuperacionService';
import { EnvelopeIcon } from '@heroicons/vue/24/solid';
import router from '../router';

type Paso = 'enviar' | 'verificar' | 'cambiar';

const paso = ref<Paso>('enviar');
const email = ref('');
const codigo = ref('');
const nuevaContraseña = ref('');
const confirmarContraseña = ref('');
const verContraseña = ref(false);
const verConfirmar = ref(false);

const cargando = ref(false);
const error = ref('');
const exito = ref('');
const tiempoRestante = ref(300);

let intervalo: ReturnType<typeof setInterval>;

const enviarCodigo = async () => {
  error.value = '';
  exito.value = '';

  if (!email.value.trim()) {
    error.value = 'Ingresa tu email';
    return;
  }

  cargando.value = true;

  try {
    await recuperacionService.iniciarRecuperacion(email.value, 'email');
    exito.value = 'Código enviado a tu email';
    paso.value = 'verificar';
    tiempoRestante.value = 300;

    intervalo = setInterval(() => {
      tiempoRestante.value--;
      if (tiempoRestante.value <= 0) {
        clearInterval(intervalo);
        paso.value = 'enviar';
        error.value = 'Código expirado, intenta de nuevo';
      }
    }, 1000);
  } catch (err: any) {
    error.value = err.response?.data?.error || 'Error al enviar código';
  } finally {
    cargando.value = false;
  }
};

const verificarCodigo = async () => {
  error.value = '';

  if (!codigo.value.trim() || codigo.value.length !== 6) {
    error.value = 'Ingresa un código válido de 6 dígitos';
    return;
  }

  cargando.value = true;

  try {
    await recuperacionService.verificarCodigo(email.value, codigo.value);
    exito.value = 'Código verificado';
    paso.value = 'cambiar';
  } catch (err: any) {
    error.value = err.response?.data?.error || 'Código inválido';
  } finally {
    cargando.value = false;
  }
};

const cambiarContraseña = async () => {
  error.value = '';

  if (!nuevaContraseña.value) {
    error.value = 'Ingresa una nueva contraseña';
    return;
  }

  if (nuevaContraseña.value.length < 6) {
    error.value = 'La contraseña debe tener al menos 6 caracteres';
    return;
  }

  if (nuevaContraseña.value !== confirmarContraseña.value) {
    error.value = 'Las contraseñas no coinciden';
    return;
  }

  cargando.value = true;

  try {
    await recuperacionService.cambiarContraseñaRecuperacion(
      email.value,
      codigo.value,
      nuevaContraseña.value,
      confirmarContraseña.value
    );

    clearInterval(intervalo);
    exito.value = 'Contraseña cambiada exitosamente';

    setTimeout(() => {
      router.push('/login');
    }, 2000);
  } catch (err: any) {
    error.value = err.response?.data?.error || 'Error al cambiar contraseña';
  } finally {
    cargando.value = false;
  }
};

const formatearTiempo = (segundos: number) => {
  const mins = Math.floor(segundos / 60);
  const segs = segundos % 60;
  return `${mins}:${segs < 10 ? '0' : ''}${segs}`;
};

const volverAlLogin = () => {
  clearInterval(intervalo);
  router.push('/login');
};

const volverAEnviar = () => {
  clearInterval(intervalo);
  paso.value = 'enviar';
  error.value = '';
};
</script>

<template>
  <div class="min-h-screen bg-gradient-to from-[#344F37] to-[#611232] flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md">
      
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-[#344F37] mb-2">Recuperar contraseña</h1>
        <p class="text-gray-600 text-sm">Te enviaremos un código a tu email</p>
      </div>

      <!-- PASO 1: Enviar código -->
      <div v-if="paso === 'enviar'" class="space-y-4">
        
        <p class="text-gray-700 font-semibold">Ingresa tu email</p>

        <!-- Mensaje error -->
        <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded text-sm">
          {{ error }}
        </div>

        <!-- Input -->
        <input
          v-model="email"
          type="email"
          placeholder="tu@email.com"
          class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#344F37]"
        />
        
        <!-- Botones -->
        <div class="flex gap-2">
          <button
            @click="volverAlLogin"
            class="flex-1 py-2 bg-[#D9298A] hover:bg-[#690035] text-white font-semibold rounded-lg transition disabled:opacity-50"
          >
            Volver
          </button>
          <button
            @click="enviarCodigo"
            :disabled="cargando"
            class="flex-1 py-2 bg-[#344F37] hover:bg-[#98BF45] text-white font-semibold rounded-lg transition disabled:opacity-50"
          >
            {{ cargando ? 'Enviando...' : 'Enviar código' }}
          </button>
        </div>
      </div>

      <!-- PASO 2: Verificar código -->
      <div v-else-if="paso === 'verificar'" class="space-y-4">
        <div class="text-center">
          <p class="text-gray-700 font-semibold mb-2">Código recibido</p>
          <p class="text-sm text-gray-600 mb-4">Ingresa el código de 6 dígitos</p>
          <p class="text-sm font-semibold text-[#D9298A]">
            Tiempo restante: {{ formatearTiempo(tiempoRestante) }}
          </p>
        </div>

        <!-- Mensaje error -->
        <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded text-sm">
          {{ error }}
        </div>

        <!-- Input código -->
        <input
          v-model="codigo"
          type="text"
          maxlength="6"
          placeholder="000000"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#344F37] text-center text-2xl tracking-widest font-mono"
        />

        <!-- Botones -->
        <div class="flex gap-2">
          <button
            @click="volverAEnviar"
            class="flex-1 px-6 py-2 bg-[#D9298A] hover:bg-[#690035] text-white font-bold rounded-lg transition"
          >
            Atrás
          </button>
          <button
            @click="verificarCodigo"
            :disabled="cargando"
            class="flex-1 px-6 py-2 bg-[#344F37] hover:bg-[#98BF45] text-white font-bold rounded-lg transition"
          >
            {{ cargando ? 'Verificando...' : 'Verificar' }}
          </button>
        </div>
      </div>

      <!-- PASO 3: Cambiar contraseña -->
      <div v-else-if="paso === 'cambiar'" class="space-y-4">
        <p class="text-gray-700 font-semibold">Nueva contraseña</p>

        <!-- Mensaje error -->
        <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded text-sm">
          {{ error }}
        </div>

        <!-- Mensaje éxito -->
        <div v-if="exito" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded text-sm">
          {{ exito }}
        </div>

        <!-- Nueva contraseña -->
        <div class="relative">
          <input
            v-model="nuevaContraseña"
            :type="verContraseña ? 'text' : 'password'"
            placeholder="••••••••"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#344F37] pr-10"
          />
          <button
            type="button"
            @click="verContraseña = !verContraseña"
            class="absolute right-3 top-2.5 text-xl"
          >
            {{ verContraseña ? '🙈' : '👁️' }}
          </button>
        </div>

        <!-- Confirmar contraseña -->
        <div class="relative">
          <input
            v-model="confirmarContraseña"
            :type="verConfirmar ? 'text' : 'password'"
            placeholder="••••••••"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#344F37] pr-10"
          />
          <button
            type="button"
            @click="verConfirmar = !verConfirmar"
            class="absolute right-3 top-2.5 text-xl"
          >
            {{ verConfirmar ? '🙈' : '👁️' }}
          </button>
        </div>

        <!-- Botón -->
        <button
          @click="cambiarContraseña"
          :disabled="cargando"
          class="w-full py-2 bg-[#344F37] hover:bg-[#98BF45] text-white font-bold rounded-lg transition disabled:opacity-50"
        >
          {{ cargando ? 'Cambiando...' : 'Cambiar contraseña' }}
        </button>
      </div>

    </div>
  </div>
</template>
