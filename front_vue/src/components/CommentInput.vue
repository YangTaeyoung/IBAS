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
        <input type="submit" v-on:click="addComment()" value="댓글등록"
                class="submit site-button"/>
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
      this.$emit("addComment", this.comment_cont);
      this.comment_cont = ""
    }
  },

}
</script>

<style scoped>

</style>