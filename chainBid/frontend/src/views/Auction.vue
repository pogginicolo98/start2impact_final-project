<template lang="html">
  <div class="container">
    <h1>{{ auction.title }}</h1>
  </div>
</template>

<script>
  // @ is an alias to /src
  import { apiService } from "@/common/api.service.js";

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
        auction: {},
        error: null
      };
    },
    methods: {
      setPageTitle(title) {
        document.title = title;
      },
      async getAuctionData() {
        /*
          Retrieve a specific auction's data and
          set page title.
        */

        let endpoint = `/api/auctions/${this.id}/`;
        await apiService(endpoint)
          .then(response => {
            this.auction = response;
            this.setPageTitle(response.title);
          });
      }
    },
    created() {
      this.getAuctionData();
    }
  }
</script>

<style lang="css" scoped>
</style>
