import { createRouter, createWebHistory } from 'vue-router'
import Myinfo from '../Myinfo.vue'
import MyClass from '../components/MyClass.vue'


const routes = [
    { path: '/', component: Myinfo },
    { path: '/my_info/myclass', component: MyClass},

]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router
