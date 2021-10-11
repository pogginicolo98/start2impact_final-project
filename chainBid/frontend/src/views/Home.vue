<template>
  <div class="container mt-3 mt-md-5">
    <div class="row justify-content-start">
      <!-- X col per signle auction -->
      <div class="col-12 col-md-6 col-lg-4 col-xxl-3"
           v-for="(auction, index) in auctions"
           :key="index">
           <!-- Card -->
           <router-link :to="{ name: 'auction', params: { id: auction.id } }">
             <div class="card mb-4 mx-auto"
                  style="width: 18rem; height: 21rem;">
                  <!-- Card image -->


                  <!-- Card body -->
                  <div class="card-body text-center">
                    <p class="card-title text-custom fw-bold fs-4">{{ auction.title }}</p>
                    <div class="card-img-wrap mt-3 mb-2">
                      <img alt="product image"
                           class="card-img"
                           :src="auction.image">
                    </div>
                    <p class="card-text text-custom fs-5 mb-1">€{{ auction.last_price }}</p>
                    <template v-if="auction.remaining_time">
                      <p class="card-text text-danger">Started</p>
                    </template>
                    <template v-else>
                      <p class="card-text text-muted">No bids yet</p>
                    </template>
                    <!-- <p class="card-text">€{{ auction.last_price }}</p> -->
                    <hr class="text-custom my-2">
                    <p class="card-text text-muted">Opened {{ getOpenedAt(auction) }}</p>
                  </div>
             </div> <!-- Card -->
           </router-link>
      </div> <!-- X col, signle auction -->
    </div> <!-- Row -->

    <!-- Load more auction -->
    <div class="mb-5 mt-2 text-center" >
      <!-- Spinner -->
      <div v-show="loadingAuctions">
        <div class="spinner-border text-success"
             role="status"
             style="width: 3rem; height: 3rem;">
        </div>
      </div>

      <!-- Button -->
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
    name: "Home",
    data() {
      return {
        auctions: [],
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
    background-color: #F8F4F1;
    transition: transform 0.2s ease;
    box-shadow: 0 4px 6px 0 rgba(0, 0, 0, 0.1);
    border-radius: 10%;
    border: 0;
    margin-bottom: 1.5em;
  }

  .card:hover {
    transform: scale(1.1);
  }

  .card-img-wrap {
    overflow: hidden;
    position: relative;
  }
  .card-img-wrap:after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.3);
    opacity: 0;
    transition: opacity .25s;
  }
  .card-img-wrap img {
    transition: transform .25s;
    width: 100%;
  }
  .card:hover .card-img-wrap img {
    transform: scale(1.2);
  }
  .card:hover .card-img-wrap:after {
    opacity: 1;
  }

  .text-custom {
    color: #37251B;
  }
</style>
