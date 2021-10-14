<template lang="html">
  <nav class="navbar navbar-expand-lg navbar-dark bg-gradient-violet sticky-top shadow">
    <div class="container">
      <!-- Brand and logo -->
      <router-link class="navbar-brand"
                   :to="{ name: 'home' }">
        <img alt="logo"
             class="d-inline-block mb-2"
             src="../../../static-storage/logo-200x32-orig.png">
      </router-link>

      <!-- Collapsed menu button -->
      <button aria-controls="navbarSupportedContent"
              aria-expanded="false"
              aria-label="Toggle navigation"
              class="navbar-toggler"
              data-bs-target="#navbarSupportedContent"
              data-bs-toggle="collapse"
              type="button">
              <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Navbar elements -->
      <div class="collapse navbar-collapse"
           id="navbarSupportedContent">
           <!-- Links -->
           <ul class="navbar-nav ml-auto mb-2 mb-lg-0">
             <li class="nav-item">
               <router-link class="nav-link"
                            exact
                            :to="{ name: 'home' }"
                            >Live acutions
               </router-link>
             </li>
             <li class="nav-item">
               <router-link class="nav-link"
                            :to="{ name: 'closed auctions' }"
                            >Closed auctions
               </router-link>
             </li>
             <li class="nav-item" v-if="isStaffUser">
               <router-link class="nav-link"
                            :to="{ name: 'schedule auctions' }"
                            >Schedule auctions
               </router-link>
             </li>
             <li class="nav-item">
               <a class="nav-link"
                  href="#"
                  >How it works
               </a>
             </li>
           </ul>

           <!-- Dropdown menu -->
           <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
             <!-- Dropdown button -->
             <li class="nav-item dropdown">
               <a aria-expanded="false"
                  class="nav-link"
                  data-bs-toggle="dropdown"
                  href="#"
                  id="navbarDarkDropdownMenuLink"
                  role="button">
                  <i class="bi bi-person-lines-fill fs-3 nav-icon"></i>
               </a>

               <!-- Dropdown elements -->
               <ul aria-labelledby="navbarDarkDropdownMenuLink"
                   class="dropdown-menu dropdown-menu-dark">
                   <li><h6 class="dropdown-header"
                     >{{ requestUser }}
                   </h6></li>
                   <li><a class="dropdown-item"
                          href="#"
                          >Profile
                   </a></li>
                   <li><a class="dropdown-item"
                          href="#"
                          >Change password
                   </a></li>
                   <li><a class="dropdown-item"
                          href="/accounts/logout/">
                          <i class="bi bi-box-arrow-left fs-5 nav-icon"></i>
                   </a></li>
               </ul>
             </li>
           </ul>
      </div> <!-- Navbar elements -->
    </div> <!-- Container -->
  </nav>
</template>

<script>
  // @ is an alias to /src
  import { apiService } from "@/common/api.service.js";

  export default {
    name: "NavbarComponent",
    data() {
      return {
        requestUser: null,
        isStaffUser: null
      };
    },
    methods: {
      async setUserInfo() {
        /*
          Retrieve the username of the request user and
          store it in the local storage.
        */

        let endpoint = "/api/user/";
        await apiService(endpoint)
          .then(response => {
            this.requestUser = response.username;
            this.isStaffUser = response.is_staff;
            window.localStorage.setItem("username", this.requestUser);
          });
      }
    },
    created() {
      this.setUserInfo();
    }
  }
</script>

<style lang="css">
  .nav-icon {
    color: #ffe3b0;
  }

  .nav-icon:hover {
    color: #ffe169;
  }

  .nav-link:hover {
    color: #f5c8bd !important;
  }

  .router-link-active {
    color: #f5c8bd !important;
  }
</style>
