<template>
  <div class="home">
    <!-- Error 404 -->
    <div class="not-found"
         v-if="notFound">
         <Error404Component/>
    </div>

    <!-- Homepage -->
    <div class="container mt-3"
         v-else>
         <!-- Title -->
         <div class="text-center fw-bold fs-32px">
           <p>Live auctions</p>
         </div>

         <!-- Auctions -->
         <div class="row justify-content-start mt-4"
              v-if="auctions.length > 0">
              <div class="col-12 col-md-6 col-lg-4 col-xxl-3"
                   v-for="(auction, index) in auctions"
                   :key="index">
                   <!-- Card -->
                   <router-link :to="{ name: 'auction', params: { id: auction.id } }">
                     <div class="card card-auction position-relative text-card-auction mb-4 mx-auto"
                          style="width: 18rem; height: 21rem;">
                          <div class="card-body text-center">
                            <!-- Card title -->
                            <p class="text-truncate fw-bold fs-24px mb-2">{{ auction.title }}</p>

                            <!-- Card image -->
                            <div class="card-img-wrap-auction">
                              <img alt="product image"
                                   class="card-img-auction"
                                   :src="auction.image">
                            </div>

                            <!-- Card body -->
                            <p class="fs-20px mt-3 mb-1">{{ auction.last_price }} €</p>
                            <p class="text-danger fs-17px"
                               v-if="auction.remaining_time"
                               >Started
                            </p>
                            <p class="text-muted fs-17px"
                               v-else
                               >No bids yet
                            </p>
                          </div>

                          <!-- Card footer -->
                          <div class="position-absolute bottom-0 start-50 translate-middle-x text-center"
                               style="width: 90%">
                               <hr class="mb-1">
                               <p class="text-muted fs-14px mb-1">{{ getDateFromNow(auction.opened_at) }}</p>
                          </div>
                     </div>
                   </router-link> <!-- Card -->
              </div> <!-- Col -->
      </div> <!-- Auctions -->

      <!-- No live auctions -->
      <div class="text-center mt-5"
           v-else>
           <p class="fs-20px fw-blod text-muted">We are sorry but there are no live auctions at the moment...</p>
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
    </div> <!-- Container -->
  </div>
</template>

<script>
  // @ is an alias to /src
  import { apiService } from "@/common/api.service.js";
  import Error404Component from "@/components/Error404.vue";
  import moment from 'moment';

  export default {
    name: "Home",
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

        let endpoint = "/api/auctions/";
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
      getDateFromNow(date) {
        return moment(date).fromNow();
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
      document.title = "Live auctions | ChainBid";
      this.getAuctions();
      this.getNextAuctions();
    }
  };
</script>

<style lang="css" scoped>
</style>
