export default function ({ $axios, store, redirect }) {
  $axios.onRequest((config) => {
    const token = 'admin:admin'
    if (token) {
      config.headers.common['x-token'] = token
    }
    return config
  })
  $axios.onResponseError((error) => {
    if (error.response && (error.response.status === 401 || error.response.status === 403)) {
      redirect('/login')
    }
  })
}
