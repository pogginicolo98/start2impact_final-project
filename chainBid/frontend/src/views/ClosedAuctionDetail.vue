<template lang="html">
  <div class="container mt-3 mt-lg-5">
    <div class="row">
      <!-- Title for mobile formats -->
      <div class="col-12 d-lg-none mb-2">
        <h1>{{ auction.title }}</h1>
      </div>

      <!-- Image -->
      <div class="col-12 col-lg-5">
        <img alt="product image"
             class="img-fluid img-thumbnail"
             :src="auction.image">
      </div>

      <!-- New bid -->
      <div class="col-12 col-lg-7 mt-3 mt-lg-0">
        <!-- Title for desktop formats -->
        <h1 class="d-none d-lg-block">{{ auction.title }}</h1>
        <div class="card">
          <div class="card-body">
              <p class="card-title fs-18px">Won by {{ auction.winner }}</p>
              <p class="card-text text-muted fs-14px mb-0">Initial price: €{{ auction.initial_price }}</p>
              <p class="card-text text-success fs-14px mb-0">Final price: €{{ auction.final_price }}</p>
              <hr>
              <p class="card-text text-muted fs-14px mb-0">Opened at: {{ getDate(auction.opened_at) }}</p>
              <p class="card-text text-success fs-14px  mb-0">Closed at: {{ getDate(auction.closed_at) }}</p>
          </div>
        </div>
      </div> <!-- New bid -->
    </div> <!-- Row 1 -->

    <!-- Description -->
    <div class="row">
      <div class="col-12 col-lg-5">
        <div class="card mt-3" style="width: 100%">
          <div class="card-header">
            <i class="bi bi-justify-left icon"></i><span class="fw-bold fs-18px"> Description</span>
          </div>
          <div class="card-body">
            <p class="card-text my-2">{{ auction.description }}</p>
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
  .fs-18px {
    font-size: 18px;
  }

  .fs-15px {
    font-size: 15px;
  }

  .fs-14px {
    font-size: 14px;
  }

  .icon {
    font-size: 24px;
  }

  .card-header {
    background-color: white;
  }

  .card-body {
    background-color: rgba(0,0,0,.03);
  }
</style>
