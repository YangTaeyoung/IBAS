<template>
  <div>

    <div class="dlab-divider bg-gray-dark"></div>

    <div class="comment-form" id="respond">

      <!-- 댓글입력창 -->
      <p class="comment-form-comment">
        <label for="comment">Comments</label>
        <textarea rows="8" name="comment_cont" v-model="comment_cont"
                  placeholder="댓글을 남겨보세요!" required="required"
                  id="comment"></textarea>
      </p>
      <!-- 댓글작성 버튼 -->
      <p class="form-submit" style="text-align: right">
        <input v-on:click="addComment(comment_cont)" value="댓글등록"
               class="submit site-button" id="submit" name="submit">
      </p>

    </div>

  </div>

</template>

<script>

export default {
  name: "Comment-input.vue",

  data: () => {
    return {
      comment_cont: null
    }
  },

  methods: {
    addComment: function () {
      console.log("call parent add comment function...", this.comment_cont)

      if(this.comment_cont === null) {
        // 빈 내용을 댓글로 추가하려는 경우
        alert('댓글을 입력하세요!');
      } else if(confirm("댓글을 등록하시겠습니까?")) {
        this.$emit("addComment", this.comment_cont);
      }
    }
  },

}
</script>

<style scoped>

</style>