<template lang="html">
  <div class="container mt-3 mt-md-5 ">
    <!-- Bid form -->
    <div class="row justify-content-center">
      <div class="col-12 col-lg-6">
        <AuctionFormComponent @refresh-auctions="getAuctions"/>
      </div>
    </div>

    <div class="table-responsive mt-3">
      <table class="table table-hover caption-top">
        <caption>Scheduled auctions</caption>
        <thead>
          <tr>
            <th scope="col">Id</th>
            <th scope="col">Title</th>
            <th scope="col">Initial Price</th>
            <th scope="col">Opening date</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(auction, index) in auctions"
              :key="index">
              <th scope="row">{{ auction.id }}</th>
              <td><router-link :to="{ name: 'auction editor', params: { id: auction.id } }">{{ auction.title }}</router-link></td>
              <td v-if="auction.initial_price">€{{ auction.initial_price }}</td>
              <td v-else>Not set</td>
              <td v-if="auction.opened_at">{{ getOpeningDate(auction) }}</td>
              <td v-else>Not set</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Load more auction -->
    <div class="mb-5 mt-2 text-center" >
      <!-- Spinner -->
      <div v-show="loadingAuctions">
        <div class="spinner-border text-success"
             role="status"
             style="width: 3rem; height: 3rem;">
        </div>
      </div>

      <!-- Button -->
      <button class="btn btn-success"
              v-show="next"
              @click="getAuctions"
              >Show more
      </button>
    </div>
  </div>
</template>

<script>
  // @ is an alias to /src
  import { apiService } from "@/common/api.service.js";
  import AuctionFormComponent from "@/components/AuctionForm.vue";
  import moment from 'moment';

  export default {
    name: "ScheduleAuctions",
    components: {
      AuctionFormComponent
    },
    data() {
      return {
        auctions: [],
        next: null,
        loadingAuctions: false
      }
    },
    methods: {
      async getAuctions(refresh) {
        /*
          Retrieve active auctions according to pagination.
          If "refresh" is true re-initialize the auction list.
        */

        let endpoint = "/api/schedule-auctions/";
        if (this.next && refresh != true) {
          endpoint = this.next;
        }
        this.loadingAuctions = true;
        await apiService(endpoint)
          .then(response => {
            if (refresh === true) {
              this.auctions.splice(0, (this.auctions.length));
            }
            this.auctions.push(...response.results);
            this.loadingAuctions = false;
            if (response.next) {
              this.next = response.next;
            } else {
              this.next = null;
            }
          });
      },
      getOpeningDate(auction) {
        return moment(auction.opened_at).fromNow();
      }
    },
    created() {
      document.title = "Schedule auctions";
      this.getAuctions();
    }
  }
</script>

<style lang="css" scoped>
  a {
    text-decoration: none;
  }
</style>
