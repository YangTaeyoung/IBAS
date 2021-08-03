<template>
  <div>
    <!-- 댓글란과 대댓글란 구분선-->
    <div class="dlab-divider bg-gray-dark"></div>

    <div class="comment-form" >
      <p class="comment-form-comment">
        <textarea placeholder="답글을 입력하세요!" row="8" name="comment_cont" v-model="comment_cont"></textarea>
      </p>
      <div class="extra-cell text-right">
        <button id="comment-delete" type="button" class="site-button radius-xl m-l10 red" @click="cancelInput()">작성취소</button>
        <button id="re-comment-submit" type="submit" class="site-button radius-xl m-l10 m-r15" @click="addRecomment()">답글작성</button>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: "recomment_input",

  data: () => {
    return {
      comment_cont: null
    }
  },

  methods: {
    cancelInput: function () {
      this.$emit("cancelInput");
    },

    addRecomment: function () {
      this.$emit("addRecomment", this.comment_cont);
      this.comment_cont = "";
      this.cancelInput();
    }


  }
}
</script>

<style scoped>

</style>