<template>
    <div class="text-center">
      <v-dialog
          v-model="isPopup"
          width="500"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn
              color="primary"
              dark
              v-bind="attrs"
              v-on="on"
          >
            Have Read?
          </v-btn>
        </template>

        <v-card>
          <v-card-title
              class="headline grey lighten-2"
              primary-title
          >
            Rating Book
          </v-card-title>

          <v-card-text>
            How do you rate this book?
          </v-card-text>

          <div class="text-center">
            <v-rating v-model="rating"></v-rating>
          </div>

          <v-divider></v-divider>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
                color="primary"
                text
                @click="isPopup = false"
            >
              Close
            </v-btn>
            <v-btn
                color="primary"
                text
                @click="rate"
            >
              Submit
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
</template>

<script>
export default {
  name: "RateDialogComponent",
  data() {
    return {
      isPopup: false,
      rating: 0
    };
  },
  methods: {
    rate() {
      if (this.rating <= 0) {
        window.alert("Please rate this book");
        return;
      }
      let body = {
        bid: this.$props.bid,
        rating: this.rating
      };
      this.post(this.$URL.rating, body, (res) => {
        if (res.success) {
          this.add_read();
        } else {
          window.alert(res.message);
        }
      })
    },
    add_read() {
      console.log(this.bid)
      this.post(this.$URL.read, { bid: this.$props.bid }, (res) => {
        if (res.success) {
          this.isPopup = false;
          this.$emit("refresh");
        } else {
          window.alert(res.message);
        }
      })
    }
  },
  props: ["bid"]
}
</script>

<style scoped>

</style>