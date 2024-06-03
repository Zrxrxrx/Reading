<template>
  <div>
    <title>FocusReads - Profile</title>
    <v-container>
      <h1>Profile</h1>
      <span>
        <h2 :class="[`${ user.nameColor }--text`]">{{ user.name }}</h2>
        <p>(uid: {{ user.id }})</p>
        <p>Register Date: {{ getDate }}</p>
        <p>Book of age: {{ getBookofAge }}</p>
      </span>
      <v-avatar class="white--text ma-5" color="primary" rounded size="80"
        > {{ user.isAdmin === true ? "Admin" : "User" }} </v-avatar
      >
      <v-btn class="ma-5" to="/editPassword">Edit Password</v-btn>
      <v-btn @click="isEdit = !isEdit">Edit</v-btn>
      <v-row v-if="isEdit === true">
          <v-col cols="6">
              <v-select
                  :items="nameColors"
                  label="Name Color"
                  @change="nameColor = $event"
                  dense
              ></v-select>
          </v-col>
          <v-col cols="6">
              <v-btn @click="updateNameColor()" v-if="isEdit === true">Change Name Color</v-btn>
          </v-col>
      </v-row>
      <div>
        Age
        <v-text-field :disabled="!isEdit" v-model="user.age">{{ user.age }}</v-text-field>
      </div>
      <div>
        Monthly Goal
        <v-text-field :disabled="!isEdit" v-model="user.goal">{{
          user.goal
        }}</v-text-field>
      </div>
      <div>
        About Me
        <v-textarea :disabled="!isEdit" v-model="user.aboutMe">{{
          user.aboutMe
        }}</v-textarea>
      </div>
      <div>
        Photo URL
        <v-text-field disabled v-model="user.picURL">{{ user.picURL }}</v-text-field>
      </div>
      <v-btn v-show="isEdit" @click="updateProfile">Submit</v-btn>
      <div>
        Your Perference Tags
        <v-btn
          class="ma-5"
          color="primary"
          outlined
          @click="isAddTag = !isAddTag"
        >
          +
        </v-btn>
        <div v-show="isAddTag">
          <v-text-field label="Tag name" v-model="newTagName"></v-text-field>
          <v-btn color="green" outlined @click="addTag">Accept</v-btn>
        </div>
      </div>
      <span v-for="tag in user.tag" :key="tag">
        <v-btn class="ma-5" color="primary" dark>
          <!-- {{ getTag(tag) }} -->
          {{ tag }}
        </v-btn>
      </span>
    </v-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isEdit: false,
      isAddTag: false,
      user: {},
      aboutMe: undefined,
      age: undefined,
      goal: undefined,
      picURL: undefined,
      newTagName: "",
      tagList: [],
      nameColor: '#000',
      nameColors: [
          "blue",
          "green",
          "orange",
          "yellow",
          "pink",
          "black",
          "purple",
          "brown"
      ],
    };
  },
  created() {
      this.getProfile();
      this.getNameColors();
  },
  methods: {
    getProfile() {
      this.get(this.$URL.profile, null, (res) => {
        this.user = res
      });
    },

    getNameColors() {
      this.get(this.$URL.nameColor, null, (res) => {
        this.nameColors = res['colors']
      });
    },

    updateProfile() {
      let body = {
        age: this.user.age,
        goal: this.user.goal,
        picURL: this.user.picURL,
        aboutMe: this.user.aboutMe,
      };

      this.put(this.$URL.profile, body, (res) => {
        if (res.success) {
          console.log("updated profile successfully");
          this.$router.go("/profile");
        }
      });
    },

    updateNameColor() {
      let body = {
        nameColor: this.nameColor.split("(")[0].replaceAll(" ", ''),
      };

      this.post(this.$URL.nameColor, body, (res) => {
          if (res.success) {
              alert("Successfully changed name color!")
              localStorage.removeItem("token")
              console.log("updated name color successfully");
              this.$router.go("/profile");
        }
      });
    },

    // toDate(timestamp) {
    //   return 
    // },

    // getTag(tagId) {
    //   this.get(this.$URL.tag + "?id=" + tagId, null, (res) => {
    //     if (res.success) {
    //       return res["name"];
    //     }
    //   });
    //   return "";
    // },

    addTag() {
      // add tag to user
      let body = {
        name: this.newTagName,
      };
      this.post(this.$URL.userTag, body, (res) => {
        if (res.success) {
          this.user.tag.push(this.newTagName)
          this.newTagName = "";
        }
      });
    },
  },
  computed: {
    // convert timestamp to date
    getDate: function fun1() {
      if (this.user && this.user.registerDate) {
        return new Date(this.user.registerDate * 1000).toLocaleString()
      } else {
        return ""
      }
    }, 

    // convert timestamp to date stirng
    getBookofAge: function fun2() {
      if (this.user && this.user.registerDate) {
        let now = new Date()
        let register_date = new Date(this.user.registerDate * 1000)
        let diff_seconds = now - register_date
        let day = diff_seconds / 1000 / 360 / 24
        return day.toFixed(3) + ' days'
      } else {
        return ""
      }
    }
  }
};
</script>