<template lang="pug">
  article.tags
    header Tags
      div.f-right
        feed-link(:link="atom")
    content
      ul
        li(v-for='tag_info, tag of tags')
          nuxt-link(:to="tag_info.slug") {{tag}}
          |           ({{tag_info.length}})
</template>

<script lang="ts">
const FeedLink = () => import("~/components/FeedLink")

export default {
  components: {
    FeedLink
  },
  data() {
    return {data}
  },
  head() {
    return {
      title: "Tags",
      link: [{ rel: 'alternate', href: this.atom, type: 'application/atom+xml' }]
    }
  }
}
</script>