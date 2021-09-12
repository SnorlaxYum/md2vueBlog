<template lang="pug">
cat-page(:name="name" :atom="atom" :posts="posts" :isTag="false" :tags="tags")
</template>
<script>
const CatPage = () => import('~/routeComponents/PostListPage')

export default {
  data() {
    return {data}
  },
  components: {
    CatPage
  }
}
</script>