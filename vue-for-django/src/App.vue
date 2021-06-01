<template>
  <div class="clearfix">
    <ol class="comment-list">
      <li v-for="(comment, i) in comment_list" v-bind:key="i" :id="'comment_' + comment.comment_id" class="comment">

          <comment @delete="deleteComment(i)" :sendComment="comment" ></comment>

      </li>
    </ol>
  </div>
</template>

<script>
import axios from "axios";
import Comment from "./components/Comment";

export default {
  data: () => {
    return {
      comment_list: null,
    };
  },

  components: {
    'comment': Comment
  },

  mounted() { // DOM 객체 생성 후 drf server 에서 데이터를 가져와 todoList 저장
    axios({
      method: "GET",
      url: "http://127.0.0.1:8000/comment"
    })
        .then(response => {
          this.comment_list = response.data;
        })
        .catch(response => {
          console.log("Failed to get todoList", response);
        });
  },

  methods: {
    deleteComment: function (index) {
      console.log('delete '+index)
    }
  }
};


</script>






<style>

ol.comment-list li.comment .comment-body {
  margin-left: 0;
  border: 1px solid #e9e9e9;
  margin-bottom: 30px;
}

ol.comment-list li.comment .reply a {
  position: static;
}

.reply-btn-div {
  margin-top: 15px;
  font-weight: 400;
  font-size: 14px;
}

/*댓글 관련 아웃라인 none*/
* {
  outline: none;
}

.comment-btn {
  padding: 0;
  color: #4611a7;
  border-color: transparent;
  background-color: white;
  cursor: pointer;
  display: inline-block;
}

.comment-btn:hover {
  color: #0e91e3;
}

.comment-profile-size {
  width: 35px;
  height: 35px;
  border: 2px solid #606269;
  border-radius: 17.5px;
  margin-right: 10px;

}

input:disabled {
  padding: 0px;
  cursor: auto;
  font-size: 14px;
  width: 706px;
  display: block;
  color: #606269;
  cursor: alias;
  background-color: transparent;
  border-width: 0px;
}

.reply-line {
  height: 1px;
  position: relative;
  margin: 20px 0;
}
</style>
