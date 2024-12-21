<template>
  <table class="table-container">
    <thead class="head-container">
      <tr class="row-container">
        <th v-for="(title, index) in titles" class="column-container" :class="{'remove-border': index === titles.length - 1}">{{title}}</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(title, index) in articles" class="row-container remove-rounded" :class="{'remove-border': index !== articles.length - 1}">
        <th class="column-container remove-border article-container">
          <button @click="showSelected(index)" class="button-container chevron-container">
            <IconBase :name="show && indexSelected === index ? 'chevron-down' : 'chevron-right'" type="fas" />
          </button>
          <span class="span-container">{{title.title}}</span>
        </th>
        <th class="column-container remove-border">hello</th>
        <th class="column-container remove-border">
          <button class="button-container">
            <IconBase type="far" name="comment-dots" />
          </button>
        </th>
      </tr>
      <tr v-if="show && indexSelected === articles[index]" class="child-row">
        <td colspan="3" class="child-container">
          <table class="child-table">
            <tbody>
            <tr
                v-for="(article, childIndex) in articles[index].articles"
                :key="childIndex"
                class="child-row-container"
            >
              <td class="column-container remove-border article-container">
                <span class="span-container">{{ article.title }}</span>
              </td>
              <td class="column-container remove-border">{{ article.text }}</td>
              <td class="column-container remove-border">
                <button class="button-container">
                  <IconBase type="far" name="comment-dots" />
                </button>
              </td>
            </tr>
            </tbody>
          </table>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import IconBase from "@/components/icons/IconBase.vue";

export default {

  components: {
    IconBase
  },

  data () {
    return {
      show: false,
      indexSelected: null
    }
  },

  props: {
    titles: {
      type: Array,
      default: []
    },
    articles: {
      type: Array,
      default: []
    }
  },

  methods: {
    showSelected(index) {
      if (this.indexSelected === index) {
        this.indexSelected = null;
        this.show = false;
      } else {
        this.indexSelected = index;
        this.show = true;
      }
    }
  }
}
</script>

<style scoped>

.table-container {
  padding-top: .5rem;
  width: 100%;
  color: #2E3E8A;
}

.row-container {
  display: flex;
  justify-content: space-between;
  border: 1px solid #F0F2FC;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
}

.row-container.remove-border {
  border-bottom: 0;
}

.column-container {
  margin: .7rem;
  display: flex;
  justify-content: start;
  width: 100%;
  border-right: .2rem solid #F0F2FC;
  font-weight: bold;
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
  margin-left: .5rem;
}

.chevron-container {
  width: 30px;
}

.template-container {
  display: flex;
  flex-direction: column;
}

</style>
