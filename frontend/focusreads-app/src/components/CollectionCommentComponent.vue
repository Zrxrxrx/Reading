<template>
  <div>
    <v-card class="ma-1">
      <v-card-title>Comment</v-card-title>
      <v-card-text>
        Write a comment for this collection.
        <v-textarea counter v-model="commentContent"></v-textarea>
        <v-btn @click="submit">Submit</v-btn>
      </v-card-text>
    </v-card>
    <v-card v-for="comment in comments" :key="comment.id" class="ma-1">
        <v-card-subtitle >
            <v-row class="pa-3">
                <i style="font-style: normal;" :class="[`${comment.user.nameColor}--text`]">
                    {{ comment.username }}
                </i>
                <v-spacer></v-spacer>
                <v-btn v-if="comment.user.id === uid || isAdmin === true" @click="deleteComment(comment.id)" color="red">Delete</v-btn>
            </v-row>
      </v-card-subtitle>
      <v-card-text>
        {{ comment.content }}
      </v-card-text>
      <v-card-text>
        Created at {{ dateTime(comment.created_at) }}
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  name: "CollectionCommentComponent",
  props: ["cid"],
  data() {
    return {
      comments: [
        // {
        //   id: 1,
        //   content: "This is a comment content",
        //   username: "user",
        //   created_at: 1650266949
        // }
      ],
      commentContent: "",
      uid: this.getUserId(),
      isAdmin: this.getIsAdmin(),
    }
  },
  mounted() {
    this.getComments();
  },
  methods: {
      getUserId() {
          return JSON.parse(atob(localStorage.getItem('token').split(".")[1]))["uid"]
      },
      getIsAdmin() {
          return JSON.parse(atob(localStorage.getItem('token').split(".")[1]))["isAdmin"]
      },
      deleteComment(cid) {
          this.delete(this.$URL.comment + cid, {params: {cid: this.cid}}, (res) => {
              if (res.success) {
                  alert("Successfully deleted comment.")
                  this.$router.go();
              } else {
                  alert(res.message)
              }
          });
      },
    getComments() {
      // helper function to sort comments by created_at
      function sortByCreatedAt(a, b) {
        console.log(a.created_at, b.created_at);
        return b.created_at - a.created_at
      }
      this.get(this.$URL.comment, {params: {cid: this.cid}}, (res) => {
        if (res.success) {
          this.comments = res.comments;
          this.comments.sort(sortByCreatedAt);
        }
      });

    },
    submit() {
      if (this.contentValid() === false) {
        return;
      }

      this.post(this.$URL.comment, {
        content: this.commentContent,
        cid: this.cid
      }, (res) => {
        if (res.success) {
          let newComment = {
            id: res.comment.id,
            content: res.comment.content,
            username: res.comment.username,
            created_at: res.comment.created_at,
            user: {
                id: this.uid,
                isAdmin: this.isAdmin,
                nameColor: JSON.parse(atob(localStorage.getItem('token').split(".")[1]))["nameColor"],
            },
          }
          this.comments.unshift(newComment);
          this.commentContent = "";
        }
      });
    },
    dateTime(timestamp) {
      return new Date(timestamp * 1000).toLocaleString();
    },
    contentValid() {
      if (this.commentContent.length < 5) {
        window.alert("Comment content is too short");
        return false;
      }
      const strList = this.commentContent.split(" ");
      if (strList.length > 200) {
        window.alert("Comment content is too long, should be less than 200 words");
        return false;
      }
      return true;
    }
  },

}
</script>

<style scoped>
</style>