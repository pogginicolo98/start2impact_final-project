<template lang="html">
  <div class="container mt-4 mt-lg-5">
    <div class="row">
      <!-- Title mobile formats -->
      <div class="col-12 d-lg-none">
        <p class="text-card-auction fw-bold fs-32px mb-2 ms-2">{{ auction.title }}</p>
      </div>

      <!-- Image -->
      <div class="col-12 col-lg-5 mt-0 mt-lg-3">
        <figure class="figure">
         <img alt="product image"
              class="figure-img img-fluid rounded img-thumbnail-detail"
              :src="auction.image">
        </figure>
      </div>

      <!-- Bid -->
      <div class="col-12 col-lg-7 mt-3 mt-lg-0">
        <!-- Title desktop formats -->
        <p class="text-card-auction fs-32px fw-bold d-none d-lg-block mb-3 ms-2">{{ auction.title }}</p>
        <!-- Card -->
        <div class="card card-detail">
          <div class="card-body card-body-detail">
            <div class="row mb-4">
              <!-- Current price -->
              <div class="col-auto">
                <p class="text-muted fs-15px fw-bold mb-0">Current price</p>
                <p class="text-card-auction fs-20px mb-0">{{ lastPrice }} €</p>
              </div>

              <!-- Remaining time -->
              <div class="col-auto">
                <p class="text-muted fs-15px fw-bold mb-0">Closing in</p>
                <template v-if="isStarted">
                  <p class="text-danger fs-20px mb-0">{{ getRemainingTime }}</p>
                </template>
                <template v-else>
                  <p class="text-card-auction fs-20px mb-0">Less than 24 hours</p>
                </template>
              </div>
            </div>

            <!-- Form -->
            <BidFormComponent :auction="auction"
                              :isLastUser="isLastUser"/>
          </div>
        </div> <!-- Card -->
      </div> <!-- Bid -->
    </div> <!-- Row 1 -->

    <!-- Description -->
    <div class="row">
      <div class="col-12 col-lg-5">
        <div class="card card-detail mt-3"
             style="width: 100%">
             <div class="card-header card-header-detail text-card-auction">
               <i class="fa-solid fa-align-left me-2"></i><span class="fs-18px fw-bold">Description</span>
             </div>
             <div class="card-body card-body-detail pb-1">
               <p class="text-card-auction mb-2">{{ auction.description }}</p>
               <p class="text-muted fs-14px mb-0"><strong>Initial price</strong>: {{ auction.initial_price }} €</p>
               <p class="text-muted fs-14px mb-0"><strong>Opened</strong>: {{ getOpenedAtFromNow }}</p>
               <!-- <p class="text-muted fs-14px mb-0">Opened {{ getOpenedAtFromNow }}</p> -->
             </div>
        </div>
      </div>
    </div> <!-- Row 2 -->
  </div> <!-- Container -->
</template>

<script>
  // @ is an alias to /src
  import { apiService } from "@/common/api.service.js";
  import BidFormComponent from "@/components/BidForm.vue";
  import moment from 'moment';

  export default {
    name: "Auction",
    props: {
      id: {
        type: Number,
        required: true
      }
    },
    components: {
      BidFormComponent
    },
    data() {
      return {
        auction: {},
        isLastUser: false,
        lastPrice: null,
        remainingTime: null,
        timerInfo: null,
        timerDisplay: null
      };
    },
    computed: {
      isStarted() {
        return this.remainingTime !== null;
      },
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
            this.auction = response;
            this.lastPrice = response.last_price;
            document.title = `${response.title} | ChainBid`;
          });
      },
      async getAuctionInfo() {
        /*
          Retrieve last bid.
        */

        let endpoint = `/api/auctions/${this.id}/info/`;
        await apiService(endpoint)
          .then(response => {
            this.isLastUser = response.is_last_user;
            this.lastPrice = response.last_price;
            if (this.remainingTime === null && response.remaining_time != null) {
              // Initialize timerDisplay
              this.remainingTime = response.remaining_time;
              this.timerDisplay = setInterval(this.decrementTimerDisplay, 1000);
            } else if (this.remainingTime < response.remaining_time - 2 || this.remainingTime > response.remaining_time + 2) {
              // Reset timerDisplay if it differs from the original for more than +-2 seconds
              this.remainingTime = response.remaining_time;
              clearInterval(this.timerDisplay);
              this.timerDisplay = setInterval(this.decrementTimerDisplay, 1000);
            }
          });
      },
      clearTimers() {
          clearInterval(this.timerInfo);
          clearInterval(this.timerDisplay);
      },
      decrementTimerDisplay() {
        if (this.remainingTime > 0) {
          this.remainingTime -= 1;
        } else {
          clearInterval(this.timerDisplay);
        }
      }
    },
    created() {
      this.getAuctionData();
      this.timerInfo = setInterval(this.getAuctionInfo, 1000);
    },
    beforeDestroy() {
      this.clearTimers();
    }
  }
</script>

<style lang="css" scoped>
  .icon {
    font-size: 24px;
  }
</style>
