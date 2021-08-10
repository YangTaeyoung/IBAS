<template>
  <div class="clear" id="comment-list">
    <template v-if="comment_list != null && comment_list.length > 0">
      <!-- 게시글과 댓글을 구분짓는 구분선 -->
      <div class="dlab-divider bg-gray-dark"></div>

    </template>

    <div class="comments-area" id="comments">

      <div class="clearfix">
        <ol class="comment-list">
          <li v-for="(comment, i) in comment_list" :key="comment.comment_id" class="comment">

            <comment @deleteComment="deleteComment(comment.comment_id, i)" @updateComment="updateComment"
                     @addRecomment="addComment"
                     :send-comment="comment" :send-logined-user="logined_user" :send-index="i"
                     :send-comment-set="comment_set_list[i]"></comment>

          </li>
        </ol>

        <comment-input @addComment="addComment"></comment-input>

      </div>
    </div>
  </div>
</template>

<script>
import Vue from 'vue';
import axios from "axios";
import Comment from "./components/Comment";
import CommentInput from "./components/CommentInput";
import {alert_msg_for_client} from "./assets/response.js"

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.baseURL = 'https://inhabas.com';
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
    this.board_no = pathname[pathname.length - 1]
    if (/board\/contest\/detail\/\d+/.test(location.pathname)) {
      this.board_type = 'contest'
    } else if (/board\/detail\/\d+/.test(location.pathname)) {
      this.board_type = 'board'
      this.board_no = pathname[3]
    } else if (/lect\/room\/\d+\/detail\/\d+/.test(location.pathname)) {
      this.board_type = 'lect'
    } else if (/staff\/member\/delete\/detail\/\d+/.test(location.pathname)) {
      this.board_type = 'staff'
    } else if (/activity\/\d+\/detail/.test(location.pathname)) {
      this.board_type = 'board'
      this.board_no = pathname[2]
    }

    this.fetch_all_comment()
  },

  methods: {
    fetch_all_comment: function () {
      axios({
        method: 'get',
        url:  "comment/" + this.board_type + "/view/" + this.board_no
      })
          .then(response => {
            this.comment_list = response.data.comment_list;
            this.comment_set_list = response.data.comment_set_list;
            this.logined_user = response.data.logined_user;
          })
          .catch(response => {
            console.log("Failed to get commentList", response);
          });
    },

    addComment: function (comment_cont, comment_cont_ref, index) {
      if (comment_cont.trim() === "") {
        alert('댓글을 입력하세요!')
      } else {
        var postData = {comment_cont: comment_cont, comment_cont_ref: comment_cont_ref}
        axios({
          method: 'post',
          url: "comment/" + this.board_type + "/register/" + this.board_no,
          data: postData
        })
            .then(response => {
              // 통신 성공하면, 해당 댓글 정보 받아와서, 새로 붙이기.
              if (comment_cont_ref === undefined) { // 댓글
                this.comment_list.push(response.data.comment); // 댓글 붙이기
                this.comment_set_list.push([]); // 해당 댓글의 대댓글 배열 생성
              } else { // 대댓글
                this.comment_set_list[index].push(response.data.comment); // 대댓글 붙이기
              }
            })
            .catch(response => {
              console.log("Failed to add the comment", response);
              alert_msg_for_client(response)
              alert("덧글 등록에 실패했습니다. 새로고침한 후 지속되면 웹팀에 문의하세요!!")
            })
      }
    },

    deleteComment: function (comment_id, index) {
      if (confirm('댓글을 삭제하시겠습니까?')) {
        axios.delete("comment/delete/" + comment_id)
            .then(() => {
              Vue.delete(this.comment_list, index);  // 해당 댓글 삭제
              Vue.delete(this.comment_set_list, index);  // 대댓글 컴포넌트를 생성하게 만드는 대댓글 데이터 삭제
            })
            .catch(response => {
              console.log("Failed to remove the comment", response);
              alert_msg_for_client(response)
              alert("덧글 삭제에 실패했습니다. 새로고침한 후 지속되면 웹팀에 문의하세요!!")
            });
      }
    },

    updateComment: function (comment_id, comment_cont, index) {
      if (comment_cont.trim() === "") {
        alert('댓글을 입력하세요!')
      } else {
        axios.put("comment/update/" + comment_id, {comment_cont: comment_cont})
            .then(response => {
              console.log('반응이 왔엉', response)
              this.comment_list[index] = response.data.comment;
            })
            .catch(response => {
              console.log("Failed to update the comment", response);
              alert_msg_for_client(response)
              alert("덧글 수정에 실패했습니다. 새로고침한 후 지속되면 웹팀에 문의하세요!!")
            });
      }
    }
  }
};


</script>

