import { createRouter, createWebHistory } from 'vue-router'

import Home from "../views/Home.vue";
import About from "../views/About.vue";
import Records from "../views/Records.vue";
import PostDetail from "../views/PostDetail.vue";
import Search from "../views/Search.vue";
import Login from "../views/Login.vue";
import Admin from "../views/Admin.vue";
import Library from "../views/Library.vue";
import Guestbook from "../views/Guestbook.vue";
import Changelog from "../views/Changelog.vue";

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  { 
    path: '/about',
    name: 'About',
    component: About
  },
  {
    path: '/records',
    name: 'Records',
    component: Records
  },
  {
    path: '/posts/:id',
    name: 'PostDetail',
    component: PostDetail
  },
  {
    path: '/search',
    name: 'Search',
    component: Search
  },
  {
    path: '/library',
    name: 'Library',
    component: Library
  },
  {
    path: '/guestbook',
    name: 'Guestbook',
    component: Guestbook
  },
  {
    path: '/changelog',
    name: 'Changelog',
    component: Changelog
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  { 
    path: '/admin',
    name: 'Admin',
    component: Admin,
    meta: {
      requiresAuth: true,
    },
  }
];

const router = createRouter(
  {
    history: createWebHistory(),
    routes
  });

router.beforeEach((to) => {
  const token = localStorage.getItem("access_token");

  if (to.meta.requiresAuth && !token) {
    return "/login";
  }

  return true;
});

export default router;
