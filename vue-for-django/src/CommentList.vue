<template>
  <div class="clear" id="comment-list">
    <div class="comments-area" id="comments">
      <div class="clearfix">
        <ol class="comment-list">
          <li v-for="(comment, i) in comment_list" v-bind:key="i" :ref="'comment_' + i" class="comment">

              <comment @deleteComment="deleteComment(i)" @updateComment="updateComment(comment)" :sendComment="comment" ></comment>

                <div v-if="comment_set_list[i]!=null">
                  <div v-for="(commentRef, j) in comment_set_list[i]"  v-bind:key="j">
                    <div  class="dlab-divider bg-gray-dark"></div>
                    <comment :send-comment="commentRef" style="margin-left: 20px;"></comment>
                  </div>
                </div>

          </li>
        </ol>

        <comment-input></comment-input>

      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Comment from "./components/Comment";
import CommentInput from "./components/CommentInput";

export default {
  data: () => {
    return {
      comment_list: null,
      comment_set_list: null,
    };
  },

  components: {
    'comment-input': CommentInput,
    'comment': Comment
  },

  mounted() { // DOM 객체 생성 후 drf server 에서 데이터를 가져와 CommentList 렌더링
    // let pathname = location.pathname.split('/')
    // let board_type = pathname[0]
    // let board_no = pathname[pathname.length-1]

    axios({
      method: "GET",
      url: "http://127.0.0.1:8000/comment/" //+ board_type + "/view/" + board_no
    })
        .then(response => {
          this.comment_list = response.data.comment_list;
          this.comment_set_list = response.data.comment_set_list;
        })
        .catch(response => {
          console.log("Failed to get todoList", response);
        });
  },

  methods: {
    deleteComment: function (index) {
      let commentToDelete = this.$refs["comment_"+index][0];
      commentToDelete.parentNode.removeChild(commentToDelete);
      // axios({
      //   method: "POST",
      //   url: "http://127.0.0.1:8000/comment/delete/",
      //   xsrfHeaderName: "X-CSRFToken",
      // })
      //     .then(response => {
      //       let commentToDelete = this.$refs["comment_"+index][0];
      //       commentToDelete.parentNode.removeChild(commentToDelete);
      //       console.log("Success!" , response.data);
      //     })
      //     .catch(response => {
      //       console.log("Failed to remove the comment", response);
      //     });
    },
    updateComment: function (comment) {
      console.log(comment);
      // axios({
      //   method: "POST",
      //   url: "http://127.0.0.1:8000/comment/update/",
      //   data: {
      //      'comment_id': comment.comment_id,
      //      'comment_cont: comment.comment_cont
      //   },
      //   xsrfHeaderName: "X-CSRFToken",
      // })
      //     .then(response => {
      //       console.log("Success!" , response.data);
      //     })
      //     .catch(response => {
      //       console.log("Failed to update the comment", response);
      //     });
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
