<template>
  <svg
      xmlns="http://www.w3.org/2000/svg"
      :width="width"
      :height="height"
      viewBox="0 0 24 24"
      :fill="color"
      role="img"
      aria-label="Search icon"
      class="icon-search"
  >
    <path
        d="M11 2a9 9 0 1 1-6.36 15.36l-4.29 4.3a1 1 0 0 1-1.42-1.42l4.3-4.29A9 9 0 0 1 11 2Zm0 2a7 7 0 1 0 4.95 11.95 7 7 0 0 0-4.95-11.95Z"
    />
  </svg>
</template>

<script>
export default {
  name: "IconSearch",
  props: {
    width: {
      type: String,
      default: "24",
    },
    height: {
      type: String,
      default: "24",
    },
    color: {
      type: String,
      default: "currentColor",
    },
  },
};
</script>

<style scoped>
.icon-search {
  margin-left: .2rem;
  margin-right: .2rem;
}
</style>
