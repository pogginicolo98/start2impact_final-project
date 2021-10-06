<template lang="html">
  <div class="container mt-3 mt-lg-5">
    <div class="card">
      <div class="auction-image">
        <img alt="product image"
             class="card-img-top"
             :src="auction.image">
      </div>
      <div class="card-body">
        <button class="btn btn-success"
                type="submit"
                >Create
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
    name: "AuctionEditor",
    props: {
      id: {
        type: Number,
        required: true
      }
    },
    data() {
      return {
        auction: {}
      }
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

        let endpoint = `/api/schedule-auctions/${this.id}/`;
        await apiService(endpoint)
          .then(response => {
            this.auction = response;
            document.title = response.title;
          });
      },
    },
    created() {
      this.getAuctionData();
    },
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
</style>
