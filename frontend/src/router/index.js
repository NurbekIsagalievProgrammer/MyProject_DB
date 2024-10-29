import { createRouter, createWebHistory } from 'vue-router';
import AnimalTypeView from '../views/AnimalTypeView.vue';
import BreedView from '../views/BreedView.vue';
import AnimalView from '../views/AnimalView.vue';
import WeightingView from '../views/WeightingView.vue';
import UserView from '../views/UserView.vue';

const routes = [
  {
    path: '/animaltypes',
    name: 'AnimalType',
    component: AnimalTypeView,
  },
  {
    path: '/breeds',
    name: 'Breed',
    component: BreedView,
  },
  {
    path: '/animals',
    name: 'Animal',
    component: AnimalView,
  },
  {
    path: '/weightings',
    name: 'Weighting',
    component: WeightingView,
  },
  {
    path: '/users',
    name: 'User',
    component: UserView,
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
