<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <router-link :to="isLogin() ? '/dashboard' : '/'" class="text-decoration-none white--text">
          <h2>FocusReads</h2>
        </router-link>

    </div>
    <v-spacer></v-spacer>
<v-container v-if="isLogin() === true">
            <v-row justify="center">
                <v-col cols="3">
                    <v-text-field
                        label="Search"
                        prepend-inner-icon="mdi-magnify"
                        style="max-height: 36px"
                        @keyup.enter="globalSearch"
                        @change="searchInput = $event"
                    ></v-text-field>
                </v-col>
            </v-row>
        </v-container>
      <v-spacer></v-spacer>
      <v-btn v-show="isAdmin()" color="error" to="/admin/books" class="ml-1">Admin</v-btn>

      <v-btn v-show="isLogin()" to="/profile" class="ml-1">Profile</v-btn>

      <v-btn
        v-if="isLogin() === true"
        color="primary"
        elevation="6"
        plain
        outlined
        @click="logout" class="ml-1"
      >
        <span class="mr-2 white--text">Logout</span>
      </v-btn>
      <v-btn v-else color="primary" elevation="6" plain outlined to="/login">
        <span class="mr-2 white--text">Login</span>
    </v-btn>

        
    </v-app-bar>

    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "App",

  components: {},

  data: () => ({
      //
      user : "NULL",
      searchInput: "",
  }),

  methods: {
    // TODO: replace all alert() to vuetify things
    isLogin() {
      return localStorage.getItem("token") != null;
    },
    isAdmin() {
        if (localStorage.getItem("token")) {
            return JSON.parse(atob(localStorage.getItem("token").split(".")[1]))["isAdmin"]
        }
    },
    logout() {
      console.log("logout()");
      localStorage.removeItem("token");
      alert("logout success");
      this.$router.push("/");
    },
    globalSearch(){
        console.log(this.searchInput)
        this.$router.push("/search/" + this.searchInput)
    }
  },
};
</script>
