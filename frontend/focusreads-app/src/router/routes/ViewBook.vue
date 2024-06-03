<template>
    <div>
        <title>FocusReads - {{title}} by {{author}}</title>
        <v-container class="grey lighten-5">
            <v-btn outlined elevation="2" color="primary" @click="$router.go(-1)">
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

                            <template>
                                <v-container  style="margin-left: -3px; margin-top: -1em; margin-bottom: -1em;">
                                    <v-rating
                                        color="warning"
                                        dense
                                        half-increments
                                        length=5
                                        readonly
                                        size=25
                                        :value="avg_rating"
                                    ></v-rating>
                                  <v-card-text v-if="readCount == 1">A person has read this book.</v-card-text>
                                  <v-card-text v-else-if="readCount !== 0">{{ readCount }} people have read this book.</v-card-text>
                                  <v-card-text v-else>Nobody has read this book.</v-card-text>
                                </v-container>
                            </template>

                        <v-card-text v-if="isbn != ''">
                            <p>ISBN: {{ isbn }}</p>
                            <p>Date of Publication: {{ dop }}</p>
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
                    <v-container>
                        <a :href="purchase"
                            v-if="purchase !== null && purchase !== undefined && purchase !== ''"
                            style="text-transform: capitalize;"
                        >Buy this book on {{purchase.split('.')[0].includes('www') ? purchase.split('.')[1].replace('https://', '').replace('http://', '') : purchase.split('.')[0].replace('https://', '').replace('http://', '')}}</a>
                    </v-container>
                    <SelectCollections :bid="$props.id" labelName="Add to Collection" style="margin: 20px;"/>
                  <IsReadComponent :bid="$props.id" @refreshRating="refresh"/>
                </v-col>
                <v-col>
                    <v-form>
                        <v-text-field
                            counter="80"
                            hint="Title of Book"
                            label="Title"
                            :value="title"
                            readonly
                        ></v-text-field>
                        <v-tooltip bottom>
                            <template v-slot:activator="{ on, attrs }">
                                <a :href="'https://en.wikipedia.org/wiki/' + author.replaceAll(' ', '_')" v-bind="attrs" v-on="on" >
                                    <v-text-field
                                        counter
                                        maxlength="50"
                                        hint="Author's Full Name"
                                        label="Author"
                                        :value="author"
                                        readonly
                                    ></v-text-field>
                                </a>
                            </template>
                            <span>Find out about {{author}} on Wikipedia</span>
                        </v-tooltip>
                        <v-text-field
                            counter
                            maxlength="80"
                            hint="Book Edition"
                            label="Edition"
                            :value="edition"
                            readonly
                        ></v-text-field>
                        <v-row>
                            <v-col cols="6">
                                <v-text-field
                                    counter
                                    maxlength="13"
                                    hint="ISBN"
                                    label="ISBN"
                                    :value="isbn"
                                    readonly
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
                                        readonly
                                        scrollable
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
                            :value="categories"
                            readonly
                        ></v-text-field>
                        <v-textarea
                            counter
                            label="Introduction (Brief)"
                            :rules="rules"
                            :value="introduction"
                            readonly
                        ></v-textarea>
                    </v-form>
                </v-col>
            </v-row>
          <BookReviewComponent v-if="id" :bid="id"/>
        </v-container>
    </div>
</template>

<script>
import SelectCollectionsComponent from "@/components/SelectCollectionsComponent";
import BookReviewComponent from "@/components/BookReviewComponent";
import IsReadComponent from "@/components/IsReadComponent";
export default {
    components: {IsReadComponent, BookReviewComponent, SelectCollections: SelectCollectionsComponent},
    data(){
        return {
            title: '',
            author: '',
            edition: '',
            isbn: '',
            dop: '',
            cover: '',
            categories: '',
            purchase: '',
            introduction: '',
            rules: [v => v != undefined && (v.length <= 130 || 'Max 130 characters')],
            tooltip: false,
            avg_rating: 1.5,
            readCount: 0,
            menu: false,
        }
    },
    created() {
        this.updateBook();
        this.get_avg_rating();
    },
    methods: {
      updateBook() {
        // get book data from backend and show it on the frontend
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
            this.readCount = res.readCount
          } else {
            window.alert("Failed to fetch book information: " + res.message);
          }
        });
      },
      get_avg_rating() {
        // get average rating from backend and show it on the frontend
        this.get(this.$URL.rating+this.$props.id, null, (res) => {
          if (res.success) {
            this.avg_rating = res.avg_rating
          } else {
            window.alert("Failed to fetch book rating: " + res.message);
          }
        });
      },
      refresh() {
        // refresh the page
        this.updateBook();
        this.get_avg_rating();
      },
    },
    props: ['id'],
}
</script>