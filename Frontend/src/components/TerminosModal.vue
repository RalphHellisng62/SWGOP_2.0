<script setup lang="ts">
import { ref } from 'vue';
import { XMarkIcon } from '@heroicons/vue/24/solid';

defineProps<{
  isOpen: boolean;
}>();

defineEmits<{
  cerrar: [];
  aceptar: [];
}>();

const acepta = ref(false);
</script>

<template>
  <Transition name="modal">
  <div v-if="isOpen" class="fixed inset-0 bg-black/10 flex items-center justify-center z-50 p-4">
    <div class="bg-white rounded-2xl shadow-2xl max-w-5xl w-full max-h-[85vh] overflow-y-auto">
      
      <!-- Header -->
      <div class="sticky top-0 bg-[#344F37] text-white p-6 flex justify-between items-center">
        <h2 class="text-2xl font-bold">Términos y Condiciones</h2>
        <button
          @click="$emit('cerrar')"
          class="hover:bg-[#2a3d2c] p-1 rounded transition"
        >
          <XMarkIcon class="w-6 h-6" />
        </button>
      </div>

      <!-- Contenido -->
      <div class="p-8 space-y-6 text-gray-700">
        
        <section>
          <h3 class="text-xl font-bold text-[#344F37] mb-3">1. Aceptación de Términos</h3>
          <p class="text-sm leading-relaxed">
            Al acceder y utilizar SWGOP (Sistema Web de Gestión Operativa Presidencial), aceptas estar vinculado por estos términos y condiciones. Si no estás de acuerdo con alguna parte de estos términos, no debes usar este servicio.
          </p>
        </section>

        <section>
          <h3 class="text-xl font-bold text-[#344F37] mb-3">2. Descripción del Servicio</h3>
          <p class="text-sm leading-relaxed">
            SWGOP es un sistema de gestión de biblioteca que permite registrar, consultar y administrar el inventario de libros, así como gestionar préstamos y devoluciones. El servicio está diseñado para uso administrativo interno.
          </p>
        </section>

        <section>
          <h3 class="text-xl font-bold text-[#344F37] mb-3">3. Responsabilidades del Usuario</h3>
          <p class="text-sm leading-relaxed">
            El usuario es responsable de:
          </p>
          <ul class="text-sm leading-relaxed list-disc pl-5 mt-2 space-y-1">
            <li>Mantener la confidencialidad de sus credenciales de acceso</li>
            <li>Notificar inmediatamente sobre acceso no autorizado a su cuenta</li>
            <li>Usar el sistema únicamente para propósitos autorizados</li>
            <li>No intentar acceder a funcionalidades no autorizadas</li>
          </ul>
        </section>

        <section>
          <h3 class="text-xl font-bold text-[#344F37] mb-3">4. Privacidad de Datos</h3>
          <p class="text-sm leading-relaxed">
            Los datos personales y registros de transacciones recopilados serán utilizados únicamente para administrar la biblioteca. La información no será compartida con terceros sin consentimiento autorizado.
          </p>
        </section>

        <section>
          <h3 class="text-xl font-bold text-[#344F37] mb-3">5. Limitación de Responsabilidad</h3>
          <p class="text-sm leading-relaxed">
            SWGOP se proporciona "tal cual". No nos hacemos responsables por pérdida de datos, interrupciones del servicio o daños indirectos resultantes del uso del sistema.
          </p>
        </section>

        <section>
          <h3 class="text-xl font-bold text-[#344F37] mb-3">6. Modificación de Términos</h3>
          <p class="text-sm leading-relaxed">
            Nos reservamos el derecho de modificar estos términos en cualquier momento. Las modificaciones entrarán en vigor cuando se publiquen en el sistema.
          </p>
        </section>

        <section>
          <h3 class="text-xl font-bold text-[#344F37] mb-3">7. Contacto</h3>
          <p class="text-sm leading-relaxed">
            Para preguntas sobre estos términos, contacta al administrador del sistema.
          </p>
        </section>

      </div>

      <!-- Footer con checkbox y botones -->
      <div class="bg-gray-50 border-t p-6 space-y-4">
        
        <!-- Checkbox -->
        <label class="flex items-start gap-3 cursor-pointer">
          <input
            v-model="acepta"
            type="checkbox"
            class="mt-1 w-4 h-4 accent-[#344F37] cursor-pointer"
          />
          <span class="text-sm text-gray-700">
            He leído y acepto los Términos y Condiciones
          </span>
        </label>

        <!-- Botones -->
        <div class="flex gap-3 pt-4">
          <button
            @click="$emit('cerrar')"
            class="flex-1 py-2 border border-gray-300 text-gray-700 font-semibold rounded-lg hover:border-[#344F37] transition"
          >
            Cerrar
          </button>
          <button
            @click="$emit('aceptar')"
            :disabled="!acepta"
            :class="[
              'flex-1 py-2 font-semibold rounded-lg transition',
              acepta
                ? 'bg-[#344F37] hover:bg-[#2a3d2c] text-white cursor-pointer'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            ]"
          >
            Aceptar
          </button>
        </div>

      </div>

    </div>
  </div>
  </Transition>
</template>

<style scoped>
/* Scrollbar personalizada */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #ffffff;
}

::-webkit-scrollbar-thumb {
  background: #344F37;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #2a3d2c;
}

/* Animación del fondo */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.25s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-to,
.modal-leave-from {
  opacity: 1;
}

/* Animación del panel */
.modal-enter-active .bg-white,
.modal-leave-active .bg-white {
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-enter-from .bg-white,
.modal-leave-to .bg-white {
  opacity: 0;
  transform: scale(0.92) translateY(-20px);
}

.modal-enter-to .bg-white,
.modal-leave-from .bg-white {
  opacity: 1;
  transform: scale(1) translateY(0);
}
</style>
