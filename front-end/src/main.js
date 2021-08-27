import { createApp } from 'vue'
import Comment from './CommentList.vue'
import Myinfo from './Myinfo.vue'
import router from './router/MyInfoIndex.js'

createApp(Comment).mount('#CommentList')
createApp(Myinfo).use(router).mount('#Myinfo')