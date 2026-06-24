import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Inventario from '../views/Inventario.vue';
import Prestamos from '../views/Prestamos.vue';
import EditarPerfil from '../views/EditarPerfil.vue';
import RecuperarContraseña from '../views/RecuperarContraseña.vue';

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/inventario',
    name: 'Inventario',
    component: Inventario,
    meta: { requiresAuth: true }
  },
  {
    path: '/prestamos',
    name: 'Prestamos',
    component: Prestamos,
    meta: { requiresAuth: true }
  },
  {
    path: '/editarPerfil',
    name: 'EditarPerfil',
    component: EditarPerfil,
    meta: { requiresAuth: true }
  },
  {
    path: '/recuperar-contraseña',
    name: 'RecuperarContraseña',
    component: RecuperarContraseña
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Guard de autenticación (Versión moderna - sin warning)
router.beforeEach((to) => {
  const token = localStorage.getItem('access_token');
  const estaAutenticado = !!token;

  if (to.meta.requiresAuth && !estaAutenticado) {
    return '/login';
  }

  if (to.path === '/login' && estaAutenticado) {
    return '/inventario';
  }

  // Si no hay redirección, se continúa normalmente
  return true;
});

export default router;