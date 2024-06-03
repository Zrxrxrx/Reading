<template>
    <div>
        <title>FocusReads - User Management</title>
        <template>
            <v-card>
                <v-card-title>
                    User Management
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
                    :items="users"
                    :search="search"
                >
                    <template v-slot:[`item.name`]="{ item }">
                        <i style="font-style: normal" :class="[`${item.nameColor}--text`]">{{ item.name }}</i>
                    </template>
                    <template v-slot:[`item.blocked`]="{ item }">
                        <v-btn
                            :color="primary"
                            elevation="2"
                            outlined
                            @click="blockUser(item.id, item.blocked, item)"
                        >
                            {{ item.blocked != true ? "Block" : "Unblock" }}
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
                    { text: 'Name', value: 'name' },
                    { text: 'Email', value: 'email' },
                    { text: 'Block', value: 'blocked', sortable: false, filterable: false },
                ],
                users: [
                ],
            }
        },
        methods: {
            // This is a method which interacts with the backend to block or unblock a specified user
            blockUser (uid, isBlocked, item) {
                this.post(this.$URL.block, { "uid": uid, "block": !(isBlocked) }, (res => {
                    if (res.success) {
                        // If the backend reports the user has been blocked
                        if (res.blocked == true) {
                            window.alert("Successfully blocked " + res.username)
                            item.blocked = true
                        // If the backend reports the user has been unblocked
                        } else {
                            window.alert("Successfully unblocked " + res.username)
                            item.blocked = false
                        }
                        // if (res.block == 'True') {
                        //     el.innerText = "Unblock"
                        // } else {
                        //     el.innerText = "Block"
                        // }
                    } else {
                        window.alert("Failed to block user: " + res.message)
                    }
                }));
            },
        },
        created () {
            // Get a list of users from the backend
            this.get(this.$URL.listUsers, {}, (res) => {
                if (res.success) {
                    this.users = res['users']
                } else {
                    window.alert("Failed to fetch list of users: " + res.message);
                }
            });
        }
    }
</script>