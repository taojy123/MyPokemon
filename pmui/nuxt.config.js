
export default {
  // mode: 'universal',
  mode: 'spa',
  /*
  ** Headers of the page
  */
  head: {
    title: process.env.npm_package_name || 'Pokemon Card',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: process.env.npm_package_description || '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },
  /*
  ** Customize the progress-bar color
  */
  loading: { color: '#fff' },
  /*
  ** Global CSS
  */
  css: [
    'mint-ui/lib/style.css',
    '~/assets/css/main.css'
  ],
  /*
  ** Plugins to load before mounting the App
  */
  plugins: [
    '@/plugins/mint-ui',
    '@/plugins/axios',
  ],
  /*
  ** Nuxt.js dev-modules
  */
  buildModules: [
  ],
  /*
  ** Nuxt.js modules
  */
  modules: [
    // Doc: https://axios.nuxtjs.org/usage
    '@nuxtjs/axios',
  ],
  /*
  ** Axios module configuration
  ** See https://axios.nuxtjs.org/options
  */
  axios: {
    baseURL: process.env.API_URL || 'http://127.0.0.1:8000', // yuse env API_URL to override
    browserBaseURL: process.env.API_URL_BROWSER || 'http://127.0.0.1:8000', // use env API_URL_BROWSER to override
    credentials: false // cross-site Access-Control requests doesn't need to be made using credentials
  },
  /*
  ** Build configuration
  */
  build: {
    // transpile: [/^mint-ui/],
    /*
    ** You can extend webpack config here
    */
    // vendor: ['axios'],
    extend (config, ctx) {
    }
  }
}
