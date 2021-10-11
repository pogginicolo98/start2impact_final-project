<template lang="html">
  <div class="container mt-3 mt-lg-5">
    <h2 class="mb-3">{{ modifiedAuction.title }}</h2>
    <div class="row">
      <!-- Edit image -->
      <div class="col-12 col-lg-5">
        <div class="card pb-1"
             style="width: 100%">
             <div class="card-header">
               <i class="bi bi-pencil-square fs-24px me-2"></i>
               <span class="fw-bold fs-18px">Edit image</span>
             </div>
             <div class="card-body card-body-custom">
               <img alt="product image"
                    class="img-fluid"
                    :src="getImage">
               <div class="col-12 mt-3 fs-18px">
                 <input accept="image/*"
                        class="form-control"
                        type="file"
                        :class="{'is-invalid': imageIsInvalid}"
                        @change="onImageSelected">
                 <div class="invalid-feedback">{{ image.error }}</div>
               </div>
               <div class="col-12 col-sm-1 col-md-1 col-lg-12 col-xl-1 col-xxl-1 d-grid d-block mt-2 fs-18px ms-auto">
                 <button class="btn btn-success"
                         type="submit"
                         @click="onUpload"
                         ><i class="bi bi-cloud-upload"></i>
                 </button>
               </div>
             </div>
        </div>
      </div>

      <!-- Edit data -->
      <div class="col-12 col-lg-7 mt-3 mt-lg-0">
        <div class="card pb-1"
             style="width: 100%">
             <div class="card-header">
               <i class="bi bi-pencil-square fs-24px me-2"></i>
               <span class="fw-bold fs-18px">Edit Data</span>
             </div>
             <div class="card-body card-body-custom">
               <AuctionFormComponent :auction="modifiedAuction"
                                     @refresh-auctions="updateData"/>
             </div>
        </div>
      </div>
    </div> <!-- Row -->
  </div> <!-- Container -->
</template>

<script>
  // @ is an alias to /src
  import { apiService } from "@/common/api.service.js";
  import AuctionFormComponent from "@/components/AuctionForm.vue";

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
    async beforeRouteEnter(to, from, next) {
      /*
        Retrieve a specific auction's data before entering in the page,
        in order to pass auction's data to the component and fill the fields
        before rendering the page.
      */

      let endpoint = `/api/schedule-auctions/${to.params.id}/`;
      await apiService(endpoint)
        .then(response => {
          to.params.auction = response;
        });
      return next();
    },
    data() {
      return {
        modifiedAuction: this.auction,
        image: {
          file: null,
          url: null,
          error: null
        },
        error: null
      }
    },
    computed: {
      getImage() {
        if (this.image.url) {
          return this.image.url;
        }
        return this.modifiedAuction.image;
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
          /*
            Update auction's data displayed.
          */

          let endpoint = `/api/schedule-auctions/${this.modifiedAuction.id}/`;
          await apiService(endpoint)
            .then(response => {
              this.modifiedAuction = response;
              document.title = `${response.title} | ChainBid`;
            });
        }
    },
    created() {
      document.title = `${this.modifiedAuction.title} | ChainBid`;
    },
  }
</script>

<style lang="css" scoped>
</style>
