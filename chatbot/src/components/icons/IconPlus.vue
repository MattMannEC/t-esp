<template>
  <svg
      xmlns="http://www.w3.org/2000/svg"
      :width="width"
      :height="height"
      viewBox="0 0 24 24"
      :fill="color"
      role="img"
      aria-label="Plus icon"
  >
    <path d="M12 5v6H6v2h6v6h2v-6h6v-2h-6V5h-2z" />
  </svg>
</template>

<script>
export default {
  name: "PlusIcon",
  props: {
    width: {
      type: String,
      default: "24", // Largeur par défaut
    },
    height: {
      type: String,
      default: "24", // Hauteur par défaut
    },
    color: {
      type: String,
      default: "currentColor", // Couleur par défaut (hérite de la couleur du texte environnant)
    },
  },
};
</script>
