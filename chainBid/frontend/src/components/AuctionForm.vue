<template lang="html">
  <div class="auction-form">
    <form novalidate
          @submit.prevent="onSubmit">
          <!-- Title -->
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
                     v-model="title.value"
                     :class="{'is-invalid': isTitleInvalid}">
              <div class="invalid-feedback">
                <ul>
                  <li v-for="(error, index) in title.errors"
                      :key="index"
                      >{{ error }}
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Description -->
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
                        v-model="description.value"
                        :class="{'is-invalid': isDescriptionInvalid}">
              </textarea>
              <p class="mt-1 text-end small mb-0 mb-xxl-2"
                 :class="{'text-muted': descriptionCharsValid,
                          'text-danger': !descriptionCharsValid}"
                 >{{ countDescriptionChars }}/240
              </p>
              <div class="invalid-feedback">
                <ul>
                  <li v-for="(error, index) in description.errors"
                      :key="index"
                      >{{ error }}
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Initial price -->
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
                       v-model="initialPrice.value"
                       :class="{'is-invalid': isInitialPriceInvalid}">
                <div class="invalid-feedback">
                  <ul>
                    <li v-for="(error, index) in initialPrice.errors"
                        :key="index"
                        >{{ error }}
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <!-- Opening date -->
          <div class="mb-3 row">
            <label class="col-xxl-3 col-form-label"
                   for="opening-date"
                   >Opening date
            </label>
            <div class="col-xxl-9">
              <input class="form-control"
                     id="opening-date"
                     type="datetime-local"
                     v-model="openedAt.value">
            </div>
          </div>

          <!-- Submit button -->
          <div class="col-sm-2 mt-2 ms-auto d-grid d-block">
            <button class="btn btn-success"
                    type="submit"
                    v-if="isNewAuction"
                    >Create
            </button>
            <button class="btn btn-success"
                    type="submit"
                    v-else
                    >Update
            </button>
          </div>
    </form>
  </div>
</template>

<script>
  // @ is an alias to /src
  import { apiService } from "@/common/api.service.js";
  import { countDecimalPlaces } from "@/common/utility.js";
  import moment from "moment";

  export default {
    name: "AuctionFormComponent",
    props: {
      auction: {
        type: Object,
        required: false
      }
    },
    data() {
      return {
        title: {
          value: null,
          errors: []
        },
        description: {
          value: null,
          errors: []
        },
        initialPrice: {
          value: null,
          errors: []
        },
        openedAt: {
          value: null
        },
        error: null
      };
    },
    computed: {
      isNewAuction() {
        if (this.auction) {
          return false;
        }
        return true;
      },
      countDescriptionChars() {
        if (this.description.value) {
          return this.description.value.length;
        }
        return 0;
      },
      descriptionCharsValid() {
        if (this.description.value) {
          return this.description.value.length <= 240;
        }
        return true;
      },
      isTitleInvalid() {
        return this.title.errors.length != 0;
      },
      isDescriptionInvalid() {
        return this.description.errors.length != 0;
      },
      isInitialPriceInvalid() {
        return this.initialPrice.errors.length != 0;
      }
    },
    methods: {
      initializeForm() {
        if (this.auction) {
          this.title.value = this.auction.title;
          this.description.value = this.auction.description;
          this.initialPrice.value = this.auction.initial_price;
          this.openedAt.value = moment.utc(this.auction.opened_at, 'YYYY-MM-DDTHH:mm').format('YYYY-MM-DDTHH:mm');
        }
      },
      validateForm() {
        /*
          Validation schedule auction form fields.

          :fields
          - title:
              1) The field cannot be empty.
              2) 50 characters maximum.
          - description:
              1) 240 characters maximum.
          -initial_price:
              1) 999999999.99 maximum value.
              2) 2 decimals maximum.
              3) Only positive numbers.
        */

        let formIsValid = true;
        let maxCharTitle = 50;
        let maxCharDescription = 240;
        // Title validation
        this.title.errors = [];
        if (!this.title.value) {
          this.title.errors.push("Please enter a title.");
          formIsValid = false;
        } else if (this.title.value.length > maxCharTitle) {
          this.title.errors.push(`Maximum number of characters exceeded (${this.title.value.length}/${maxCharTitle}).`);
          formIsValid = false;
        }
        // Description validation
        this.description.errors = [];
        if (this.description.value) {
          if (this.description.value.length > maxCharDescription) {
            this.description.errors.push("Maximum number of characters exceeded.");
            formIsValid = false;
          }
        }
        // Initial_price validation
        this.initialPrice.errors = [];
        if (this.initialPrice.value != null) {
          let decimals = countDecimalPlaces(this.initialPrice.value)
          if (this.initialPrice.value > 999999999.99) {
            this.initialPrice.errors.push("Maximum allowed price: €9999999999.99");
            formIsValid = false;
          }
          if (decimals > 2) {
            this.initialPrice.errors.push("Please enter a price with no more than 2 decimals.");
            formIsValid = false;
          }
          if (this.initialPrice.value < 0) {
            this.initialPrice.errors.push("Please enter a positive price.");
            formIsValid = false;
          } else if (this.initialPrice.value == 0) {
            this.initialPrice.value = null;
          }
        }
        return formIsValid;
      },
      async onSubmit() {
        /*
          Create new auction.
        */

        if (this.validateForm()) {
          let endpoint = "/api/schedule-auctions/";
          let method = "POST";
          if (this.auction) {
            endpoint += this.auction.id + "/";
            method = "PUT";
          }
          let data = {
            title: this.title.value,
            description: this.description.value,
            initial_price: this.initialPrice.value,
            opened_at: this.openedAt.value
          };
          await apiService(endpoint, method, data)
            .then(response => {
              let param = null;
              if (response.detail) {
                // Da gestire per la pagina "not found"
                this.error = response.detail;
              }
              if (!this.auction) {
                param = true;
                this.title.value = null;
                this.description.value = null;
                this.initialPrice.value = null;
                this.openedAt.value = null;
              }
              this.$emit("refresh-auctions", param);
            });
        }
      }
    },
    created() {
      this.initializeForm();
    }
  }
</script>

<style lang="css" scoped>
</style>
