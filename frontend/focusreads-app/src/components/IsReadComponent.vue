<template>
  <div>
    <v-card class="pa-3" v-if="!read">
      <RateDialogComponent @refresh="getIsRead" :bid="bid"/>
    </v-card>

    <v-card class="pa-3" v-else>
      <div>
        You have read this book.
        <v-rating :value="rating" readonly></v-rating>
        <v-btn @click="unRead" color="primary">Mark Unread</v-btn>
      </div>
    </v-card>

  </div>
</template>

<script>
import RateDialogComponent from "@/components/RateDialogComponent";

export default {
  name: "isReadComponent.vue",
  components: {RateDialogComponent},

  props: ['bid'],
  data() {
    return {
      read: true,
      rating: 0,
    }
  },
  methods: {
    getIsRead() {
      this.get(this.$URL.isRead, {params: {bid: this.bid}}, (res) => {
        if (res.success) {
          this.read = res.read;
          this.rating = res.rating;
          this.$emit('refreshRating');
        }
      });
    },
    unRead() {
      this.delete(this.$URL.read, {bid: this.bid}, (res) => {
        if (res.success) {
          this.read = false;
          this.rating = 0;
          this.$emit('refreshRating')
        }
      });
    }
  },
  created() {
    this.getIsRead();
  },
}
</script>

<style scoped>

</style>