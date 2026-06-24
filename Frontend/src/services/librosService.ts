import api from './api';

export const librosService = {
  obtenerLibros() {
    return api.get('/libros/');
  },

  obtenerLibro(id: number) {
    return api.get(`/libros/${id}/`);
  },

  crearLibro(datos: any) {
    const formData = new FormData();

    formData.append('titulo', datos.titulo);
    formData.append('autor', datos.autor);
    formData.append('nt', datos.nt);
    formData.append('etiqueta', datos.etiqueta);
    formData.append('categoria', datos.categoria);
    formData.append('ejemplares', datos.ejemplares);

    if (datos.foto instanceof File) {
      formData.append('foto', datos.foto);
    }

    return api.post('/libros/', formData);
  },

  actualizarLibro(id: number, datos: any) {
    return api.patch(`/libros/${id}/`, datos);
  },

  eliminarLibro(id: number) {
    return api.delete(`/libros/${id}/`);
  },

  cambiarEstado(id: number, estado: string) {
    return api.patch(`/libros/${id}/`, { estado });
  },
};