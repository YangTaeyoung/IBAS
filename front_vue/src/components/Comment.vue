<template>
  <div class="comment-body">
    <div class="comment-author vcard">
      <cite class="fn">
        <img
            src="/media/"
            width="35"
            height="35" class="comment-profile-size"
            alt="현재 브라우저에서 지원하지 않는 형식입니다."> {{ comment.writer_name }}
      </cite>
    </div>
    <div class="dlab-post-meta m-l10">
      <ul class="d-flex">
        <li class="post-author">
          <a href="javascript:void(0);"> {{ comment.writer_major }}
            {{ comment.comment_writer | truncate(2) }}학번</a>
        </li>


        <li class="post-comment"><i
            class="ti ti-alarm-clock"></i>
          <a href="javascript:void(0);">
            {{ comment.comment_created | timeFormat }}
          </a>
        </li>
      </ul>
    </div>

    <input type="text" :disabled="isDisabled === true"
           style="width: 706px"
           name="comment_cont"
           class="comments-area"
           :id="'comment_cont_' + comment.comment_id"
           v-model="comment.comment_cont"
           autofocus>


    <div class="reply-btn-div">

      <button class="btnAdd comment-btn m-r20" @click="Recomment()">
        <i class="fa fa-commenting m-r5"></i>답글쓰기</button>


      <template v-if="logined_user.user_stu === comment.comment_writer" >
        <button @click="updateComment()" class="comment-btn m-r10">
          <i class="fa fa-pencil m-r5"></i>수정</button>
      </template>

      <template v-if="logined_user.user_stu === comment.comment_writer || logined_user.user_role < 3" >
        <button @click="deleteComment()" class="comment-btn m-r10">
          <i class="fa fa-trash m-r5"></i>삭제</button>
      </template>

      <template v-if="recomment_mode === true">
        <!-- 대댓글 입력 창 -->
        <recomment_input @cancelInput="Recomment" @addRecomment="addRecomment"></recomment_input>
      </template>

      <template v-if="comment_set_list != null">
        <div v-for="(recomment, j) in comment_set_list"  v-bind:key="j" :ref="'recomment_' + recomment.comment_id">
          <recomment @deleteRecomment="deleteRecomment" @updateRecomment="updateRecomment"
                   :send-recomment="recomment" :send-logined-user="logined_user" style="margin-left: 20px;"></recomment>
        </div>
      </template>

    </div>
  </div>
</template>

<script>
import ReCommentInput from "./ReCommentInput";
import ReComment from "./ReComment";
import axios from "axios";

export default {
  props: ['sendComment', 'sendLoginedUser', 'sendIndex', 'sendCommentSet'],
  name: "Comment.vue",


  data: () => {
    return {
      index: null,
      comment: null,
      isDisabled: true,
      logined_user: null,
      comment_set_list: null,
      recomment_mode: false,

    };
  },

  components: {
    'recomment_input': ReCommentInput,
    'recomment': ReComment
  },

  created() {
    this.comment = this.sendComment;
    this.logined_user = this.sendLoginedUser;
    this.index = this.sendIndex;
    this.comment_set_list = this.sendCommentSet;
  },

  methods: {  // CRUD 로직이 들어갈 부분
    // 댓글 수정하도록 상위 컴포넌트(commentList)에 이벤트 발생
    updateComment: function () {
      if (this.isDisabled === false) {
        this.updateRecomment(this.comment.comment_id, this.comment.comment_cont)
      }
      this.isDisabled = !this.isDisabled;
    },

    // 대댓글 수정하도록 상위 컴포넌트(commentList)에 이벤트 발생
    updateRecomment: function(comment_id, comment_cont) {
      this.$emit("updateComment", comment_id, comment_cont);
    },

    // 댓글 삭제하도록 상위 컴포넌트(commentList)에 이벤트 발생
    deleteComment: function () {
        this.$emit('deleteComment', this.comment.comment_id)
    },

    // 대댓글 삭제하기
    deleteRecomment: function (comment_id) {
      if (confirm('댓글을 삭제하시겠습니까?')) {
        axios.delete("http://127.0.0.1:8000/comment/delete/" + comment_id)
            .then(response => {
              let commentToDelete = this.$refs['recomment_' + comment_id][0];
              commentToDelete.parentNode.removeChild(commentToDelete);
              console.log("Success deletion!" , response);
            })
            .catch(response => {
              console.log("Failed to remove the comment", response);
            });
      }
    },

    // 대댓글 입력 창 열고 닫기
    Recomment: function () {
      this.recomment_mode = !this.recomment_mode;
    },

    // 대댓글 등록하기
    addRecomment: function (recomment_cont) {
      console.log('addREcomment..')
      this.$emit('addRecomment', recomment_cont, this.comment.comment_id, this.index)
    }
  },

  filters: {
    truncate: function (text, length) {
      return String(text).slice(0,length)
    },
    timeFormat: function (date) {
      date = new Date(date)
      let month = date.getMonth() + 1;
      let day = date.getDate();
      let hour = date.getHours();
      let minute = date.getMinutes();

      month = month >= 10 ? month : '0' + month;
      day = day >= 10 ? day : '0' + day;
      hour = hour >= 10 ? hour : '0' + hour;
      minute = minute >= 10 ? minute : '0' + minute;

      return date.getFullYear() + '-' + month + '-' + day + ' ' + hour + ':' + minute;
    }
  }
}
</script>

<style scoped>

</style>