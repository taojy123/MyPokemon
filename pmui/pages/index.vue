<template>
  <div class="container">
    <mt-header fixed title="我的对局">
      <mt-button slot="right" icon="more" @click="newGame"></mt-button>
    </mt-header>

    <div class="games">
      <mt-cell v-for="game in games" :key="game.id" :value="game.name" :is-link="true" :to="`/game/${game.id}`">
        <span slot="icon">
          <img v-for="pic in game.pics" :key="pic" width="24" height="24" :src="pic">
        </span>
      </mt-cell>
    </div>

  </div>
</template>

<script>

export default {
  head: { title: '我的对局' },
  data() {
    return {
      name: '123',
      games: []
    }
  },
  methods: {
    newGame () {
      this.$router.push('/new')
      // top.location.href = '/new'
    }
  }
}
</script>


<style>

</style>
