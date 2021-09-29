<template>
  <div class="container">
    <div class="row justify-content-start">
      <!-- X col per signle auction -->
      <div class="col-12 col-md-6 col-lg-4 col-xxl-3"
           v-for="(auction, index) in auctions"
           :key="index">
           <!-- Card -->
           <div class="card mt-3 mx-auto"
                style="width: 18rem; height: 22rem;">
                <!-- Card image -->
                <div class="auction-image">
                  <img alt="image"
                       class="card-img-top"
                       :src="auction.image">
                </div>

                <!-- Card body -->
                <div class="card-body text-center">
                  <h4 class="card-title">{{ auction.title }}</h4>
                  <hr>
                  <p class="card-text text-success">
                    Current price: <strong>{{ auction.last_price }} €</strong>
                  </p>
                  <template v-if="auction.remaining_time">
                    <p class="card-text text-danger">
                      <strong>Started</strong>
                    </p>
                  </template>
                  <template v-else>
                    <p class="card-text text-muted">
                      <strong>No bids yet</strong>
                    </p>
                  </template>
                  <div class="d-grid">
                    <router-link class="btn btn-success"
                                 :to="{ name: 'auction', params: { id: auction.id } }"
                                 >Bid
                    </router-link>
                  </div>
                </div> <!-- Card body -->
           </div> <!-- Card -->
      </div> <!-- X col, signle auction -->
    </div> <!-- Row -->

    <!-- Load more auction -->
    <div class="my-4 text-center" >
      <!-- Spinner -->
      <div v-show="loadingAuctions">
        <div class="spinner-border text-success mt-3"
             role="status"
             style="width: 3rem; height: 3rem;">
        </div>
      </div>

      <!-- Button -->
      <button class="btn btn-success mt-4"
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

  export default {
    name: "Home",
    data() {
      return {
        auctions: [],
        timer: '',
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
          });
      }
    },
    created() {
      document.title = "ChainBid";
      this.getAuctions();
    }
  };
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
</style>
