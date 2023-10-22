<template>
  <div>
    {{ options }}
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "AdvancedSearchPage",
  data: () => ({
    options: {}
  }),
  mounted: function() {
    this.getOptions()
  },
  methods: {
    async getOptions() {
      const headers = {"Authorization": `Bearer ${process.env.VUE_APP_PDAP_TOKEN}`}
      console.log(process.env.VUE_APP_PDAP_TOKEN, process.env.VUE_APP_BASE_URL)
      const res = await axios.get(`${process.env.VUE_APP_BASE_URL}/advanced-search-options`, {headers}) 
      this.options = res.data
    }
  }
}
</script>