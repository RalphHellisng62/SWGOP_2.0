import api from './api';

export const recuperacionService = {
  iniciarRecuperacion(email_o_telefono: string, tipo: string) {
    return api.post('/auth/recuperacion/iniciar/', {
      email_o_telefono,
      tipo,
    });
  },

  verificarCodigo(email_o_telefono: string, codigo: string) {
    return api.post('/auth/recuperacion/verificar/', {
      email_o_telefono,
      codigo,
    });
  },

  cambiarContraseñaRecuperacion(
    email_o_telefono: string,
    codigo: string,
    nueva_contraseña: string,
    confirmar_contraseña: string
  ) {
    return api.post('/auth/recuperacion/cambiar/', {
      email_o_telefono,
      codigo,
      nueva_contraseña,
      confirmar_contraseña,
    });
  },
};