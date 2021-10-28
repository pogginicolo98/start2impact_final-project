<template lang="html">
  <div class="profile">
    <!-- Error 404 -->
    <div class="not-found"
         v-if="notFound">
         <Error404Component/>
    </div>

    <!-- Profile -->
    <div class="container mt-3"
         v-else>
         <!-- Title -->
         <div class="text-center fw-bold fs-32px">
           <p>Auctions won</p>
         </div>

         <!-- Auctions won -->
         <div class="row justify-content-start mt-4"
              v-if="auctions.length > 0">
              <div class="col-12"
                   v-for="(auction, index) in auctions"
                   :key="index">
                   <!-- Card -->
                   <router-link :to="{ name: 'closed auction detail', params: { id: auction.id } }">
                     <div class="card card-auction position-relative text-card-auction mb-3"
                          style="width: 100%; height: 7rem;">
                          <div class="card-body">
                            <div class="row">
                              <div class="col-2">
                                <!-- Card image -->
                                  <img alt="product image"
                                       class="img-fluid"
                                       :src="auction.image">
                              </div>
                              <div class="col-6">
                                <!-- Card title -->
                                <p class="text-truncate fw-bold fs-24px mb-2">{{ auction.title }}</p>
                                <p class="text-muted text-truncate fs-14px" v-if="!auction.description">No description provided</p>
                                <p class="text-muted text-truncate fs-14px" v-else>{{ auction.description }}</p>
                              </div>
                              <div class="col-2">
                                <!-- Card body -->
                                <p class="fs-20px">{{ auction.final_price }} €</p>
                                <!-- Card footer -->
                                <p class="text-muted fs-14px">{{ getDate(auction.closed_at) }}</p>
                              </div>
                              <div class="col-2 d-flex align-items-end">
                                <div class="ms-auto">
                                  <a class="btn btn-violet rounded-pill"
                                     download
                                     :href="auction.json_file"
                                     >Download<i class="fa-solid fa-file-arrow-down ms-2"></i>
                                  </a>
                                </div>
                              </div>
                            </div>
                          </div>
                     </div>
                   </router-link> <!-- Card -->
              </div> <!-- Col -->
         </div> <!-- Auctions won -->

         <!-- No auction won -->
         <div class="text-center mt-5"
              v-else>
              <p class="fs-20px fw-blod text-muted">No auction won</p>
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
    data() {
      return {
        auctions: [],
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
      getDate(date) {
        return moment.utc(date, 'YYYY/MM/DD - HH:mm:ss').format('YYYY/MM/DD - HH:mm:ss');
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
      this.getAuctions();
      this.getNextAuctions();
    }
  }
</script>

<style lang="css" scoped>
</style>
