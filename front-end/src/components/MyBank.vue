<template>
  <!--예산신청내역-->
  <!--===== 내가 신청한 예산내역 코드 시작 =====-->

    <div class="row">
      <div class="col-xl-12">
        <div class="content-box">
          <!-- 제목 div -->
          <div class="content-header">
            <h3 class="title"><i class="la la-money m-r5"></i>예산신청 내역</h3>
          </div>
          <div class="content-body">
            <div class="myinfo-table-padding">
              <!-- 내가 신청한 예산신청 리스트 -->
              <table class="table">
                <thead>
                <!-- 테이블 1행: 제목 -->
                <tr>
                  <th class="border-top-0" scope="col">진행상황</th>
                  <th class="border-top-0" scope="col">신청명</th>
                  <th class="border-top-0" scope="col"></th>
                  <th class="border-top-0" scope="col">작성일</th>
                  <th class="border-top-0" scope="col">검토일</th>
                  <th class="border-top-0" scope="col">입금일</th>
                </tr>
                </thead>
                <!-- 내가 신청한 예산내역 테이블 -->
                <tbody>
<!--                {% if my_bank_list|length == 0 %}-->
                <tr>
                  <td colspan="6" class="text-center">내가 작성한 예산신청 내역이 없습니다.</td>
                </tr>
<!--                {% endif %}-->
<!--                {% for my_bank in my_bank_list %}-->
                <tr>
                  <!-- 현재 상태 -->
<!--                  <td>{{ my_bank.bank_apply.bank_apply_name }}</td>-->
                  <td>승인</td>

                  <!-- 신청 제목 -->
<!--                  <td>{{ my_bank.bank_title }}</td>-->
                  <td>웹프로젝트 강의 결제</td>
                  <!-- 원글로 넘어가는 a태크 -->
                  <td>
<!--                    <a href="{% url 'bank_support_detail' bank_no=my_bank.bank_no %}">원문보기-->
                      <a href="#">원문보기
                        ▶</a>
                  </td>
                    <!-- 게시글 작성일 -->
<!--                  <td>{{ my_bank.bank_created|date:"Y-m-d" }}</td>-->
                  <td>2122-12-31</td>

                  <!-- 게시글 검토일 (총무가 승인, 거절 버튼을 누른 일자) 만약 아직 검토 전이면, '-'로 표기되어야 함. -->
<!--                  <td>{% if my_bank.bank_checked is not None %}-->
<!--                    {{ my_bank.bank_checked|date:"Y-m-d" }}{% else %}-->
<!--                    -{% endif %}-->
<!--                  </td>-->
                  <td>-</td>
                  <!-- 총무가 돈을 입금한 날 (아직 입금 전이면, '-'로 표기되어야 함. -->
<!--                  <td>{% if my_bank.bank_allowed is not None %}-->
<!--                    {{ my_bank.bank_allowed|date:"Y-m-d" }}{% else %}-->
<!--                    -{% endif %}-->
<!--                  </td>-->
                  <td>-</td>
                </tr>
<!--                {% endfor %}-->
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

  <!--===== 내가 신청한 예산내역 코드 끝 =====-->
</template>

<script>
export default {
  name: "MyBank.vue"
}
</script>

<style scoped>

</style>