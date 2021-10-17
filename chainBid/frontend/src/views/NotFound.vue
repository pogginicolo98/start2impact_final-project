<template lang="html">
  <div class="not-found">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-auto text-center">
          <img class="img-fluid" src="../../../static-storage/page-not-found.png" alt="page-not-found">
          <!-- <p class="fw-bold fs-32px">{{ message }}</p>  -->
          <div class="">
            <router-link class="btn btn-violet rounded-pill fs-20px"
                         exact
                         :to="{ name: 'home' }"
                         >Return to the homepage
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "NotFound",
  data() {
    return {
      message: "Page not found"
    }
  }
}
</script>

<style lang="css" scoped>
</style>
