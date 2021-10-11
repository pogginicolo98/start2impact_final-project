<template>
  <div id="app">
    <NavbarComponent />
    <router-view />
  </div>
</template>

<script>
  import NavbarComponent from "@/components/Navbar.vue";

  export default {
    name: "App",
    components: {
      NavbarComponent
    }
  }
</script>

<style>
  body {
    background-color: #F2E9E4;
  }

  a {
    text-decoration: none;
  }

  .btn:focus {
    box-shadow: none !important;
  }

  .fs-18px {
    font-size: 18px;
  }

  .fs-15px {
    font-size: 15px;
  }

  .fs-14px {
    font-size: 14px;
  }

  .fs-20px {
    font-size: 20px;
  }

  .fs-24px {
    font-size: 24px;
  }

  .card-header {
    background-color: white;
  }

  .card-body-custom {
    background-color: rgba(0,0,0,.03);
  }
</style>
