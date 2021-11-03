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
               <div class="offcanvas-body mx-lg-auto pt-0 pt-lg-0">
                 <ul class="navbar-nav">
                   <li class="nav-item d-lg-none">
                     <p class="text-muted text-center fs-18px fw-bold">{{ user.username }}</p>
                   </li>
                   <li class="nav-item d-lg-none">
                     <div class="row justify-content-between">
                       <div class="col-auto ms-3">
                         <router-link class="btn btn-violet rounded-pill"
                                      :to="{ name: 'profile', params: { slug: user.slug } }"
                                      ><i class="fa-solid fa-user me-2"></i>Profile
                         </router-link>
                       </div>
                       <div class="col-auto me-3">
                         <a class="btn btn-violet rounded-pill"
                            href="/accounts/logout/"
                            ><i class="fa-solid fa-right-from-bracket me-2"></i>Log out
                         </a>
                       </div>
                     </div>
                   </li>
                   <li class="nav-item d-lg-none">
                     <hr class="text-muted">
                   </li>
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
                   <li class="nav-item" v-if="user.is_staff">
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

                <div class="btn-group">
                  <router-link class="nav-link btn-menu"
                               :to="{ name: 'profile', params: { slug: user.slug } }"
                               ><i class="fa-solid fa-user fs-20px"></i>
                  </router-link>
                  <button aria-expanded="false"
                          class="nav-link btn-menu"
                          data-bs-toggle="dropdown"
                          data-bs-display="static"
                          type="button"
                          ><i class="fa-solid fa-chevron-down"></i><span class="visually-hidden">Toggle Dropdown</span>

                  </button>
                  <!-- Dropdown elements -->
                  <ul aria-labelledby="navbarDarkDropdownMenuLink"
                      class="dropdown-menu dropdown-menu-dark dropdown-menu-lg-end">
                      <li>
                        <router-link class="dropdown-item"
                                     :to="{ name: 'profile', params: { slug: user.slug } }"
                                     >{{ user.username }}
                        </router-link>
                      </li>
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
                </div>
              </li>
            </ul>
          </div>
        </div>
    </div>
  </nav>
</template>

<script>
  export default {
    name: "NavbarComponent",
    props: {
      requestUser: {
        type: Object,
        required: true
      }
    },
    data() {
      return {
        user: this.requestUser
      };
    }
  }
</script>

<style lang="css" scoped>
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
