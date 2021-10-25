<template lang="html">
  <div class="schedule-auction-detail">
    <!-- Error 404 -->
    <div class="not-found"
         v-if="notFound">
         <Error404Component :auctionNotAvailable="true"/>
    </div>

    <!-- Schedule auction detail -->
    <div class="container mt-3"
         v-else>
         <!-- Title -->
         <div class="text-center text-card-auction fw-bold fs-32px">
           <p>{{ modifiedAuction.title }}</p>
         </div>

         <div class="row mt-4">
           <!-- Edit image -->
           <div class="col-12 col-lg-5">
             <div class="card card-detail"
                  style="width: 100%">
                  <div class="card-header card-header-detail text-card-auction">
                    <div class="row justify-content-between">
                      <div class="col-auto">
                        <span class="fw-bold fs-18px">Image</span>
                      </div>
                      <div class="col-auto">
                        <button class="btn btn-icon p-0"
                                style="width: 27px; height: 27px;"
                                @click="toggleEditImage"
                                ><i class="fa-solid fa-pen"></i>
                        </button>
                      </div>
                    </div>
                  </div>
                  <div class="card-body card-body-detail">
                    <img alt="product image"
                         class="img-fluid"
                         :src="getImage">
                    <div class="col-12 mt-3 fs-18px">
                      <input accept="image/*"
                             class="form-control"
                             type="file"
                             :class="{'is-invalid': isImageInvalid}"
                             :disabled="!editImage"
                             @change="onImageSelected">
                      <div class="invalid-feedback">{{ image.error }}</div>
                    </div>
                    <div class="col-12 col-sm-3 col-md-2 col-lg-4 col-xl-3 d-grid d-block mt-3 ms-auto">
                      <button class="btn btn-violet rounded-pill"
                              type="submit"
                              :class="{'disabled': !editImage}"
                              @click="onUpload"
                              >Upload<i class="fa-solid fa-upload ms-2"></i>
                      </button>
                    </div>
                  </div>
             </div>
           </div>

           <!-- Edit data -->
           <div class="col-12 col-lg-7 mt-4 mt-lg-0">
             <div class="card card-detail"
                  style="width: 100%">
                  <div class="card-header card-header-detail text-card-auction">
                    <div class="row justify-content-between">
                      <div class="col-auto">
                        <span class="fw-bold fs-18px">Data</span>
                      </div>
                      <div class="col-auto">
                        <button class="btn btn-icon p-0 me-2"
                                style="width: 27px; height: 27px;"
                                data-bs-toggle="modal"
                                data-bs-target="#deleteAuctionModal"
                                ><i class="fa-solid fa-trash-can"></i>
                        </button>
                        <button class="btn btn-icon p-0"
                                style="width: 27px; height: 27px;"
                                @click="toggleEditData"
                                ><i class="fa-solid fa-pen"></i>
                        </button>
                      </div>
                    </div>
                  </div>
                  <div class="card-body card-body-detail">
                    <AuctionFormComponent :auction="modifiedAuction"
                                          :enableEdit="editData"
                                          @not-found="setNotFound"
                                          @refresh-auctions="updateData"/>
                  </div>
             </div>
           </div>
         </div> <!-- Row -->

         <!-- Delete auction modal -->
         <div aria-hidden="true"
              aria-labelledby="deleteAuctionModalLabel"
              class="modal fade"
              id="deleteAuctionModal"
              tabindex="-1">
              <div class="modal-dialog">
                <div class="modal-content">
                  <div class="modal-body text-center">
                    <p class="text-card-auction fw-bold fs-20px"
                       id="deleteAuctionModalLabel"
                       >Do you want to delete the following auction?
                    </p>
                    <p class="text-card-auction fs-18px">{{ auction.title }}</p>
                    <div class="row justify-content-between mt-4">
                      <div class="col-auto">
                        <button class="btn btn-secondary rounded-pill"
                                data-bs-dismiss="modal"
                                type="button"
                                >Cancel
                        </button>
                      </div>
                      <div class="col-auto">
                        <button class="btn btn-danger rounded-pill"
                                data-bs-dismiss="modal"
                                type="button"
                                @click="deleteAuction"
                                >Delete
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
         </div> <!-- Delete auction modal -->
    </div> <!-- Container -->
  </div>
</template>

<script>
  // @ is an alias to /src
  import { apiService } from "@/common/api.service.js";
  import AuctionFormComponent from "@/components/AuctionForm.vue";
  import Error404Component from "@/components/Error404.vue";

  export default {
    name: "AuctionEditor",
    components: {
      AuctionFormComponent,
      Error404Component
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
        modifiedAuction: this.auction,
        image: {
          file: null,
          url: null,
          error: null
        },
        editImage: false,
        editData: false,
        notFound: false
      }
    },
    computed: {
      getImage() {
        if (this.image.url) {
          return this.image.url;
        }
        return this.modifiedAuction.image;
      },
      isImageInvalid(){
        return this.image.error != null;
      }
    },
    methods: {
      toggleEditImage() {
        this.editImage = !this.editImage;
      },
      toggleEditData() {
        this.editData = !this.editData;
      },
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
                console.log(response.detail);
                this.notFound = true;
              } else {
                this.image.url = URL.createObjectURL(this.image.file);
                this.image.file = null;
                if (this.image.error) {
                  this.image.error = null;
                }
              }
            })
            .catch(error => {
              console.log(error);
              this.notFound = true;
            });
          }
        },
        async updateData() {
          /*
            Update auction's data after save.
          */

          let endpoint = `/api/schedule-auctions/${this.modifiedAuction.id}/`;
          await apiService(endpoint)
            .then(response => {
              if (response.detail) {
                console.log(response.detail);
                this.notFound = true;
              } else {
                this.modifiedAuction = response;
                document.title = `${response.title} | Schedule auctions | ChainBid`;
              }
            })
            .catch(error => {
              console.log(error);
              this.notFound = true;
            });
        },
        async deleteAuction() {
          /*
            Delete auction and redirect to the schedule auctions page.
          */

          let endpoint = `/api/schedule-auctions/${this.modifiedAuction.id}/`;
          let method = "DELETE"
          await apiService(endpoint, method)
            .then(response => {
              if (response.detail) {
                console.log(response.detail);
                this.notFound = true;
              } else {
                this.$router.push({name: "schedule auctions"});
                this.$toasted.show(`${this.modifiedAuction.title} deleted`, {icon: "trash-can"});
              }
            })
            .catch(error => {
              console.log(error);
              this.notFound = true;
            });
        },
        setNotFound() {
          this.notFound = true;
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
        })
        .catch(error => {
          console.log(error);
        });
      return next();
    },
    created() {
      if (this.auction.detail) {
        console.log(this.auction.detail);
        this.notFound = true;
      }
      document.title = `${this.modifiedAuction.title} | Schedule auctions | ChainBid`;
    }
  }
</script>

<style lang="css" scoped>
  input[type=file]::file-selector-button {
    background-color: #4A4E69 !important;
    border-color: #4A4E69 !important;
    color: #FFF !important;
  }

  input[type=file]:hover::file-selector-button {
    background-color: #52528E !important;
  }

  input[type=file]:disabled::file-selector-button {
    background-color: #4A4E69 !important;
    pointer-events: none;
    opacity: .65;
  }

  .modal-content {
    background-color: #F2E9E4;
    border-color: #C9ADA7;
  }
</style>
