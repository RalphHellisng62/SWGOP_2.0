import { ref, computed } from 'vue';

interface Usuario {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  foto?: string;
  telefono?: string;
}

// Estado global reactivo
const usuarioGlobal = ref<Usuario | null>(null);

export const useUsuario = () => {
  
  const cargarUsuario = (usuario: Usuario) => {
    usuarioGlobal.value = usuario;
    localStorage.setItem('usuario', JSON.stringify(usuario));
  };

  const actualizarUsuario = (usuarioActualizado: Usuario) => {
    usuarioGlobal.value = usuarioActualizado;
    localStorage.setItem('usuario', JSON.stringify(usuarioActualizado));
  };

  const inicializarDesdeLocalStorage = () => {
    const usuarioGuardado = localStorage.getItem('usuario');
    if (usuarioGuardado) {
      try {
        usuarioGlobal.value = JSON.parse(usuarioGuardado);
      } catch (e) {
        console.error('Error al parsear usuario del localStorage:', e);
        localStorage.removeItem('usuario');
      }
    }
  };

  const limpiarUsuario = () => {
    usuarioGlobal.value = null;
    localStorage.removeItem('usuario');
  };

  // Computed para acceso seguro
  const usuario = computed(() => usuarioGlobal.value);

  return {
    usuarioGlobal,           // ref directo (útil para templates)
    usuario,                 // computed (mejor práctica para reactividad)
    cargarUsuario,
    actualizarUsuario,
    inicializarDesdeLocalStorage,
    limpiarUsuario
  };
};