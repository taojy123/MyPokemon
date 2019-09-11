<template>
  <div class="container">
    <mt-header fixed title="新建对局">
    </mt-header>

    <div>
      <mt-field label="名称" placeholder="请输入名称" v-model="name"></mt-field>
    </div>

  </div>
</template>

<script>

export default {
  head: { title: '新建对局' },
  data() {
    return {
      name: ''
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
