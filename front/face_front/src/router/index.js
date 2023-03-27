import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import findface from '../views/findface.vue'
import bootstrap from '../views/bootstrap.vue'
import videoShow from '../views/videoShow.vue'
import compareFace from '../views/compareFace.vue' 
import landmarks from '../views/landmarks.vue'
import manage from '../views/manage.vue'
import dashboard from '../views/mydashboard.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      children:[
        {
          path: '',
          name: dashboard,
          component: dashboard
        },
        {
          path: 'findface',
          name: 'findface',
          component: findface
        },
        {
          path: 'compare',
          name: 'compareFace',
          component: compareFace
        },
        {
          path: 'landmarks',
          name: 'landmarks',
          component: landmarks
        },
        {
          path: 'videoshow',
          name: 'videoShow',
          component: videoShow
        },
        {
          path: 'manage',
          name: 'manage',
          component: manage
        },
        {
          path: 'bootstrap',
          name: 'bootstrap',
          component: bootstrap
        }
      ]
    },
  ]
})

export default router
