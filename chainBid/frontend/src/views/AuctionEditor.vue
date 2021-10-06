<template lang="html">
  <div class="container mt-3 mt-lg-5">
    <h1>{{ error }}</h1>
    <div class="row">
      <div class="col-12 col-lg-5">
        <div class="card">
          <img alt="product image"
               class="card-img-top"
               :src="auction.image">
          <div class="card-body">
            <div class="row">
              <!-- <form novalidate @submit.prevent="onSubmit"> -->
                <div class="col-9">
                  <input type="file" accept="image/*" class="form-control" @change="onImageSelected" id="file-input">
                  <!-- <input class="form-control" type="file" id="formFile" v-model="image"> -->
                </div>
                <div class="col-3">
                  <button class="btn btn-success"
                          @click="onUpload"
                          type="submit"
                          >Upload
                  </button>
                </div>
              <!-- </form> -->
            </div>
         </div>
        </div>
      </div>

      <div class="col-12 col-lg-7 mt-3 mt-lg-0">
        <AuctionFormComponent/>
      </div>
    </div>
  </div> <!-- Container -->
</template>

<script>
  // @ is an alias to /src
  import { apiService, apiServicev2 } from "@/common/api.service.js";
  import AuctionFormComponent from "@/components/AuctionForm.vue";
  import moment from 'moment';

  export default {
    name: "AuctionEditor",
    components: {
      AuctionFormComponent
    },
    props: {
      id: {
        type: Number,
        required: true
      }
    },
    data() {
      return {
        auction: {},
        image: null,
        error: null
      }
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

        let endpoint = `/api/schedule-auctions/${this.id}/`;
        await apiService(endpoint)
          .then(response => {
            this.auction = response;
            document.title = response.title;
          });
      },
      onImageSelected(event) {
        this.image = event.target.files[0];
      },
      async onUpload() {
        let endpoint = `/api/schedule-auctions/${this.id}/upload-image/`;
        let method = "PUT";
        let data = new FormData();
        data.append('image', this.image);
        // let contentType = "multipart/form-data; boundary=image";
        await apiServicev2(endpoint, method, data)
          .then(response => {
            this.error = response;
          });
      }
    },
    created() {
      this.getAuctionData();
    },
  }
</script>

<style lang="css" scoped>
  .auction-image {
    /*
      Fixed width and height, image not stretched and centered.
    */
    width: 100%;
    height: 10rem;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
  }
</style>
