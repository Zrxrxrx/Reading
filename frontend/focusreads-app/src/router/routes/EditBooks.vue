<template>
    <div>
        <title>FocusReads - Edit Book</title>
        <v-container class="grey lighten-5">
            <v-btn outlined elevation="2" color="primary" to="/admin/books">
                &lt; Back
            </v-btn>
            <v-row>
                <v-col>
                    <v-card
                        class="mx-auto"
                        max-width="344"
                    >
                        <v-img v-if="cover !== null"
                            :src="cover"
                            height=250
                            contain
                        ></v-img>
                        <v-card-title>
                            {{ title }} {{ edition != "" ? `(${edition})` : "" }}
                        </v-card-title>

                        <v-card-subtitle>
                            {{ author }}
                        </v-card-subtitle>

                        <v-card-text v-if="isbn != ''">
                            <p>ISBN: {{ isbn }}</p>
                            <p>Published: {{ dop }}</p>
                            <p>{{ introduction }}</p>
                        </v-card-text>

                        <v-card-actions v-if="categories">
                            <v-chip
                                class="ma-2"
                                color="primary"
                                v-for="category in categories" :key="category"
                            >
                                {{ category }}
                            </v-chip>
                        </v-card-actions>
                    </v-card>
                    <v-text-field
                        counter="130"
                        hint="URL for Book Cover"
                        label="Book Cover"
                        :value="cover"
                        @change="cover = $event"
                    ></v-text-field>
                </v-col>
                <v-col>
                    <v-form>
                        <v-text-field
                            counter="80"
                            hint="Title of Book"
                            label="Title"
                            :value="title"
                            @change="title = $event"
                        ></v-text-field>
                        <v-text-field
                            counter
                            maxlength="50"
                            hint="Author's Full Name"
                            label="Author"
                            :value="author"
                            @change="author = $event"
                        ></v-text-field>
                        <v-text-field
                            counter
                            maxlength="80"
                            hint="Book Edition"
                            label="Edition"
                            :value="edition"
                            @change="edition = $event"
                        ></v-text-field>
                        <v-row>
                            <v-col cols="6">
                                <v-text-field
                                    counter
                                    maxlength="13"
                                    hint="ISBN"
                                    label="ISBN"
                                    :value="isbn"
                                    @change="isbn = $event"
                                ></v-text-field>
                            </v-col>
                            <v-spacer></v-spacer>
                            <v-col cols="6">
                                <v-menu
                                    ref="menu"
                                    v-model="menu"
                                    :close-on-content-click="false"
                                    :return-value.sync="dop"
                                    transition="scale-transition"
                                    offset-y
                                    max-width="290px"
                                    min-width="auto"
                                >
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-text-field
                                            v-model="dop"
                                            label="Date of Publication"
                                            prepend-icon="mdi-calendar"
                                            v-bind="attrs"
                                            v-on="on"
                                        ></v-text-field>
                                    </template>
                                    <v-date-picker
                                        v-model="dop"
                                        type="month"
                                        no-title
                                        scrollable
                                        :value="dop"
                                    >
                                        <v-spacer></v-spacer>
                                        <v-btn
                                            text
                                            color="primary"
                                            @click="menu = false"
                                        >
                                            Cancel
                                        </v-btn>
                                        <v-btn
                                            text
                                            color="primary"
                                            @click="$refs.menu.save(dop)"
                                        >
                                            OK
                                        </v-btn>
                                    </v-date-picker>
                                </v-menu>
                            </v-col>
                        </v-row>
                        <v-text-field
                            counter
                            maxlength="130"
                            hint="Categories (Separated by ';')"
                            label="Categories"
                            :value="categories.join(';')"
                            @change="categories = $event == '' ? '' : $event.split(';')"
                        ></v-text-field>
                        <v-text-field
                            counter
                            maxlength="130"
                            hint="Purchase Link"
                            label="Purchase Link"
                            :value="purchase"
                            @change="purchase = $event"
                        ></v-text-field>
                        <v-textarea
                            counter
                            label="Introduction (Brief)"
                            :rules="rules"
                            :value="introduction"
                            @change="introduction = $event"
                        ></v-textarea>
                        <v-btn color="primary" @click="submit">Submit</v-btn>
                        <v-btn color="red" @click="delBook" class="float-right text--white">Delete</v-btn>
                    </v-form>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<script>
export default {
    data(){
        return {
            title: '',
            author: '',
            edition: '',
            isbn: '',
            dop: new Date().toISOString().substr(0, 7),
            categories: '',
            purchase: '',
            introduction: '',
            cover: '',
            rules: [v => v != undefined && (v.length <= 130 || 'Max 130 characters')], // rule for char length of textarea
            dop_menu: false,
        }
    },
    created() {
        // get book information from backend and fill in data on page
        this.post(this.$URL.getBook, { id: this.$props.id }, (res) => {
            if (res.success) {
                this.title = res.title
                this.author = res.author
                this.edition = res.edition
                this.isbn = res.isbn
                this.dop = res.dop
                this.categories = res.categories.split(";")
                this.purchase = res.purchase
                this.introduction = res.introduction
                this.cover = res.cover
            } else {
                window.alert("Failed to fetch book information: " + res.message);
            }
        });
    },
    props: ['id'],
    methods: {
        submit() {
            // TODO: should replace all alert()
            // ensure all required fields are filled
            if (this.title === '') {
                window.alert('Book title is empty')
                return
            }

            if (this.author === '') {
                window.alert('Book author is empty')
                return
            }

            if (this.edition === '') {
                window.alert('Edition is empty')
                return
            }

            if (this.isbn === '') {
                window.alert('Isbn is empty')
                return
            }

            if (this.dop === '') {
                window.alert('Date of Publication is empty')
                return
            }

            if (this.categories.length === 0) {
                window.alert('Categories are empty')
                return
            }

            if (this.introduction === '') {
                window.alert('Introduction is empty')
                return
            }

            // ensure all required fields are not over the limit for chars
            if (this.title.length > 80) {
                window.alert('Book title is too long')
                return
            }

            if (this.author.length > 50) {
                window.alert('Book author is too long')
                return
            }

            if (this.edition.length > 80) {
                window.alert('Edition is too long')
                return
            }

            if (this.isbn.length > 13) {
                window.alert('Isbn is too long')
                return
            }

            if (this.categories.length > 130) {
                window.alert('Categories are too long')
                return
            }

            if (this.introduction.length > 130) {
                window.alert('Introduction is too long')
                return
            }

            if (this.cover !== null && this.cover.length > 130) {
                window.alert('Book cover URL is too long')
                return
            }

            if (this.purchase !== null && this.purchase.length > 130) {
                window.alert('Purchase URL is too long')
                return
            }
            
            // submit new data to backend
            this.post(this.$URL.editBook, { "id": this.$props.id, "title": this.title, "author": this.author, "edition": this.edition, "isbn": this.isbn, "dop": this.dop, "categories": this.categories.join(";"), "purchase" : this.purchase, "introduction": this.introduction, "cover": this.cover }, res => {
                if (res.success) {
                    this.$router.push('/admin/books')
                } else {
                    window.alert(res.message)
                }
            })
        },
        // delete book from system
        delBook() {
            if (confirm("Are you sure you want to delete this book?")) {
                this.post(this.$URL.deleteBook, { "id": this.$props.id }, res => {
                    if (res.success) {
                        this.$router.push('/admin/books')
                    } else {
                        window.alert(res.message)
                    }
                })
            }
        }
    }
}
</script>