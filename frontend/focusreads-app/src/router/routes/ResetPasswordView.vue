<template>
  <v-main>
    <title>FocusReads - Reset Password</title>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card class="elevation-12">
            <v-toolbar dark color="primary">
              <v-toolbar-title>Reset Password</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-form>
                <v-text-field
                  name="email"
                  label="Email"
                  type="email"
                  v-model="email"
                ></v-text-field>
                <v-btn @click="sendEmail">Send Email</v-btn>
                <p v-show="isSent">Email Sent</p>
                <v-otp-input tpye="number" v-model="code">Code</v-otp-input>
                <v-text-field
                  id="password"
                  name="password"
                  label="Password"
                  type="password"
                  v-model="password"
                ></v-text-field>
                <v-text-field
                  label="Confirm Password"
                  type="password"
                  v-model="confirmPassword"
                ></v-text-field>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" @click="reset">Submit</v-btn>
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
      confirmPassword: "",
      code: "",
      isSent: false,
    };
  },
  created() {
    console.log("resetPassword page created");
  },
  methods: {
    // TODO: replace all alert() to vuetify things

    sendEmail() {
      // send request to send OTP email
      if (!this.email) {
        window.alert("email is empty");
        return;
      }

      this.isSent = true;
    },

    reset() {
      // hard coding for skipping email verification
      // send reset password request to backend after data validation
      if (!this.isSent) {
        window.alert("Please send the email code")
        return;
      }

      if (this.code !== "123456") {
        window.alert("code is incorrect");
        return;
      }

      if (!this.password) {
        window.alert("password is empty");
        return;
      }

      if (this.password !== this.confirmPassword) {
        window.alert("Confirm Password is not same");
        return;
      }

      let body = {
        email: this.email,
        password: this.password,
        code: this.code,
      };

      this.post(this.$URL.resetPassword, body, (res) => {
        if (res.success) {
          window.alert('Reset Password successfully');
          this.$router.push("/");
        } else {
          window.alert(res.message);
        }
      });
    },
  },
};
</script>