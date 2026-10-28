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
import Friends from "../views/Friends.vue";
import { trackPage } from "../composables/site";

import TreeLifePrivacy from "../views/TreeLifePrivacy.vue";
import TreeLifeSupport from "../views/TreeLifeSupport.vue";

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
  { path: '/friends', name: 'Friends', component: Friends },
  {
    path: '/guestbook',
    name: 'Guestbook',
    component: Guestbook
  },
  {
    path: '/changelog',
    redirect: '/'
  },
  {
    path: '/showcase',
    redirect: '/library?tab=works'
  },
  {
    path: '/treelife/privacy',
    alias: '/privacy',
    name: 'TreeLifePrivacy',
    component: TreeLifePrivacy,
    meta: {
      title: 'TreeLife 隐私政策',
    },
  },
  {
    path: '/treelife/support',
    alias: '/support',
    name: 'TreeLifeSupport',
    component: TreeLifeSupport,
    meta: {
      title: 'TreeLife 技术支持',
    },
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

router.afterEach((to, from, failure) => {
  if (failure) return;
  if (to.path !== from.path || !from.matched.length) {
    trackPage(to.path);
    window.scrollTo({ top: 0, behavior: 'instant' });
  }
  document.title = to.meta.title
    ? `${to.meta.title} · Magnolia`
    : 'Magnolia';
});

export default router;
