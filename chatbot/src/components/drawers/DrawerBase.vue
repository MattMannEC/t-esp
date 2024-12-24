<template>
  <div class="drawer-container">
    <div class="background-container" @click="drawerStore.closeDrawer()" />
    <div class="drawer-content">
      <Component :is="drawer" :data="data" />
    </div>
  </div>
</template>

<script>
import {useDrawerStore} from "@/store/drawerStore/DrawerStore.js";
import ChatBotDrawer from "@/components/drawers/ChatBotDrawer.vue";

export default {

  components: {
    ChatBotDrawer
  },

  props: {
    drawer: {
      type: String,
      required: true,
      default: ''
    },
    data: {
      type: Object,
      required: false,
      default: {}
    }
  },

  computed: {
    drawerStore () {
      return useDrawerStore()
    }
  },

  mounted() {
    console.log('base', this.drawer, this.data)
  }

}
</script>

<style scoped>
.drawer-container {
  display: flex;
  position: fixed;
  top: 0;
  right: 0;
  z-index: 1000;
  height: 100%;
  width: 100%;
  box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1);
}

.background-container {
  flex: 2;
  background-color: rgba(0, 0, 0, 0.5);
  cursor: pointer;
}

.drawer-content {
  flex: 1;
  background-color: white;
  display: flex;
  box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1);
}
</style>
