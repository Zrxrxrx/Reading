<template>
  <div>
    Your Reading Progress {{ progressText }}
    <v-progress-linear :value="goalPercentage"></v-progress-linear>
    <div v-show="finish">
      You have finished your monthly goal on {{ finishDate }}
    </div>
  </div>
</template>

<script>
export default {
  name: "GoalBarComponent.vue",
  data() {
    return {
      haveRead: 0,
      goalSetting: 0,
      goalPercentage: 0,
      progressText: "(0/0)",
      finish: false,
      finishDate: "",
      finishTimeStamp: 0,
    }
  },
  computed: {
    calGoalPercentage() {
      return this.haveRead / this.goalSetting * 100
    },
    calProgressText() {
      return `(${this.haveRead}/${this.goalSetting})`
    },
    calFinishDate() {
      let date =  new Date(this.finishTimeStamp * 1000)
      return date.toLocaleDateString()
    },
  },
  methods: {
    getGoal() {
      this.get(this.$URL.goal, null, (response) => {
        if (response.success) {
          this.goalSetting = response.goal_target
          this.haveRead = response.goal_achieved
          this.goalPercentage = this.calGoalPercentage
          this.progressText = this.calProgressText
          this.finish = response.isFinish
          if (this.finish) {
            this.finishTimeStamp = response.date
            this.finishDate = this.calFinishDate
          }
        }
      })
    }
  },
  created() {
    this.getGoal()
  }

}
</script>

<style scoped>

</style>