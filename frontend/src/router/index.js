import Vue from 'vue'
import Router from 'vue-router'
import Ghostwriter from '@/components/Ghostwriter'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Ghostwriter',
      component: Ghostwriter
    }
  ]
})
