<template>
  <div id="listing_myclass" class="tab-pane">
    <div class="row">
      <!--========================= 내가수강중인 강의 박스 =========================-->
      <!-- 만약 현재 내가 수강중인 강의가 없을 경우, 반스 전체가 안보이게끔 처리 필요 -->
      <div class="col-xl-12">
        <div class="content-box">
          <div class="content-header">
            <h3 class="title">내가 수강 중인 강의</h3>
          </div>
          <div class="content-body">
            <div class="row {% if my_lect_ing_list|length == 0 %}justify-content-center{% endif %}">
              <!--================= 여기부터 박스 내 게시글 반복시작 =================-->
              <!-- 게시글 1 -->
<!--              {% if my_lect_ing_list|length == 0 %}-->
              <p class="text-center">내가 수강 중인 강의가 없습니다.</p>
<!--              {% else %}-->
<!--              {% for my_lect_ing in my_lect_ing_list %}-->
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
                    <h3 class="title"><a
                        href="#">강의제목</a>
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
                        <strong>31일</strong>
<!--                        {% if my_lect_ing.lect_state.state_no == 4 %}-->
                        <span class="recruiting-end">완 강</span>
<!--                        {% elif my_lect_ing.lect_state.state_no == 3 %}-->
<!--                        {% if my_lect_ing.is_expired %}-->
                        <span class="recruiting-ing">진행중</span>
<!--                        {% else %}-->
                        <span class="recruiting">모집중</span>
<!--                        {% endif %}-->
<!--                        {% endif %}-->
                      </li>
                      <!-- 강의 내용에 대한 짧은 소개 -->
                      <li class="text-cut">안녕하세요
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
                        <span>금요일</span>
                        <!-- 강의 진행방식 Zoom 혹은 강의실 호수 -->
                        <span class="text-primary mr-3 m-l30"><i
                            class="ti-location-pin"></i></span>
                        <!-- 강의 진행방식을 DB에서 가져와야 함 -->
                        <span>오프라인</span>일
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
<!--              {% endfor %}-->
<!--              {% endif %}-->
            </div>
<!--            {# 페이지네이션 #}-->
            <div style="display: flex; justify-content: center; align-items: center">
              <nav aria-label="Page navigation example">
                <!-- staff_margin_bottom_0는 staff_cr.css에 정의되어 있음.  -->
                <ul class="pagination m-b0">
                  <li class="page-item"><a class="page-link" href="#">&lt;</a>
                  </li>
                  <li class="page-item"><a class="page-link" href="#">1</a>
                  </li>
                  <li class="page-item"><a class="page-link" href="#">&gt;</a>
                  </li>
                </ul>
              </nav>
            </div>
<!--            {# 페이지네이션 #}-->
          </div>
        </div>
      </div>
      <!--========================= 내가수강중인 강의 박스 끝 =========================-->
      <!--========================= 이미 수강한 강의 박스 시작 =========================-->
      <div class="col-xl-12">
        <div class="content-box">
          <div class="content-header">
            <h3 class="title">수강 완료한 강의</h3>
          </div>
          <div class="content-body">
            <div class="row">
              <!--================= 여기부터 박스 내 게시글 반복시작 =================-->
              <!-- 게시글 1 -->
<!--              {% if my_lect_fin_list|length == 0 %}-->
              <p>내가 수강 완료한 강의가 없습니다.</p>
<!--              {% else %}-->
<!--              {% for my_lect_fin in my_lect_fin_list %}-->
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
                      <a href="#">파이썬계산기</a>
                    </h3>
                    <!-- 강의 간단소개 -->
                    <ul class="event-meta">
                      <!-- 마감일 및 모집 상태 -->
                      <li class="event-date">
                        <!-- 강의 시작월 -->
                        <!-- 강의 모집 마감월이 아니라 시작월을 가져와야 함 -->
                        <span class="text-primary">11월</span>
                        <!-- 강의 시작일 -->
                        <!-- 강의 모집 마감일이 아니라 시작일을 가져와야 함 -->
                        <strong>12일</strong>
<!--                        {% if my_lect_fin.lect_state.state_no == 4 %}-->
                        <span class="recruiting-end">완 강</span>
<!--                        {% elif my_lect_fin.lect_state.state_no == 3 %}-->
<!--                        {% if my_lect_fin.is_expired %}-->
                        <span class="recruiting-ing">진행중</span>
<!--                        {% else %}-->
                        <span class="recruiting">모집중</span>
<!--                        {% endif %}-->
<!--                        {% endif %}-->
                      </li>
                      <!-- 강의 내용에 대한 짧은 소개 -->
                      <li class="text-cut">ㅎㅇ
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
                        <span>일요일</span>
                        <!-- 강의 진행방식 Zoom 혹은 강의실 호수 -->
                        <span class="text-primary mr-3 m-l30"><i
                            class="ti-location-pin"></i></span>
                        <!-- 강의 진행방식을 DB에서 가져와야 함 -->
                        <span>줌</span>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
<!--              {% endfor %}-->
<!--              {% endif %}-->
            </div>
            <div style="display: flex; justify-content: center; align-items: center">
              <nav aria-label="Page navigation example">
                <!-- staff_margin_bottom_0는 staff_cr.css에 정의되어 있음.  -->
                <ul class="pagination m-b0">
                  <li class="page-item"><a class="page-link" href="#">&lt;</a>
                  </li>
                  <li class="page-item"><a class="page-link" href="#">1</a>
                  </li>
                  <li class="page-item"><a class="page-link" href="#">&gt;</a>
                  </li>
                </ul>
              </nav>
            </div>
          </div>
        </div>
      </div>
      <!--========================= 과거 수강한 강의 박스  =========================-->
    </div>
  </div>
</template>

<script>
export default {
  name: "MyClass.vue"
}
</script>

<style scoped>

</style>