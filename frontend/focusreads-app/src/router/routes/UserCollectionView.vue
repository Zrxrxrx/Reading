<template>
  <div>
    <title>FocusReads - My collections</title>
    <v-container>
      <div class="d-flex">
        <h2 v-if="collections.length !== 0">My Collections</h2>
        <v-spacer></v-spacer>
        <v-dialog
            v-model="newDialog"
            width="400"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-btn
                color="primary"
                v-bind="attrs"
                v-on="on"
                class="ma-3"
            >
              Add Collection
            </v-btn>
          </template>

          <v-card>
            <v-card-title class="text-h5 grey lighten-2">
              New Collection
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-col>
                  <v-text-field
                      label="Name"
                      required
                      v-model="newCollectionName"
                  ></v-text-field>
                </v-col>
                <v-col>
                  <v-textarea
                      label="Description"
                      required
                      v-model="newCollectionDesc"
                  ></v-textarea>
                </v-col>
                <v-col>
                  <v-switch
                      v-model="newCollectionPublic" label="Public"
                  >
                  </v-switch>
                </v-col>
              </v-container>
            </v-card-text>

            <v-divider></v-divider>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                  color="primary"
                  text
                  @click="newDialog = false"
              >
                Close
              </v-btn>
              <v-btn
                  color="primary"
                  text
                  @click="add_collection"
              >
                Add
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog
            v-model="editDialog"
            width="400"
        >
          <v-card>
            <v-card-title class="text-h5 grey lighten-2">
              Edit Collection
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-col>
                  <v-text-field
                      label="Name"
                      required
                      v-model="editItem.name"
                  >
                  </v-text-field>
                </v-col>
                <v-col>
                  <v-textarea
                      label="Description"
                      required
                      v-model="editItem.description"
                  ></v-textarea>
                </v-col>
                <v-col>
                  <v-switch
                      v-model="editItem.isPublic" label="Public"
                  >
                  </v-switch>
                </v-col>
                <v-col>
                  <v-btn v-show="editItem.deleteable" color="error" @click="doDelete">Delete</v-btn>
                </v-col>
              </v-container>
            </v-card-text>

            <v-divider></v-divider>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                  color="primary"
                  text
                  @click="editDialog = false"
              >
                Close
              </v-btn>
              <v-btn
                  color="primary"
                  text
                  @click="doEdit"
              >
                Submit
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </div>
      <v-col v-for="collection in collections" :key="collection.id">
          <v-card elevation="2" class="pa-2">
              <div class="d-flex">
                  <router-link :to="collection_url(collection.id)">
                      <p class="text-h6">{{collection.name}}</p>
                  </router-link>
                  <v-spacer></v-spacer>
                  <v-avatar
                      :color="(collection.isPublic ? 'green' : 'red') + ' lighten-2'"
                      rounded
                      max-height="35"
                      width="80"
                      class="mr-5"
                  >
                      {{ collection.isPublic ? 'Public' : 'Private'}}
                  </v-avatar>
                  <v-btn
                      @click="editEvent(collection)"
                  >
                      Edit
                  </v-btn>
              </div>
              <div>
                  <p v-if="collection.description !== '' && collection.description !== null" class="mb-1"><b>Description:</b> {{collection.description}}</p>
                  <p v-if="collection.books.length > 0" class="mb-1"><b>Books:</b> {{collection.books.length}} {{collection.books.length === 1 ? 'Book' : 'Books'}}</p>
                  <p v-else class="mb-1"><b>Books: Empty</b></p>
              </div>
          </v-card>
      </v-col>
      <v-spacer class="my-6"></v-spacer>
      <h3 v-if="joined.length !== 0">Joined Collections</h3>
      <v-col v-for="collection in joined" :key="collection.id">
          <v-card elevation="2" class="pa-2">
              <div class="d-flex">
                  <router-link :to="collection_url(collection.id)">
                      <p class="text-h6">{{collection.name}}</p>
                  </router-link>
                  <v-spacer></v-spacer>
                  <v-avatar
                      :color="(collection.isPublic ? 'green' : 'red') + ' lighten-2'"
                      rounded
                      max-height="35"
                      width="80"
                      class="mr-5"
                  >
                      {{ collection.isPublic ? 'Public' : 'Private'}}
                  </v-avatar>
              </div>
              <div>
                  <p v-if="collection.description !== '' && collection.description !== null" class="mb-1"><b>Description:</b> {{collection.description}}</p>
                  <p v-if="collection.books.length > 0" class="mb-1"><b>Books:</b> {{collection.books.length}} {{collection.books.length === 1 ? 'Book' : 'Books'}}</p>
                  <p v-else class="mb-1"><b>Books: Empty</b></p>
              </div>
          </v-card>
        </v-col>
    </v-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      newCollectionName: '',
      newCollectionDesc: '',
      newCollectionPublic: false,
      collections: [],
      joined: [],
      newDialog: false,
      editDialog: false,
      editItem: {},
    }
  },
  methods: {
      getUserId() {
        // Get the user id from token
          return JSON.parse(atob(localStorage.getItem('token').split(".")[1]))["uid"]
      },
      // create new collection
      add_collection() {
      // construct the request
      let body = {
        name: this.newCollectionName,
        description: this.newCollectionDesc,
        isPublic: this.newCollectionPublic,
      }
      // send the new collection data to the backend
      this.post(this.$URL.collection, body, (res) => {
        if (res.success) {
          this.newDialog = false
          this.list_collection()
          this.newCollectionDesc = this.newCollectionName = ''
        } else {
          window.alert(res.message);
        }
      })
      },
    // get the user's collections from the backend
    list_collection() {
      this.get(this.$URL.userCollections, null, (res) => {
        if (res.success) {
            this.collections = res.collections
            this.joined = res.joined.filter(collection => collection.isPublic === true)
        }
      })
    },
    // generate a url for a specified collection
    collection_url(id) {
      return '/collection/' + id;
    },
    // show edit collection modal
    editEvent(item) {
      this.editDialog = true;
      this.editItem = JSON.parse(JSON.stringify(item))
    },
    // edit collection data
    doEdit() {
      // construct the request
      let body = {
        cid: this.editItem.id,
        name: this.editItem.name,
        description: this.editItem.description,
        isPublic: this.editItem.isPublic
      }
      // send the data to the backend
      this.put(this.$URL.collection, body, (res) => {
        if (res.success) {
          this.editDialog = false
          this.list_collection()
          this.editItem = {}
        } else {
          window.alert(res.message);
        }
      })
    },
    // delete a collection
    doDelete() {
      let args = {
        cid: this.editItem.id,
      }
      this.delete(this.$URL.collection, args, (res) => {
        if (res.success) {
          this.editDialog = false
          this.list_collection()
          this.editItem = {}
        } else {
          window.alert(res.message);
        }
      })
    },

  },
  created() {
    // fetch collection data on page load
    this.list_collection();
  }
}
</script>