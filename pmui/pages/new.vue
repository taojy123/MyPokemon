<template>
  <div class="container">
    <mt-header title="新建对局">
    </mt-header>

    <mt-field label="名称" placeholder="请输入名称" v-model="name"></mt-field>

    <mt-cell title="挑选你的精灵"></mt-cell>
    <div
      :v-infinite-scroll="loadMore"
      :infinite-scroll-disabled="loading"
      :infinite-scroll-distance="10"
      :infinite-scroll-immediate-check="true">
      <mt-cell v-for="pokemon in pokemons" :key="pokemon.name" :title="pokemon.name" :value="pokemon.system" @click.native="newGame(pokemon.id)">
        <img slot="icon" :src="pokemon.pic" width="24" height="24">
      </mt-cell>
    </div>

  </div>
</template>

<script>

import { Indicator } from 'mint-ui';

export default {
  head: { title: '新建对局' },
  async asyncData (context) {
    const r = await context.$axios.get(`/game/api/pokemons/`, {params: {init_pokemon: 1}})
    return {
      pokemons: r.data
    }
  },
  data() {
    return {
      name: '',
      loading: false
    }
  },
  methods: {
    loadMore() {
      this.loading = true;
      this.loading = false;
    },
    newGame (pokemonId) {
      Indicator.open()
      const url = '/game/api/new/'
      const name = this.name
      const pokemon_id = pokemonId
      this.$axios.post(url, {name, pokemon_id}).then(res => {
        Indicator.close()
        this.$message.alert('创建成功').then(()=>{
          const gameId = res.data.id
          this.$router.push(`/game/${gameId}`)
        })

      })
    }
  }
}
</script>


<style>

</style>
