import Vue from 'vue'
import VueRouter from 'vue-router'
import LoginView from './routes/LoginView'
import RegisterView from './routes/RegisterView'
import LandingView from './routes/LandingView'
import DashboardView from './routes/DashboardView'
import ResetPasswordView from './routes/ResetPasswordView'
import ProfileView from './routes/ProfileView'
import EditPasswordView from './routes/EditPasswordView'
import AdminView from './routes/AdminView'
import AdminUsers from './routes/AdminUsers'
import AdminBooks from './routes/AdminBooks'
import EditBooks from './routes/EditBooks'
import NewBook from './routes/NewBook'
import ViewBook from './routes/ViewBook'
import SearchView from './routes/SearchView'
import RankingList from './routes/RankingList'
import UserCollectionView from './routes/UserCollectionView'
import CollectionView from './routes/CollectionView'
Vue.use(VueRouter)

// requiresAuth is a navigation guard - ensures users are logged in before entering a page
// if a user is not logged in, the user is redirected to the login screen with an appropriate error message
const requiresAuth = (to, from, next) => {
    if (localStorage.getItem("token")) {
        next();
        return;
    } else {
        next({
            path: '/login',
            query: {
                type: 'warning',
                msg: 'You are not logged in'
            }
        })
    }
}

// requiresAdmin is a navigation guard - ensures an admin user is logged in before entering a page
// if an admin user is not logged in, the user is redirected to the login screen with an appropriate error message
const requiresAdmin = (to, from, next) => {
    if (localStorage.getItem("token") && JSON.parse(atob(localStorage.getItem("token").split(".")[1]))["isAdmin"] == true
) {
        next();
        return;
    } else {
        next({
            path: '/login',
            query: {
                type: 'warning',
                msg: 'You are not logged in as an administrator'
            }
        })
    }
}

// A list of all routes for browser navigation
// beforeEnter: requiresAuth refers to pages which require user login
// beforeEnter: requiresAdmin refers to pages which require admin user login
const routes = [
    { path: '/login', component: LoginView, name: "Login" },
    { path: '/', component: LandingView },
    { path: '/dashboard', component: DashboardView, beforeEnter: requiresAuth },
    { path: '/register', component: RegisterView },
    { path: '/resetpassword', component: ResetPasswordView },
    { path: '/profile', component: ProfileView, beforeEnter: requiresAuth },
    { path: '/editPassword', component: EditPasswordView, beforeEnter: requiresAuth },
    { path: '/admin', component: AdminView, children: [ { path: 'users', component: AdminUsers }, { path: 'books', component: AdminBooks } ], beforeEnter: requiresAdmin },
    { path: '/admin/books/edit/:id', component: EditBooks, props: true, beforeEnter: requiresAdmin },
    { path: '/admin/books/new', component: NewBook, beforeEnter: requiresAdmin },
    { path: '/book/:id', component: ViewBook, props: true },
    { path: '/search/:query', component: SearchView, props: true },
    { path: '/ranking', component: RankingList },
    { path: '/collection', component: UserCollectionView },
    { path: '/user/collection', component: UserCollectionView },
    { path: '/collection/:id', component: CollectionView, props: true },
]
export default new VueRouter({
    routes
})
