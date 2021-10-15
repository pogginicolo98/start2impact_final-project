<template lang="html">
  <div class="container mt-4 mt-md-5">
    <!-- New auction -->
    <div class="row justify-content-center">
      <div class="col-12 col-lg-6">
        <div class="card card-detail"
             style="width: 100%">
             <div class="card-header card-header-detail text-card-auction">
               <i class="fa-solid fa-calendar-plus fs-24px me-2"></i>
               <span class="fw-bold fs-18px">Create a new auction</span>
             </div>
             <div class="card-body card-body-detail">
               <AuctionFormComponent @refresh-auctions="getAuctions"/>
             </div>
        </div>
      </div>
    </div>

    <!-- Scheduled auctions -->
    <template v-if="auctions.length > 0">
      <div class="table-responsive text-nowrap mt-5">
        <table class="table table-hover caption-top text-card-auction">
          <caption>
            <i class="fa-solid fa-database fs-20px me-2"></i>
            <span>Scheduled auctions</span>
          </caption>
          <thead>
            <tr>
              <th scope="col"><i class="fa-solid fa-key me-2"></i>ID</th>
              <th scope="col">Title</th>
              <th scope="col">Initial Price</th>
              <th scope="col"><i class="fa-solid fa-calendar-days me-2"></i>Opening date</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(auction, index) in auctions"
                :key="index">
                <th scope="row">{{ auction.id }}</th>
                <td>
                  <router-link :to="{ name: 'auction editor', params: { id: auction.id } }">
                    <i class="fa-solid fa-pen-to-square me-1"></i>{{ auction.title }}
                  </router-link>
                </td>
                <td v-if="auction.initial_price">{{ auction.initial_price }} €</td>
                <td v-else>Not set</td>
                <td v-if="auction.opened_at">{{ getOpeningDate(auction) }}</td>
                <td v-else>Not set</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="row mt-4 mb-5">
        <div class="position-relative">
          <button class="position-absolute top-50 start-0 translate-middle-y btn btn-violet rounded-pill ms-5"
                  style="width: 40px; height: 40px;"
                  type="button"
                  :class="{'disabled': !hasPrevious}"
                  @click="getAuctions('previous')"
                  ><i class="fa-solid fa-angle-left"></i>
          </button>
          <p class="position-absolute top-50 start-50 translate-middle text-card-auction">
            <i class="fa-regular fa-file-lines me-2"></i>{{ currentPage }}/{{ pages }}
          </p>
          <button class="position-absolute top-50 end-0 translate-middle-y btn btn-violet rounded-pill me-5"
                  style="width: 40px; height: 40px;"
                  type="button"
                  :class="{'disabled': !hasNext}"
                  @click="getAuctions('next')"
                  ><i class="fa-solid fa-angle-right"></i>
          </button>
        </div>
      </div>
    </template>

    <!-- Archive empty -->
    <template v-else>
      <div class="text-center mt-5">
        <p class="fs-32px fw-blod text-muted">There are no auctions in the archive</p>
      </div>
    </template>
  </div> <!-- Container -->
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
        currentPage: 1,
        pages: 1,
        previous: null,
        next: null,
        loadingAuctions: false
      }
    },
    computed: {
      hasPrevious() {
        if (this.previous) {
          return true;
        }
        return false;
      },
      hasNext() {
        if (this.next) {
          return true;
        }
        return false;
      }
    },
    methods: {
      async getAuctions(action) {
        /*
          Retrieve active auctions according to pagination.
          If "refresh" is true re-initialize the auction list.
        */

        let endpoint = "/api/schedule-auctions/";
        if (action === "previous") {
          endpoint = this.previous;
          this.currentPage -= 1;
        } else if (action === "next") {
          endpoint = this.next;
          this.currentPage += 1;
        }
        this.loadingAuctions = true;
        await apiService(endpoint)
          .then(response => {
            this.auctions.splice(0, (this.auctions.length));
            this.auctions.push(...response.results);
            this.loadingAuctions = false;
            if (response.next) {
              this.next = response.next;
              this.pages = Math.ceil(response.count / response.results.length);
            } else {
              this.next = null;
            }
            if (response.previous) {
              this.previous = response.previous;
            } else {
              this.previous = null;
            }
          });
      },
      getOpeningDate(auction) {
        return moment(auction.opened_at).fromNow();
      }
    },
    created() {
      document.title = "Schedule auctions | ChainBid";
      this.getAuctions();
    }
  }
</script>

<style lang="css" scoped>
</style>
