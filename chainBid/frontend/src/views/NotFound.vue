<template lang="html">
  <div class="container position-absolute top-50 start-50 translate-middle">
    <div class="text-center">
      <img class="img-fluid" src="../../../static-storage/page-not-found.png" alt="page-not-found">
      <div class="">
        <router-link class="btn btn-violet rounded-pill fs-20px"
                     :to="{ name: 'home' }"
                     >Back to homepage
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "NotFound"
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
