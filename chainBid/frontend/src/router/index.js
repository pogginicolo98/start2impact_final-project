import Vue from "vue";
import VueRouter from "vue-router";
import Home from "@/views/Home.vue";
import Auction from "@/views/Auction.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/auction/:id",
    name: "auction",
    component: Auction,
    props: true
  },
];

const router = new VueRouter({
  mode: "history",
  routes,
});

export default router;
