<template>
  <div class="clear" id="comment-list">
    <template v-if="comment_list!=null">
      <!-- 게시글과 댓글을 구분짓는 구분선 -->
      <div class="dlab-divider bg-gray-dark"></div>
    </template>
    <div class="comments-area" id="comments">
      <div class="clearfix">
        <ol class="comment-list">
          <li v-for="(comment, i) in comment_list" v-bind:key="i" :ref="'comment_' + comment.comment_id" class="comment">

            <comment @deleteComment="deleteComment" @updateComment="updateComment" @addRecomment="addComment"
                     :send-comment="comment" :send-logined-user="logined_user" :send-index="i" :send-comment-set="comment_set_list[i]"></comment>
<!--
            <div v-if="comment_set_list[i]!=null">
              <div v-for="(commentRef, j) in comment_set_list[i]"  v-bind:key="j" :ref="'comment_' + commentRef.comment_id">
                <comment @deleteComment="deleteComment" @updateComment="updateComment"
                    :send-comment="commentRef" :send-logined-user="logined_user"
                         style="margin-left: 20px;"></comment>
              </div>
            </div>-->

          </li>
        </ol>

        <comment-input @addComment="addComment"></comment-input>

      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Comment from "./components/Comment";
import CommentInput from "./components/CommentInput";

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export default {
  data: () => {
    return {
      logined_user: null,
      comment_list: null,
      comment_set_list: null,
      board_type: null,
      board_no: null,
    };
  },

  components: {
    'comment-input': CommentInput,
    'comment': Comment
  },

  mounted() { // DOM 객체 생성 후 drf server 에서 데이터를 가져와 CommentList 렌더링
    let pathname = location.pathname.split('/')
    this.board_type = pathname[1]
    this.board_no = pathname[pathname.length-2]
    this.fetch_all_comment()
  },

  methods: {
    fetch_all_comment: function () {
      var this_vue = this
      //console.log(this_vue.board_type, this_vue.board_no)

      axios.get("http://127.0.0.1:8000/comment/" + this_vue.board_type + "/view/" + this_vue.board_no)
          .then(response => {
            this.comment_list = response.data.comment_list;
            this.comment_set_list = response.data.comment_set_list;
            this.logined_user =response.data.logined_user;
          })
          .catch(response => {
            console.log("Failed to get commentList", response);
          });
    },
    addComment: function (comment_cont, comment_cont_ref, index) {
      if(confirm('댓글을 등록하시겠습니까?')) {
        var this_vue = this;
        console.log("add comment...");

        var postData = {comment_cont: comment_cont, comment_cont_ref: comment_cont_ref}
        axios.post("http://127.0.0.1:8000/comment/" + this_vue.board_type + "/register/" + this_vue.board_no, postData)
            .then(function (response) {
              // 통신 성공하면, 해당 댓글 정보 받아와서, 새로 붙이기.
              console.log('adding comment POST', response);
              if (comment_cont_ref === undefined) {
                console.log('댓글', comment_cont_ref)
                this_vue.comment_list.push(response.data.comment);
              } else {
                console.log('대댓글', comment_cont_ref)
                // 첫 대댓글 오류
                if (this_vue.comment_set_list[index] == null) {
                  this_vue.comment_set_list[index] = [response.data.comment,];
                } else {
                  this_vue.comment_set_list[index].push(response.data.comment);
                }
              }

            })
            .catch(function (err) {
              console.log("adding error", err);
            })
      }
    },
    deleteComment: function (comment_id) {
      if(confirm('댓글을 삭제하시겠습니까?')) {
        console.log("deleting comment", comment_id)

        axios.delete("http://127.0.0.1:8000/comment/delete/" + comment_id)
            .then(response => {
              let commentToDelete = this.$refs['comment_' + comment_id][0];
              commentToDelete.parentNode.removeChild(commentToDelete);
              console.log("Success deletion!", response);
            })
            .catch(response => {
              console.log("Failed to remove the comment", response);
            });
      }
    },
    updateComment: function (comment_id, comment_cont) {
      if(confirm('댓글을 수정하시겠습니까?')) {
        console.log('update comment' + comment_id + comment_cont);
        axios.put("http://127.0.0.1:8000/comment/update/" + comment_id, {comment_cont: comment_cont})
            .then(response => {
              console.log("Success!", response.data);
            })
            .catch(response => {
              console.log("Failed to update the comment", response);
            });
      }
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
