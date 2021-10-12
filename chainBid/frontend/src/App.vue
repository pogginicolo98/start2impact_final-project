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

  .fs-14px {
    font-size: 14px;
  }

  .fs-15px {
    font-size: 15px;
  }

  .fs-17px {
    font-size: 17px;
  }

  .fs-18px {
    font-size: 18px;
  }

  .fs-20px {
    font-size: 20px;
  }

  .fs-24px {
    font-size: 24px;
  }

  .fs-32px {
    font-size: 32px;
  }

  .card-img-auction {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .card-auction {
    background-color: #F8F4F1;
    transition: transform 0.2s ease;
    box-shadow: 0 4px 6px 0 rgba(0, 0, 0, 0.1);
    border-radius: 20px;
    border: 0;
    margin-bottom: 1.5em;
  }

  .card-auction:hover {
    transform: scale(1.1);
  }

  .card-img-wrap-auction {
    overflow: hidden;
    position: relative;
    height: 9rem;
    border-radius: 10px;
  }
  .card-img-wrap-auction:after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.2);
    opacity: 0;
    transition: opacity .25s;
  }
  .card-img-wrap-auction img {
    transition: transform .25s;
    width: 100%;
  }
  .card-auction:hover .card-img-wrap-auction img {
    transform: scale(1.2);
  }
  .card-auction:hover .card-img-wrap-auction:after {
    opacity: 1;
  }

  .text-card-auction {
    color: #37251B;
  }

  .bg-gradient-violet {
    background-image: linear-gradient(to bottom right, #22223B, #4A4E69);
  }

  .text-violet {
    color: #4A4E69;
  }

  .img-thumbnail-detail {
    background-color: rgba(242,233,228,0.5);
    border-color: #C9ADA7;
  }

  .card-detail {
    border-color: #C9ADA7;
  }

  .card-header-detail {
    background: #F2E9E4;
    border-color: #C9ADA7;
  }

  .card-body-detail {
    background: rgba(242,233,228,0.5);
  }
</style>
