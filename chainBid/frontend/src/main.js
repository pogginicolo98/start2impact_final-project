import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import Clipboard from "v-clipboard";
import Toasted from "vue-toasted";

Vue.config.productionTip = false;
Vue.use(Clipboard);
Vue.use(Toasted, {
  position: "bottom-right",
  duration: 3000,
  className: "vue-toast rounded fw-bold",
  iconPack: "fontawesome",
  singleton: true
});

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
