<template>
  <div class="container mt-3 mt-md-5">
    <div class="row justify-content-start">
      <div class="col-12 col-md-6 col-lg-4 col-xxl-3"
           v-for="(auction, index) in auctions"
           :key="index">
           <!-- Card -->
           <router-link :to="{ name: 'closed auction detail', params: { id: auction.id } }">
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
                    <template v-if="!isCanceled(auction)">
                      <p class="text-card-auction fs-20px mt-2 mb-1">Won by @{{ auction.winner }}</p>
                      <p class="text-card-auction fs-17px">€{{ auction.final_price }}</p>
                    </template>
                    <template v-else>
                      <p class="text-danger fs-17px mt-4">Canceled</p>
                    </template>
                  </div>

                  <!-- Card footer -->
                  <div class="position-absolute bottom-0 start-50 translate-middle-x text-center" style="width: 90%">
                    <hr class="text-card-auction mb-1">
                    <p class="text-muted fs-14px mb-1">Closed {{ getClosedAt(auction) }}</p>
                  </div>
             </div>
           </router-link> <!-- Card -->
      </div>
    </div> <!-- Row -->

    <!-- Pagination -->
    <div class="mb-5 mt-2 text-center" >
      <div v-show="loadingAuctions">
        <div class="spinner-border text-success"
             role="status"
             style="width: 3rem; height: 3rem;">
        </div>
      </div>
      <button class="btn btn-success"
              v-show="next"
              @click="getAuctions"
              >Show more
      </button>
    </div>
  </div> <!-- Container -->
</template>

<script>
  // @ is an alias to /src
  import { apiService } from "@/common/api.service.js";
  import moment from 'moment';

  export default {
    name: "ClosedAuctions",
    data() {
      return {
        auctions: [],
        next: null,
        loadingAuctions: false
      };
    },
    methods: {
      async getAuctions() {
        /*
          Retrieve active auctions according to pagination.
        */

        let endpoint = "/api/closed-auctions/";
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
          });
      },
      getClosedAt(auction) {
        return moment(auction.closed_at).fromNow();
      },
      isCanceled(auction) {
        if (auction.winner != "None") {
          return false;
        }
        return true;
      }
    },
    created() {
      document.title = "Closed auctions | ChainBid";
      this.getAuctions();
    }
  }
</script>

<style lang="css" scoped>
  .auction-image {
    /*
      Fixed width and height, image not stretched and centered.
    */
    width: 100%;
    height: 10rem;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .card {
      transition: transform 0.2s ease;
      box-shadow: 0 4px 6px 0 rgba(22, 22, 26, 0.18);
      border-radius: 0;
      border: 0;
      margin-bottom: 1.5em;
    }

  .card:hover {
    transform: scale(1.1);
  }
</style>
