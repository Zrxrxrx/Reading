<template>
    <div>
        <title>FocusReads - Home</title>
        <p>You logged in as <i style="font-style: normal;" :class="[`${nameColor}--text`]">{{username}}</i></p>
        <GoalBar />
        <v-btn to="/user/collection">My collections</v-btn>
        <v-btn to="/ranking">Ranking List</v-btn>
        <v-card>
            <v-card-title>
                Recommended Books!
                <v-spacer></v-spacer>
                <v-text-field
                    v-model="search"
                    append-icon="mdi-magnify"
                    label="Filter"
                    single-line
                    hide-details
                ></v-text-field>
            </v-card-title>
            <v-data-table
                :headers="headers"
                :items="books"
                :search="search"
            >
                <template v-slot:[`item.view`]="{ item }">
                    <v-btn
                        color="primary"
                        elevation="2"
                        outlined
                        :to="viewBook(item.id)"
                    >
                        View Book
                    </v-btn>
                </template>
            </v-data-table>
        </v-card>
    </div>
</template>

<script>
    import GoalBarComponent from "@/components/GoalBarComponent";

    export default {
     components: {GoalBar: GoalBarComponent},
      data(){
            return {
                username: this.getUserName(),
                nameColor: this.getNameColor(),
                search: '', // required for frontend filtering
                // template for table data
                headers: [
                    { text: 'Title', value: 'name' },
                    { text: 'Author', value: 'author' },
                    { text: 'Date of Publication', value: 'dop' },
                    { text: 'View Book', value: 'view', sortable: false, filterable: false },
                ],
                books: [],
            }
        },
        created() {
            // get a list of books from the backend
            this.get(this.$URL.recommend, {}, (res) => {
                if (res.success) {
                    this.books = res['books']
                } else {
                    window.alert("Failed to fetch list of books: " + res.message);
                }
            });
            console.log('Dashboard Page')
        },
        methods: {
            // parses the token to extract the username
            getUserName() {
                return JSON.parse(atob(localStorage.getItem('token').split(".")[1]))["username"]
            },
            // parses the token to extract the username
            getNameColor() {
                return JSON.parse(atob(localStorage.getItem('token').split(".")[1]))["nameColor"]
            },
            // returns a link to navigate to a book
            viewBook (bid) {
                return `/book/${bid}`
            },
        }
    }
</script>