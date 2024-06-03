<template>
  <v-main>
    <!-- Based on https://codesandbox.io/s/0q4kvj8n0l?file=/src/components/Login.vue -->
    <title>FocusReads - Login</title>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-alert v-if="$route.query.type" :type="$route.query.type">
            {{ $route.query.msg }}
          </v-alert>
          <v-card class="elevation-12">
            <v-toolbar dark color="primary">
              <v-toolbar-title>Login form</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              If you don't have an account, you can register for one
              <router-link to="/register">here</router-link>!
              <v-form>
                <v-text-field
                  name="email"
                  label="Email"
                  type="email"
                  v-model="email"
                  @keyup.enter="login"
                ></v-text-field>
                <v-text-field
                  id="password"
                  name="password"
                  label="Password"
                  type="password"
                  v-model="password"
                  @keyup.enter="login"
                ></v-text-field>
              </v-form>
              Forget your password? You can reset it
              <router-link to="/resetpassword">here</router-link>!
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" @click="login">Login</v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-main>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      password: "",
    };
  },
  created() {
    console.log("login page created");
  },
  methods: {
    // TODO: replace all alert()
    login() {
        // basic form validation
      if (!this.email) {
        window.alert('email is empty')
        return
      }
      
      if (!this.password) {
        window.alert('password is empty')
        return
      }
    
      // construct the request data
      let body = {
        email: this.email,
        password: this.password,
      };

      // send login request to backend
      this.post(this.$URL.login, body, (res) => {
        // if successful, send user to dashboard after storing login token in localStorage
        if (res.success) {
          localStorage.setItem("token", res.token);
          this.$router.push("/dashboard");
        } else {
          window.alert(res.message);
        }
      });
    },
  },
};
</script>
