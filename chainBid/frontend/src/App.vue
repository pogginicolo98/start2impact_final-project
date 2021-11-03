<template>
  <div id="app">
    <NavbarComponent :requestUser="requestUser"
                     v-if="!loading"/>
    <router-view :key="$route.fullPath"
                 v-if="!loading"/>
  </div>
</template>

<script>
  // @ is an alias to /src
  import { apiService } from "@/common/api.service.js";
  import NavbarComponent from "@/components/Navbar.vue";

  export default {
    name: "App",
    components: {
      NavbarComponent
    },
    data() {
      return {
        requestUser: {},
        loading: true
      }
    },
    mounted() {
      /*
        Retrieve current user informations.
      */

      let endpoint = "/api/user/";
      apiService(endpoint)
        .then(response => {
          if (response.detail) {
            console.log(response);
            this.$router.push({name: "not found"});
          } else {
            this.requestUser = response;
            this.loading = false;
            window.localStorage.setItem("requestUserUsername", response.username);
          }
        })
        .catch(error => {
          console.log(error);
          this.$router.push({name: "not found"});
        });
    }
  }
</script>

<style>
  @import "./assets/css/app.css"
</style>
