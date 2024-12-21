<template>
  <FontAwesomeIcon :icon="icon"/>
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
      validator: (value) => {
        return ['fas', 'far', 'fal', 'fat'].includes(value)
      }
    }
  },

  computed: {
    icon() {
      return [this.type, this.name]
    }
  }
}
</script>
