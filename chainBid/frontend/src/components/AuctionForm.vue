<template lang="html">
  <div class="card">
    <div class="card-body">
      <h2 class="text-center mb-4">Schedule a new auction</h2>
      <form novalidate
            @submit.prevent="onSubmit">
            <!-- Title form -->
            <div class="mb-3 row">
              <label class="col-xxl-3 col-form-label"
                     for="title"
                     >Title
              </label>
              <div class="col-xxl-9">
                <input class="form-control"
                       id="title"
                       required
                       type="text"
                       v-model="title"
                       :class="{'is-invalid': titleValidation.isInvalid}">
                <div class="invalid-feedback">
                  <ul>
                    <li v-for="(error, index) in titleValidation.errors"
                        :key="index"
                        >{{ error }}
                    </li>
                  </ul>
                </div>
              </div>
            </div>

            <!-- Description form -->
            <div class="mb-0 mb-xxl-2 row">
              <label class="col-xxl-3 col-form-label"
                     for="description"
                     >Description
              </label>
              <div class="col-xxl-9">
                <textarea class="form-control"
                          id="description"
                          rows="3"
                          type="text"
                          v-model="description"
                          :class="{'is-invalid': descriptionValidation.isInvalid}">
                </textarea>
                <p class="text-muted mt-1 text-end small mb-0 mb-xxl-2">{{ countDescriptionChars }}/240</p>
                <div class="invalid-feedback">
                  <ul>
                    <li v-for="(error, index) in descriptionValidation.errors"
                        :key="index"
                        >{{ error }}
                    </li>
                  </ul>
                </div>
              </div>
            </div>

            <!-- Initial price form -->
            <div class="mb-3 row">
              <label class="col-xxl-3 col-form-label"
                     for="initial-price"
                     >Initial price
              </label>
              <div class="col-xxl-9">
                <div class="input-group has-validation">
                  <span class="input-group-text"
                        id="euro-symbol"
                        >€
                  </span>
                  <input aria-describedby="euro-symbol"
                         class="form-control"
                         id="initial-price"
                         step="0.01"
                         type="number"
                         v-model="initialPrice"
                         :class="{'is-invalid': initialPriceValidation.isInvalid}">
                  <div class="invalid-feedback">
                    <ul>
                      <li v-for="(error, index) in initialPriceValidation.errors"
                          :key="index"
                          >{{ error }}
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            <!-- Opening date form -->
            <div class="mb-3 row">
              <label class="col-xxl-3 col-form-label"
                     for="opening-date"
                     >Opening date
              </label>
              <div class="col-xxl-9">
                <input class="form-control"
                       id="opening-date"
                       type="datetime-local"
                       v-model="openedAt">
              </div>
            </div>

            <!-- Button -->
            <div class="col-sm-2 mt-2 ms-auto d-grid d-block">
              <button class="btn btn-success"
                      type="submit"
                      >Create
              </button>
            </div>
      </form>
      <p class="text-danger mt-2">{{ error }}</p>
    </div> <!-- Card body -->
  </div> <!-- Card -->
</template>

<script>
  // @ is an alias to /src
  import { apiService } from "@/common/api.service.js";
  import { countDecimalPlaces } from "@/common/utility.js";

  export default {
    name: "AuctionFormComponent",
    data() {
      return {
        title: null,
        description: null,
        initialPrice: null,
        openedAt: null,
        titleValidation: {
          isInvalid: false,
          errors: []
        },
        descriptionValidation: {
          isInvalid: false,
          errors: []
        },
        initialPriceValidation: {
          isInvalid: false,
          errors: []
        },
        error: null
      };
    },
    computed: {
      countDescriptionChars() {
        if (this.description) {
          return this.description.length;
        }
        return 0;
      }
    },
    methods: {
      validateForm() {
        /*
          Validation schedule auction form fields.

          :fields
          - title:
              1) The field cannot be empty.
              2) 50 characters maximum.
          - description:
              1) 240 characters maximum.
          -initialPrice:
              1) 9999999999.99 maximum value.
              2) 2 decimals maximum.
              3) Only positive numbers.
        */

        // Title validation
        this.titleValidation.isInvalid = false;
        this.titleValidation.errors = [];
        if (!this.title) {
          this.titleValidation.errors.push("Please enter a title.");
          this.titleValidation.isInvalid = true;
        } else if (this.title.length > 50) {
          this.titleValidation.errors.push("Maximum number of characters exceeded.");
          this.titleValidation.isInvalid = true;
        }
        // Description validation
        this.descriptionValidation.isInvalid = false;
        this.descriptionValidation.errors = [];
        if (this.description) {
          if (this.description.length > 240) {
            this.descriptionValidation.errors.push("Maximum number of characters exceeded.");
            this.descriptionValidation.isInvalid = true;
          }
        }
        // InitialPrice validation
        this.initialPriceValidation.isInvalid = false;
        this.initialPriceValidation.errors = [];
        if (this.initialPrice != null) {
          let decimals = countDecimalPlaces(this.initialPrice)
          if (this.initialPrice > 9999999999.99) {
            this.initialPriceValidation.errors.push("Maximum allowed price: €9999999999.99");
            this.initialPriceValidation.isInvalid = true;
          }
          if (decimals > 2) {
            this.initialPriceValidation.errors.push("Please enter a price with no more than 2 decimals.");
            this.initialPriceValidation.isInvalid = true;
          }
          if (this.initialPrice < 0) {
            this.initialPriceValidation.errors.push("Please enter a positive price.");
            this.initialPriceValidation.isInvalid = true;
          } else if (this.initialPrice == 0) {
            this.initialPrice = null;
          }
        }
        // Results
        if (this.titleValidation.isInvalid || this.descriptionValidation.isInvalid || this.initialPriceValidation.isInvalid) {
          return false;
        }
        return true;
      },
      async onSubmit() {
        /*
          Create new auction.
        */

        if (this.validateForm()) {
          let endpoint = `/api/schedule-auctions/`;
          let method = "POST";
          let data = {
            title: this.title,
            description: this.description,
            initial_price: this.initialPrice,
            opened_at: this.openedAt
          };
          await apiService(endpoint, method, data)
            .then(response => {
              if (response.detail) {
                this.error = response.detail;
              }
              this.title = null;
              this.description = null;
              this.initialPrice = null;
              this.openedAt = null;
              this.$emit("refresh-auctions", true);
            });
        }
      }
    }
  }
</script>

<style lang="css" scoped>
</style>
