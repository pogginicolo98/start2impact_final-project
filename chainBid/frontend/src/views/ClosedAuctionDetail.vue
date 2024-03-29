<template lang="html">
  <div class="closed-auction-detail">
    <!-- Error 404 -->
    <div class="not-found"
         v-if="notFound">
         <Error404Component :auctionNotAvailable="true"/>
    </div>

    <!-- Closed auction detail -->
    <div class="container mt-3 mt-lg-4"
         v-else>
         <div class="row">
           <!-- Title mobile formats -->
           <div class="col-12 d-lg-none">
             <p class="text-truncate fw-bold fs-32px mb-2 ms-2">{{ auction.title }}</p>
           </div>

           <!-- Image and description -->
           <div class="col-12 col-lg-5 mt-3">
             <!-- Image -->
             <div class="col-12">
               <figure class="figure">
                <img alt="product image"
                     class="figure-img img-fluid rounded img-thumbnail-detail"
                     :src="auction.image">
               </figure>
             </div>

             <!-- Description desktop formats -->
             <div class="col-12 d-none d-lg-block">
               <div class="card card-detail"
                    style="width: 100%">
                    <div class="card-header card-header-detail">
                      <i class="fa-solid fa-align-left me-2"></i><span class="fs-18px fw-bold">Description</span>
                    </div>
                    <div class="card-body card-body-detail">
                      <p class="text-muted my-2"
                         v-if="!auction.description"
                         >No description provided
                      </p>
                      <p class="my-2"
                         v-else
                         >{{ auction.description }}
                      </p>
                    </div>
               </div>
             </div>
           </div>

           <!-- Info -->
           <div class="col-12 col-lg-7 mb-2">
             <!-- Title desktop formats -->
             <p class="text-truncate fs-32px fw-bold d-none d-lg-block mb-3 ms-2">{{ auction.title }}</p>

             <!-- Card -->
             <div class="card card-detail">
               <div class="card-body card-body-detail">
                 <!-- Winner -->
                 <p class="fs-20px"
                    v-if="auction.winner"
                    ><span class="fw-bold">Winner: </span>
                    <router-link :to="{ name: 'profile', params: { slug: auction.winner_slug } }">@{{ auction.winner }}</router-link>
                 </p>
                 <p class="text-danger fw-bold fs-20px"
                    v-else
                    >Auction canceled
                 </p>

                 <!-- Table stats -->
                 <div class="table-responsive text-nowrap">
                   <table class="table text-card-auction">
                     <thead>
                       <tr>
                         <th class="text-nowrap"
                             scope="col"
                             >Initial price
                         </th>
                         <th class="text-nowrap"
                             scope="col"
                             v-if="auction.final_price"
                             >Final price
                         </th>
                         <th class="text-nowrap"
                             scope="col"
                             >Opened at
                         </th>
                         <th class="text-nowrap"
                             scope="col"
                             >Closed at
                         </th>
                       </tr>
                     </thead>
                     <tbody>
                       <tr>
                         <td>{{ auction.initial_price }} €</td>
                         <td v-if="auction.final_price">{{ auction.final_price }} €</td>
                         <td>{{ getDate(auction.opened_at) }}</td>
                         <td>{{ getDate(auction.closed_at) }}</td>
                       </tr>
                     </tbody>
                   </table>
                 </div>

                 <div class="mt-2"
                      v-if="auction.tx_id">
                      <!-- Hash -->
                      <p class="fw-bold mb-1">SHA256:</p>
                      <div class="container box-icon rounded pe-1">
                        <div class="row">
                          <div class="col-9 col-sm-10 col-xxl-11">
                            <p class="mt-3"
                               id="text-hash"
                               >{{ auction.hash }}
                            </p>
                          </div>
                          <div class="col-3 col-sm-2 col-xxl-1 text-end ps-0">
                            <button class="btn btn-icon my-1"
                                    style="width: 46px; height: 38px;"
                                    v-html="copyToClipboardMessage"
                                    @click="copyToClipboard(auction.hash)">
                            </button>
                          </div>
                        </div>
                      </div>

                      <!-- Transaction ID -->
                      <p class="fw-bold mb-1 mt-2">Transaction ID:</p>
                      <div class="container box-icon rounded pe-1">
                        <div class="row">
                          <div class="col-9 col-sm-10 col-xxl-11">
                            <p class="mt-3"
                               id="text-hash"
                               >{{ auction.tx_id }}
                            </p>
                          </div>
                          <div class="col-3 col-sm-2 col-xxl-1 text-end ps-0">
                            <a class="btn btn-icon my-1"
                               style="width: 46px; height: 38px;"
                               :href="txIdLink"
                               ><i class="fa-solid fa-link"></i>
                            </a>
                          </div>
                        </div>
                      </div>
                 </div>

                 <div class="text-danger mt-2"
                      v-else>
                      <p class="mb-0">Something went wrong and the auction results were not recorded on the blockchain.</p>
                      <p>Please contact the support for more information.</p>
                 </div>

                 <!-- Download -->
                 <div class="d-grid d-sm-block text-end mt-3">
                   <a class="btn btn-violet rounded-pill"
                      download
                      v-if="auction.json_file"
                      :href="auction.json_file"
                      ><i class="fa-solid fa-file-arrow-down me-2"></i>Download
                   </a>
                 </div>
               </div>
             </div> <!-- Card -->
           </div> <!-- Info -->
         </div> <!-- Row 1 -->

         <!-- Description mobile formats -->
         <div class="row d-lg-none">
           <div class="col-12 col-lg-5">
             <div class="card card-detail mt-3"
                  style="width: 100%">
                  <div class="card-header card-header-detail">
                    <i class="fa-solid fa-align-left me-2"></i><span class="fs-18px fw-bold">Description</span>
                  </div>
                  <div class="card-body card-body-detail">
                    <p class="text-muted my-2"
                       v-if="!auction.description"
                       >No description provided
                    </p>
                    <p class="my-2"
                       v-else
                       >{{ auction.description }}
                    </p>
                  </div>
             </div>
           </div>
         </div> <!-- Row 2 -->
    </div> <!-- Container -->
  </div>
</template>

<script>
  // @ is an alias to /src
  import { apiService } from "@/common/api.service.js";
  import Error404Component from "@/components/Error404.vue";
  import moment from 'moment';

  export default {
    name: "Auction",
    components: {
      Error404Component
    },
    props: {
      slug: {
        type: String,
        required: true
      }
    },
    data() {
      return {
        auction: {},
        copyToClipboardMessage: "<i class='fa-solid fa-clone'></i>",
        txIdLink: null,
        notFound: false
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

        let endpoint = `/api/closed-auctions/${this.slug}/`;
        await apiService(endpoint)
          .then(response => {
            if (response.detail) {
              console.log(response.detail);
              this.notFound = true;
            } else {
              this.auction = response;
              this.txIdLink = `https://ropsten.etherscan.io/tx/${response.tx_id}`;
              document.title = `${response.title} | Closed auctions | ChainBid`;
            }
          })
          .catch(error => {
            console.log(error);
            this.notFound = true;
          });
      },
      getDate(date) {
        return moment.utc(date, 'YYYY/MM/DD - HH:mm:ss').format('YYYY/MM/DD - HH:mm:ss');
      },
      copyToClipboard(text) {
        /*
          Change copy to clipboard button's icon.
        */

        this.$clipboard(text);
        if (this.copyToClipboardMessage === "<i class='fa-solid fa-clone'></i>") {
          this.copyToClipboardMessage = "<i class='fa-solid fa-clipboard-check'></i>";
          setTimeout(() => {
            this.copyToClipboardMessage = "<i class='fa-solid fa-clone'></i>";
          }, 5000);
        }
      }
    },
    created() {
      this.getAuctionData();
    }
  }
</script>

<style lang="css" scoped>
</style>
