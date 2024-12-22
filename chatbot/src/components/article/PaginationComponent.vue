<template>
  <div class="body-container">
    <div class="number-article-container">
      <span>{{numberArticles[0]}} to {{numberArticles[1]}} of {{totalArticles}}</span>
    </div>
    <div class="pagination-container">
      <button>
        <IconBase v-if="page !== 1" @click="page -= 1" type="fas" name="chevron-left" />
      </button>
      <span class="number-page-container">{{page}} to {{pages}}</span>
      <button>
        <IconBase v-if="page !== pages" @click="page += 1" type="fas" name="chevron-right" />
      </button>
    </div>
  </div>
</template>

<script>
import IconBase from "@/components/icons/IconBase.vue";

export default {

  components: {
    IconBase
  },

  data () {
    return {
      page: 1
    }
  },

  props: {
    pages: {
      type: Number,
      default: null
    },
    numberArticles: {
      type: Array,
      default: []
    },
    totalArticles: {
      type: Number,
      default: null
    }
  },

  watch: {
    page (value) {
      this.$emit('pageSelected', value)
    }
  }


}
</script>

<style scoped>
.body-container {
  width: 100%;
  display: flex;
  justify-content: end;
}

button {
  all: unset;
  cursor: pointer;
}

span {
  font-weight: bold;
}

.number-article-container {
  margin-right: .4rem;
}

.number-page-container {
  margin: 0 .4rem;
}
</style>
