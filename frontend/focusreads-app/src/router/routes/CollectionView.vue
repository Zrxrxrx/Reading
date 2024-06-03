<template>
    <div>
        <v-container>
            <div class="d-flex">
                <h2>{{ collection.name }}</h2>
                <v-spacer></v-spacer>
                <v-btn v-if="uid !== collection.owner.id && !collection.joined.map(u => u.id).includes(uid)" @click="join()">Join</v-btn>
                <v-btn v-if="uid !== collection.owner.id && collection.joined.map(u => u.id).includes(uid)" @click="leave()">Leave</v-btn>
                <template v-if="uid === collection.owner.id">
                    <v-dialog
                        v-model="dialog"
                        width="500"
                    >
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn v-bind="attrs" v-on="on">Members</v-btn>
                        </template>
                        <v-card>
                            <v-card-title class="text-h5 grey lighten-2">
                                Member List
                            </v-card-title>

                            <v-card-text class="pa-3">
                                <template v-if="collection.joined.length !== 0">
                                    <v-simple-table>
                                        <template v-slot:default>
                                            <thead>
                                                <tr>
                                                    <th class="tex">
                                                        User
                                                    </th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <tr
                                                    v-for="user in collection.joined"
                                                    :key="user.id"
                                                >
                                                    <td><i style="font-style: normal;" :class="[`${user.nameColor}--text`]">{{ user.username }}</i></td>
                                                </tr>
                                            </tbody>
                                        </template>
                                    </v-simple-table>
                                </template>
                                <p v-else class="h4-text">No users have joined this collection</p>
                            </v-card-text>
                            <v-divider></v-divider>

                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn
                                    color="primary"
                                    text
                                    @click="dialog = false"
                                >
                                    Close
                                </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                </template>

            </div>
            <div class="d-flex mt-3">
                <p v-if="collection.description !== '' && collection.description !== null">{{ collection.description }}</p>
                <v-spacer></v-spacer>
                <v-btn disabled>{{books.length}} {{books.length === 1 ? 'Book' : 'Books'}}</v-btn>
            </div>
            <div class="ma-3">
                <v-container no-gutters style="display: flex; flex-flow: row wrap; width: 100%;">
                    <v-card
                        class="pa-2"
                        elevation="2"
                        outlined
                        tile
                        v-for="b in books" :key="b.id"
                        style="flex: auto; align-self: flex-start; margin: 0 8px 8px 0; min-width: 20%;"
                    >
                        <v-img v-if="b.cover !== null && b.cover !== undefined"
                            :src="b.cover"
                            height=250
                            contain
                        ></v-img>
                        <v-col>
                            <router-link :to="book_url(b.id)">
                                <p class="text-h5">
                                    {{ b.name }}
                                </p>
                            </router-link>
                            <p class="text-body-1 grey--text">{{b.author}}</p>

                        </v-col>
                        <v-col v-if="uid === collection.owner.id">
                            <v-btn color="error" @click="delete_book(b.id)">Remove</v-btn>
                        </v-col>
                    </v-card>
                </v-container>
            </div>
            <CollectionCommentComponent v-if="collection.id && (uid === collection.owner.id || collection.joined.map(u => u.id).includes(uid))" :cid="collection.id" />
        </v-container>
    </div>
</template>

<script>
import CollectionCommentComponent from "@/components/CollectionCommentComponent";
export default {
    components: {CollectionCommentComponent},
    data() {
        return {
            collection: {
                'joined': [],
                'owner': {id: 1}
            },
            books: [],
            uid: this.getUserId(),
            dialog: false,
        }
    },
    // get the collection data on page load
    created() {
        this.get_collection()
    },
    props: ['id'],
    methods: {
        getUserId() {
            return JSON.parse(atob(localStorage.getItem('token').split(".")[1]))["uid"]
        },
        // fetch collection data from the backend
        get_collection() {
            this.get(this.$URL.collection + this.$props.id, null, res => {
                if (res.success) {
                    if ((res.collection.owner.id !== this.uid && res.collection.isPublic === false) && (JSON.parse(atob(localStorage.getItem('token').split(".")[1]))["isAdmin"] !== true)) {
                        this.$router.push({
                            path: '/login',
                            query: {
                                type: 'warning',
                                msg: 'You are not able to access that collection'
                            }
                        })
                    }
                    this.collection = res.collection
                    this.books = res.books
                }
            })
        },
        join() {
            this.post(this.$URL.reader + this.$props.id, null, res => {
                alert(res.message)
                if (res.success) this.$router.go()
            })
        },
        leave() {
            this.delete(this.$URL.reader + this.$props.id, null, res => {
                alert(res.message)
                if (res.success) this.$router.go()
            })
        },
        // generate a url for navigating to the books for the book links
        book_url(bid) {
            return '/book/' + bid
        },
        // remove a book from the collection
        delete_book(bid) {
            const body = {
                bid: bid,
                cid: this.$props.id
            }
            // requires user confirmation to prevent accidental deletion
            if (confirm("Are you sure you want to delete this book from collection?")) {
                this.delete(this.$URL.collection + '/delete_book', body, (res) => {
                    if (res.success) {
                        console.log('delete to collection success')
                        this.get_collection();
                    }
                })
            }
        },
    }
}
</script>