<template>
  <!--작성글관리-->

    <div class="row">
      <!-- 내가 작성한 글을 담는 div -->
      <div class="col-xl-12">
        <!-- 내가 작성한 게시글 부분  -->
        <div class="content-box">
          <!-- 내가 작성한 게시글 제목 -->
          <div class="content-header">
            <h3 class="title"><i class="la la-file-text m-r5"></i> 내가 작성한 게시글</h3>
          </div>
          <!-- 게시글 담는 div -->
          <div class="myinfo-table-padding">
            <!-- 내가 작성한 게시글 테이블 -->
            <table class="table">
              <thead>
              <!-- 테이블 1행: 제목 -->

              <tr class="border-0">
                <th class="border-top-0" scope="col">게시판 유형</th>
                <th style="width: 550px" class="border-top-0" scope="col">제목</th>
                <th class="border-top-0" scope="col">작성일</th>
              </tr>
              </thead>
              <tbody>
<!--              {% if my_board_list|length == 0 %}-->
              <td class="text-center" colspan="3">
                내가 작성한 게시글이 없습니다.
              </td>
<!--              {% endif %}-->
<!--              {% for my_board in my_board_list %}-->
              <tr>
                <!-- 게시판 유형 -->
<!--                <td>{{ my_board.board_type_no.board_type_name }}</td>-->
                <td>자유게시판</td>
                <!-- 게시글 제목 (클릭하면 해당 게시글로 이동하도록 a태그로 둠 -->
                <td>
<!--                  <a href="{% url 'board_detail' board_no=my_board.board_no %}">{{ my_board.board_title }}</a>-->
                  <a href="#">내가 쓴 게시글 제목</a>
                </td>
                <!-- 게시글 작성일 -->
<!--                <td>{{ my_board.board_created|date:"Y-m-d" }}</td>-->
                <td>2021-12-31</td>

              </tr>
<!--              {% endfor %}-->
              </tbody>

            </table>
          </div>
        </div>
        <!-- 내가 작성한 댓글 담는 div -->
        <div class="content-box">
          <!-- 내가 작성한 댓글 제목부분 -->
          <div class="content-header">
            <h3 class="title"><i class="la la-file-text m-r5"></i> 내가 작성한 댓글</h3>
          </div>
          <!-- 내가 작성한 댓글 내용 담는 div -->
          <div class="myinfo-table-padding">
            <!-- 댓글 내용 테이블 -->
            <table class="table">
              <!-- 테이블 1행: 제목 -->
              <thead>
              <tr>
                <th class="border-top-0" scope="col">게시판 유형</th>
                <th class="border-top-0" scope="col">댓글내용</th>
                <th class="border-top-0" scope="col"></th>
                <th class="border-top-0" scope="col">작성일</th>
              </tr>
              </thead>
              <!-- 댓글 내용 테이블 -->
              <tbody>
<!--              {% if my_comment_list|length == 0 %}-->
              <tr>
                <td class="text-center" colspan="4">
                  내가 작성한 덧글이 없습니다.
                </td>
              </tr>
<!--              {% endif %}-->
<!--              {% for my_comment in my_comment_list %}-->
              <tr>
                <!-- 게시판 유형 -->
<!--                <td>{{ my_comment.board_type }}</td>-->
                <td>자유게시판</td>
                <!-- 댓글내용 -->
<!--                <td>{{ my_comment.comment_cont }}</td>-->
                <td>ㅎㅇㅎㅇ</td>
                <!-- 원문으로 이동하는 a태그 -->
                <td>
<!--                  <a href="{% url 'board_detail' board_no=my_comment.comment_board_ref %}">원문보기-->
                  <a href="#">원문보기
                    ▶</a></td>
<!--                <td>{{ my_comment.comment_created|date:"Y-m-d" }}</td>-->
                <td>2021-12-31</td>
              </tr>
<!--              {% endfor %}-->
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

</template>

<script>
export default {
  name: "MyContent.vue"
}
</script>

<style scoped>

</style>