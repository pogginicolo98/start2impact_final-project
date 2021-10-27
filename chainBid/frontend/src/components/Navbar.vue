<template lang="html">
  <nav class="navbar navbar-expand-lg navbar-dark bg-gradient-violet-navbar sticky-top shadow">
    <div class="container">
        <div class="col-8 col-lg-2">
          <!-- Brand and logo -->
          <router-link class="navbar-brand"
                       :to="{ name: 'home' }"
                       ><img alt="logo"
                             class="d-inline-block mb-2"
                             src="../../../static-storage/assets/favicon x32.png">
                        ChainBid
          </router-link>
        </div>
        <div class="col-4 col-lg-8">
          <!-- Collapsed menu button -->
          <div class="text-end">
            <button aria-controls="offcanvasNavbar"
                    class="navbar-toggler"
                    data-bs-target="#offcanvasNavbar"
                    data-bs-toggle="offcanvas"
                    type="button"
                    ><span class="navbar-toggler-icon"></span>
            </button>
          </div>

          <div aria-labelledby="offcanvasNavbarLabel"
               class="offcanvas offcanvas-end mx-auto"
               id="offcanvasNavbar"
               tabindex="-1">
               <div class="offcanvas-header">
                 <!-- Brand and logo -->
                 <router-link class="navbar-brand"
                              :to="{ name: 'home' }"
                              ><img alt="logo"
                                    class="d-inline-block mb-2"
                                    src="../../../static-storage/assets/favicon x32.png">
                              ChainBid
                 </router-link>
                 <button aria-label="Close"
                         class="fa-solid fa-xmark btn-menu text-muted fs-32px"
                         data-bs-dismiss="offcanvas"
                         type="button">
                 </button>
               </div>
               <div class="offcanvas-body mx-lg-auto">
                 <ul class="navbar-nav">
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
               </div>
          </div>
        </div>

        <div class="col-2 d-none d-lg-block">
          <div class="d-flex justify-content-end">
            <!-- Dropdown menu -->
            <ul class="navbar-nav">
              <!-- Dropdown button -->
              <li class="nav-item dropdown">
                <a aria-expanded="false"
                   class="nav-link"
                   data-bs-toggle="dropdown"
                   href="#"
                   id="navbarDarkDropdownMenuLink"
                   role="button">
                   <i class="fa-solid fa-user-gear fs-24px"></i>
                </a>

                <!-- Dropdown elements -->
                <ul aria-labelledby="navbarDarkDropdownMenuLink"
                    class="dropdown-menu dropdown-menu-dark">
                    <li><h6 class="dropdown-header">{{ requestUser }}</h6></li>
                    <li>
                      <a class="dropdown-item"
                           href="/accounts/password_change/"
                           >Change password
                      </a>
                    </li>
                    <li>
                      <a class="dropdown-item"
                           href="/accounts/logout/"
                           ><i class="fa-solid fa-right-from-bracket fs-14px me-2"></i>Log out
                      </a>
                    </li>
                </ul>
              </li>
            </ul>
          </div>
        </div>
    </div>
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
            if (response.detail) {
              console.log(response);
              this.$router.push({name: "not found"});
            } else {
              this.requestUser = response.username;
              this.isStaffUser = response.is_staff;
              window.localStorage.setItem("username", this.requestUser);
            }
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

  .btn-menu {
    background: rgba(0, 0, 0, 0.01);
    border: 0px;
  }

  @media screen and (max-width: 992px) {
    .offcanvas {
      background-image: linear-gradient(to bottom, #22223B, #4A4E69) !important;
    }

    .offcanvas-end {
      width: 300px;
    }
  }

  @media screen and (min-width: 992px) {
    .offcanvas-end {
      width: 600px;
    }
  }
</style>
