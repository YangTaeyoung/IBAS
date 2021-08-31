<template>
  <!--내정보-->
  <div id="listing_my_info" class="tab-pane active">
    <div class="row">
      <div class="col-xl-12">
        <div class="content-box">
          <!--내 정보 상세보기란-->
          <!--제목부분-->
          <div class="content-header">
            <h3 class="title"><i class="la la-user"></i>내정보 상세보기</h3>
          </div>
          <!--내용부분-->
          <div class="content-body">
            <table class="table" style="margin-top: 30px; width: 95%; margin-left: 2.5%">
              <tbody>
              <!--이름-->
              <tr>
                <th scope="row">이름</th>
                <!-- Back : 자기 이름 뜨도록 수정 -->
                                <td>{{ response.data.logined_user.user_name }}</td>
<!--                <td>윤예진</td>-->
                <!-- 수정하기 버튼, 누르면 모달 뜸 -->
                <td>
                  <!--                  {% if my_wait_request|length == 0 %} {# 이름 변경 신청한 것이 없는 경우 #}-->
                  <a href="javascript:void(0);" data-toggle="modal"
                     data-target="#name_edit"><i class="la la-pencil"></i></a>
                  <!--                  {% else %} {# 이미 이름 변경 신청을 한 경우 #}-->
                  <!-- 이 부분 클릭하면 변경 신청했던 내역 모달 떠서 보게 해주세요. -->
                  <!--                  <a href="javascript:void(0);" data-toggle="modal"-->
                  <!--                     data-target="#name_edit_list">이름 신청 이력 보기</a>-->
                  <!--                  {% endif %}-->
                </td>
              </tr>
              <!--학번-->
              <tr>
                <th scope="row">학번</th>
                <!--Back : 자기 학번 뜨도록 수정-->
                <!--                <td>{{ logined_user.user_stu }}</td>-->
                <td>12192355</td>
                <td></td>
              </tr>
              <!--학과-->
              <tr>
                <th scope="row">학과</th>
                <!--Back : 자기 학과 뜨도록 수정-->
                <!--                <td>{{ logined_user.user_major.major_name }}</td>-->
                <td>글로벌금융학과</td>
                <!--수정하기 버튼, 누르면 모달 뜸-->
                <td>
                  <a href="javascript:void(0);" data-toggle="modal"
                     data-target="#major_edit"><i class="la la-pencil"></i></a>
                </td>
              </tr>
              <!--학년-->
              <!--              {% if logined_user.user_grade != 5 %}-->
              <tr>
                <th scope="row">학년</th>
                <!--Back : 자기 학년 뜨도록 수정-->
                <!--                {% if logined_user.user_grade == 0 %}-->
                <td><span style="color:#1d61aa;">IBAS</span>에서 졸업해주셔서 감사합니다.
                </td>
                <!--                {% else %}-->
                <!--                <td>{{ logined_user.user_grade }}학년</td>-->
                <!--                <td>3학년</td> -->
                <!--                {% endif %}-->
                <td>
                  <a href="javascript:void(0);" data-toggle="modal"
                     data-target="#grade_edit"><i class="la la-pencil"></i></a>
                </td>
              </tr>
              <!--              {% endif %}-->
              <!--이메일-->
              <tr>
                <th scope="row">이메일</th>
                <!--Back : 자기 이메일 번호 뜨도록 수정-->
                <!--                <td>{{ request.session.logined_email }}</td>-->
                <td>abcdefghijk@gmail.com</td>
                <td></td>
              </tr>
              <!--전화번호-->
              <tr>
                <th scope="row">전화번호</th>
                <!--Back : 자기 핸드폰 번호 뜨도록 수정-->
                <!--                <td>{{ logined_user.user_phone }}</td>-->
                <td>010-9999-9999</td>
                <!--수정하기 버튼, 누르면 모달 뜸-->
                <td>
                  <a href="javascript:void(0);" data-toggle="modal"
                     data-target="#phone_edit"><i class="la la-pencil"></i></a>
                </td>
              </tr>
              <!--승인상태-->
              <tr>
                <th scope="row">권한</th>
                <!--Back : 승인 안되면 미승인, 승인되면 승인 뜨도록 수정-->
                <!--                <td>{{ logined_user.user_auth.auth_name }}</td>-->
                <td>미승인</td>
                <td>
                  <!--                  {% if logined_user.user_auth.auth_no == 2 %}-->
                  <!--                  <a href="{% url 'user_activate_request' %}"-->
                  <a href="#"
                     onclick="alert('회비 납부 확인 요청이 완료되었습니다. \n\n순차적으로 확인하고 있으니 더 이상 요청하지 말아주세요.')">
                    회비 납부 확인 요청
                  </a>
                  <!--                  {% endif %}-->
                </td>
              </tr>
              <!--권한-->
              <tr>
                <th scope="row">역할</th>
                <!--                {# Back : 회장이면 회장, 부회장이면 부회장 ...... 일반회원이면 일반회원으로 뜨도록 수정 #}-->
                <!--                <td>{{ logined_user.user_role.role_name }}</td>-->
                <td>일반회원</td>

                <td>
                  <!--                  {# 회장, 부회장에게만 노출 #}-->
                  <!--                  {% if logined_user.user_role.role_no <= 2 %}-->
                  <!--                  <a href="{% url 'management' %}">관리자 페이지</a>-->
                  <a href="#">관리자 페이지</a>
                  <!--                  {% endif %}-->
                </td>
              </tr>
              <!--이름-->
              <tr>
                <th scope="row">자기소개</th>
                <!--                {# Back : 자기 소개 뜨도록 수정, 등록 안돼있으면 아래 내용 뜨도록 #}-->
                <!--                {% if logined_user.user_intro %}-->
                <td style="width: 50%">
                  <!--                  {{ logined_user.user_intro|linebreaksbr }} &nbsp;&nbsp;&nbsp;-->
                  ㅎㅇㅎㅇ &nbsp;&nbsp;&nbsp;
                  <!--                  {% if logined_user.user_apply_publish == 1 %}-->
                  <span style="color:#00a834">(공개됨)</span>
                  <!--                  {% else %}-->
                  <span style="color:red">(비공개됨)</span>
                  <!--                  {% endif %}-->
                </td>
                <!--                {% else %}-->
                <!--                <td style="width: 50%">-->
                <!--                  아직 등록된 자기소개가 없습니다.-->
                <!--                </td>-->
                <!--                {% endif %}-->
                <!-- 수정하기 버튼, 누르면 모달 뜸 -->
                <td>
                  <a href="javascript:void(0);" data-toggle="modal"
                     data-target="#self_intro_edit"><i class="la la-pencil"></i></a>
                </td>
              </tr>
              <!--아래 선 하나 더 보이게 추가한 곳-->
              <tr>
                <th></th>
                <td></td>
                <td></td>
              </tr>
              </tbody>
            </table>
            <!--회원탈퇴 버튼-->
            <!--            {% if is_superuser or is_cfo %}-->
            <div class="clearfix text-center">
              <p class="my_info_modal_content"><i class="la la-check"></i>
                회장단의 경우 권한이 이양되기 전까지 회원탈퇴를 할 수 없습니다. 회장에게 권한 이양을 요청하세요</p>
            </div>
            <!--            {% else %}-->
            <ol class="comment-list">
              <li class="comment">
                <div class="comment-body">
                  <div class="reply"><a href="javascript:void(0);"
                                        class="comment-reply-link"
                                        data-toggle="modal"
                                        data-target="#withdrawal">회원탈퇴</a></div>
                </div>
              </li>
            </ol>
            <!--            {% endif %}-->
          </div>
        </div>
        <div class="content-box">
          <div class="content-header">
            <h3 class="title"><i class="la la-share"></i>계정연동</h3>
          </div>
          <!--계정연동 버튼들, Back : 주석보고 각 조건에 맞게 해당하는 버튼만 뜨도록 수정-->
          <div class="content-body">
            <!--구글 계정으로 로그인하였을 때-->
            <!--네이버 계정 연동 안했을 때-->
            <form id="form-connect-social-account" class="dlab-form m-t10"
                  action="#" method="post">
              <!--            action="{% url 'connect_social_account_before_setting' %}" method="post">-->

              <!--              {% csrf_token %}-->
              <div class="text-center m-b10">
                <!--                {% if request.session.provider == "google" and is_google_existed %}-->
                <div href="#" class="site-button bg-secondary" style="width: 45%">
                  <i class="fa fa-google m-r10"></i>
                  구글 계정으로 로그인하였습니다.
                </div>

                <!--Back : 누르면 구글계정 연동하는 창으로 이동하도록 수정-->
                <!--                {% elif request.session.provider != "google" and is_google_existed %}-->
                <div href="#" class="site-button bg-secondary" style="width: 45%">
                  <i class="fa fa-google m-r10"></i>
                  구글 계정이 연동되어 있습니다.
                </div>
                <!--                {% else %}-->
                <a href="#"
                   class="site-button google-plus btn-block"
                   style="width: 45%"
                   onclick="document.getElementById('form-connect-social-account').submit()">
                  <i class="fa fa-google m-r10"></i>
                  구글 계정 연동하기
                </a>
                <input type="hidden" name="provider" value="google"/>
                <!--                {% endif %}-->
                <!--Back : 누르면 네이버 계정 연동하는 창으로 이동하도록 수정-->
                <!--                {% if request.session.provider == "naver" and is_naver_existed %}-->
                <div href="#" class="site-button bg-secondary"
                     style="width: 45%; margin-left: 20px">
                  <span class="naver-logo m-r10">N</span>
                  네이버 계정으로 로그인하였습니다.
                </div>
                <!--                {% elif request.session.provider != "naver" and is_naver_existed %}-->
                <div href="#" class="site-button bg-secondary"
                     style="width: 45%; margin-left: 20px">
                  <span class="naver-logo m-r10">N</span>
                  네이버 계정이 연동되어 있습니다.
                </div>
                <!--                {% else %}-->
                <a href="#"
                   class="site-button whatsapp btn-block"
                   style="width: 45%; margin-left: 20px"
                   onclick="document.getElementById('form-connect-social-account').submit()">
                  <span class="naver-logo m-r10">N</span>
                  네이버 계정 연동하기</a>
                <input type="hidden" name="provider" value="naver"/>
                <!--                {% endif %}-->

              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- 이름 수정 Modal -->
    <div class="modal fade modal-bx-info modal-lg" id="name_edit" tabindex="-1" role="dialog"
         aria-labelledby="ReportReviewsModalLongTitle" aria-hidden="true">
      <div class="modal-dialog " role="document">
        <div class="modal-content">
          <!--제목부분-->
          <div class="modal-header">
            <!--            <h5 class="modal-title" id="ReportReviewsModalLongTitle">이름수정</h5>-->
            <h5 class="modal-title" id="ReportReviewsModalLongTitle_1">이름수정</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true"><i class="la la-close"></i></span>
            </button>
          </div>
          <!--내용부분-->
          <div class="modal-body">
            <form id="form-user-update-request"
                  action="#" class="dlab-form"
                  method="post">
              <!--              action="{% url 'user_update_request_register' %}" class="dlab-form"-->

              <!--              {% csrf_token %}-->
              <!--수정설명 부분-->
              <div class="clearfix">
                <p class="my_info_modal_content"><i class="la la-check"></i>이름은 회장의 승인을
                  통하여 수정할 수 있습니다. </p>
              </div>
              <!--수정할 이름 적는 부분-->
              <div class="form-group">
                <input name="updated_user_name" required="required" class="form-control"
                       placeholder="수정하고 싶은 이름을 적어주세요" type="text"/>
              </div>
              <!--수정신청하기 버튼, Back : 누르면 회장에게 승인을 요구하도록 수정-->
              <a href="#" class="site-button"
                 style="display: grid; justify-items: center;"
                 onclick="goSubmit('form-user-update-request', true,'수정신청하시겠습니까?')">수정신청</a>
            </form>
          </div>
        </div>
      </div>
    </div>
    <!-- Modal End -->

    <!-- 이름 수정 신청 내역 Modal -->
    <div class="modal fade modal-bx-info modal-lg" id="name_edit_list" tabindex="-1" role="dialog"
         aria-labelledby="ReportReviewsModalLongTitle" aria-hidden="true">
      <div class="modal-dialog " role="document">
        <div class="modal-content">
          <!--제목부분-->
          <div class="modal-header">
            <h5 class="modal-title" id="ReportReviewsModalLongTitle_2">이름 수정 신청 이력</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true"><i class="la la-close"></i></span>
            </button>
          </div>
          <!--내용부분-->
          <div class="modal-body">
            <table class="table">
              <thead>
              <tr>
                <th scope="col" style="text-align: center">신청일</th>
                <th scope="col" style="text-align: center">기존이름</th>
                <th scope="col" style="text-align: center">신청이름</th>
                <th scope="col" style="text-align: center">상태</th>
              </tr>
              </thead>
              <!--신청이력 뜨는 부분-->
              <tbody>
              <!--              {% for my_update_request in my_update_request_list %}-->
              <tr>
                <!--신청 날짜 뜨는 부분, back : 신청일 뜨도록 수정-->
                <!--                <td style="text-align: center">{{ my_update_request.updated_date|date:"Y-m-d h:i" }}</td>-->
                <td style="text-align: center">2021-12-31 11:22</td>

                <!--기존 이름 뜨는 부분, back : 기존 이름 뜨도록 하고, 이름 변경되도 내역에는 남아있도록,,-->
                <!--                <td style="text-align: center">{{ my_update_request.updated_user.user_name }}</td>-->
                <td style="text-align: center">윤예진</td>
                <!--새롭게 신청한 이름 뜨는 부분, back : 신청한 이름 뜨도록 하고, 이름 재수정시에 바뀌지 않고 그대로 있도록-->
                <!--                <td style="text-align: center">{{ my_update_request.updated_user_name }}</td>-->
                <td style="text-align: center">진예윤</td>
                <!--승인 상태 나타내는 부분, back : 승인되면 '승인', 승인 대기중이면 '대기' 뜨도록-->
                <!--                <td style="text-align: center">{{ my_update_request.updated_state.state_name }}</td>-->
                <td style="text-align: center">승인</td>
              </tr>
              <!--              {% endfor %}-->
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    <!-- Modal End -->

    <!-- 학과 수정 Modal -->
    <div class="modal fade modal-bx-info modal-lg" id="major_edit" tabindex="-1" role="dialog"
         aria-labelledby="ReportReviewsModalLongTitle" aria-hidden="true">
      <div class="modal-dialog " role="document">
        <div class="modal-content">
          <!--제목부분-->
          <div class="modal-header">
            <h5 class="modal-title" id="ReportReviewsModalLongTitle_3">학과수정</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true"><i class="la la-close"></i></span>
            </button>
          </div>
          <!--내용부분-->
          <div class="modal-body">
            <form id="id-form-user-major-update" class="dlab-form"
                  action="#" method="post">
              <!--              action="{% url 'user_major_update' %}" method="post">-->

              <!--              {% csrf_token %}-->
              <!--일단 input창으로 해둠, Back : 학과선택할 수 있는 창 뜰 수 있도록 수정-->
              <div class="form-group" style="display: grid">
                <a href="javascript:void(0);" data-toggle="modal"
                   data-target="#search_major" style="display: flex">
                  <i class="la la-search m-t10 m-r10"></i>
                  <input id="user_major" name="user_major" class="form-control"
                         placeholder="전공을 검색하려면 클릭하세요" type="text"
                         style="width: 95%"/>
                </a>
              </div>
              <!--수정하기 버튼, Back : 누르면 내정보에 반영되도록 수정-->
              <a href="#" class="site-button"
                 style="display: grid; justify-items: center;"
                 onclick="goSubmit('id-form-user-major-update')">수정</a>
            </form>
          </div>
        </div>
      </div>
    </div>
    <!-- Modal End -->

    <!-- 이름 수정 Modal -->
    <div class="modal fade modal-bx-info modal-lg" id="grade_edit" tabindex="-1" role="dialog"
         aria-labelledby="ReportReviewsModalLongTitle" aria-hidden="true">
      <div class="modal-dialog " role="document">
        <div class="modal-content">
          <!--제목부분-->
          <div class="modal-header">
            <h5 class="modal-title" id="ReportReviewsModalLongTitle_4">학년수정</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true"><i class="la la-close"></i></span>
            </button>
          </div>
          <!--내용부분-->
          <div class="modal-body">
            <form id="form-user-grade-update"
                  action="#" class="dlab-form"
                  method="post">
              <!--              action="{% url 'user_grade_update' %}" class="dlab-form"-->
              <!--              {% csrf_token %}-->
              <select class="mb-4" name="user_grade">
                <!--                <option name="user_grade" value="{{ logined_user.user_grade }}">학년선택-->
                <option name="user_grade" value="#">학년선택
                </option>
                <option name="user_grade" value="1">1학년</option>
                <option name="user_grade" value="2">2학년</option>
                <option name="user_grade" value="3">3학년</option>
                <option name="user_grade" value="4">4학년 이상</option>
                <option name="user_grade" value="0">졸업</option>
              </select>
              <a href="#" class="site-button"
                 style="display: grid; justify-items: center;"
                 onclick="goSubmit('form-user-grade-update')">수정</a>
            </form>
          </div>
        </div>
      </div>
    </div>
    <!-- Modal End -->

    <!-- 전공 검색 Modal -->
    <div class="modal fade modal-bx-info modal-lg" id="search_major" tabindex="-2" role="dialog"
         aria-labelledby="ReportReviewsModalLongTitle" aria-hidden="true" style="width: 100%">
      <div class="modal-dialog " role="document">
        <div class="modal-content">
          <!--제목부분-->
          <div class="modal-header">
            <h5 class="modal-title" id="ReportReviewsModalLongTitle_5">전공 검색</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true"><i class="la la-close"></i></span>
            </button>
          </div>
          <!--내용부분-->
          <div class="modal-body">
            <div class="card-body" style="width: 100%; height: 300px;">
              <!-- 검색 영역 -->
              <div class="searchBox" style="width: 100%;">
                <input class="form-control" type="text" id="search_1" onkeyup="filter()"
                       placeholder="전공을 검색하세요"/>
              </div>
              <!-- 전공 리스트 영역 -->
              <div class="listBox" style="width: 100%;">
                <table class="table table-hover">
                  <thead>
                  <tr>
                    <th>학교명</th>
                    <th>단과대학</th>
                    <th>학과명</th>
                  </tr>
                  </thead>
                  <tbody>
                  <!--전공 리스트를 단과대학, 학과명 순으로 가져옴-->
                  <!--                  {% for major in major_list %}-->
                  <!--                  <tr class="listInner"-->
                  <!--                    onclick="printResult({{ major.major_no }})">-->
                  <!--                    <td class="colleges">{{ major.major_colleage }}</td>-->
                  <!--                    <td class="major_names" id="major_name_{{ major.major_no }}"></td>-->
                  <!--                    <td class="major_names" id="major_name_1"-->
                  <!--                        data-dismiss="modal"-->
                  <!--                        aria-label="Close">{{ major.major_name }}-->
                  <!--                    </td>-->
                  <!--                  </tr>-->
                  <!--                  {% endfor %}-->
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Modal End -->
    <!-- 전공 검색 팝업창 -->
    <div id="major-search-popup" class="card major-search-popup ">
      <div class="card-header"
           style="display: flex; align-items: center; justify-content: space-between">
        <h4 class="m-b0"> 전공 검색 </h4>
        <!-- 닫기 버튼 -->
        <i class="fa fa-close fa-2x btn-exit" onclick="popDown()"></i>
      </div>
      <div class="card-body">

        <!-- 검색 영역 -->
        <div class="searchBox">
          <input class="form-control" type="text" id="search" onkeyup="filter()"
                 placeholder="전공을 입력하세요"/>
        </div>
        <!-- 전공 리스트 영역 -->
        <div class="listBox">
          <table class="table table-hover">
            <thead>
            <tr>
              <th>학교명</th>
              <th>단과대학</th>
              <th>학과명</th>
            </tr>
            </thead>
            <tbody>
            <!--전공 리스트를 단과대학, 학과명 순으로 가져옴-->
            <!--            {% for major in major_list %}-->
            <!--            <tr class="listInner" onclick="printResult({{ major.major_no }})">-->
            <!--              <td class="colleges">{{ major.major_colleage }}</td>-->
            <!--              <td id="major_name_{{ major.major_no }}"></td>-->
            <!--              <td id="major_name_2"-->
            <!--                class="major_names">{{ major.major_name }}-->
            <!--              </td>-->
            <!--            </tr>-->
            <!--            {% endfor %}-->
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <!-- 전화번호 수정 Modal -->
    <div class="modal fade modal-bx-info modal-lg" id="phone_edit" tabindex="-1" role="dialog"
         aria-labelledby="ReportReviewsModalLongTitle" aria-hidden="true">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <!--제목부분-->
          <div class="modal-header">
            <h5 class="modal-title" id="ReportReviewsModalLongTitle_6">전화번호수정</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true"><i class="la la-close"></i></span>
            </button>
          </div>
          <!--내용부분-->
          <div class="modal-body">
            <form id="update-phone-number" class="dlab-form">
              <!--              {% csrf_token %}-->
              <!--수정할 전화번호 입력창, Back : 입력하면 전화번호 중복체크 하도록 수정-->
              <div class="form-group pb-0 mb-1">
                <input id="user_phone" name="user_phone" class="form-control"
                       placeholder="수정하고 싶은 전화번호을 적어주세요" type="tel"
                       maxlength="13"
                       required="required"
                       onkeyup="inputPhoneNumber(this)"
                />
              </div>
              <p id="error_text_phone" class="mx-auto font-10 m-0 p-0"
                 style="color:red; display: none"></p>
              <input type="submit" class="site-button" style="width: 100%"
                     onclick='return phone_check("#");' value="수정">
              <!--              onclick='return phone_check("{% url "user_phone_update" %}");' value="수정">-->

            </form>
          </div>
        </div>
      </div>
    </div>
    <!-- Modal End -->
    <!-- 자기소개 수정 Modal -->
    <div class="modal fade modal-bx-info modal-lg" id="self_intro_edit" tabindex="-1" role="dialog"
         aria-labelledby="ReportReviewsModalLongTitle" aria-hidden="true">
      <div class="modal-dialog " role="document">
        <div class="modal-content">
          <!--제목부분-->
          <div class="modal-header">
            <h5 class="modal-title" id="ReportReviewsModalLongTitle_7">자기소개</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true"><i class="la la-close"></i></span>
            </button>
          </div>
          <!--내용부분-->
          <div class="modal-body">
            <form id="form-user-intro-update"
                  action="#" class="dlab-form"
                  method="post">
              <!--              action="{% url 'user_intro_update' %}" class="dlab-form"-->

              <!--              {% csrf_token %}-->
              <div class="form-group">
                <!--소개 공개 동의 체크박스 부분-->
                <div class="input-block">
                  <p class="my_info_modal_content"><i class="la la-check"></i>자기소개 공개에
                    동의하시면 졸업 후 졸업생 명예의 전당에 정보가 공개됩니다.</p>
                  <!--                  {% if logined_user.user_apply_publish == 1 %}-->
                  <input id="intro_open_1" name="user_apply_publish" type="checkbox"
                         value="1" checked="checked"/>
                  <!--                  {% else %}-->
                  <input id="intro_open_2" name="user_apply_publish" type="checkbox"
                         value="1"/>
                  {% endif %}
                  <label for="intro_open_1">자기소개 공개에 동의합니다.</label>
                </div>
                <hr/>
                <!--설명 내용 수정 부분-->
                <textarea name="user_intro" required="required"
                          class="form-control"
                          placeholder="간단한 본인 소개를 적어주세요">ㅎㅇㅎㅇ</textarea>
                <!--                placeholder="간단한 본인 소개를 적어주세요">{% if logined_user.user_intro %}{{ logined_user.user_intro }}{% endif %}</textarea>-->
              </div>
              <!--수정신청하기 버튼, Back : 누르면 회장에게 승인을 요구하도록 수정-->
              <a href="#" class="site-button"
                 style="display: grid; justify-items: center;"
                 onclick="goSubmit('form-user-intro-update')">수정</a>
            </form>
          </div>
        </div>
      </div>
    </div>
    <!-- Modal End -->

    <!--    {% if not is_superuser and not is_cfo %}-->
    <div class="modal fade modal-bx-info modal-lg" id="withdrawal" tabindex="-1" role="dialog"
         aria-labelledby="ReportReviewsModalLongTitle" aria-hidden="true">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="ReportReviewsModalLongTitle">회원탈퇴</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true"><i class="la la-close"></i></span>
            </button>
          </div>
          <div class="modal-body">
            <!--            <form class="dlab-form" action="{% url 'user_withdrawal' %}" method="post">-->
            <form class="dlab-form" action="#" method="post">
              <!--                {% csrf_token %}-->
              <div class="form-group pb-0 mb-1">
                <input type="hidden" name="user_stu"
                       value="12192355"
                       class="form-control"/>
                <!--                value="{{ logined_user.user_stu }}"-->
                <h6 class="mb-3"> 회원님과 관련된 모든 데이터가
                  삭제되며, 어떤 경우라도 복구가 불가능함을 알립니다. <br/>이에 동의합니까? </h6>
                <input id="agreement" class="form-check" type="checkbox"
                       name="agreement" value="1" required="required"
                       onchange="document.getElementById('btn-withdrawal').disabled= !document.getElementById('btn-withdrawal').disabled;"/>
                <label class="font-16 mb-4" for="agreement">네, 모든 사실을 인지하였으며, 그럼에도
                  탈퇴하길 원합니다.</label>
                <!--                {# 체크박스를 만들땐 라벨 태그를 뒤에 두자. #}-->

                <p class="font-13" style="color: red; line-height: 120%;"> 예외: <b>예산을
                  등록한 이력이 있는 회원, 예산 지원신청을 한 이력이 있는 회원, 동아리 연혁을 작성한 회원, 공지사항을 작성한
                  회원, 공모전 게시판 게시글을 작성한 회원, 활동 게시판 게시글을 작성한 회원</b>의 경우 데이터 무결성을 위해
                  학번 및 이름을 남기고 삭제됩니다. </p>
              </div>
              <div class="d-flex justify-content-center">
                <button id="btn-withdrawal" class="btn btn-danger" type="submit"
                        disabled="disabled">회원 탈퇴
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <!--    {% endif %}-->
    <!-- Modal End -->


  </div>
</template>

<script>
export default {
  name: "MyProfile.vue"
}
</script>

<style scoped>

</style>