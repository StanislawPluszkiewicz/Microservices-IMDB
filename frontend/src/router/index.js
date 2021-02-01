import Vue from 'vue'
import Router from 'vue-router'
import Movie from '../components/Movie'
import Profile from '../components/Profile'
import Home from '../components/Home'

Vue.use(Router)

/*const routes = [
    { path: '/', name: 'Home', component: Home},
    { path: '/movie', name: 'Movie', component: Movie},
    { path: '/profile', name: 'Profile', component: Profile},
  ]*/

export default new Router({
    routes: [
      {
        path: '/',
        name: 'Home',
        component: Home
      },
      {
        path: '/movie/:id',
        name: 'Movie',
        component: Movie
      }
    ]
  })