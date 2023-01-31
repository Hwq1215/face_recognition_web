import Vue from 'vue'
import Router from 'vue-router'
import HomeView from '../views/HomeView.vue'
import findface from '../views/findface.vue'
Vue.use(Router)

export default new Router({
  routes: [
      {
        path:'/',
        redirect: '/home',
      },
      {
        path: '/home',
        name: 'home',
        component: HomeView,
        children:[
          {
            path: 'findface',
            name: 'findface',
            component: findface
          }
        ]
      },
    ]
})

