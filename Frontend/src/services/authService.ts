import api from './api';

interface LoginData {
  username: string;
  password: string;
}

let refreshPromise: Promise<any> | null = null;

export const authService = {
  login(datos: LoginData) {
    return api.post('/auth/login/', datos);
  },

  registro(datos: any) {
    return api.post('/auth/registro/', datos);
  },

  guardarToken(access: string, refresh: string, usuario?: any) {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    if (usuario) {
      localStorage.setItem('usuario', JSON.stringify(usuario));
    }
  },

  obtenerToken() {
    return localStorage.getItem('access_token');
  },

  estaAutenticado() {
    return !!localStorage.getItem('access_token');
  },

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('usuario');
    refreshPromise = null;
  },

  async refreshToken() {
    const refresh = localStorage.getItem('refresh_token');
    if (!refresh) throw new Error('No refresh token available');

    if (refreshPromise) return refreshPromise;

    refreshPromise = api
      .post('/auth/token/refresh/', { refresh })
      .then((response) => {
        const { access } = response.data;
        localStorage.setItem('access_token', access);
        refreshPromise = null;
        return response;
      })
      .catch((error) => {
        refreshPromise = null;
        throw error;
      });

    return refreshPromise;
  },

  obtenerPerfil() {
    return api.get('/auth/perfil/');
  },

  actualizarPerfil(datos: any) {
    const formData = new FormData();
    if (datos.foto instanceof File) formData.append('foto', datos.foto);
    if (datos.username) formData.append('username', datos.username);
    if (datos.email) formData.append('email', datos.email);

    return api.put('/auth/perfil/actualizar/', formData);
  },

  cambiarContraseña(contraseña_actual: string, contraseña_nueva: string) {
    return api.post('/auth/perfil/cambiar-contraseña/', {
      contraseña_actual,
      contraseña_nueva,
    });
  },
};