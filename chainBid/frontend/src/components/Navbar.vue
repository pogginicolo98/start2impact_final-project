<template lang="html">
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark bg-gradient">
    <div class="container">
      <a class="navbar-brand" href="#">
        <img src="../../../static-storage/logo-200x32-orig.png" alt="logo" class="d-inline-block mb-2">
      </a>

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mx-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="#">Live acutions</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">Closed auctions</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">How it works</a>
          </li>
        </ul>
        <div class="nav-item dropdown">
          <div class="btn-group">
            <button type="button" class="btn btn-outline-primary">Nome utente</button>
            <button type="button" class="btn btn-outline-primary dropdown-toggle dropdown-toggle-split" data-bs-toggle="dropdown" aria-expanded="false">
              <span class="visually-hidden">Toggle Dropdown</span>
            </button>
            <ul class="dropdown-menu dropdown-menu-dark">
              <li><a class="dropdown-item" href="#">Profile</a></li>
              <li><a class="dropdown-item" href="#">Change Password</a></li>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item" href="#">Log Out</a></li>
            </ul>
          </div>
        </div>
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
</style>
