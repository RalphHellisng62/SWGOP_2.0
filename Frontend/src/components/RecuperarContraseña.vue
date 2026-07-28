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
  <Transition name="fade-modal">
    <div v-if="props.isOpen" class="fixed inset-0 bg-black/25 backdrop-blur-sm flex items-center justify-center z-50 p-4 select-none">
      <div class="bg-white rounded-3xl shadow-2xl p-6 w-full max-w-md transform transition-all">

        <!-- Header -->
        <div class="flex justify-between items-start px-6 py-5 bg-[#344F37] rounded-4xl shadow-md">
          <div>
            <h2 class="text-2xl font-bold text-white">Recuperar contraseña</h2>
            <p class="text-gray-200 text-sm mt-1">Sigue los pasos para cambiar tu contraseña</p>
          </div>
          <button 
            @click="emit('cerrar')" 
            class="text-gray-300 hover:text-white transition-all duration-300 hover:scale-110 active:scale-90 cursor-pointer p-1"
          >
            <XCircleIcon class="w-7 h-7" />
          </button>
        </div>

        <!-- Progress Bar -->
        <div class="px-2 pt-6">
          <div class="flex items-center justify-between">
            <!-- Paso 1 -->
            <div class="w-8 h-8 rounded-full flex items-center justify-center font-bold text-white transition-all duration-300 shadow-sm"
                :class="paso === 'enviar' ? 'bg-[#344F37] scale-110' : 'bg-[#98BF45]'">
              1
            </div>

            <!-- Línea 1 -->
            <div class="flex-1 h-1 bg-gray-400 mx-2 relative rounded-full overflow-hidden">
              <div class="h-1 bg-[#98BF45] transition-all duration-500 absolute left-0 top-0"
                  :style="{ width: ['verificar','cambiar','completado'].includes(paso) ? '100%' : '0%' }"></div>
            </div>

            <!-- Paso 2 -->
            <div class="w-8 h-8 rounded-full flex items-center justify-center font-bold text-white transition-all duration-300 shadow-sm"
                :class="['verificar','cambiar','completado'].includes(paso) ? (paso === 'verificar' ? 'bg-[#344F37] scale-110' : 'bg-[#98BF45]') : 'bg-gray-400 text-gray-200'">
              2
            </div>

            <!-- Línea 2 -->
            <div class="flex-1 h-1 bg-gray-400 mx-2 relative rounded-full overflow-hidden">
              <div class="h-1 bg-[#98BF45] transition-all duration-500 absolute left-0 top-0"
                  :style="{ width: ['cambiar','completado'].includes(paso) ? '100%' : '0%' }"></div>
            </div>

            <!-- Paso 3 -->
            <div class="w-8 h-8 rounded-full flex items-center justify-center font-bold text-white transition-all duration-300 shadow-sm"
                :class="['cambiar','completado'].includes(paso) ? (paso === 'cambiar' ? 'bg-[#344F37] scale-110' : 'bg-[#98BF45]') : 'bg-gray-400 text-gray-200'">
              3
            </div>

            <!-- Línea 3 -->
            <div class="flex-1 h-1 bg-gray-400 mx-2 relative rounded-full overflow-hidden">
              <div class="h-1 bg-[#98BF45] transition-all duration-500 absolute left-0 top-0"
                  :style="{ width: paso === 'completado' ? '100%' : '0%' }"></div>
            </div>

            <!-- Paso 4 -->
            <div class="w-8 h-8 rounded-full flex items-center justify-center font-bold text-white transition-all duration-300 shadow-sm"
                :class="paso === 'completado' ? 'bg-[#344F37] scale-110' : 'bg-gray-400 text-gray-200'">
              4
            </div>
          </div>

          <p class="text-center text-sm mt-3 text-gray-500 font-medium">
            Paso {{ paso === 'enviar' ? 1 : paso === 'verificar' ? 2 : paso === 'cambiar' ? 3 : 4 }} de 4
          </p>
        </div>

        <!-- Transición interna para los pasos -->
        <Transition name="fade-step" mode="out-in">
          
          <!-- PASO 1 -->
          <div v-if="paso === 'enviar'" key="enviar" class="px-1 pt-4 space-y-4">
            <p class="text-gray-700 font-semibold">Por favor, ingrese el correo electrónico asociado a su cuenta</p>

            <div v-if="error" class="bg-red-50 border-l-4 border-red-500 text-red-700 p-3 rounded-lg text-sm animate-pulse">
              {{ error }}
            </div>

            <div class="relative">
              <input
                v-model="email"
                type="email"
                placeholder="example@correo.com"
                class="w-full px-4 py-3 bg-gray-200 border border-gray-300 rounded-lg focus:outline-none focus:border-[#344F37] transition-all duration-300 ease-out hover:shadow-md"
              />
              <EnvelopeIcon class="w-6 h-6 icono absolute right-4 top-3.5 pointer-events-none" />
            </div>

            <div class="flex gap-3 pt-2">
              <button 
                @click="volverAlLogin"
                class="flex-1 py-3 bg-[#D9298A] hover:bg-[#690035] text-white font-semibold rounded-4xl shadow-md transition-all duration-300 hover:scale-105 active:scale-95 cursor-pointer"
              >
                Volver
              </button>
              <button 
                @click="enviarCodigo" 
                :disabled="cargando"
                class="flex-1 py-3 bg-[#344F37] hover:bg-[#98BF45] text-white font-semibold rounded-4xl shadow-md transition-all duration-300 hover:scale-105 active:scale-95 disabled:opacity-50 cursor-pointer"
              >
                {{ cargando ? 'Enviando...' : 'Enviar código' }}
              </button>
            </div>
          </div>

          <!-- PASO 2 -->
          <div v-else-if="paso === 'verificar'" key="verificar" class="px-1 pt-4 space-y-4">
            <div class="text-center">
              <p class="text-gray-700 font-semibold mb-1">Código recibido</p>
              <p class="text-sm text-gray-500 mb-3">Ingresa el código de 6 dígitos</p>
              <p class="text-sm font-bold text-[#D9298A] bg-pink-50 py-1.5 px-4 rounded-full inline-block">
                ⏱️ Tiempo restante: {{ formatearTiempo(tiempoRestante) }}
              </p>
            </div>

            <div v-if="error" class="bg-red-50 border-l-4 border-red-500 text-red-700 p-3 rounded-lg text-sm animate-pulse">
              {{ error }}
            </div>

            <input
              v-model="codigo"
              type="text"
              maxlength="6"
              placeholder="000000"
              class="w-full px-4 py-3 bg-gray-200 border border-gray-300 rounded-lg focus:outline-none focus:border-[#344F37] text-center text-3xl tracking-widest font-mono font-bold transition-all duration-300 ease-out hover:shadow-md"
            />

            <div class="flex gap-3 pt-2">
              <button 
                @click="volverAEnviar"
                class="flex-1 py-3 bg-[#D9298A] hover:bg-[#690035] text-white font-bold rounded-4xl shadow-md transition-all duration-300 hover:scale-105 active:scale-95 cursor-pointer"
              >
                Atrás
              </button>
              <button 
                @click="verificarCodigo" 
                :disabled="cargando"
                class="flex-1 py-3 bg-[#344F37] hover:bg-[#98BF45] text-white font-bold rounded-4xl shadow-md transition-all duration-300 hover:scale-105 active:scale-95 disabled:opacity-50 cursor-pointer"
              >
                {{ cargando ? 'Verificando...' : 'Verificar' }}
              </button>
            </div>
          </div>

          <!-- PASO 3 -->
          <div v-else-if="paso === 'cambiar'" key="cambiar" class="px-1 pt-4 space-y-4">
            <p class="text-gray-700 font-semibold">Nueva contraseña</p>

            <div v-if="error" class="bg-red-50 border-l-4 border-red-500 text-red-700 p-3 rounded-lg text-sm animate-pulse">
              {{ error }}
            </div>
            <div v-if="exito" class="bg-green-50 border-l-4 border-green-500 text-green-700 p-3 rounded-lg text-sm">
              {{ exito }}
            </div>

            <!-- Nueva contraseña -->
            <div class="relative">
              <input
                v-model="nuevaContraseña"
                :type="verContraseña ? 'text' : 'password'"
                placeholder="Nueva contraseña"
                class="w-full px-4 py-3 border border-[#344F37] rounded-4xl focus:outline-none focus:ring-2 focus:ring-[#344F37] pr-12 transition-all"
              />
              <button 
                type="button" 
                @click="verContraseña = !verContraseña"
                class="absolute right-4 top-3.5 text-gray-500 hover:text-[#344F37] transition-colors cursor-pointer"
              >
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
                class="w-full px-4 py-3 border border-[#344F37] rounded-4xl focus:outline-none focus:ring-2 focus:ring-[#344F37] pr-12 transition-all"
              />
              <button 
                type="button" 
                @click="verConfirmar = !verConfirmar"
                class="absolute right-4 top-3.5 text-gray-500 hover:text-[#344F37] transition-colors cursor-pointer"
              >
                <EyeIcon v-if="verConfirmar" class="w-5 h-5" />
                <EyeSlashIcon v-else class="w-5 h-5" />
              </button>
            </div>

            <button 
              @click="cambiarContraseña" 
              :disabled="cargando"
              class="w-full py-3 bg-[#344F37] hover:bg-[#98BF45] text-white font-bold rounded-4xl shadow-md transition-all duration-300 hover:scale-105 active:scale-95 disabled:opacity-50 cursor-pointer mt-2"
            >
              {{ cargando ? 'Cambiando...' : 'Cambiar contraseña' }}
            </button>
          </div>

          <!-- PASO 4 - Completado -->
          <div v-else-if="paso === 'completado'" key="completado" class="px-1 pt-6 space-y-4 text-center">
            <div class="w-20 h-20 rounded-full bg-green-100 mx-auto flex items-center justify-center shadow-inner animate-bounce">
              <span class="text-5xl">✅</span>
            </div>
            <h2 class="text-2xl font-bold text-[#344F37]">¡Contraseña actualizada!</h2>
            <p class="text-gray-600 text-sm">Ahora puedes iniciar sesión con tu nueva contraseña.</p>

            <button 
              @click="emit('cerrar')"
              class="w-full py-3 rounded-4xl bg-[#344F37] hover:bg-[#98BF45] text-white font-bold shadow-md transition-all duration-300 hover:scale-105 active:scale-95 cursor-pointer mt-4"
            >
              Volver al inicio de sesión
            </button>
          </div>

        </Transition>

      </div>
    </div>
  </Transition>
</template>

<style scoped>
/* Transición general para abrir/cerrar el modal */
.fade-modal-enter-active,
.fade-modal-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}


input, button, label {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.icono {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-modal-enter-from,
.fade-modal-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

/* Transición suave al cambiar entre pasos */
.fade-step-enter-active,
.fade-step-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-step-enter-from {
  opacity: 0;
  transform: translateX(10px);
}

.fade-step-leave-to {
  opacity: 0;
  transform: translateX(-10px);
  
}


.anim-logo{
  animation: logo .9s ease forwards;
}
</style>