<template lang="html">
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark bg-gradient">
    <div class="container">
      <!-- Brand and logo -->
      <a class="navbar-brand"
         href="#">
         <img alt="logo"
              class="d-inline-block mb-2"
              src="../../../static-storage/logo-200x32-orig.png">
      </a>

      <!-- Collapsed menu button -->
      <button aria-controls="navbarSupportedContent"
              aria-expanded="false"
              aria-label="Toggle navigation"
              class="navbar-toggler"
              data-bs-target="#navbarSupportedContent"
              data-bs-toggle="collapse"
              type="button">
              <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Navbar elements -->
      <div class="collapse navbar-collapse"
           id="navbarSupportedContent">
           <!-- Links -->
           <ul class="navbar-nav ml-auto mb-2 mb-lg-0">
             <li class="nav-item">
               <!-- aria-current da gestire dinamicamente -->
               <a aria-current="page"
                  class="nav-link active"
                  href="#"
                  >Live acutions
                </a>
             </li>
             <li class="nav-item">
               <a class="nav-link"
                  href="#"
                  >Closed auctions
               </a>
             </li>
             <li class="nav-item">
               <a class="nav-link"
                  href="#"
                  >How it works
               </a>
             </li>
           </ul>

           <!-- Dropdown menu -->
           <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
             <!-- Dropdown button -->
             <li class="nav-item dropdown">
               <a aria-expanded="false"
                  class="nav-link"
                  data-bs-toggle="dropdown"
                  href="#"
                  id="navbarDarkDropdownMenuLink"
                  role="button">
                  <i class="bi bi-person-lines-fill fs-3 nav-icon"></i>
               </a>

               <!-- Dropdown elements -->
               <ul aria-labelledby="navbarDarkDropdownMenuLink"
                   class="dropdown-menu dropdown-menu-dark">
                   <li><h6 class="dropdown-header"
                     >Username
                   </h6></li>
                   <li><a class="dropdown-item"
                          href="#"
                          >Profile
                   </a></li>
                   <li><a class="dropdown-item"
                          href="#"
                          >Change password
                   </a></li>
                   <li><a class="dropdown-item"
                          href="#">
                          <i class="bi bi-box-arrow-left fs-5 nav-icon"></i>
                   </a></li>
               </ul>
             </li>
           </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: "NavbarComponent"
}
</script>

<style lang="css" scoped>
  .nav-icon {
    color: #ffe3b0;
  }

  .nav-icon:hover {
    color: #ffe169;
  }

  .nav-link {
    color: #fcede9 !important;
  }

  .nav-link:hover {
    color: #eea391 !important;
  }

  .active {
    color: #eea391 !important;
  }
</style>
