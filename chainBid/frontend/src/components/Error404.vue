<template lang="html">
  <div class="container position-absolute top-50 start-50 translate-middle text-center">
      <div v-if="auctionNotAvailable">
        <img alt="auction-not-available"
             class="img-fluid"
             src="../../../static-storage/assets/clock.png">
        <p class="text-card-auction fs-32px fw-bold mt-3">Auction no more available...</p>
      </div>
      <div v-else>
        <img alt="page-not-found"
             class="img-fluid"
             src="../../../static-storage/assets/page-not-found.png">
      </div>
      <div>
        <router-link class="btn btn-violet rounded-pill fs-20px"
                     :to="{ name: 'home' }"
                     >Back to homepage
        </router-link>
      </div>
  </div>
</template>

<script>
  export default {
    name: "Error404Component",
    props: {
      auctionNotAvailable: {
        type: Boolean,
        required: false
      }
    }
}
</script>

<style lang="css" scoped>
  html, body{
    height: 100% !important;
  }

  .router-link-active {
    color: #fff !important;
  }
</style>
