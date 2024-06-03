<template>
    <div>
        <title>FocusReads - Ranking List</title>
        <v-container class="ma-1">
            <p class="text-h3">Top Book!</p>
        </v-container>
        <v-row>
            <v-col style="padding: 10px;" v-if="top_book.cover !== null" align="center">
                <v-container>
                    <v-img :src="top_book.cover" height="250" contain></v-img>
                </v-container>
            </v-col>
            <v-col style="padding: 10px;" align="center">
                <v-container>
                    <p class="text-h5">{{ top_book.name }}</p>
                    <p class="text-subtitle2">{{ top_book.author }}</p>
                    <p class="text-caption">{{ top_book.introduce }}</p>
                    <v-rating
                        color="warning"
                        dense
                        half-increments
                        length=5
                        readonly
                        size=25
                        :value="top_book.avg_rating"
                        class="my-3"
                    ></v-rating>
                    <v-btn color="primary" elevation="2" outlined :to="viewBook(top_book.id)">See More</v-btn>
                    <v-spacer></v-spacer>
                    <v-chip
                        class="ma-2"
                        color="primary"
                        v-for="category in top_book.categories.split(';')" :key="category"
                    >
                        {{ category }}
                    </v-chip>
                </v-container>
            </v-col>
        </v-row>
        <hr class="my-2">
        <v-row>
            <v-col>
                <v-card>
                    <v-card-title>
                        New Books
                        <v-spacer></v-spacer>
                        <v-text-field
                            v-model="new_search"
                            append-icon="mdi-magnify"
                            label="Filter"
                            single-line
                            hide-details
                        ></v-text-field>
                    </v-card-title>
                    <v-data-table
                        :headers="new_headers"
                        :items="new_books"
                        :search="new_search"
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
                        <!--
                        <template v-slot:[`item.add`]="{ item }">
                            <v-btn
                                color="primary"
                                elevation="2"
                                outlined
                                :to="viewBook(item.id)"
                            >
                                Add Book
                            </v-btn>
                        </template>
                        -->
                    </v-data-table>
                </v-card>
            </v-col>
            <v-col>
                <v-card>
                    <v-card-title>
                        Top Books
                        <v-spacer></v-spacer>
                        <v-text-field
                            v-model="top_search"
                            append-icon="mdi-magnify"
                            label="Filter"
                            single-line
                            hide-details
                        ></v-text-field>
                    </v-card-title>
                    <v-data-table
                        :headers="top_headers"
                        :items="books"
                        :search="top_search"
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
                        <template v-slot:[`item.avg_rating`]="{ item }">
                            <v-tooltip left>
                                <template v-slot:activator="{ on, attrs }">
                                    <v-container v-bind="attrs" v-on="on" style="margin-left: -3px; margin-top: -1em; margin-bottom: -1em;">
                                        <v-rating
                                            dense
                                            length="5"
                                            readonly
                                            color="warning"
                                            :value="item.avg_rating"
                                        ></v-rating>
                                    </v-container>
                                </template>
                                <span>There {{ item.ratings.length === 1 ? "is" : "are" }} {{ item.ratings.length }} {{ item.ratings.length === 1 ? "rating" : "ratings" }}</span>
                            </v-tooltip>
                        </template>
                        <template v-slot:[`item.asdf`]="{ item }">
                            {{books.map(book => book.id).indexOf(item.id)+1}}
                        </template>
                    </v-data-table>
                </v-card>
            </v-col>
        </v-row>
    </div>
</template>

<script>
    export default {
        data(){
            return {
                // two tables (one for new books one for popular books) means there needs to be two sets of filters
                new_search: '',
                top_search: '',
                // there also needs to be two templates for table data
                new_headers: [
                    { text: 'Title', value: 'name' },
                    { text: 'Author', value: 'author' },
                    { text: 'View Book', value: 'view', sortable: false, filterable: false },
                    // { text: 'Add to Collection', value: 'add', sortable: false, filterable: false },
                ],
                top_headers: [
                    { text: 'Rank', value: 'asdf' },
                    { text: 'Title', value: 'name' },
                    { text: 'Author', value: 'author' },
                    { text: 'Average Rating', value: 'avg_rating', filterable: false },
                    { text: 'View Book', value: 'view', sortable: false, filterable: false },
                    // { text: 'Add to Collection', value: 'add', sortable: false, filterable: false },
                ],
                // the data is sorted differently on the frontend, so there are two book collections
                books: [],
                new_books: [],
                top_book: {},
            }
        },
        created() {
            // get a list of books to display on the dashboard
            this.get(this.$URL.listBooks, {}, (res) => {
                if (res.success) {
                    this.books = JSON.parse(JSON.stringify(res['books'])).sort((a,b) => {
                        if (a.avg_rating < b.avg_rating) {
                            return 1;
                        }
                        else if (a.avg_rating > b.avg_rating) {
                            return -1;
                        }
                        return 0;
                    })
                    this.new_books = JSON.parse(JSON.stringify(res['books'])).sort((a,b) => {
                        if (a.id < b.id) return 1;
                        else if (a.id > b.id) return -1;
                        return 0;
                    })
                    this.top_book = this.books[0]
                } else {
                    window.alert("Failed to fetch list of books: " + res.message);
                }
            });
            console.log('Ranking Page')
        },
        methods: {
            // generate a link to view a book
            viewBook (bid) {
                return `/book/${bid}`
            },
        }
    }
</script>