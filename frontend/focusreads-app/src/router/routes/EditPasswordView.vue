<template>
  <v-main>
    <title>FocusReads - Edit Password</title>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card class="elevation-12">
            <v-toolbar dark color="primary">
              <v-toolbar-title>Edit Password</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-form>
                <v-text-field
                  label="Old Password"
                  type="password"
                  v-model="oldPassword"
                ></v-text-field>
                <v-text-field
                  label="New Password"
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
              <v-btn color="primary" @click="editPass">Submit</v-btn>
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
      oldPassword: "",
      password: "",
      confirmPassword: "",
    };
  },
  created() {
    console.log("Edit Password page created");
  },
  methods: {
    // TODO: replace all alert() to vuetify things

    editPass() {
      // send editing password request to server
      if (!this.oldPassword) {
        window.alert("old password is empty");
        return;
      }

      if (!this.password) {
        window.alert("new password is empty");
        return;
      }

      if (this.oldPassword === this.password) {
        window.alert("New password should not same as old");
        return;
      }

      if (this.password !== this.confirmPassword) {
        window.alert("Confirm Password is not same");
        return;
      }

      let body = {
        password: this.password,
      };

      this.post(this.$URL.editPassword, body, (res) => {
        if (res.success) {
          window.alert("Edit Password successfully");
          this.$router.push("/profile");
        } else {
          window.alert(res.message);
        }
      });
    },
  },
};
</script>