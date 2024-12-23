<template>
  <div id="app">
    <SidebarComponent/>
    <div class="router">
      <RouterView/>
    </div>
  </div>
</template>

<script>

import {defineComponent} from "vue";
import SidebarComponent from "@/components/sidebar/SidebarComponent.vue";

export default defineComponent({
  components: {SidebarComponent}
})
</script>

<style scoped>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0;
  color: #949ED1;
  height: 100%;
  width: 100%;
  font-size: 12px;
  padding: 0;
}

.router {
  padding: 0 2rem;
  width: 100%;
}

</style>
