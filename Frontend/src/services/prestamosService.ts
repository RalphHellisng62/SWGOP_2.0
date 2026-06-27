import api from './api';

export const prestamosService = {
  obtenerPrestamos() {
    return api.get('/prestamos/');
  },

  obtenerLibrosDisponibles() {
  return api.get('/libros/');
},

  registrarPrestamo(datos: any) {
    return api.post('/prestamos/', datos);
  },


  obtenerPrestamo(id: number) {
    return api.get(`/prestamos/${id}/`);
  },

  crearPrestamo(datos: any) {
    return api.post('/prestamos/', datos);
  },

  actualizarPrestamo(id: number, datos: any) {
    return api.patch(`/prestamos/${id}/`, datos);
  },

  eliminarPrestamo(id: number) {
    return api.delete(`/prestamos/${id}/`);
  },

  marcarPrestamoDevuelto(id: number) {
    return api.patch(`/prestamos/${id}/`, { estado: 'devuelto' });
  },
};