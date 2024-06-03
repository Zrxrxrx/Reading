<template>
  <v-main>
    <title>FocusReads - Register</title>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card class="elevation-12">
            <v-toolbar dark color="primary">
              <v-toolbar-title>Registration form</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              If you already have an account, you can login
              <router-link to="/login">here</router-link>!
              <v-form>
                <v-text-field
                  name="name"
                  label="Name"
                  type="text"
                  v-model="name"
                  @keyup.enter="register"
                ></v-text-field>
                <v-text-field
                  name="email"
                  label="Email"
                  type="email"
                  v-model="email"
                  @keyup.enter="register"
                ></v-text-field>
                <v-text-field
                  id="password"
                  name="password"
                  label="Password"
                  type="password"
                  v-model="password"
                  @keyup.enter="register"
                ></v-text-field>
                <v-text-field
                  id="confirmPassword"
                  name="confirmPassword"
                  label="Confirm Password"
                  type="password"
                  v-model="confirmpassword"
                  @keyup.enter="register"
                ></v-text-field>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" @click="register">Register</v-btn>
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
      name: "",
      email: "",
      password: "",
      confirmpassword: ""
    };
  },
  created() {
    console.log("register page created");
  },
  methods: {
      register() {
          // TODO: should replace all alert()
          // basic form validation
          if (this.name === '') {
            window.alert('username is empty')
            return
          }
          
          if (this.password === '') {
            window.alert('password is empty')
            return
          }
          
          if (this.password !== this.confirmpassword) {
            window.alert('Confirm Password is not same')
            return
          }

          // send registration data to the backend
          this.post(this.$URL.register, {"username": this.name, "password": this.password, "email": this.email}, res=>{
            if (res.success) {
              console.log('register success')
              this.$router.push('/login')
            } else {
              window.alert(res.message)
            }
          })
      }
  }
}
</script>