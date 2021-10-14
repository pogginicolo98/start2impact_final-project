<template lang="html">
  <div>
    <form novalidate
          @submit.prevent="onSubmit">
          <div class="row">
            <!-- Input -->
            <div class="col-12 col-sm-5 col-md-4 col-lg-5 col-xl-4 col-xxl-4 pe-sm-0">
              <label class="position-relative d-block">
                <i class="fa-solid fa-euro-sign position-absolute top-50 start-0 translate-middle text-muted ms-3"></i>
                <input aria-describedby="bidFormFeedback"
                       class="form-control rounded-pill"
                       placeholder="Price"
                       step="0.01"
                       style="padding-left: 27px;"
                       type="number"
                       v-model="newPrice.value"
                       :class="{'is-invalid': isInitialPriceInvalid}"
                       :disabled="isLastUser">
              </label>
              <div class="invalid-feedback d-block"
                   id="bidFormFeedback">
                   <ul>
                     <li v-for="(error, index) in newPrice.errors"
                         :key="index"
                         >{{ error }}
                     </li>
                  </ul>
              </div>
            </div>

            <!-- Button -->
            <div class="col-12 col-sm-3 col-md-2 col-lg-3 col-xl-2 d-grid d-block">
              <button class="btn rounded-pill"
                      style="height: 38px;"
                      type="submit"
                      :class="{'btn-danger': isLastUser,
                               'btn-violet': !isLastUser}"
                      :disabled="isLastUser"
                      >Bid<i class="fa-solid fa-hand ms-2"></i>
              </button>
            </div>
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
            this.newPrice.errors.push("Maximum allowed: €9999999999.99");
            formIsValid = false;
          }
          if (decimals > 2) {
            this.newPrice.errors.push("Please enter no more than 2 decimals.");
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
</style>
