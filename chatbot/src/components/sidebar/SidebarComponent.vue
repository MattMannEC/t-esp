<template>
  <div class="sidebar-main-container">
    <div class="icon-app-container">
      <IconBase
        type="fas"
        name="scale-balanced"
        size="xl"
        background="deep-blue"
      />
    </div>

    <div class="navigation-container">
      <RouterLink
          v-for="(item, index) in navigation"
          :key="index"
          :to="{ name: item.name }"
          @mouseenter="hover = index"
          @mouseleave="hover = null"
      >
        <IconBase
          :type="item.icon.type"
          :name="item.icon.name"
          :action="isSameRoute(item.name) || isHover(index) ? 'focus' : ''"
          size="xl"
          color="deep-blue-color"
        />
      </RouterLink>
    </div>
  </div>
</template>

<script>
import IconBase from "@/components/icons/IconBase.vue";
export default {

  components: {
    IconBase
  },

  data() {
    return {
      hover: null
    }
  },

  computed: {
    currentRoute () {
      return this.$route.name
    },
    navigation () {
      const items = [
        {
          name: 'article',
          icon: {
            type: 'fas',
            name: 'house',
          }
        },
        {
          name: 'chatbot',
          icon: {
            type: 'far',
            name: 'comment-dots',
          }
        }
      ]
      return items
    }
  },

  methods: {
    isSameRoute (route) {
      return this.currentRoute === route
    },
    isHover (index) {
      return this.hover === index
    }
  }
}
</script>

<style scoped>

.sidebar-main-container {
  height: 100%;
  width: 4.5rem;
  background-color: #E0E4FC;
}

.navigation-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-top: .2rem;
}

.icon-app-container{
  width: 100%;
  display: flex;
  justify-content: center;
  padding: 1rem;
}



</style>
