<template lang="html">
  <div class="not-found">
    <Error404Component/>
  </div>
</template>

<script>
  // @ is an alias to /src
  import Error404Component from "@/components/Error404.vue";

  export default {
    name: "NotFound",
    components: {
      Error404Component
    },
  }
</script>

<style lang="css">
</style>
