<template lang="html">
  <div class="container mt-4 mt-lg-5">
    <div class="row">
      <!-- Title mobile formats -->
      <div class="col-12 d-lg-none">
        <p class="text-card-auction fw-bold fs-32px mb-2 ms-2">{{ auction.title }}</p>
      </div>

      <!-- Image -->
      <div class="col-12 col-lg-5 mt-0 mt-lg-3">
        <div class="col-12">
          <figure class="figure">
           <img alt="product image"
                class="figure-img img-fluid rounded img-thumbnail-detail"
                :src="auction.image">
          </figure>
        </div>
        <div class="col-12 d-none d-lg-block">
          <div class="card card-detail"
               style="width: 100%">
               <div class="card-header card-header-detail text-card-auction">
                 <i class="fa-solid fa-align-left me-2"></i><span class="fs-18px fw-bold">Description</span>
               </div>
               <div class="card-body card-body-detail">
                 <p class="my-2">{{ auction.description }}</p>
               </div>
          </div>
        </div>
      </div>

      <!-- Info -->
      <div class="col-12 col-lg-7 mb-2">
        <!-- Title desktop formats -->
        <p class="text-card-auction fs-32px fw-bold d-none d-lg-block mb-3 ms-2">{{ auction.title }}</p>
        <!-- Card -->
        <div class="card card-detail">
          <div class="card-body card-body-detail">
            <p class="text-card-auction fs-20px"><span class="fw-bold me-2">Winner:</span>@{{ auction.winner }}</p>

            <div class="table-responsive text-nowrap">
              <table class="table text-card-auction">
                <thead>
                  <tr>
                    <th class="text-nowrap" scope="col">Initial price</th>
                    <th class="text-nowrap" scope="col">Final price</th>
                    <th class="text-nowrap" scope="col">Opened at</th>
                    <th class="text-nowrap" scope="col">Closed at</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>{{ auction.initial_price }} €</td>
                    <td>{{ auction.final_price }} €</td>
                    <td>{{ getDate(auction.opened_at) }}</td>
                    <td>{{ getDate(auction.closed_at) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <p class="text-card-auction fw-bold mb-1 mt-2">SHA256:</p>
            <div class="container hash rounded text-card-auction pe-1">
              <div class="row">
                <div class="col-9 col-sm-10">
                  <p class="mt-3" id="text-hash">{{ auction.hash }}</p>
                </div>
                <div class="col-3 col-sm-2 text-end">
                  <button class="btn btn-violet my-1" @click="copyToClipboard(auction.hash)"><i class="fa-solid fa-clone"></i></button>
                </div>
              </div>
            </div>

            <p class="text-card-auction fw-bold mb-1 mt-2">Transaction ID:</p>
            <div class="container hash rounded text-card-auction pe-1">
              <div class="row">
                <div class="col-9 col-sm-10">
                  <p class="mt-3" id="text-hash">{{ auction.tx_id }}</p>
                </div>
                <div class="col-3 col-sm-2 text-end">
                  <a class="btn btn-violet my-1"
                     :href="txIdLink"
                     ><i class="fa-solid fa-link"></i>
                  </a>
                </div>
              </div>
            </div>

            <div class="text-end mt-3">
              <a class="btn btn-violet rounded-pill"
                 download
                 :href="auction.json_file"
                 >Download<i class="fa-solid fa-file-arrow-down ms-2"></i>
              </a>
            </div>
          </div>
        </div>
      </div> <!-- New bid -->
    </div> <!-- Row 1 -->

    <!-- Description -->
    <div class="row d-lg-none">
      <div class="col-12 col-lg-5">
        <div class="card card-detail mt-3"
             style="width: 100%">
             <div class="card-header card-header-detail text-card-auction">
               <i class="fa-solid fa-align-left me-2"></i><span class="fs-18px fw-bold">Description</span>
             </div>
             <div class="card-body card-body-detail">
               <p class="my-2">{{ auction.description }}</p>
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
        txIdLink: null
      };
    },
    computed: {
      getOpenedAt() {
        return moment(this.auction.opened_at).fromNow();
      }
    },
    methods: {
      async getAuctionData() {
        /*
          Retrieve a specific auction's data and set page title.
        */

        let endpoint = `/api/closed-auctions/${this.id}/`;
        await apiService(endpoint)
          .then(response => {
            this.auction = response;
            this.txIdLink = `https://ropsten.etherscan.io/tx/${response.tx_id}`;
            document.title = `${response.title} | ChainBid`;
          });
      },
      getDate(date) {
        return moment.utc(date, 'YYYY/MM/DD, HH:mm:ss').format('YYYY/MM/DD, HH:mm:ss');
      },
      copyToClipboard(text) {
        this.$clipboard(text)
      }
    },
    created() {
      this.getAuctionData();
    }
  }
</script>

<style lang="css" scoped>
  .hash {
    border: 1px solid;
    border-color: #C9ADA7;
    background-color: #F2E9E4;
  }
</style>
