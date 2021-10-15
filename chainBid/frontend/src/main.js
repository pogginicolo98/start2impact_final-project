import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import Clipboard from 'v-clipboard'

Vue.config.productionTip = false;
Vue.use(Clipboard);

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
