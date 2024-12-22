<template>
  <table class="table-container">
    <thead class="head-container">
    <tr class="row-container remove-border">
      <th v-for="(title, index) in titles" :key="index" class="column-container" :class="{'remove-border': index === titles.length - 1}">
        {{ title }}
      </th>
    </tr>
    </thead>
    <tbody class="body-container">
      <template v-for="(item, index) in displayArticles" :key="index">
        <!-- Parent Row -->
        <tr class="row-container remove-rounded" :class="{'remove-border': index !== articles.length - 1}">
          <th class="column-container remove-border first-column">
            <button @click="toggleRow(index, false)" class="button-container chevron-container">
              <IconBase :name="show && indexSelected === index ? 'chevron-down' : 'chevron-right'" type="fas" />
            </button>
            <span class="span-container">{{ item.title }}</span>
          </th>
          <th class="column-container remove-border title-apercu-container">{{ item.aperçu }}</th>
          <th class="column-container remove-border">
            <button class="button-container">
              <IconBase type="far" name="comment-dots" />
            </button>
          </th>
        </tr>
        <!-- Child Rows -->
        <tr v-if="show && indexSelected === index" class="child-row">
          <td colspan="3" class="child-container">
            <div class="color-container"></div>
            <table class="child-table">
              <tbody>
              <tr
                  v-for="(article, indexArticle) in displayArticles[indexSelected].articles"
                  :key="indexArticle"
                  class="row-container remove-rounded" :class="{'remove-border': index !== articles.length - 1}"
              >
                <th class="column-container remove-border">
                  <button @click="toggleRow(indexArticle, true)" class="button-container chevron-container">
                    <IconBase :name="showChild && indexChildSelected === indexArticle ? 'chevron-down' : 'chevron-right'" type="fas" />
                  </button>
                  <span class="span-container">{{ article.title }}</span>
                </th>
                <th class="column-container remove-border child-text-container">
                  {{ article.text }}
                </th>
                <th class="column-container remove-border">
                  <button class="button-container">
                    <IconBase type="far" name="comment-dots" />
                  </button>
                </th>
              </tr>
              </tbody>
            </table>
          </td>
        </tr>
      </template>
    </tbody>
    <tfoot class="pagination-container">
      <tr>
        <th>
          <PaginationComponent
              :pages="numberPages"
              :number-articles="numberArticles"
              :total-articles="totalArticles"
              @pageSelected="updatePageSelected" />
        </th>
      </tr>
    </tfoot>
  </table>
</template>

<script>
import IconBase from "@/components/icons/IconBase.vue";
import PaginationComponent from "./PaginationComponent.vue"

export default {
  components: {
    IconBase,
    PaginationComponent
  },

  data() {
    return {
      show: false,
      indexSelected: null,
      indexChildSelected: null,
      showChild: null,
      pageSelected: 1
    };
  },

  props: {
    titles: {
      type: Array,
      default: [],
    },
    articles: {
      type: Array,
      default: [],
    },
    articleToDisplay: {
      type: Number,
      default: 10
    }
  },

  computed: {
    numberPages () {
      return Math.ceil(this.articles.length / this.articleToDisplay)
    },
    displayArticles () {
      const startIndex = (this.pageSelected - 1) * this.articleToDisplay
      const endIndex = this.pageSelected * this.articleToDisplay
      return this.articles.slice(startIndex, endIndex)
    },
    numberArticles () {
      if(this.displayArticles.length === this.articleToDisplay) {
        return [(this.pageSelected - 1) * this.articleToDisplay + 1, this.pageSelected * this.articleToDisplay]
      } else {
        return [(this.pageSelected - 1) * this.articleToDisplay + 1, (this.pageSelected - 1) * this.articleToDisplay + this.displayArticles.length]
      }
    },
    totalArticles () {
      return this.articles.length
    }
  },

  methods: {
    toggleRow(index, isChild = false) {
      if (isChild) {
        this.indexChildSelected = this.indexChildSelected === index ? null : index;
        this.showChild = this.indexChildSelected !== null;
      } else {
        this.indexSelected = this.indexSelected === index ? null : index;
        this.show = this.indexSelected !== null;
      }
    },
    updatePageSelected (value) {
      this.pageSelected = value
    }
  },
};
</script>

<style scoped>


.table-container {
  padding-top: 0.5rem;
  width: 100%;
  color: #2e3e8a;
  border-collapse: collapse;
}

.body-container {
  overflow-y: auto;
}

.row-container {
  display: flex;
  justify-content: space-between;
  border: 1px solid #EBEDFB;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
}

.row-container.remove-border {
  border-bottom: 0;
}

.column-container {
  margin: 0.7rem;
  display: inline-block;
  width: 100%;
  border-right: 0.2rem solid #EBEDFB;
  font-weight: bold;
  text-align: start;
}


.column-container.remove-border {
  border: none;
}

.remove-rounded {
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}

.span-container {
  font-weight: bold;
}

.button-container {
  all: unset;
  cursor: pointer;
  margin-right: 4rem;
  margin-left: 0.5rem;
}

.chevron-container {
  width: 30px;
}

.column-container.child-text-container {
  max-width: 379px;
  text-overflow: ellipsis !important;
  white-space: nowrap;
  overflow: hidden;
}


.child-container {
  display: flex;
  padding: 0;
}

.child-table {
  width: 100%;
  border-collapse: collapse;
}

.child-row {
  width: 100%;
}

.color-container {
  width: .2rem;
  background-color: #F6F8FE;
  border: 2px solid #EBEDFB;
}

.pagination-container {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: end;
  border: 1px solid #EBEDFB;
  border-bottom-left-radius: 5px;
  border-bottom-right-radius: 5px;
  padding: .7rem;
}


</style>
