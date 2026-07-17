<script setup lang="ts">
import { ref } from 'vue';
import { recuperacionService } from '../services/recuperacionService';
import { EnvelopeIcon, XCircleIcon, EyeIcon, EyeSlashIcon } from '@heroicons/vue/24/solid';

const props = defineProps<{
    isOpen: boolean
}>()

const emit = defineEmits<{
    cerrar: []
}>()

type Paso = 'enviar' | 'verificar' | 'cambiar' | 'completado';

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

let intervalo: ReturnType<typeof setInterval> | null = null;

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
        clearInterval(intervalo!);
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

    if (intervalo) clearInterval(intervalo);
    exito.value = 'Contraseña cambiada exitosamente';

    setTimeout(() => {
      paso.value = 'completado';
    }, 1500);
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
  if (intervalo) clearInterval(intervalo);
  emit('cerrar');
};

const volverAEnviar = () => {
  if (intervalo) clearInterval(intervalo);
  paso.value = 'enviar';
  error.value = '';
  exito.value = '';
};
</script>

<template>
  <Transition name="step" mode="out-in">
    <div v-if="props.isOpen" class="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md">

        <!-- Header -->
        <div class="flex justify-between items-start px-6 py-5 bg-[#344F37] rounded-2xl">
          <div>
            <h2 class="text-2xl font-bold text-white">Recuperar contraseña</h2>
            <p class="text-gray-300 text-sm mt-1">Sigue los pasos para cambiar tu contraseña</p>
          </div>
          <button @click="emit('cerrar')" class="text-gray-400 hover:text-white transition">
            <XCircleIcon class="w-7 h-7 icono2" />
          </button>
        </div>

        <!-- Progress Bar -->
        <div class="px-6 pt-6">
          <div class="flex items-center justify-between">
            <!-- Paso 1 -->
            <div class="w-8 h-8 rounded-full flex items-center justify-center text-white transition-colors"
                :class="paso === 'enviar' ? 'bg-[#344F37]' : 'bg-[#98BF45]'">
              1
            </div>

            <!-- Línea 1 -->
            <div class="flex-1 h-1 bg-gray-300 mx-2 relative">
              <div class="h-1 bg-[#98BF45] transition-all duration-500 absolute left-0 top-0"
                  :style="{ width: ['verificar','cambiar','completado'].includes(paso) ? '100%' : '0%' }"></div>
            </div>

            <!-- Paso 2 -->
            <div class="w-8 h-8 rounded-full flex items-center justify-center text-white transition-colors"
                :class="['verificar','cambiar','completado'].includes(paso) ? 'bg-[#344F37]' : 'bg-gray-200 text-gray-500'">
              2
            </div>

            <!-- Línea 2 -->
            <div class="flex-1 h-1 bg-gray-300 mx-2 relative">
              <div class="h-1 bg-[#98BF45] transition-all duration-500 absolute left-0 top-0"
                  :style="{ width: ['cambiar','completado'].includes(paso) ? '100%' : '0%' }"></div>
            </div>

            <!-- Paso 3 -->
            <div class="w-8 h-8 rounded-full flex items-center justify-center text-white transition-colors"
                :class="['cambiar','completado'].includes(paso) ? 'bg-[#344F37]' : 'bg-gray-200 text-gray-500'">
              3
            </div>

            <!-- Línea 3 -->
            <div class="flex-1 h-1 bg-gray-300 mx-2 relative">
              <div class="h-1 bg-[#98BF45] transition-all duration-500 absolute left-0 top-0"
                  :style="{ width: paso === 'completado' ? '100%' : '0%' }"></div>
            </div>

            <!-- Paso 4 -->
            <div class="w-8 h-8 rounded-full flex items-center justify-center text-white transition-colors"
                :class="paso === 'completado' ? 'bg-[#344F37]' : 'bg-gray-200 text-gray-500'">
              4
            </div>
          </div>

          <p class="text-center text-sm mt-3 text-gray-500">
            Paso {{ paso === 'enviar' ? 1 : paso === 'verificar' ? 2 : paso === 'cambiar' ? 3 : 4 }} de 4
          </p>
        </div>

        <!-- PASO 1 -->
        <div v-if="paso === 'enviar'" key="enviar" class="px-1 pt-3 space-y-4">
          <p class="text-gray-700 font-semibold">Ingresa tu email</p>

          <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded text-sm">
            {{ error }}
          </div>

          <div class="relative">
            <input
              v-model="email"
              type="email"
              placeholder="Ingrese el email asociado a tu cuenta"
              class="w-full px-4 py-3 border border-[#344F37] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#344F37]"
            />
            <EnvelopeIcon class="icono absolute right-4 top-4 text-gray-400" />
          </div>

          <div class="flex gap-2">
            <button @click="volverAlLogin"
                    class="flex-1 py-3 bg-[#D9298A] hover:bg-[#690035] text-white font-semibold rounded-lg transition">
              Volver
            </button>
            <button @click="enviarCodigo" :disabled="cargando"
                    class="flex-1 py-3 bg-[#344F37] hover:bg-[#98BF45] text-white font-semibold rounded-lg transition disabled:opacity-50">
              {{ cargando ? 'Enviando...' : 'Enviar código' }}
            </button>
          </div>
        </div>

        <!-- PASO 2 -->
        <div v-else-if="paso === 'verificar'" key="verificar" class="px-1 pt-3 space-y-4">
          <div class="text-center">
            <p class="text-gray-700 font-semibold mb-2">Código recibido</p>
            <p class="text-sm text-gray-600 mb-4">Ingresa el código de 6 dígitos</p>
            <p class="text-sm font-semibold text-[#D9298A]">
              Tiempo restante: {{ formatearTiempo(tiempoRestante) }}
            </p>
          </div>

          <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded text-sm">
            {{ error }}
          </div>

          <input
            v-model="codigo"
            type="text"
            maxlength="6"
            placeholder="000000"
            class="w-full px-4 py-3 border border-[#344F37] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#344F37] text-center text-2xl tracking-widest font-mono"
          />

          <div class="flex gap-2">
            <button @click="volverAEnviar"
                    class="flex-1 py-3 bg-[#D9298A] hover:bg-[#690035] text-white font-bold rounded-lg transition">
              Atrás
            </button>
            <button @click="verificarCodigo" :disabled="cargando"
                    class="flex-1 py-3 bg-[#344F37] hover:bg-[#98BF45] text-white font-bold rounded-lg transition disabled:opacity-50">
              {{ cargando ? 'Verificando...' : 'Verificar' }}
            </button>
          </div>
        </div>

        <!-- PASO 3 -->
        <div v-else-if="paso === 'cambiar'" key="cambiar" class="px-1 pt-3 space-y-4">
          <p class="text-gray-700 font-semibold">Nueva contraseña</p>

          <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded text-sm">
            {{ error }}
          </div>
          <div v-if="exito" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded text-sm">
            {{ exito }}
          </div>

          <!-- Nueva contraseña -->
          <div class="relative">
            <input
              v-model="nuevaContraseña"
              :type="verContraseña ? 'text' : 'password'"
              placeholder="Nueva contraseña"
              class="w-full px-4 py-3 border border-[#344F37] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#344F37] pr-12"
            />
            <button type="button" @click="verContraseña = !verContraseña"
                    class="icono absolute right-4 top-3.5 text-gray-500">
              <EyeIcon v-if="verContraseña" class="w-5 h-5" />
              <EyeSlashIcon v-else class="w-5 h-5" />
            </button>
          </div>

          <!-- Confirmar -->
          <div class="relative">
            <input
              v-model="confirmarContraseña"
              :type="verConfirmar ? 'text' : 'password'"
              placeholder="Confirmar contraseña"
              class="w-full px-4 py-3 border border-[#344F37] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#344F37] pr-12"
            />
            <button type="button" @click="verConfirmar = !verConfirmar"
                    class="icono absolute right-4 top-3.5 text-gray-500">
              <EyeIcon v-if="verConfirmar" class="w-5 h-5" />
              <EyeSlashIcon v-else class="w-5 h-5" />
            </button>
          </div>

          <button @click="cambiarContraseña" :disabled="cargando"
                  class="w-full py-3 bg-[#344F37] hover:bg-[#98BF45] text-white font-bold rounded-lg transition disabled:opacity-50">
            {{ cargando ? 'Cambiando...' : 'Cambiar contraseña' }}
          </button>
        </div>

        <!-- PASO 4 - Completado -->
        <div v-else-if="paso === 'completado'" key="completado" class="px-1 pt-3 space-y-4">
          <div class="w-24 h-24 rounded-full bg-green-100 mx-auto flex items-center justify-center">
            <span class="text-6xl">✅</span>
          </div>
          <h2 class="text-2xl font-bold text-[#344F37]">¡Contraseña actualizada!</h2>
          <p class="text-gray-600">Ahora puedes iniciar sesión con tu nueva contraseña.</p>

          <button @click="emit('cerrar')"
                  class="w-full py-3 rounded-xl bg-[#344F37] hover:bg-[#98BF45] text-white font-bold transition">
            Volver al inicio de sesión
          </button>
        </div>

      </div>
    </div>
  </Transition>
</template>