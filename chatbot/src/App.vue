<template>
  <div id="app" :class="{'relative': drawerStore.getShowDrawer}">
    <SidebarComponent/>
    <div class="router">
      <RouterView/>
    </div>
    <template v-if="drawerStore.getShowDrawer">
      <DrawerBase
        :drawer="drawerStore.getDrawer.name"
        :data="drawerStore.getDrawer.data"
      />
    </template>
  </div>

</template>

<script>

import SidebarComponent from "@/components/sidebar/SidebarComponent.vue";
import DrawerBase from "@/components/drawers/DrawerBase.vue";
import {useDrawerStore} from "@/store/drawerStore/DrawerStore.js";

export default {

  components: {
    DrawerBase,
    SidebarComponent
  },

  computed: {
    drawerStore () {
      return useDrawerStore()
    }
  }

}
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
  z-index: 0;
}

.relative {
  position: relative;
}

.router {
  padding: 0 1rem;
  width: 100%;
}

</style>
