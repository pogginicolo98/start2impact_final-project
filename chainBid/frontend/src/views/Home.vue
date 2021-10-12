<template>
  <div class="container mt-3 mt-md-5">
    <div class="row justify-content-start">
      <div class="col-12 col-md-6 col-lg-4 col-xxl-3"
           v-for="(auction, index) in auctions"
           :key="index">
           <!-- Card -->
           <router-link :to="{ name: 'auction', params: { id: auction.id } }">
             <div class="card card-auction mb-4 mx-auto position-relative"
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
                    <p class="text-card-auction fs-20px mt-2 mb-1">€{{ auction.last_price }}</p>
                    <template v-if="auction.remaining_time">
                      <p class="text-danger fs-17px">Started</p>
                    </template>
                    <template v-else>
                      <p class="text-muted fs-17px">No bids yet</p>
                    </template>
                  </div>

                  <!-- Card footer -->
                  <div class="position-absolute bottom-0 start-50 translate-middle-x text-center" style="width: 90%">
                    <hr class="text-card-auction mb-1">
                    <p class="text-muted fs-14px mb-1">Opened {{ getOpenedAt(auction) }}</p>
                  </div>
             </div>
           </router-link> <!-- Card -->
      </div>
    </div> <!-- Row -->

    <!-- Pagination -->
    <!-- <div :class="{"position-absolute top-50 start-50 translate-middle": firstLoading,
                  "mb-5 mt-2 text-center": !firstLoading}"> -->
    <div :class="{'position-absolute top-50 start-50 translate-middle': firstLoading,
                  'mb-5 mt-2 text-center': !firstLoading}">
      <div v-show="loadingAuctions">
        <div class="spinner-grow text-violet"
             role="status"
             style="width: 3rem; height: 3rem;">
        </div>
      </div>
      <div v-show="!loadingAuctions">
        <button class="btn btn-success"
                v-show="next"
                @click="getAuctions"
                >Show more
        </button>
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
        next: null,
        loadingAuctions: false,
        firstLoading: true
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
      getOpenedAt(auction) {
        return moment(auction.opened_at).fromNow();
      }
    },
    created() {
      document.title = "ChainBid";
      this.getAuctions();
    }
  };
</script>


<style lang="css" scoped>
</style>
