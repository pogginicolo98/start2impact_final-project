<template lang="html">
  <div>
    <form novalidate
          @submit.prevent="onSubmit">
          <!-- Input -->
          <div class="col-12 col-sm-6 col-md-5 col-lg-6 col-xl-5 col-xxl-4">
            <div class="input-group has-validation fs-15px">
              <span class="input-group-text" style="border-radius: 50rem 0px 0px 50rem"><i class="fa-solid fa-euro-sign"></i></span>
              <input aria-describedby="euro-symbol"
                     class="form-control"
                     style="border-radius: 0px 50rem 50rem 0px"
                     placeholder="Price"
                     step="0.01"
                     type="number"
                     v-model="newPrice.value"
                     :class="{'is-invalid': isInitialPriceInvalid}"
                     :disabled="isLastUser">
              <div class="invalid-feedback">
                <ul>
                  <li v-for="(error, index) in newPrice.errors"
                      :key="index"
                      >{{ error }}
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Button -->
          <div class="col-12 col-sm-6 col-md-5 col-lg-6 col-xl-5 col-xxl-4 mt-2 d-grid d-block">
            <button class="btn btn-primary rounded-pill"
                    type="submit"
                    :class="{'btn-danger': isLastUser,
                             'btn-primary': !isLastUser}"
                    :disabled="isLastUser"
                    >Place a bid <i class="fa-solid fa-hand"></i>
            </button>
          </div>
    </form>
  </div>
</template>

<script>
  // @ is an alias to /src
  import { apiService } from "@/common/api.service.js";
  import { countDecimalPlaces } from "@/common/utility.js";

  export default {
    name: "BidFormComponent",
    props: {
      auction: {
        type: Object,
        required: true
      },
      isLastUser: {
        type: Boolean,
        required: true
      }
    },
    data() {
      return {
        newPrice: {
          value: null,
          errors: []
        },
        error: null
      };
    },
    computed: {
      isInitialPriceInvalid() {
        return this.newPrice.errors.length != 0;
      }
    },
    methods: {
      validateForm() {
        /*
          Validation bid form fields.

          :fields
          -price:
              1) 999999999.99 maximum value.
              2) 2 decimals maximum.
              3) Higher than last_price.
        */

        let formIsValid = true;
        // Price validation
        this.newPrice.errors = [];
        if (this.newPrice.value > this.auction.last_price) {
          let decimals = countDecimalPlaces(this.newPrice.value)
          if (this.newPrice.value > 999999999.99) {
            this.newPrice.errors.push("Maximum allowed price: €9999999999.99");
            formIsValid = false;
          }
          if (decimals > 2) {
            this.newPrice.errors.push("Please enter a price with no more than 2 decimals.");
            formIsValid = false;
          }
        } else {
          this.newPrice.errors.push("Please enter a price higher than the current price.");
          formIsValid = false;
        }
        return formIsValid;
      },
      async onSubmit() {
        /*
          Send a new bid.
        */

        if (this.validateForm()) {
          let endpoint = `/api/auctions/${this.auction.id}/bid/`;
          let method = "POST";
          let data = { price: this.newPrice.value };
          await apiService(endpoint, method, data)
            .then(response => {
              if (response.detail) {
                this.error = response.detail;
              }
              this.newPrice.value = null;
            });
        }
      }
    }
  }
</script>

<style lang="css" scoped>
 .btn-primary {
   background-color: #4A4E69;
   border-color: #4A4E69;
 }

 .btn-primary:hover {
   background-color: #44475F;
   border-color: #44475F;
 }
</style>
