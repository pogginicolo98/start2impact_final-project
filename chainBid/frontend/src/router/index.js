import Vue from "vue";
import VueRouter from "vue-router";
import Home from "@/views/Home.vue";
import Auction from "@/views/Auction.vue";
import ScheduleAuctions from "@/views/ScheduleAuctions.vue";
import AuctionEditor from "@/views/AuctionEditor.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: Home
  },
  {
    path: "/auction/:id",
    name: "auction",
    component: Auction,
    props: true
  },
  {
    path: "/schedule-auctions",
    name: "schedule auctions",
    component: ScheduleAuctions
  },
  {
    path: "/schedule-auctions/:id",
    name: "auction editor",
    component: AuctionEditor,
    props: true
  },
];

const router = new VueRouter({
  mode: "history",
  routes,
});

export default router;
