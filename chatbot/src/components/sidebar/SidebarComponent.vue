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
      <RouterLink :to="{ name: 'article' }">
        <IconBase
          type="fas"
          name="house"
          :action="isSameRoute ('article') ?'focus' : ''"
          size="xl"
          color="deep-blue-color"
        />
      </RouterLink>
      <RouterLink :to="{ name: 'chatbot' }">
        <IconBase
          type="far"
          name="comment-dots"
          :action="isSameRoute ('chatbot') ?'focus' : ''"
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

  computed: {
    currentRoute () {
      return this.$route.name
    }
  },

  methods: {
    isSameRoute (route) {
      return this.currentRoute === route
    }
  }
}
</script>

<style scoped>

.sidebar-main-container {
  height: 100%;
  width: 4rem;
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
