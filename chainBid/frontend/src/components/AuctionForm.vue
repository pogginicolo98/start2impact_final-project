<template lang="html">
  <div class="card">
    <div class="card-body">
      <h2 class="text-center mb-4">Schedule a new auction</h2>
      <form novalidate
            @submit.prevent="onSubmit">
            <!-- Input -->
            <div class="mb-3 row">
              <label for="title" class="col-xxl-3 col-form-label">Title</label>
              <div class="col-xxl-9">
                <input type="text" class="form-control" id="title" v-model="title">
              </div>
            </div>
            <div class="mb-3 row">
              <label for="description" class="col-xxl-3 col-form-label">Description</label>
              <div class="col-xxl-9">
                <textarea type="text" class="form-control" id="description" rows="3" v-model="description"></textarea>
              </div>
            </div>
            <div class="mb-3 row">
              <label for="initial-price" class="col-xxl-3 col-form-label">Initial price</label>
              <div class="col-xxl-9">
                <div class="input-group">
                  <span class="input-group-text" id="euro-symbol">€</span>
                  <input type="number" class="form-control" id="initial-price" step="0.01" aria-describedby="euro-symbol" v-model="initialPrice">
                </div>
              </div>
            </div>
            <div class="mb-3 row">
              <label for="opening-date" class="col-xxl-3 col-form-label">Opening date</label>
              <div class="col-xxl-9">
                <input type="datetime-local" class="form-control" id="opening-date" v-model="openedAt">
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
    </div>
  </div>
</template>

<script>
  // @ is an alias to /src
  import { apiService } from "@/common/api.service.js";

  export default {
    name: "AuctionFormComponent",
    data() {
      return {
        title: null,
        description: null,
        initialPrice: null,
        openedAt: null,
        error: null
      };
    },
    methods: {
      async onSubmit() {
        /*
          Create new auction.
        */

        if (this.error) {
          this.error = null;
        } else {
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
              } else if (response) {
                this.error = response;
              }
            });
        }
      }
    }
  }
</script>

<style lang="css" scoped>
</style>
