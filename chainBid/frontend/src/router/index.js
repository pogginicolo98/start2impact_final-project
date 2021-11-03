import Vue from "vue";
import VueRouter from "vue-router";
import Home from "@/views/Home.vue";
import Auction from "@/views/Auction.vue";
import ScheduleAuctions from "@/views/ScheduleAuctions.vue";
import AuctionEditor from "@/views/AuctionEditor.vue";
import ClosedAuctions from "@/views/ClosedAuctions.vue";
import ClosedAuctionDetail from "@/views/ClosedAuctionDetail.vue";
import Profile from "@/views/Profile.vue";
import NotFound from "@/views/NotFound.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: Home
  },
  {
    path: "/auction/:slug",
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
    path: "/schedule-auctions/:slug",
    name: "auction editor",
    component: AuctionEditor,
    props: true
  },
  {
    path: "/closed-auctions",
    name: "closed auctions",
    component: ClosedAuctions
  },
  {
    path: "/closed-auctions/:slug",
    name: "closed auction detail",
    component: ClosedAuctionDetail,
    props: true
  },
  {
    path: "/profile/:slug",
    name: "profile",
    component: Profile,
    props: true
  },
  {
    path: "*",
    name: "not found",
    component: NotFound
  }
];

const router = new VueRouter({
  mode: "history",
  routes,
});

export default router;
