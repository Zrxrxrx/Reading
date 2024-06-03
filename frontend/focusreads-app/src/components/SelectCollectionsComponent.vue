<template>
  <v-select
      v-model="selected"
      :items="collections"
      item-text="name"
      item-value="id"
      chips
      :label="labelName"
      multiple
  >
      <template slot="no-data">
          <p class="text-body1" style="margin: 10px;">
              There are no collections available at this time.
          </p>
  </template></v-select>
</template>
<script>
export default {
  name: 'SelectCollectionsComponent',
  props: ['bid', 'labelName'],
  data() {
    return {
      collections: [],
      selected: [],
    }
  },
  created() {
    this.get_collections()
  },
  methods: {
    get_collections() {
      this.get(this.$URL.userCollections, null, (res) => {
        if (res.success) {
          this.collections = res.collections
          this.check_collections()
          this.hide_read()
        }
      })
    },
    check_collections() {
      this.collections.forEach(c => {
        c.books.forEach(b => {
          if (b.id == this.$props.bid) {
            this.selected.push(c.id)
          }
        })
      })
      this.watchHook = true
    },
    add_book_to_collection(cid) {
      const body = {
        bid: this.$props.bid,
        cid: cid
      }
      this.post(this.$URL.collection + '/add_book', body, (res) => {
        if (res.success) {
          console.log('add to collection success')
        }
      })
    },
    delete_book_from_collection(cid) {
      const body = {
        bid: this.$props.bid,
        cid: cid
      }
      this.delete(this.$URL.collection + '/delete_book', body, (res) => {
        if (res.success) {
          console.log('delete to collection success')
        }
      })
    },
    hide_read() {
      this.collections = this.collections.filter(c => {
        return c.isRead === false
      })
    }
  },
  watch: {
    selected: function (newArr, oldArr) {
      if (newArr.length > oldArr.length) {
        const diff = newArr.filter(x => !oldArr.includes(x))[0]
        console.log('add collection ' + diff)
        this.add_book_to_collection(diff)
      } else if (newArr.length < oldArr.length) {
        const diff = oldArr.filter(x => !newArr.includes(x))[0]
        console.log('del collection ' + diff)
        this.delete_book_from_collection(diff)
      }
    }
  }
}
</script>