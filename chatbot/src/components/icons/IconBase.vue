<template>
  <div class="container" :class="[action, size, background, color]">
    <FontAwesomeIcon :icon="icon" :size="size" />
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
      default: 'md',
      validator: (value) => ['sm', 'md', 'lg', 'xl'].includes(value)
    },
    background: {
      type: String,
      required: false,
      default: ''
    },
    color: {
      type: String,
      required: false,
      default: ''
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
  width: 1.2rem;
  height: 1.2rem;
}

.xl {
  width: 2.2rem;
  height: 2.2rem;
}

.click:hover {
  cursor: pointer;
  background-color: #C0CAF8;
  color: white;
}

.focus {
  cursor: pointer;
  background-color: #C0CAF8;
  border: 1px solid #B0BCF7;
}

.deep-blue {
  background-color: #405BDD;
  color: white;
}

.deep-blue-color {
  color: #405BDD;
}

.error {
  color: #EF5350;
}

</style>
