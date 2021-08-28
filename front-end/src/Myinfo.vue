<template>
  <div id="my-info">
    <!-- inner page banner -->
    <!--    <img src='../../../my_info/static/images/myinfo_bg.jpg' alt="" style="height: 20%; width: 100%; overflow: hidden">-->
    <!-- inner page banner END -->
    <div class="listing-details-head">
      <div class="container">
        <div class="listing-info-box">
          <!--프로필 사진, Back : 본인 프로필 사진 나오도록 수정-->
          <div class="listing-theme-logo">
            <img src="/media/{{ logined_user.user_pic }}" alt="" class="bg-white"
                 style="max-width: 130px; max-height: 130px; min-width: 130px; min-height: 130px;">
          </div>
          <div class="listing-info">
            <!--이름, 학과, 학번 표시되는 곳, Back : 본인 이름, 학과, 한번 들어갈 수 있도록 수정-->
            <div class="listing-info-left">
              <!--            <h3 class="title">{{ logined_user.user_name }}</h3>-->
              <h3 class="title">윤예진</h3>
              <p>글로벌금융학과 &#8226; 12192355</p>
              <!--              <p>{{ logined_user.user_major.major_name }} &#8226; {{ logined_user.user_stu }}</p>-->

            </div>
            <!--상단 오른쪽에 뜨는버튼 버튼-->
            <div class="listing-info-right">
              <!--              <div class="listing-info-right" v-if="logined_user.user_role.role_no <= 4">-->

              <!--회원관리, 회장단만 보이게, 상단바에 배치랑 고민헤볼것-->
              <a href="#" class="site-button m-r5"><i
                  class="la la-users m-r5"></i>회원관리</a>
              <!--사진변경-->
              <a href="javascript:void(0);" data-toggle="modal" data-target="#photo_edit"
                 class="site-button purple m-r5"><i class="la la-photo m-r5"></i>사진변경</a>
              <!--사진삭제-->
              <a href="javascript:void(0);" class="site-button gray"
                 onClick="goSubmit('form-user-pic-delete')"><i class="la la-trash m-r5"></i>사진삭제</a>
              <form id="form-user-pic-delete" action="#" method="post">
                <!--              {% csrf_token %}-->
                <input type="hidden" name="user_stu" value="{{ logined_user.user_stu }}">
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 사진 수정 Modal -->
    <div class="modal fade modal-bx-info modal-lg" id="photo_edit" tabIndex="-1" role="dialog"
         aria-labelledby="ReportReviewsModalLongTitle" aria-hidden="true">
      <div class="modal-dialog " role="document">
        <div class="modal-content">
          <div class="modal-header">
            <!--상단 제목부분-->
            <h5 class="modal-title" id="ReportReviewsModalLongTitle">프로필 사진 수정</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true"><i class="la la-close"></i></span>
            </button>
          </div>

          <!--내용부분, 이미지 첨부하는 곳 들어감, Back : 가능하면....원래 사진 뜰 수 있도록 수정, 어려우면 없어도 될듯-->
          <div class="modal-body">
            <form id="form-user-pic-update" action="#" method="post"
                  class="dlab-form" encType="multipart/form-data">
              <!--            {% csrf_token %}-->
              <div class="content-body">
                <div class="form-group" style="margin-bottom: 4px">
                  <input
                      type="file"
                      name="user_pic"
                      accept="image/*"
                      required="required"
                      multiple
                  />
                </div>
                <p style="color: red; font-size: 8pt; text-align: center;">여러 개의 파일 첨부 시 마지막 파일만
                  반영됩니다.</p>
              </div>
              <!--수정버튼, Back : 누르면 프로필 사진에 반영되도록 수정-->
              <a href="#" class="site-button" style="display: grid; justify-items: center;"
                 onClick="">수정</a>
            </form>
          </div>
        </div>
      </div>
    </div>
    <!-- Modal End -->
  </div>
  <!--마이인포의 상단 메뉴부분 해당 버튼 누르면 해당하는 곳으로 이동,Back : 각 메뉴에 따라 권한자만 보이게 수정-->
  <div class="listing-details-nav">
    <div class="container">
      <ul class="listing-nav nav">
        <!--강의실 메뉴버튼,Back : 모두에게 보이게 수정-->
          <li><router-link to="/my_info/myClass" data-toggle="tab"><i
              class="la la-home"></i><span>강의실</span></router-link></li>
        <!--개설강의 메뉴버튼,Back : 강의자만 보이게 수정-->
          <li><router-link to="/my_info/classSet" data-toggle="tab"><i
              class="la la-book"></i><span>개설 강의 관리</span></router-link>
          </li>
        <!--작성들관리 메뉴버튼,Back : 모두에게 보이게 수정-->
          <li><router-link to="/my_info/myContent" data-toggle="tab"><i
              class="la la-list-alt"></i><span>작성 글 관리</span></router-link>
          </li>
        <!--예산신청내역 메뉴버튼,Back : 모두에게 보이게 수정-->

          <li><router-link to="/my_info/myBank" data-toggle="tab"><i class="la la-money"></i><span>예산 신청 내역</span></router-link>
          </li>
        <!--내정보 메뉴버튼,Back : 모두에게 보이게 수정-->
          <li><router-link to="/my_info/test/" data-toggle="tab" class="active"><i
              class="la la-user"></i><span>내 정보</span></router-link>
          </li>
      </ul>
    </div>
  </div>

  <!-- 버튼누르면 보여지는 곳 목록-->
  <div class="section-full listing-details-content">
    <div class="container">
      <!--강의실, 모두에게 보임-->
      <div class="tab-content">
        <router-view/>

      </div>
    </div>
  </div>
</template>

<script>

import axios from "axios";

axios.defaults.baseURL = 'http://localhost:8000/';


export default {
  props: ['sendLoginedUser', 'sendUserPic', 'sendUserName', 'sendUserMajor', 'sendUserStu', 'sendUserRole', 'sendMajorName',],
  name: "Myinfo.vue",

  data: () => {
    return {
      // isDisabled: true,
      logined_user: null,
      user_pic: null,
      user_name: null,
      // user_major: null,
      // user_stu: null,
      // user_role: null,
      // major_name: null,

    };
  },
}
</script>

