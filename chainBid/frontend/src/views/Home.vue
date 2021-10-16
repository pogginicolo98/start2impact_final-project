<template>
  <div class="container mt-3">
    <!-- Title -->
    <div class="text-center text-card-auction fw-bold fs-32px">
      <p>Live auctions</p>
    </div>

    <!-- Auctions -->
    <div class="row justify-content-start mt-4">
      <div class="col-12 col-md-6 col-lg-4 col-xxl-3"
           v-for="(auction, index) in auctions"
           :key="index">
           <!-- Card -->
           <router-link :to="{ name: 'auction', params: { id: auction.id } }">
             <div class="card card-auction position-relative mb-4 mx-auto"
                  style="width: 18rem; height: 21rem;">
                  <div class="card-body text-center">
                    <!-- Card title -->
                    <p class="text-card-auction fw-bold fs-24px mb-2">{{ auction.title }}</p>

                    <!-- Card image -->
                    <div class="card-img-wrap-auction">
                      <img alt="product image"
                           class="card-img-auction"
                           :src="auction.image">
                    </div>

                    <!-- Card body -->
                    <p class="text-card-auction fs-20px mt-3 mb-1">{{ auction.last_price }} €</p>
                    <template v-if="auction.remaining_time">
                      <p class="text-danger fs-17px">Started</p>
                    </template>
                    <template v-else>
                      <p class="text-muted fs-17px">No bids yet</p>
                    </template>
                  </div>

                  <!-- Card footer -->
                  <div class="position-absolute bottom-0 start-50 translate-middle-x text-center"
                       style="width: 90%">
                       <hr class="text-card-auction mb-1">
                       <p class="text-muted fs-14px mb-1">{{ getDateFromNow(auction.opened_at) }}</p>
                  </div>
             </div>
           </router-link> <!-- Card -->
      </div> <!-- Col -->
    </div> <!-- Auctions -->

    <!-- Pagination -->
    <div :class="{'position-absolute top-50 start-50 translate-middle': firstLoading,
                  'mb-5 mt-2 text-center': !firstLoading}">
      <div v-show="loadingAuctions">
        <div class="spinner-grow text-violet"
             role="status"
             style="width: 3rem; height: 3rem;">
        </div>
      </div>
    </div>
  </div> <!-- Container -->
</template>

<script>
  // @ is an alias to /src
  import { apiService } from "@/common/api.service.js";
  import moment from 'moment';

  export default {
    name: "Home",
    data() {
      return {
        auctions: [],
        firstLoading: true,
        next: null,
        loadingAuctions: false
      }
    },
    methods: {
      async getAuctions() {
        /*
          Retrieve active auctions according to pagination.
        */

        let endpoint = "/api/auctions/";
        if (this.next) {
          endpoint = this.next;
        }
        this.loadingAuctions = true;
        await apiService(endpoint)
          .then(response => {
            this.auctions.push(...response.results);
            this.loadingAuctions = false;
            if (response.next) {
              this.next = response.next;
            } else {
              this.next = null;
            }
            if (this.firstLoading) {
              this.firstLoading = false;
            }
          });
      },
      getDateFromNow(date) {
        return moment(date).fromNow();
      },
      getNextUser() {
        /*
          Retrieve new auction when scrolling down.
        */

        window.onscroll = () => {
          if (this.next && !this.loadingAuctions) {
            let bottomOfWindow = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight;
            if (bottomOfWindow) {
              this.getAuctions();
            }
          }
        }
      }
    },
    mounted() {
      this.getNextUser();
    },
    created() {
      document.title = "Live auctions | ChainBid";
      this.getAuctions();
    }
  };
</script>

<style lang="css" scoped>
</style>
