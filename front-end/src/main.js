import { createApp } from 'vue'
import Comment from './CommentList.vue'
import Layout from './layouts/My_info.vue'

createApp(Comment).mount('#CommentList')
createApp(Layout).mount('#app')