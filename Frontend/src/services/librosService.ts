import api from './api';

export const librosService = {
  obtenerLibros() {
    return api.get('/libros/');
  },

  obtenerLibro(id: number) {
    return api.get(`/libros/${id}/`);
  },

 crearLibro(datos: any) {
  // Si ya es FormData, enviar directamente SIN modificar
  if (datos instanceof FormData) {
    console.log('📤 Enviando FormData directamente');
    
    // IMPORTANTE: No setear Content-Type, dejar que axios lo haga
    return api.post('/libros/', datos, {
      headers: {
        // NO incluir 'Content-Type': 'multipart/form-data'
        // axios lo detecta automáticamente
      }
    });
  }

  // Si es un objeto JSON, crear FormData
  console.log('📤 Creando FormData desde objeto');
  const formData = new FormData();

  formData.append('titulo', datos.titulo);
  formData.append('autor', datos.autor);
  formData.append('nt', datos.nt);
  formData.append('etiqueta', datos.etiqueta);
  formData.append('categoria', datos.categoria);
  formData.append('ejemplares', String(datos.ejemplares));
  formData.append('estado', datos.estado);

  if (datos.foto instanceof File) {
    formData.append('foto', datos.foto);
  }

  return api.post('/libros/', formData);
},

  actualizarLibro(id: number, datos: any) {
  const formData = new FormData();

  formData.append("nt", datos.nt);
  formData.append("etiqueta", datos.etiqueta);
  formData.append("titulo", datos.titulo);
  formData.append("autor", datos.autor);
  formData.append("categoria", datos.categoria);
  formData.append("ejemplares", String(datos.ejemplares));
  formData.append("estado", datos.estado);

  if (datos.foto instanceof File) {
      formData.append("foto", datos.foto);
  }

  return api.patch(`/libros/${id}/`, formData);
},

  eliminarLibro(id: number) {
    return api.delete(`/libros/${id}/`);
  },

  cambiarEstado(id: number, estado: string) {
    return api.patch(`/libros/${id}/`, { estado });
  },
};