<template lang="html">
  <div class="auction-detail">
    <!-- Error 404 -->
    <div class="not-found"
         v-if="notFound">
         <Error404Component :auctionNotAvailable="true"/>
    </div>

    <!-- Auction detail -->
    <div class="container mt-3 mt-lg-4"
         v-else>
         <div class="row">
           <!-- Title mobile formats -->
           <div class="col-12 d-lg-none">
             <p class="text-truncate fw-bold fs-32px mb-2 ms-2">{{ auction.title }}</p>
           </div>

           <!-- Image and description -->
           <div class="col-12 col-lg-5 mt-3">
             <!-- Image -->
             <div class="col-12">
               <figure class="figure">
                <img alt="product image"
                     class="figure-img img-fluid rounded img-thumbnail-detail"
                     :src="auction.image">
               </figure>
             </div>

             <!-- Description desktop formats -->
             <div class="col-12 d-none d-lg-block">
               <div class="card card-detail"
                    style="width: 100%">
                    <div class="card-header card-header-detail">
                      <i class="fa-solid fa-align-left me-2"></i><span class="fs-18px fw-bold">Description</span>
                    </div>
                    <div class="card-body card-body-detail pb-1">
                      <p class="text-muted mb-2"
                         v-if="!auction.description"
                         >No description provided
                      </p>
                      <p class="mb-2"
                         v-else
                         >{{ auction.description }}
                      </p>
                      <p class="text-muted fs-14px mb-0"><strong>Initial price</strong>: {{ auction.initial_price }} €</p>
                      <p class="text-muted fs-14px mb-0"><strong>Opened</strong>: {{ getOpenedAtFromNow }}</p>
                    </div>
               </div>
             </div>
           </div>

           <!-- Bid -->
           <div class="col-12 col-lg-7 mb-2">
             <!-- Title desktop formats -->
             <p class="text-truncate fs-32px fw-bold d-none d-lg-block mb-3 ms-2">{{ auction.title }}</p>

             <!-- Card -->
             <div class="card card-detail">
               <div class="card-body card-body-detail">
                 <div class="row mb-4">
                   <div class="col-12 text-danger fs-20px fw-bold"
                        v-if="auctionClosed"
                        ><p>Auction closed</p>
                   </div>

                   <template v-else>
                     <!-- Current price -->
                     <div class="col-auto">
                       <p class="text-muted fs-15px fw-bold mb-0">Current price</p>
                       <p class="fs-20px mb-0">{{ lastPrice }} €</p>
                     </div>

                     <!-- Remaining time -->
                     <div class="col-auto">
                       <p class="text-muted fs-15px fw-bold mb-0">Closing in</p>
                       <p class="text-danger fs-20px mb-0"
                          v-if="remainingTime !== null"
                          >{{ getRemainingTime }}
                       </p>
                       <p class="fs-20px mb-0"
                          v-else
                          >Less than 24 hours
                       </p>
                     </div>
                   </template>
                 </div>

                 <!-- Form -->
                 <BidFormComponent :auction="auction"
                                   :bidSocket="bidSocket"
                                   :enabled="getFormEnabled"/>
               </div>
             </div> <!-- Card -->
           </div> <!-- Bid -->
         </div> <!-- Row 1 -->

         <!-- Description mobile formats -->
         <div class="row d-lg-none">
           <div class="col-12">
             <div class="card card-detail mt-3"
                  style="width: 100%">
                  <div class="card-header card-header-detail">
                    <i class="fa-solid fa-align-left me-2"></i><span class="fs-18px fw-bold">Description</span>
                  </div>
                  <div class="card-body card-body-detail pb-1">
                    <p class="text-muted mb-2"
                       v-if="!auction.description"
                       >No description provided
                    </p>
                    <p class="mb-2"
                       v-else
                       >{{ auction.description }}
                    </p>
                    <p class="text-muted fs-14px mb-0"><strong>Initial price</strong>: {{ auction.initial_price }} €</p>
                    <p class="text-muted fs-14px mb-0"><strong>Opened</strong>: {{ getOpenedAtFromNow }}</p>
                  </div>
             </div>
           </div>
         </div> <!-- Row 2 -->
    </div> <!-- Container -->
  </div>
</template>

<script>
  // @ is an alias to /src
  import { apiService } from "@/common/api.service.js";
  import BidFormComponent from "@/components/BidForm.vue";
  import Error404Component from "@/components/Error404.vue";
  import * as ReconnectingWebSocket from "../../../static-storage/js/reconnecting-websocket.min.js";
  import moment from 'moment';

  export default {
    name: "Auction",
    components: {
      BidFormComponent,
      Error404Component
    },
    props: {
      id: {
        type: Number,
        required: true
      }
    },
    data() {
      return {
        auction: {},
        auctionClosed: false,
        isLastUser: false,
        lastPrice: null,
        remainingTime: null,
        bidSocket: null,
        timerDisplay: null,
        notFound: false
      };
    },
    computed: {
      getRemainingTime() {
        /*
          Format remainingTime in a timer (ex. 70 seconds -> 01:10).
        */

        var minutes = Math.floor(this.remainingTime / 60);
        var seconds = this.remainingTime - (minutes * 60);
        if (minutes < 10) {minutes = "0"+minutes;}
        if (seconds < 10) {seconds = "0"+seconds;}
        return `${minutes}:${seconds}`;
      },
      getOpenedAtFromNow() {
        return moment(this.auction.opened_at).fromNow();
      },
      getFormEnabled() {
        return this.isLastUser || this.auctionClosed;
      }
    },
    methods: {
      async getAuctionData() {
        /*
          Retrieve auction's data and set the page title.
        */

        let endpoint = `/api/auctions/${this.id}/`;
        await apiService(endpoint)
          .then(response => {
            if (response.detail) {
              console.log(response.detail);
              this.notFound = true;
            } else {
              this.auction = response;
              this.lastPrice = response.last_price;
              document.title = `${response.title} | Live auctions | ChainBid`;
            }
          })
          .catch(error => {
            console.log(error);
            this.notFound = true;
          });
      },
      decrementTimerDisplay() {
        if (this.remainingTime > 0) {
          this.remainingTime -= 1;
        } else {
          clearInterval(this.timerDisplay);
        }
      },
      createBidSocket() {
        /*
          Create a websocket and connect it to the Bid consumer.
        */

        this.bidSocket = new ReconnectingWebSocket(
            'ws://'
            + window.location.host
            + '/ws/auctions/'
            + this.id
            + '/bid/'
        );
        this.bidSocket.onmessage = e => {
            let data = JSON.parse(e.data);
            if (data.errors) {
              console.error(data.errors);
              this.notFound = true;
            } else if (data.closed) {
              this.remainingTime = null;
              this.auctionClosed = true;
              if (data.is_winner) {
                this.$toasted.show('You have won!', {icon: "gift"});
              }
              this.bidSocket.close();
            } else {
              this.isLastUser = data.is_last_user;
              this.lastPrice = data.last_price;
              this.remainingTime = data.remaining_time;
              if (data.remaining_time) {
                clearInterval(this.timerDisplay);
                this.timerDisplay = setInterval(this.decrementTimerDisplay, 1000);
              }
            }
        };
      }
    },
    created() {
      this.createBidSocket();
      this.getAuctionData();
    },
    beforeDestroy() {
      clearInterval(this.timerDisplay);
    }
  }
</script>

<style lang="css" scoped>
</style>
