<template lang="html">
  <div class="container mt-3 mt-lg-5">
    <div class="row">
      <div class="col-12 d-lg-none mb-2">
        <h1>{{ auction.title }}</h1>
      </div>

      <!-- Image -->
      <div class="col-12 col-lg-5">
        <img alt="product image"
             class="img-fluid img-thumbnail"
             :src="auction.image">
      </div>

      <!-- Bid -->
      <div class="col-12 col-lg-7 mt-3 mt-lg-0">
        <h1 class="d-none d-lg-block">{{ auction.title }}</h1>
        <div class="card">
          <div class="card-body">
            <div class="row mb-4">
              <!-- Current price -->
              <div class="col-auto">
                <p class="card-text text-muted fs-14px mb-0">Current price</p>
                <p class="card-text text-success fs-5"><strong>€{{ lastPrice }}</strong></p>
              </div>

              <!-- Remaining time -->
              <div class="col-auto">
                <p class="card-text text-muted fs-14px mb-0">Remaining time</p>
                <template v-if="auctionStarted">
                  <p class="card-text text-danger fs-5"><strong>{{ getRemainingTime }}</strong></p>
                </template>
                <template v-else>
                  <p class="card-text text-muted fs-5">Less than 24 hours</p>
                </template>
              </div>
            </div>

            <!-- Form -->
            <form
                  @submit.prevent="onSubmit">
                  <!-- Input -->
                  <div class="col-12 col-sm-6 col-md-5 col-lg-6 col-xl-5 col-xxl-4">
                    <div class="fs-15px">
                      <label class="visually-hidden"
                             for="floatingInput"
                             >Amount
                      </label>
                      <input aria-label="Amount"
                             class="form-control"
                             id="floatingInput"
                             placeholder="Amount"
                             step="0.01"
                             type="number"
                             v-model="bidAmount"
                             :disabled="isLastUser">
                    </div>
                  </div>

                  <!-- Button -->
                  <div class="col-12 col-sm-6 col-md-5 col-lg-6 col-xl-5 col-xxl-4 mt-2 d-grid d-block">
                    <button class="btn btn-success"
                            type="submit"
                            :class="{'btn-danger': isLastUser,
                                     'btn-success': !isLastUser}"
                            :disabled="isLastUser"
                            >Place a bid
                    </button>
                  </div>
            </form>
            <p class="text-danger mt-2">{{ error }}</p>
          </div>
        </div>
      </div> <!-- Bid -->
    </div> <!-- Row 1 -->

    <!-- Description -->
    <div class="row">
      <div class="col-12 col-lg-5">
        <div class="card mt-3" style="width: 100%">
          <div class="card-header">
            <i class="bi bi-justify-left icon"></i><span class="fw-bold fs-18px"> Description</span>
          </div>
          <div class="card-body">
            <p class="card-text my-2">{{ auction.description }}</p>
            <p class="card-text text-muted fs-14px mb-0">Initial price: {{ auction.last_price }} €</p>
            <p class="card-text text-muted fs-14px mb-2">Opened {{ getOpenedAt }}</p>
          </div>
        </div>
      </div>
    </div> <!-- Row 2 -->
  </div> <!-- Container -->
</template>

<script>
  // @ is an alias to /src
  import { apiService } from "@/common/api.service.js";
  import moment from 'moment';

  export default {
    name: "Auction",
    props: {
      id: {
        type: Number,
        required: true
      }
    },
    data() {
      return {
        auction: {},
        error: null,
        isLastUser: false,
        lastPrice: null,
        remainingTime: null,
        timerInfo: null,
        timerDisplay: null,
        bidAmount: null
      };
    },
    computed: {
      auctionStarted() {
        return this.remainingTime !== null;
      },
      getRemainingTime() {
        /*
          Convert remainingTime (seconds as Number) into Time format as string.
        */

        var minutes = Math.floor(this.remainingTime / 60);
        var seconds = this.remainingTime - (minutes * 60);
        if (minutes < 10) {minutes = "0"+minutes;}
        if (seconds < 10) {seconds = "0"+seconds;}
        return `${minutes}:${seconds}`;
      },
      getOpenedAt() {
        return moment(this.auction.opened_at).fromNow();
      }
    },
    methods: {
      setPageTitle(title) {
        document.title = title;
      },
      async getAuctionData() {
        /*
          Retrieve a specific auction's data and set page title.
        */

        let endpoint = `/api/auctions/${this.id}/`;
        await apiService(endpoint)
          .then(response => {
            this.auction = response;
            this.lastPrice = response.last_price;
            this.setPageTitle(response.title);
          });
      },
      async getAuctionInfo() {
        /*
          Retrieve auction's info about last bid.
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
      },
      async onSubmit() {
        if (!this.bidAmount) {
          this.error = "Please enter a valid amount.";
        } else {
            let endpoint = `/api/auctions/${this.id}/bid/`;
            let method = "POST";
            let data = { price: this.bidAmount };
            await apiService(endpoint, method, data)
              .then(response => {
                if (response.detail) {
                  this.error = response.detail;
                } else if (response) {
                  let objKeys = Object.keys(response);
                  this.error = response[objKeys[0]][0];
                }
              });
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
  .fs-18px {
    font-size: 18px;
  }

  .fs-15px {
    font-size: 15px;
  }

  .fs-14px {
    font-size: 14px;
  }

  .icon {
    font-size: 24px;
  }

  .card-header {
    background-color: white;
  }

  .card-body {
    background-color: rgba(0,0,0,.03);
  }
</style>
