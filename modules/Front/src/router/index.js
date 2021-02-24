import Vue from 'vue'
import Router from 'vue-router'
import Movie from '../components/movie.vue'
import Profile from '../components/profile.vue'
import Home from '../components/home.vue'

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
      },
      {
        path: '/profile/:id',
        name: 'Profile',
        component: Profile
      }
    ]
  })