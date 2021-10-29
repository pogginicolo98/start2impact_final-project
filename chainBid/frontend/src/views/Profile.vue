<template lang="html">
  <div class="profile">
    <!-- Error 404 -->
    <div class="not-found"
         v-if="notFound">
         <Error404Component/>
    </div>

    <!-- Profile -->
    <div class="container mt-5"
         v-else>
         <div class="row mt-4">
           <div class="col-12 col-xl-4">
             <div class="card card-detail"
                  style="width: 100%">
                  <div class="card-header card-header-detail">
                    <i class="fa-solid fa-circle-user fs-20px me-2"></i><span class="fs-20px fw-bold">Account</span>
                  </div>
                  <div class="card-body card-body-detail">
                    <p class="fs-17px mb-0"><strong>Username: </strong>{{ profile.username }}</p>
                    <p class="fs-17px mb-0"><strong>Email: </strong>{{ profile.email }}</p>
                    <p class="fs-17px"><strong>Auctions won: </strong>{{ profile.auctions_won }}</p>
                    <div class="row justify-content-between mt-5">
                      <div class="col-12 col-sm-auto d-grid d-sm-block">
                        <a class="btn btn-violet rounded-pill"
                             href="/accounts/password_change/"
                             ><i class="fa-solid fa-pen me-2"></i>Change password
                        </a>
                      </div>
                      <div class="col-12 col-sm-auto d-grid d-sm-block mt-1 mt-sm-0">
                        <a class="btn btn-violet rounded-pill"
                           href="/accounts/logout/"
                           ><i class="fa-solid fa-right-from-bracket me-2"></i>Log out
                        </a>
                      </div>
                    </div>
                  </div>
             </div>
           </div>
           <div class="col-12 col-xl-8 mt-4 mt-xl-0">
             <p class="fs-24px fw-bold text-center">Auctions won</p>
             <!-- Auctions won -->
             <div v-if="auctions.length > 0">
               <div class="col-12"
                    v-for="(auction, index) in auctions"
                    :key="index">
                    <!-- Card -->
                      <div class="card card-auction-profile mb-3"
                           style="width: 100%; height: 5rem;">

                             <div class="row">
                               <div class="col-md-2 d-none d-md-block">
                                 <router-link :to="{ name: 'closed auction detail', params: { id: auction.id } }">
                                   <!-- Card image -->
                                   <div class="img-test-wrap">
                                     <img alt="product image"
                                          class="img-test rounded"
                                          :src="auction.image">
                                   </div>
                                 </router-link> <!-- Card -->
                               </div>
                               <div class="col-12 col-md-10 ps-md-0">
                                 <div class="card-body">
                                   <div class="row pe-2">
                                     <div class="col-12 col-md-7 col-xxl-8">
                                       <router-link :to="{ name: 'closed auction detail', params: { id: auction.id } }">
                                         <p class="text-card-auction text-truncate fw-bold fs-20px mb-0">{{ auction.title }}</p>
                                         <div class="d-none d-md-block">
                                           <p class="text-muted fs-14px mb-0" v-if="!auction.description">No description provided</p>
                                           <p class="text-muted text-truncate fs-14px mb-0" v-else>{{ auction.description }}</p>
                                         </div>
                                         <div class="row d-md-none justify-content-between">
                                           <div class="col-auto">
                                             <p class="text-card-auction fs-16px">{{ auction.final_price }} €</p>
                                           </div>
                                           <div class="col-auto">
                                             <p class="text-muted fs-14px">{{ getDate(auction.closed_at) }}</p>
                                           </div>
                                         </div>
                                       </router-link>
                                     </div>
                                     <div class="col-md-4 col-xxl-3 d-none d-md-block align-self-end text-center">
                                       <p class="fs-16px mb-0">{{ auction.final_price }} €</p>
                                       <p class="text-muted fs-14px mb-0">{{ getDate(auction.closed_at) }}</p>
                                     </div>
                                     <div class="col-md-1 d-none d-md-block align-self-center p-0 text-end">
                                       <a class="btn btn-violet rounded-pill"
                                          download
                                          :href="auction.json_file"
                                          v-if="auction.json_file"
                                          ><i class="fa-solid fa-file-arrow-down"></i>
                                       </a>
                                       <a class="btn btn-warning disabled rounded-pill"
                                          href="#"
                                          v-else
                                          ><i class="fa-solid fa-triangle-exclamation"></i>
                                       </a>
                                     </div>
                                   </div>
                                 </div>
                               </div>
                             </div>
                      </div>
               </div> <!-- Col -->
             </div> <!-- Auctions won -->

             <!-- No auction won -->
             <div class="text-center mt-5"
                  v-else>
                  <p class="fs-20px fw-blod text-muted" v-if="profile.username === requestUser">You haven't won any auctions yet</p>
                  <p class="fs-20px fw-blod text-muted" v-else>The user has not won any auctions yet</p>
             </div>
           </div>
         </div>

         <!-- Pagination -->
         <div :class="{'position-absolute top-50 start-50 translate-middle': firstLoading,
                       'mb-5 mt-2 text-center': !firstLoading}">
           <div v-show="loadingAuctions">
             <div class="spinner-grow text-violet"
                  role="status"
                  style="width: 3rem; height: 3rem;">
             </div>
           </div>
         </div>
    </div>
  </div>
</template>

<script>
  // @ is an alias to /src
  import { apiService } from "@/common/api.service.js";
  import Error404Component from "@/components/Error404.vue";
  import moment from 'moment';

  export default {
    name: "Profile",
    components: {
      Error404Component
    },
    props: {
      slug: {
        type: String,
        required: true
      }
    },
    data() {
      return {
        auctions: [],
        profile: null,
        requestUser: null,
        firstLoading: true,
        next: null,
        loadingAuctions: false,
        notFound: false
      }
    },
    methods: {
      async getAuctions() {
        /*
          Retrieve active auctions according to pagination.
        */

        let endpoint = "/api/user-closed-auctions/";
        if (this.next) {
          endpoint = this.next;
        }
        this.loadingAuctions = true;
        await apiService(endpoint)
          .then(response => {
            if (response.detail) {
              console.log(response.detail);
              this.notFound = true;
            } else {
              this.auctions.push(...response.results);
              this.loadingAuctions = false;
              if (response.next) {
                this.next = response.next;
              } else {
                this.next = null;
              }
              if (this.firstLoading) {
                this.firstLoading = false;
              }
            }
          })
          .catch(error => {
            console.log(error);
            this.notFound = true;
          });
      },
      async getProfile() {
        /*
          Retrieve active auctions according to pagination.
        */

        let endpoint = `/api/profile/${this.slug}/`;
        await apiService(endpoint)
          .then(response => {
            if (response.detail) {
              console.log(response.detail);
              this.notFound = true;
            } else {
              this.profile = response;
            }
          })
          .catch(error => {
            console.log(error);
            this.notFound = true;
          });
      },
      getDate(date) {
        return moment.utc(date, 'YYYY/MM/DD').format('YYYY/MM/DD');
      },
      getNextAuctions() {
        /*
          Retrieve new auction when scrolling down.
        */

        window.onscroll = () => {
          if (this.next && !this.loadingAuctions) {
            let bottomOfWindow = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight;
            if (bottomOfWindow) {
              this.getAuctions();
            }
          }
        }
      }
    },
    created() {
      document.title = "Profile | ChainBid";
      this.requestUser = window.localStorage.getItem("requestUser");
      this.getAuctions();
      this.getProfile();
      this.getNextAuctions();
    }
  }
</script>

<style lang="css" scoped>
  .img-test {
    width:100%;
    height:100%;
    object-fit: cover;
    overflow: hidden;
  }

  .img-test-wrap {
    height: 65px;
    overflow: hidden;
    position: relative;
    border-radius: 10px;
    margin-top: 7.5px;
    margin-left: 7.5px;
  }

  .card-auction-profile {
    background-color: #F8F4F1;
    box-shadow: 0 4px 6px 0 rgba(0, 0, 0, 0.1);
    border-radius: 20px;
    border: 0;
  }
</style>
