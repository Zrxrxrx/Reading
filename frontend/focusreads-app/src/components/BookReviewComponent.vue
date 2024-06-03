<template>
  <div>
    <v-card class="ma-1">
      <v-card-title>Review</v-card-title>
      <v-card-text v-if="userReview.length===0">
        Write a review for this book.
        <v-textarea v-model="reviewContent"></v-textarea>
        <v-btn @click="submit">Submit</v-btn>
      </v-card-text>
    </v-card>
    <v-card v-for="review in reviews" :key="review.id" class="ma-1">
        <v-card-subtitle>
            <v-row class="pa-3">
                <i style="font-style: normal;" :class="[`${review.user.nameColor}--text`]">{{ review.user.username }}</i>
                <v-spacer></v-spacer>
                <v-btn v-if="review.user.id === uid" @click="toggleEdit(review.id, review.content)" class="mx-1">Edit</v-btn>
                <v-btn v-if="review.user.id === uid || isAdmin === true" @click="deleteReview(review.id)" color="red">Delete</v-btn>
            </v-row>
      <v-rating v-show="review.rating" :value="review.rating" color="orange" size="18" dense readonly></v-rating>
      </v-card-subtitle>
      <v-card-text>
          <p v-if="!editReview.includes(review.id)">
              {{ review.content }}
          </p>
          <v-textarea v-if="editReview.includes(review.id)" :value="review.content" v-model="editedReview"></v-textarea>
          <v-btn v-if="editReview.includes(review.id)" @click="submitEdit(review.id)">Submit</v-btn>
      </v-card-text>
      <v-card-text>
        Created at {{ dateTime(review.created_at) }}
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  name: "BookReviewComponent",
  data() {
    return {
      reviews: [
        // {
        //   id: 1,
        //   content: "This is a review content",
        //   username: "user",
        //   created_at: 1650266949
        // }
      ],
      reviewContent: "",
      userReview: [],
      editReview: [],
      editedReview: '',
      uid: this.getUserId(),
      isAdmin: this.getIsAdmin(),
    }
  },
  methods: {
      getEditReview(reviewId) {
          return this.editReview[reviewId]
      },
      toggleEdit(reviewId, editedReview="") {
          if (this.editReview.includes(reviewId)) {
              this.editReview.pop(reviewId)
          } else {
              this.editReview.push(reviewId)
              this.editedReview = editedReview
          }
      },
      getUserId() {
          return JSON.parse(atob(localStorage.getItem('token').split(".")[1]))["uid"]
      },
      getIsAdmin() {
          return JSON.parse(atob(localStorage.getItem('token').split(".")[1]))["isAdmin"]
      },
      submitEdit(reviewId) {
          this.put(this.$URL.review, {
              content: this.editedReview,
              bid: this.bid,
              rid: reviewId,
          }, (res) => {
              if (res.success) {
                  alert("Successfully edited review")
                  this.$router.go()
              } else {
                  window.alert(res.message);
              }
          });
      },
      deleteReview(reviewId) {
          if (confirm("Are you sure you want to delete your review?")) {
            this.delete(this.$URL.review + reviewId, {params: {rid: reviewId}}, (res) => {
                  if (res.success) {
                      alert("Successfully deleted review.")
                      this.$router.go();
                  } else {
                      alert(res.message)
                  }
            });
          }
      },
    getReviews() {
      this.get(this.$URL.review, {params: {bid: this.bid}}, (res) => {
        if (res.success) {
            this.reviews = res.reviews;
//            for (let review of res.reviews) {
//            this.editReview[review.id] = false;
//          }
        }
      });
    },
    submit() {
      this.post(this.$URL.review, {
        content: this.reviewContent,
        bid: this.bid
      }, (res) => {
        if (res.success) {
          this.reviews.unshift(res.review);
          this.reviewContent = "";
        } else {
          window.alert(res.message);
        }
      });
    },
    dateTime(timestamp) {
      return new Date(timestamp * 1000).toLocaleString();
    },
    haveReview() {
      const r = this.reviews.filter((review) => {
        return review.user.id == JSON.parse(atob(localStorage.getItem("token").split(".")[1]))["uid"]
      });
      this.userReview = r;
      console.log(this.userReview)
    }

  },
  created() {
    this.getReviews();
  },
  watch: {
    reviews() {
      this.haveReview();
    }
  },
  props: ["bid"]
}
</script>

<style scoped>

</style>