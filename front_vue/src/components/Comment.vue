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
            {{ comment.comment_created | timeFormat}}
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

    <input type="hidden" id="comment_id" :value="comment.comment_id">

    <div class="reply-btn-div">
      <button class="btnAdd comment-btn m-r20">
        <i class="fa fa-commenting m-r5"></i>답글쓰기
      </button>
      <button @click="updateComment()" class="comment-btn m-r10">
        <i class="fa fa-pencil m-r5"></i>수정
      </button>
      <button @click="deleteComment()" class="comment-btn m-r10">
        <i class="fa fa-trash m-r5"></i>삭제</button>
    </div>
  </div>
</template>

<script>
export default {
  props: ['sendComment'],
  name: "Comment.vue",

  data: () => {
    return {
      comment: null,
      isDisabled: true,
    };
  },

  created() {
    this.comment = this.sendComment
  },

  methods: {  // CRUD 로직이 들어갈 부분
    updateComment: function () {
      if (this.isDisabled === false) {
        this.$emit("updateComment")
      }
      this.isDisabled = !this.isDisabled
    },

    deleteComment: function () {
      this.$emit("deleteComment")  // 이벤트가 상위 컴포넌트에서 실행된 후에 다음 코드 실행됨.
      this.$destroy()
      this.$el.parentNode.removeChild(this.$el)
    },
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