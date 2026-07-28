<script setup lang="ts">
import { ref } from 'vue';

defineProps<{
  isOpen: boolean;
}>();

defineEmits<{
  aceptar: [];
}>();

const acepta = ref(false);
</script>

<template>
  <Transition name="modal">
    <div v-if="isOpen" class="fixed inset-0 bg-black/25 backdrop-blur-sm flex items-center justify-center z-50 p-4 select-none">
      <div class="bg-white rounded-3xl shadow-2xl max-w-4xl w-full max-h-[85vh] flex flex-col overflow-hidden transform transition-all">
        
        <!-- Header Institucional -->
        <div class="bg-[#344F37] text-white p-6 shadow-md shrink-0">
          <h2 class="text-xl md:text-2xl font-bold">
            Términos de Uso y Aviso Institucional
          </h2>
          <p class="text-sm text-gray-200 mt-1">
            Sistema Web de Información y Gestión Bibliotecaria (SWIGB) | Presidencia del Barrio de San José
          </p>
        </div>

        <!-- Contenido scrolleable con la información organizada -->
        <div class="p-8 space-y-6 text-gray-700 overflow-y-auto flex-1 custom-scrollbar">
          
          <!-- A. Créditos y Uso Institucional -->
          <section>
            <h3 class="text-lg font-bold text-[#344F37] mb-2 flex items-center gap-2">
              <span>A.</span> Créditos y Uso Institucional
            </h3>
            <p class="text-sm leading-relaxed">
              El Sistema Web de Información y Gestión Bibliotecaria (SWIGB) ha sido desarrollado por <strong class="text-gray-900 font-semibold">Rafael Heriberto Arenas Rivera</strong> exclusivamente para la <strong class="text-gray-900 font-semibold">Presidencia de Comunidad del Barrio de San José</strong>, con fines de uso operativo e institucional. De conformidad con la Ley Federal del Derecho de Autor vigente en México, la titularidad del software y su código fuente quedan protegidos, concediendo a la institución la licencia para su operación autorizada.
            </p>
          </section>

          <!-- B. Objeto y Alcance del Sistema -->
          <section>
            <h3 class="text-lg font-bold text-[#344F37] mb-2 flex items-center gap-2">
              <span>B.</span> Objeto y Alcance del Sistema
            </h3>
            <p class="text-sm leading-relaxed">
              SWIGB es una plataforma tecnológica orientada a la gestión bibliotecaria del instituto, administración del acervo, control de préstamos y devoluciones, gestión del perfil y edición de usuarios, así como su disponibilidad para futuras funciones administrativas relacionadas con la operación de la Presidencia del Barrio de San José. Su uso se limita estrictamente a actividades autorizadas por la institución.
            </p>
          </section>

          <!-- C. Marco Legal Aplicable -->
          <section>
            <h3 class="text-lg font-bold text-[#344F37] mb-2 flex items-center gap-2">
              <span>C.</span> Marco Legal Aplicable en México
            </h3>
            <p class="text-sm leading-relaxed">
              El presente sistema se apega a la legislación mexicana aplicable en materia de derecho de autor y protección de datos personales. En particular, el software se encuentra protegido por la <strong class="text-gray-900 font-semibold">Ley Federal del Derecho de Autor</strong>. El tratamiento de datos personales se sujetará a la ley aplicable según la naturaleza jurídica de la Presidencia del Barrio de San José (Ley General de Protección de Datos Personales en Posesión de Sujetos Obligados o normativa afín).
            </p>
          </section>

          <!-- D. Términos y Condiciones de Uso -->
          <section>
            <h3 class="text-lg font-bold text-[#344F37] mb-2 flex items-center gap-2">
              <span>D.</span> Términos y Condiciones de Uso
            </h3>
            <p class="text-sm leading-relaxed mb-2">
              El acceso al sistema es exclusivo para personal autorizado. Al operar la plataforma, el usuario acepta las siguientes condiciones:
            </p>
            <ul class="text-sm leading-relaxed list-disc pl-5 space-y-1">
              <li>El usuario es responsable directo de la custodia de sus credenciales y de la veracidad de la información que registre.</li>
              <li>Mantener la confidencialidad de sus claves y notificar inmediatamente sobre cualquier acceso no autorizado.</li>
              <li>Queda estrictamente prohibido compartir contraseñas, alterar información sin autorización previa o intentar vulnerar la seguridad del sistema.</li>
              <li>Queda prohibido utilizar el sistema para fines distintos a los operativos e institucionales.</li>
              <li>La Presidencia del Barrio de San José podrá realizar mantenimientos, actualizaciones o mejoras operativas cuando sea necesario.</li>
            </ul>
          </section>

          <!-- E. Protección de Datos Personales -->
          <section>
            <h3 class="text-lg font-bold text-[#344F37] mb-2 flex items-center gap-2">
              <span>E.</span> Protección y Privacidad de Datos
            </h3>
            <p class="text-sm leading-relaxed">
              Los datos personales recabados y los registros de transacciones serán utilizados únicamente para administrar la biblioteca, la gestión de usuarios y fines estadísticos internos. La información no será compartida con terceros sin consentimiento autorizado, salvo requerimiento legal expreso de autoridad competente.
            </p>
          </section>

          <!-- F. Cierre y Derechos -->
          <section class="border-t border-gray-100 pt-4">
            <h2 class="text-sm text-gray-500 font-semibold text-center">
              ©Presidencia del Barrio de San José. Todos los derechos reservados.
            </h2>
          </section>

        </div>

        <!-- Footer con Checkbox a la izquierda y Botón Aceptar centrado -->
        <div class="bg-gray-200 border-t border-gray-200 p-6 space-y-4 shrink-0">
          
          <!-- Checkbox -->
          <label class="flex items-start gap-3 cursor-pointer group">
            <input
              v-model="acepta"
              type="checkbox"
              class="mt-0.5 w-5 h-5 accent-[#344F37] rounded cursor-pointer transition-transform duration-200 group-hover:scale-110 shrink-0"
            />
            <span class="text-sm font-semibold text-gray-700 group-hover:text-[#344F37] transition-colors">
              He leído y acepto los Términos, Condiciones y Marco Legal Institucional
            </span>
          </label>

          <!-- Botón Aceptar centrado -->
          <div class="flex justify-center pt-2">
            <button
              @click="$emit('aceptar')"
              :disabled="!acepta"
              :class="[
                'w-full max-w-xs py-3 font-bold rounded-4xl shadow-md transition-all duration-300',
                acepta
                  ? 'bg-[#344F37] hover:bg-[#98BF45] text-white hover:scale-105 active:scale-95 cursor-pointer'
                  : 'bg-gray-600 text-gray-200 cursor-not-allowed opacity-60'
              ]"
            >
              Cerrar y aceptar
            </button>
          </div>

        </div>

      </div>
    </div>
  </Transition>
</template>

<style scoped>
/* Scrollbar personalizada para el contenido interno */
.custom-scrollbar::-webkit-scrollbar {
  width: 8px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #344F37;
  border-radius: 9999px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #98BF45;
}

/* Animación del fondo del modal */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

/* Animación del panel central */
.modal-enter-active .bg-white,
.modal-leave-active .bg-white {
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-enter-from .bg-white,
.modal-leave-to .bg-white {
  opacity: 0;
  transform: scale(0.92) translateY(-10px);
}
</style>