<template lang="html">
  <div class="container mt-4 mt-lg-5">
    <div class="row">
      <!-- Title mobile formats -->
      <div class="col-12 d-lg-none">
        <p class="text-card-auction fw-bold fs-32px mb-2 ms-2">{{ auction.title }}</p>
      </div>

      <!-- Image -->
      <div class="col-12 col-lg-5">
        <img alt="product image"
             class="img-fluid img-thumbnail img-thumbnail-detail"
             :src="auction.image">
      </div>

      <!-- Info -->
      <div class="col-12 col-lg-7 mt-3 mt-lg-0">
        <!-- Title desktop formats -->
        <p class="text-card-auction fs-32px fw-bold d-none d-lg-block mb-3 ms-2">{{ auction.title }}</p>
        <!-- Card -->
        <div class="card card-detail">
          <div class="card-body card-body-detail">
              <p class="text-card-auction fs-18px">Won by {{ auction.winner }}</p>
              <p class="card-text text-muted fs-14px mb-0">Initial price: €{{ auction.initial_price }}</p>
              <p class="text-card-auction fs-14px mb-0">Final price: €{{ auction.final_price }}</p>
              <hr>
              <p class="card-text text-muted fs-14px mb-0">Opened at: {{ getDate(auction.opened_at) }}</p>
              <p class="text-card-auction fs-14px  mb-0">Closed at: {{ getDate(auction.closed_at) }}</p>
          </div>
        </div>
      </div> <!-- New bid -->
    </div> <!-- Row 1 -->

    <!-- Description -->
    <div class="row">
      <div class="col-12 col-lg-5">
        <div class="card card-detail mt-3" style="width: 100%">
          <div class="card-header card-header-detail text-card-auction">
            <i class="fa-solid fa-align-left me-2"></i><span class="fw-bold fs-18px">Description</span>
          </div>
          <div class="card-body card-body-detail">
            <p class="my-2">{{ auction.description }}</p>
          </div>
        </div>
      </div>
    </div> <!-- Row 2 -->
  </div> <!-- Container -->
</template>

<script>
  // @ is an alias to /src
  import { apiService } from "@/common/api.service.js";
  import moment from 'moment';

  export default {
    name: "Auction",
    props: {
      id: {
        type: Number,
        required: true
      }
    },
    data() {
      return {
        auction: {}
      };
    },
    computed: {
      getOpenedAt() {
        return moment(this.auction.opened_at).fromNow();
      }
    },
    methods: {
      async getAuctionData() {
        /*
          Retrieve a specific auction's data and set page title.
        */

        let endpoint = `/api/closed-auctions/${this.id}/`;
        await apiService(endpoint)
          .then(response => {
            this.auction = response;
            document.title = `${response.title} | ChainBid`;
          });
      },
      getDate(date) {
        return moment.utc(date, 'YYYY/MM/DD, HH:mm:ss').format('YYYY/MM/DD, HH:mm:ss');
      }
    },
    created() {
      this.getAuctionData();
    }
  }
</script>

<style lang="css" scoped>
</style>
