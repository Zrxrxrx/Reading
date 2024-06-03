<template>
    <div>
        <title>FocusReads - Search</title>
        <p>You searched for <b>{{query}}</b></p>
        <v-card>
            <v-card-title>
                Search Results
                <v-spacer></v-spacer>
                <v-row style="margin-right: 20px;">
                    <v-col cols="3">
                        <v-select
                            :items="ratings_filter"
                            label="Ratings Filter"
                            @change="books = books_orig.filter((el) => el.avg_rating >= ratings_filter.indexOf($event))"
                        ></v-select>
                    </v-col>
                    <v-col cols="9">
                        <v-text-field
                            v-model="search"
                            append-icon="mdi-magnify"
                            label="Filter"
                            single-line
                            hide-details
                        ></v-text-field>
                    </v-col>
                </v-row>
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
    </div>
</template>

<script>
    export default {
        data(){
            return {
                search: '', // filter
                // template for table data
                headers: [
                    { text: 'Title', value: 'name' },
                    { text: 'Author', value: 'author' },
                    { text: 'Date of Publication', value: 'dop' },
                    { text: 'Average Rating', value: 'avg_rating', filterable: false },
                    { text: 'View Book', value: 'view', sortable: false, filterable: false },
                ],
                books: [],
                books_orig: [],
                ratings_filter: ["0+", "1+", "2+", "3+", "4+", "5"],
            }
        },
        created() {
            // Get the search results for the specified query
            this.post(this.$URL.search, {query : this.$props.query}, (res) => {
                if (res.success) {
                    this.books = res['books']
                    this.books_orig = res['books']
                } else {
                    window.alert("Failed to fetch list of books: " + res.message);
                }
            });
            console.log('Search Page')
        },
        methods: {
            // generate a link to view a specified book
            viewBook (bid) {
                return `/book/${bid}`
            },
        },
        props: ['query'],
        // if the query changes, then update the page content
        watch: {
            query: function (newVal) {
                this.post(this.$URL.search, {query : newVal}, (res) => {
                    if (res.success) {
                        this.books = res['books']
                        this.books_orig = res['books']
                    } else {
                        window.alert("Failed to fetch list of books: " + res.message);
                    }
                });
            }
        }
    }
</script>