import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue/dist/bootstrap-vue.esm'
import Icon from 'vue-awesome/components/Icon'
import App from './App.vue'
import router from './router'
import axios from 'axios'

import 'vue-awesome/icons'
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

Vue.config.productionTip = false

Vue.component('v-icon', Icon)
Vue.use(BootstrapVue);
Vue.prototype.$axios = axios

new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: {App}
})
