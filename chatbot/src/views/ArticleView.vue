<template>
  <div class="component-container">
    <div class="header-container">
      <h1 class="title-container">Constitution Française de 1958</h1>
      <div class="search-container">
        <IconBase name="magnifying-glass" type="fas" class="icon-container" />
        <input type="search" placeholder="Rechercher parmi les articles..." class="input-container"/>
      </div>
    </div>
    <div class="body-container">
      <ArrayComponent :titles="titles" :articles="constitution"></ArrayComponent>
    </div>
  </div>

</template>

<script>
import IconBase from "@/components/icons/IconBase.vue";
import ArrayComponent from "@/components/article/ArrayComponent.vue";
import { useConstitutionStore } from '@/stores/constitutionStore/ConstitutionStore.js';

export default{
  components: {
    IconBase,
    ArrayComponent
  },

  computed: {
    titles () {
      return ['Article', 'Aperçu', 'Action']
    },
    constitution () {
      return useConstitutionStore().getConstitution
    }
  },
}
</script>

<style scoped>

.component-container {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title-container {
  font-weight: bold;
}

.search-container {
  display: flex;
  color: #949ED1;
  border: 1px solid #F0F2FC;
  border-radius: 5px;
  width: 250px;
  padding: .5rem;
  box-shadow: 0px 1px #F2F2F5;
  justify-content: start;
}

.icon-container {
  padding: .2rem;
}

.input-container {
  border: none;
  width: 100%
}

.input-container:focus {
  outline: none;
}

.input-container::placeholder {
  color: #949ED1;
}

.input-container:focus::placeholder {
  color: transparent;
}
</style>
