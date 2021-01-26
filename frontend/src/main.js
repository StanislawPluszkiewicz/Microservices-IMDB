import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue/dist/bootstrap-vue.esm'
import Icon from 'vue-awesome/components/Icon'
import App from './App.vue'

import 'vue-awesome/icons'
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

Vue.component('v-icon', Icon)
Vue.use(BootstrapVue);
console.log(Vue.version)
new Vue({
  el: '#app',
  render: h => h(App)
})
