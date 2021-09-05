import { createRouter, createWebHistory } from 'vue-router'
// import Myinfo from '../Myinfo.vue'
import MyClass from '../components/MyClass.vue'
import ClassSet from "../components/ClassSet.vue";
import MyContent from "../components/MyContent.vue";
import MyBank from "../components/MyBank.vue";
import MyProfile from "../components/MyProfile.vue";


const routes = [
    { path: '/my_info/test/', component: MyProfile, name: 'MyProfile', props: true },
    { path: '/my_info/myClass', component: MyClass},
    { path: '/my_info/classSet', component: ClassSet},
    { path: '/my_info/myContent', component: MyContent},
    { path: '/my_info/myBank', component: MyBank},




]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router
