<template>
  <div class="container">
    <mt-header :title="`#${game.id} ${game.name}`">
    </mt-header>

    {{game.name}}

  </div>
</template>

<script>

export default {
  head: { title: '新建对局' },
  async asyncData (context) {
    const game_id = context.params.id
    const r = await context.$axios.get(`/game/api/game_status/`, {params: {game_id}})
    return {
      game: r.data
    }
  },
  data() {
    return {
    }
  },
  methods: {
  }
}
</script>


<style>

</style>
