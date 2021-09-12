<template lang="pug">
tag-page(:name="name" :atom="false" :posts="posts" :isTag="true" :tags="tags")
</template>
<script>
const TagPage = () => import('~/routeComponents/PostListPage')

export default {
  components: {
    TagPage
  },
  data() {
    return {data}
  }
}
</script>