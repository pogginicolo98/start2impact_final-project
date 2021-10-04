<template lang="html">
  <div>
    <form novalidate
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
                     v-model="amount"
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
</template>

<script>
  // @ is an alias to /src
  import { apiService } from "@/common/api.service.js";

  export default {
    name: "BidFormComponent",
    props: {
      id: {
        type: Number,
        required: true
      },
      isLastUser: {
        type: Boolean,
        required: true
      }
    },
    data() {
      return {
        amount: null,
        error: null
      };
    },
    methods: {
      async onSubmit() {
        /*
          Send a new bid.
        */

        if (!this.amount) {
          this.error = "Please enter a valid amount.";
        } else {
          if (this.error) {
            this.error = null;
          }
          let endpoint = `/api/auctions/${this.id}/bid/`;
          let method = "POST";
          let data = { price: this.amount };
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
    }
  }
</script>

<style lang="css" scoped>
</style>
