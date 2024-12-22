<template>
  <div class="component-container">
    <div class="header-container">
      <h1 class="title-container">Constitution Française du 4 octobre 1958</h1>
      <div class="search-container">
        <IconBase name="magnifying-glass" type="fas" class="icon-container" />
        <input
            type="search"
            placeholder="Rechercher parmi les articles..."
            v-model="searchItem"
            class="input-container"/>
      </div>
    </div>
    <div class="body-container">
      <TableComponent
        :titles="titles"
        :articles="searchItem ? articles : constitution"
      />
    </div>
  </div>

</template>

<script>
import IconBase from "@/components/icons/IconBase.vue";
import TableComponent from "@/components/article/TableComponent.vue";
import { useConstitutionStore } from "@/store/constitutionStore/ConstitutionStore.js"

export default{
  components: {
    IconBase,
    TableComponent
  },

  data () {
    return {
      searchItem: ''
    }
  },

  computed: {
    titles () {
      return ['Articles', 'Aperçu', 'Actions']
    },
    constitution () {
      return useConstitutionStore().getConstitution
    },
    articles() {
      return this.constitution
          .map(title => {
            const isTitleMatching = title.title.toLowerCase().includes(this.searchItem.toLowerCase())
                || title.aperçu.toLowerCase().includes(this.searchItem.toLowerCase())

            const matchingChildren = title.articles.filter(article =>
                article.title.toLowerCase().includes(this.searchItem.toLowerCase()))

            if (isTitleMatching) {
              return {
                ...title
              };
            }

            if (matchingChildren.length > 0) {
              return {
                ...title,
                articles: matchingChildren
              };
            }

            return null
          })
          .filter(title => title !== null)
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
  margin-bottom: .5rem;
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
