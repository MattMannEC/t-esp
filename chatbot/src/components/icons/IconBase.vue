<template>
  <div class="container" :class="[action, size]">
    <FontAwesomeIcon :icon="icon" />
  </div>
</template>
<script>
export default {
  props: {
    name: {
      type: String,
      required: true,
      default: ''
    },
    type: {
      type: String,
      required: true,
      validator: (value) => ['fas', 'far', 'fal', 'fat'].includes(value)

    },
    action: {
      type: String,
      required: false,
      default: ''
    },
    size: {
      type: String,
      required: false,
      default: 'md'
    }
  },

  computed: {
    icon() {
      return [this.type, this.name]
    }
  }
}
</script>

<style scoped>

.container{
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 25%;
}

.md {
  width: 1rem;
  height: 1rem;
}

.click:hover {
  cursor: pointer;
  background-color: #C0CAF8;
  color: white;
}
</style>
