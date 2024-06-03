<template>
    <div>
        <v-toolbar
      color="indigo"
      dark
      flat
    >

        <v-toolbar-title>Administration</v-toolbar-title>
        <template v-slot:extension>
            <v-tabs
                fixed-tabs
                dark
            >
                <v-tab to="/admin/books">
                    Books
                </v-tab>
                <v-tab to="/admin/users">
                    Users
                </v-tab>
            </v-tabs>
        </template>
    </v-toolbar>
    <router-view></router-view>
</div>
</template>

<script>
// The following are dummy methods to suppress linter errors
// The main content of this page lies in the AdminBooks.vue and AdminUsers.vue components
    export default {
        data(){
            return {
                user: 'NULL'
            }
        },
        created() {
            console.log('a')
        }
    }
</script>