import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router'
import axios from 'axios'

let $axios = axios.create({
  baseURL: "http://localhost:8080",
  withCredentials: true
})

// Automatically add token to header
$axios.interceptors.request.use((config) => {
  let token = localStorage.getItem('token');
  if (token) {
    config.headers['Authorization'] = token
  }
  return config
})

$axios.interceptors.response.use(
    response => {
      if (response.status === 200) {
        return Promise.resolve(response);
      } else {
        return Promise.reject(response);
      }
    },
    error => {
      if (error.response.status) {
        switch (error.response.status) {

          case 401: // not login yet
            console.log('401 error')
            router.push({
              path: '/login',
              query: {
                type: 'warning',
                msg: 'You are not logged in'
              }
            });
            break;
          case 403: // token expired or invalid
            console.log('403 error')
            localStorage.removeItem('token');
            router.push({
              path: '/login',
              query: {
                type: 'warning',
                msg: 'You account status is expired, Please log in again'
              }
            });
            break;
          case 404:
            break;
          default:
            // other error?
            break;
        }
        return Promise.reject(error.response);
      }
    }
);


Vue.prototype.$axios = $axios

Vue.prototype.$URL = {
  register: "auth/register",
  login: "auth/login",
  resetPassword: "auth/resetPass",
  resetVerifiy: "auth/resetVerify",
  editPassword: "user/editPass",
  adminBooks: "admin/listBooks",
  listBooks: "book/bookList",
  newBook: "admin/newBook",
  editBook: "admin/editBook",
  deleteBook: "admin/deleteBook",
  getBook: "admin/getBook",
  listUsers: "admin/listUsers",
  block: "admin/blockUser",
  profile: "user/profile",
  userTag: "user/tag",
  tag: "tag",
  collection: "collection/",
  reader: "collection/reader/",
  userCollections: "user/collections",
  book: "book/",
  goal: "user/goal_achieved",
  search: "book/search",
  rating: "rate/",
  nameColor: "user/nameColor",
  review: "book/review/",
  comment: "collection/comment/",
  read: "collection/read/",
  isRead: "collection/isread/",
  recommend: "book/recommend",
}

Vue.prototype.post = function (url, payload, callback, option) {
  $axios.post(url, payload, option).then(
    res => {
      console.log(res)
      if (res.status === 200) {
        callback(res.data)
      }
    }
  ).catch((err)=>{
    console.log(err)
  })
}

Vue.prototype.put = function (url, payload, callback, option) {
  $axios.put(url, payload, option).then(
    res => {
      console.log(res)
      if (res.status === 200) {
        callback(res.data)
      }
    }
  ).catch((err)=>{
    console.log(err)
  })
}

Vue.prototype.get = function (url, params, callback) {
  $axios.get(url, params).then(
    res => {
      console.log(res)
      if (res.status === 200) {
        callback(res.data)
      }
    }
  ).catch((err)=>{
    console.log(err)
  })
}

Vue.prototype.delete = function (url, params, callback) {
  let data = {
    data: params
  }
  $axios.delete(url, data).then(
      res => {
        console.log(res)
        if (res.status === 200) {
          callback(res.data)
        }
      }
  ).catch((err)=>{
    console.log(err)
  })
}

Vue.config.productionTip = false

new Vue({
  vuetify,
  render: h => h(App),
  router
}).$mount('#app')
