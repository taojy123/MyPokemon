<template>
  <div class="container">
    <div>
      <logo />
      <h1 class="title">
        pmui
      </h1>
      <nuxt-link to="/">Home page</nuxt-link>
      <nuxt-link to="/test">test</nuxt-link>
      <h2 class="subtitle">
        Pokemon Card UI
      </h2>
      <div class="links">
        <a
          href="https://nuxtjs.org/"
          target="_blank"
          class="button--green"
        >
          Documentation
        </a>
        <a
          href="https://github.com/nuxt/nuxt.js"
          target="_blank"
          class="button--grey"
        >
          GitHub
        </a>
      </div>
    </div>
  </div>
</template>

<script>
import Logo from '~/components/Logo.vue'

export default {
  components: {
    Logo
  }
}
</script>

<style>
</style>
