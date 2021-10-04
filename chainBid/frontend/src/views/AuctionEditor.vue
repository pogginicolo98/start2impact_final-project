<template lang="html">
  <div class="container mt-3 mt-lg-5">
    hello
  </div>
</template>

<script>
  // @ is an alias to /src
  import { apiService } from "@/common/api.service.js";
  // import BidFormComponent from "@/components/BidForm.vue";

  export default {
    name: "AuctionEditor",
    props: {
      id: {
        type: Number,
        required: true
      }
    },
    // components:{
    //   BidFormComponent
    // },
    data() {
      return {
        auction: {}
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
</style>
