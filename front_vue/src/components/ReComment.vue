<template>
  <div>

    <div class="dlab-divider bg-gray-dark"></div>

    <div class="comment-author vcard">
      <cite class="fn">
        <img
            :src="comment.comment_writer.user_pic"
            width="35"
            height="35" class="comment-profile-size"
            alt="현재 브라우저에서 지원하지 않는 형식입니다."> {{ comment.comment_writer.user_name }}
      </cite>
    </div>
    <div class="dlab-post-meta m-l10">
      <ul class="d-flex">
        <li class="post-author">
          <a href="javascript:void(0);"> {{ comment.comment_writer.user_major }}
            {{ comment.comment_writer.user_stu | subStr(2,4) }}학번</a>
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

      <template v-if="logined_user.user_stu === comment.comment_writer.user_stu">
        <button @click="updateRecomment()" class="comment-btn m-r10">
          <i class="fa fa-pencil m-r5"></i>수정
        </button>
      </template>

      <template v-if="logined_user.user_stu === comment.comment_writer.user_stu || logined_user.user_role < 3">
        <button @click="deleteRecomment()" class="comment-btn m-r10">
          <i class="fa fa-trash m-r5"></i>삭제
        </button>
      </template>

    </div>

  </div>
</template>

<script>
export default {
  name: "ReComment",
  props: ['sendRecomment', 'sendLoginedUser', 'sendIndex'],

  data: () => {
    return {
      index: null,
      comment: null,
      isDisabled: true,
      logined_user: null
    };
  },
  watch: {
    sendIndex: function (newVal) {
      this.index = newVal;
    }
  },
  created() {
    this.index = this.sendIndex;
    this.comment = this.sendRecomment;
    this.logined_user = this.sendLoginedUser;
  },
  methods: {
    // 대댓글 수정하도록 상위 컴포넌트(Comment)에 이벤트 발생
    updateRecomment: function () {
      if (this.isDisabled === false) {
        this.$emit('updateRecomment', this.comment.comment_id, this.comment.comment_cont, this.index)
      }
      this.isDisabled = !this.isDisabled;
    },

    // 대댓글 삭제하도록 상위 컴포넌트(Comment)에 이벤트 발생
    deleteRecomment: function () {
      this.$emit('deleteRecomment');
      this.$destroy()
    }

  },
  filters: {
    truncate: function (text, length) {
      return String(text).slice(0, length)
    },
    subStr: function (text, start, end) {
      return String(text).substring(start, end);
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