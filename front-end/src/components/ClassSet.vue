<template>
  <!--개설강의 관리-->

    <div class="row">
      <div class="col-xl-12">
        <div class="content-box">
          <div class="content-header">
            <h3 class="title">개설 강의 관리</h3>
          </div>
          <div class="content-body">
            <div class="row {% if my_lect_made_list|length == 0 %}justify-content-center{% endif %}">
              <!--================= 여기부터 박스 내 게시글 반복시작 =================-->
              <!-- 게시글 1 -->
<!--              {% if my_lect_made_list|length == 0 %}-->
              <p class="text-center">내가 개설한 강의가 없습니다.</p>
<!--              {% else %}-->
<!--              {% for my_lect_made in my_lect_made_list %}-->
              <div class="col-lg-4 col-md-6 col-sm-6">
                <div class="listing-bx event-listing m-b10">
                  <!-- 게시글 대표 이미지 -->
                  <!-- 이미지를 클릭하면, 해당 게시글로 이동함 -->
                  <a href="#">
                    <img style="height: 200px; width: 100%"
                         src="/media/"
                         alt="">
                  </a>
                  <!-- 강의 제목 및 간단소개 div -->
                  <div class="listing-info" style="height: 110px">
                    <!-- 강의제목 -->
                    <!-- 제목 클릭 시, 해당 게시글로 이동 -->
                    <h3 class="title">
                      <a href="#">강의 제목</a>
                    </h3>
                    <!-- 강의 간단소개 -->
                    <ul class="event-meta">
                      <!-- 마감일 및 모집 상태 -->
                      <li class="event-date">
                        <!-- 강의 시작월 -->
                        <!-- 강의 모집 마감월이 아니라 시작월을 가져와야 함 -->
                        <span class="text-primary">12월</span>
                        <!-- 강의 시작일 -->
                        <!-- 강의 모집 마감일이 아니라 시작일을 가져와야 함 -->
                        <strong>31</strong>
<!--                        {% if my_lect_made.lect_state.state_no == 4 %}-->
                        <span class="recruiting-end">종 강</span>
<!--                        {% elif my_lect_made.lect_state.state_no == 3 %}-->
<!--                        {% if my_lect_made.is_expired %}-->
                        <span class="recruiting-ing">진행중</span>
<!--                        {% else %}-->
                        <span class="recruiting">모집중</span>
<!--                        {% endif %}-->
<!--                        {% elif my_lect_made.lect_state.state_no == 2 %}-->
                        <span class="recruiting-end">거절됨</span>
<!--                        {% else %}-->
                        <span class="recruiting-wait">대기중</span>
<!--                        {% endif %}-->


                      </li>
                      <!-- 강의 내용에 대한 짧은 소개 -->
                      <li class="text-cut">강의 내용에 대한 짧은 소개
                      </li>
                    </ul>
                  </div>
                  <div class="event-bottom">
                    <ul>
                      <!-- 강의 요일, 장소, 인원 li-->
                      <li class="event-hosted">
                        <!-- 강의를 정기적으로 진행하는 요일 -->
                        <span class="text-primary mr-3">요일</span>
                        <!-- 강의에 해당하는 요일을 DB에서 가져와야 함 -->
                        <span>화</span>
                        <!-- 강의 진행방식 Zoom 혹은 강의실 호수 -->
                        <span class="text-primary mr-3 m-l30"><i
                            class="ti-location-pin"></i></span>
                        <!-- 강의 진행방식을 DB에서 가져와야 함 -->
                        <span>오프라인</span>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
<!--              {% endfor %}-->
<!--              {% endif %}-->
            </div>
          </div>
        </div>
      </div>
    </div>

</template>

<script>
export default {
  name: "ClassSet.vue"
}
</script>

<style scoped>

</style>