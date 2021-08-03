<template>
  <div class="clear" id="comment-list">
    <template v-if="comment_list!=null">
      <!-- 게시글과 댓글을 구분짓는 구분선 -->
      <h3 class="font-26">덧글</h3>
      <div class="dlab-divider bg-gray-dark"></div>

    </template>

    <div class="comments-area" id="comments">

      <div class="clearfix">
        <ol class="comment-list">
          <li v-for="(comment, i) in comment_list" :key="comment.comment_id" class="comment">

            <comment @deleteComment="deleteComment(comment.comment_id, i)" @updateComment="updateComment" @addRecomment="addComment"
                     :send-comment="comment" :send-logined-user="logined_user" :send-index="i" :send-comment-set="comment_set_list[i]"></comment>

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
import {alert_msg_for_client} from "./assets/response.js"

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.baseURL = 'https://inhabas.com/'
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
    this.board_no = pathname[pathname.length-1]
    if (location.pathname.includes('board/contest')) {
      this.board_type = 'contest'
    } else if (location.pathname.includes('board/')) {
      this.board_type = 'board'
      this.board_no = pathname[3]
    } else if (location.pathname.includes('lect/')) {
      this.board_type = 'lect'

    } else if (location.pathname.includes('staff/')) {
      this.board_type = 'staff'
    }
    else if (location.pathname.includes('activity/')){
      this.board_type = 'activity'
    }

    this.fetch_all_comment()
  },

  methods: {
    fetch_all_comment: function () {
      var this_vue = this

      axios({
        method: 'get',
        url:  "comment/" + this_vue.board_type + "/view/" + this_vue.board_no
      })
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
      if(comment_cont.trim() === "") {
        alert('댓글을 입력하세요!')
      }
      else {
        var this_vue = this;

        var postData = {comment_cont: comment_cont, comment_cont_ref: comment_cont_ref}
        axios({
          method: 'post',
          url: "comment/" + this_vue.board_type + "/register/" + this_vue.board_no,
          data: postData
        })
            .then(response => {
              // 통신 성공하면, 해당 댓글 정보 받아와서, 새로 붙이기.
              if (comment_cont_ref === undefined) { // 댓글
                this_vue.comment_list.push(response.data.comment);
              } else { // 대댓글
                this_vue.comment_set_list[index].push(response.data.comment);
              }
            })
            .catch(response => {
              console.log("Failed to add the comment", response);
              alert_msg_for_client(response)
              alert("덧글 등록에 실패했습니다. 웹팀 팀장 유동현에게 문의하세요!!")
            })
      }
    },

    deleteComment: function (comment_id, index) {
      if(confirm('댓글을 삭제하시겠습니까?')) {
        axios.delete("comment/delete/" + comment_id)
            .then(() => {
              this.comment_list.splice(index, 1);  // 해당 댓글 삭제
              this.comment_set_list[index] = null;  // 대댓글 컴포넌트를 생성하게 만드는 대댓글 데이터 삭제
            })
            .catch(response => {
              console.log("Failed to remove the comment", response);
              alert_msg_for_client(response)
              alert("덧글 삭에 실패했습니다. 웹팀 팀장 유동현에게 문의하세요!!")
            });
      }
    },

    updateComment: function (comment_id, comment_cont, index) {
      if(comment_cont.trim() === "") {
        alert('댓글을 입력하세요!')
      }
      else {
        var vm = this;
        axios({
          method: 'put',
          url: "comment/update/" + comment_id,
          data: {comment_cont: comment_cont}
        })
            .then(response => {
              vm.comment_list[index] = response.data.comment;
            })
            .catch(response => {
              console.log("Failed to update the comment", response);
              alert_msg_for_client(response)
              alert("덧글 수정에 실패했습니다. 웹팀 팀장 유동현에게 문의하세요!!")
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
