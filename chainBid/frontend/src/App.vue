<template>
  <div id="app">
    <NavbarComponent />
    <router-view />
  </div>
</template>

<script>
  import NavbarComponent from "@/components/Navbar.vue";
  // import { apiService } from "@/common/api.service.js";

  export default {
    name: "App",
    components: {
      NavbarComponent
    }
  }
</script>

<style>
</style>
