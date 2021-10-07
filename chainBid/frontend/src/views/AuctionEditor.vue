<template lang="html">
  <div class="container mt-3 mt-lg-5">
    <!-- Image -->
    <h2 class="mb-3">{{ auction.title }}</h2>
    <div class="row">
      <div class="col-12 col-lg-5">
        <div class="card" style="width: 100%">
          <div class="card-header">
            <i class="bi bi-pencil-square fs-24px"></i><span class="fw-bold fs-18px"> Edit image</span>
          </div>
          <div class="card-body">
            <img alt="product image"
                 class="img-fluid"
                 :src="getImage">
            <div class="row mt-2 fs-18px">
              <div class="col-12 col-sm-10 col-md-10 col-lg-12 col-xl-10 col-xxl-10 pe-xl-0 mt-1">
                <input accept="image/*"
                       class="form-control"
                       type="file"
                       @change="onImageSelected"
                       :class="{'is-invalid': imageIsInvalid}">
              </div>
              <div class="col-12 col-sm-1 col-md-1 col-lg-12 col-xl-1 col-xxl-1 d-grid d-block mt-1">
                <button class="btn btn-success"
                        @click="onUpload"
                        type="submit"
                        ><i class="bi bi-cloud-upload"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-12 col-lg-7 mt-3 mt-lg-0">
        <div class="card" style="width: 100%">
          <div class="card-header">
            <i class="bi bi-pencil-square fs-24px"></i><span class="fw-bold fs-18px"> Edit Data</span>
          </div>
          <div class="card-body">
            <AuctionFormComponent :auction="auction"
                                  @refresh-auctions="updateData"/>
          </div>
        </div>
      </div>
    </div>
  </div> <!-- Container -->
</template>

<script>
  // @ is an alias to /src
  import { apiService } from "@/common/api.service.js";
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
      },
      auction: {
        type: Object,
        required: false
      }
    },
    data() {
      return {
        image: {
          file: null,
          url: null,
          error: null
        },
        error: null
      }
    },
    async beforeRouteEnter(to, from, next) {
      /*
        Retrieve a specific auction's data and set page title.
      */

      let endpoint = `/api/schedule-auctions/${to.params.id}/`;
      await apiService(endpoint)
        .then(response => {
          to.params.auction = response;
        });
      return next();
    },
    computed: {
      getOpenedAt() {
        return moment(this.auction.opened_at).fromNow();
      },
      getImage() {
        if (this.image.url) {
          return this.image.url;
        }
        return this.auction.image;
      },
      imageIsInvalid(){
        return this.image.error != null;
      }
    },
    methods: {
      onImageSelected(event) {
        this.image.file = event.target.files[0];
      },
      validateForm() {
        /*
          Validation of auction image field.

          :fields
          - image:
              1) Allowed formats: "jpeg", "jpg", "png".
        */

        let allowedExtension = ["jpeg", "jpg", "png"];
        let fileExtension = this.image.file.name.split(".").pop().toLowerCase();
        for(let index in allowedExtension) {
          if(fileExtension === allowedExtension[index]) {
            return true;
          }
        }
        this.image.error = "Allowed formats: *." + allowedExtension.join(", *.");
        return false;
      },
      async onUpload() {
        /*
          Update auction image.
        */

        if (this.validateForm()){
          let endpoint = `/api/schedule-auctions/${this.id}/upload-image/`;
          let method = "PUT";
          let data = new FormData();
          data.append('image', this.image.file);
          let imageData = true;
          await apiService(endpoint, method, data, imageData)
            .then(response => {
              if (response.detail) {
                // Da gestire per la pagina "not found"
                this.error = response.detail;
              }
              this.image.url = URL.createObjectURL(this.image.file);
              this.image.file = null;
              if (this.image.error) {
                this.image.error = null;
              }
            });
          }
        },
        async updateData() {
          let endpoint = `/api/schedule-auctions/${this.auction.id}/`;
          await apiService(endpoint)
            .then(response => {
              this.auction = response;
              document.title = response.title;
            });
        }
    },
    created() {
      document.title = this.auction.title;
    },
  }
</script>

<style lang="css" scoped>
  .fs-18px {
    font-size: 18px;
  }

  .fs-15px {
    font-size: 15px;
  }

  .fs-14px {
    font-size: 14px;
  }

  .fs-20px {
    font-size: 20px;
  }

  .fs-24px {
    font-size: 24px;
  }

  .card-header {
    background-color: white;
  }

  .card-body {
    background-color: rgba(0,0,0,.03);
  }
</style>
