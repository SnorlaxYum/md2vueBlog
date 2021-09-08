<template>
<PostRoute :title="title" :date="date" :modified="modified" :slug="slug" :tags="tags" :summary="summary" :ogimage="ogimage" :category="category">
  {html}
</PostRoute>
</template>

<script>
const PostRoute = () => import('~/routeComponents/PostRoute').then(mod => mod.default)
export default {
  components: {
    PostRoute
  },
  data() {
    return {data}
  }
}
</script>