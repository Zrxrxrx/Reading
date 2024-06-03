<template>
    <div>
        <title>FocusReads - Book Management</title>
        <template>
            <v-card>
                <v-card-title>
                    Book Management
                    <v-spacer></v-spacer>
                    <v-text-field
                        v-model="search"
                        append-icon="mdi-magnify"
                        label="Filter"
                        single-line
                        hide-details
                    ></v-text-field>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" to="/admin/books/new">Add Book</v-btn>
                </v-card-title>
                <v-data-table
                    :headers="headers"
                    :items="books"
                    :search="search"
                >
                    <template v-slot:[`item.edit`]="{ item }">
                        <v-btn
                            color="primary"
                            elevation="2"
                            outlined
                            :to="editLink(item.id)"
                        >
                            Edit
                        </v-btn>
                    </template>
                </v-data-table>
            </v-card>
        </template>
    </div>
</template>

<script>
    export default {
        data () {
            return {
                search: '', // this is required for the frontend filtering to work
                // The following is a template for the table data
                headers: [
                    {
                        text: 'ID',
                        align: 'start',
                        value: 'id',
                    },
                    { text: 'Title', value: 'name' },
                    { text: 'Author', value: 'author' },
                    { text: 'Edit', value: 'edit', sortable: false, filterable: false },
                ],
                books: [
                ],
            }
        },
        methods: {
            // This is used to generate the book edit links for the table buttons
            editLink (bid) {
                return `/admin/books/edit/${bid}`
            },
        },
        created () {
            // Get a list of books from the backend
            this.get(this.$URL.adminBooks, {}, (res) => {
                if (res.success) {
                    this.books = res['books']
                } else {
                    window.alert("Failed to fetch list of books: " + res.message);
                }
            });
        }

    }
</script>