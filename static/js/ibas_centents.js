// ================================== bank 관련 js ========================================= //
//수정 아이콘을 클릭하면 등록 아이콘으로 바뀌고, 등록 아이콘을 클릭했을 때 메세지 뜨기

function bank_update_del(bank_file_id) {
    document.getElementById("bank-update-file-" + bank_file_id).remove();
}

// 아이콘 눌렀을 때 수정 comfirm 알림 나옴.
// bank_del 보고 참고 한 거라 백엔드 작업시 참고해야 함.
function bank_update(bank_no) {
    document.getElementById("form-bank-update-" + bank_no).submit()
}

// 아이콘 눌렀을 때 삭제 comfirm 알림 나옴.
function bank_del(bank_no) {
    if (confirm('정말로 삭제하시겠습니까?')) {
        document.getElementById("form-bank-delete-" + bank_no).submit()
    }
}


// select 값 설정했을때 연도도 바뀌고, 연도에 맞는 내용으로 정렬
function bank_select() {
    var select = document.getElementById("bank-select"); // select 태그 가져옴
    var selectTxt = select.options[select.selectedIndex].text; // 선택된 옵션의 글자를 가져옴
    var bankYear = document.getElementById("bank-year"); // 연도 글자 부분 h 태그를 가져옴

    // 연도 h태그 사이에 글자를 선택된 옵션으로 바꾸어 줌
    bankYear.innerHTML = selectTxt;

    //------------------------------- 연도에 맞는 자료 정렬----------------------------------------

    var dateValue = document.getElementsByClassName("bank-date"); // date input를 다 가져와야함
    var tr_head = document.getElementById("bank-tr-head"); // table head부분 가져옴
    var tr_list = document.getElementsByClassName("bank-tr"); // table body에 있는 tr부분 다 가져옴.
    var selectString = String(document.getElementById("bank-select").value); // 선택된 select를 string형으로 형변환

    //tr_list 수(tr 수)만큼 for문 돌린다.
    for (i = 0; i < tr_list.length; i++) {

        var dateYear = dateValue[i].value.split("-")[0]; // date input 가져온 것을 -기준으로 쪼개서 연도만 가져옴.

        if ("전체" === selectString) {
            tr_head.style.display = "table-row"; // 이거 해야 테이블 형태 안무너짐 // 테이블 헤드 부분
            tr_list[i].style.display = "table-row"; // 테이블 내용 부분
            bankYear.innerHTML = "전체 회계 내역"; // select 안의 내용과 다르게 나타내주기 위해 따로 다시 선언해줌
            bankYear.style.fontSize = "22px"; // 폰트 사이즈 조정
        } else if (dateYear === selectString) {
            tr_head.style.display = "table-row"; // 이거 해야 테이블 형태 안무너짐 // 테이블 헤드 부분
            tr_list[i].style.display = "table-row"; // 테이블 내용 부분
            bankYear.style.fontSize = "28px"; // 폰트 사이즈 조정
        } else {
            tr_list[i].style.display = "none"; // 테이블 내용 부분
            bankYear.style.fontSize = "28px"; // 폰트 사이즈 조정
        }

    }

}

// ================================== 동아리 활동 -> 동아리 연혁 관련 js ========================================= //

//수정 아이콘을 클릭하면 등록 아이콘으로 바뀌고, 등록 아이콘을 클릭했을 때 메세지 뜨기
function introduce_update(history_id) {
    document.getElementById('history-date-'+history_id).disabled = false; // input창 disabled속성을 해제, disabled 속성을 거짓이라 둠.
    document.getElementById('history-txt-'+history_id).disabled = false;
    document.getElementById('history-con-'+history_id).disabled = false;
    document.getElementById('history-con-'+history_id).type = "text";
    document.getElementById('history-date-'+history_id).classList.add('history-change');
    //disabled 가 해제 되었을 때 class로 테두리 css를 지정해줌.
    document.getElementById('history-txt-'+history_id).classList.add('history-change');
    //disabled 가 해제 되었을 때 class로 테두리 css를 지정해줌.
    document.getElementById('history-con-'+history_id).classList.add('history-change');
    //disabled 가 해제 되었을 때 class로 테두리 css를 지정해줌.
    document.getElementById('history-date-'+history_id).focus();
    //날짜 input 에 포커스

    //아이콘 바꾸어 주기 위해 변수 선언. 수정 아이콘을 바꾸어 주어야 하므로 id로 update를 가져옴.
    var icon = document.getElementById('history-update-'+history_id)
    // 아이콘 class 속성을 바꾸어 주어 아이콘 변경하기
    icon.setAttribute("class", "fa fa-check")

    //check 아이콘은 하나 뿐이므로 인덱스 0번 사용.
    var check_icon = document.getElementsByClassName('fa fa-check')[0]

    //check 아이콘 클릭 시 confirm 알림나옴.
    check_icon.onclick = function () {
        if (confirm("수정하시겠습니까?")) {
            document.getElementById('form-history-update-'+history_id).submit()
        }
    }
}

// 아이콘 눌렀을 때 삭제 comfirm 알림 나옴.
function introduce_del(history_id) {
    if (confirm('정말로 삭제하시겠습니까?')) {
        document.getElementById("form-history-delete-"+history_id).submit()
    }

    //삭제 아이콘 찾는 변수, 지금은 안씀.
    var del = document.getElementsByClassName('delete');
}

//동아리 연혁 추가하기 모달 보이기
function introduce_add() {
    // html에 있는 모달을 찾고
    var modalBg = document.getElementById('introduce-modal-bg');
    // 그 모달을 flex로 보이게 한다.
    modalBg.style.display = 'flex';

}

// 동아리 연혁 추가하기 모달 삭제하기
function introduce_close() {
    // html에 있는 모달을 찾고
    var modalBg = document.getElementById('introduce-modal-bg');
    // 그 모달을 안보이게 한다.
    modalBg.style.display = 'none';
}

// ================================== my_info 관련 js ========================================= //
// select 값 설정했을때 연도도 바뀌고, 연도에 맞는 내용으로 정렬
function my_info_grade() {

    var tr_head = document.getElementById("my_info_new_head"); // table head부분 가져옴
    var tr_list = document.getElementsByClassName("my_info_new_tr"); // table body에 있는 tr부분 다 가져옴.
    var selectString = String(document.getElementById("my_info_select_grade").value); // 선택된 select를 string형으로 형변환

    //tr_list 수(tr 수)만큼 for문 돌린다.
    for (i = 0; i < tr_list.length; i++) {
        var grade = String(document.getElementsByClassName("mem_grade")[i].innerHTML); // 테이블 안 학년을 다 가져와야 함.

        // 학년이라는 옵션과 선택된 select가 같으면
        if ("학년" === selectString) {
            tr_head.style.display = "table-row"; // 이거 해야 테이블 형태 안무너짐 // 테이블 헤드 부분
            tr_list[i].style.display = "table-row"; // 테이블 내용 부분

            // option 안 학년과 선택된 select가 같으면
        } else if (grade === selectString) {
            tr_head.style.display = "table-row"; // 이거 해야 테이블 형태 안무너짐 // 테이블 헤드 부분
            tr_list[i].style.display = "table-row"; // 테이블 내용 부분

        }
        // option 안 학년과 선택된 select가 같지 않으면
        else {
            tr_list[i].style.display = "none"; // 테이블 내용 부분
            tr_head.style.display = "table-row"; // 이거 해야 테이블 형태 안무너짐 // 테이블 헤드 부분

        }

    }

}

// ================================== staff 관련 js ========================================= //
// select 값 설정했을때 연도도 바뀌고, 연도에 맞는 내용으로 정렬
function staff_select() {
    for (i = 0; i < 6; i++) {
        var staffTdInner = document.getElementById("staff-td-" + i).innerText;

        var staffTr = document.getElementById("staff-tr-" + i);
    }

    var select = document.getElementById("staff-select");

    var selectTxt = select.options[select.selectedIndex].text; // 선택된 옵션의 글자를 가져옴

    // 연도와 select가 같지 않으면 안보이게
    if (staffTdInner !== selectTxt) {
        // tr_0.style.display = "table";
        staffTr.style.display = "none";

    }
    // 연도와 select가 같으면 보이게
    else {
        staffTr.style.display = "table";
        staffTr.style.border = "none"; //이 스타일은 첫번째 row(제일 최근 row)만 지정해 주어야 함.
        // staffTr.style.display = "table-cell"; // 이거 해야 테이블 형태 안무너짐
        staffTr.style.borderCollapse = "collapse"; //선 중복 방지 위함인데 수정해야 함. 선 중복된다..... 엉엉
        // tr_1.style.display = "table";
    }
}

function staff_grade() {

    var tr_head = document.getElementById("staff_new_head"); // table head부분 가져옴
    var tr_list = document.getElementsByClassName("staff_new_tr"); // table body에 있는 tr부분 다 가져옴.
    var selectString = String(document.getElementById("staff_select_grade").value); // 선택된 select를 string형으로 형변환

    //tr_list 수(tr 수)만큼 for문 돌린다.
    for (i = 0; i < tr_list.length; i++) {
        var grade = String(document.getElementsByClassName("mem_grade")[i].innerHTML); // 테이블 안 학년을 다 가져와야 함.

        // 학년이라는 옵션과 선택된 select가 같으면
        if ("학년" === selectString) {
            tr_head.style.display = "table-row"; // 이거 해야 테이블 형태 안무너짐 // 테이블 헤드 부분
            tr_list[i].style.display = "table-row"; // 테이블 내용 부분

            // option 안 학년과 선택된 select가 같으면
        } else if (grade === selectString) {
            tr_head.style.display = "table-row"; // 이거 해야 테이블 형태 안무너짐 // 테이블 헤드 부분
            tr_list[i].style.display = "table-row"; // 테이블 내용 부분

        }
        // option 안 학년과 선택된 select가 같지 않으면
        else {
            tr_list[i].style.display = "none"; // 테이블 내용 부분
            tr_head.style.display = "table-row"; // 이거 해야 테이블 형태 안무너짐 // 테이블 헤드 부분

        }

    }

}

// ================================== lectRoom 관련 js ========================================= //
function lectRoom_state() {

    var tr_head = document.getElementById("lectRoom_head"); // table head부분 가져옴
    var tr_list = document.getElementsByClassName("lectRoom_tr"); // table body에 있는 tr부분 다 가져옴.
    var selectString = String(document.getElementById("lectRoom_select_state").value); // 선택된 select를 string형으로 형변환

    //tr_list 수(tr 수)만큼 for문 돌린다.
    for (i = 0; i < tr_list.length; i++) {
        var state = String(document.getElementsByClassName("lectRoom_state")[i].innerHTML); // 테이블 안 학년을 다 가져와야 함.

        // 상태라는 옵션과 선택된 select가 같으면
        if ("상태" === selectString) {
            tr_head.style.display = "table-row"; // 이거 해야 테이블 형태 안무너짐 // 테이블 헤드 부분
            tr_list[i].style.display = "table-row"; // 테이블 내용 부분

        // option 안 학년과 선택된 select가 같으면
        } else if (state === selectString) {
            tr_head.style.display = "table-row"; // 이거 해야 테이블 형태 안무너짐 // 테이블 헤드 부분
            tr_list[i].style.display = "table-row"; // 테이블 내용 부분

        }
        // option 안 학년과 선택된 select가 같지 않으면
        else {
            tr_list[i].style.display = "none"; // 테이블 내용 부분
            tr_head.style.display = "table-row"; // 이거 해야 테이블 형태 안무너짐 // 테이블 헤드 부분

        }

    }

}

// 강의자 관점 출결관리 페이지에 필터
function lectRoom_manage_attend() {
    let tr_head = document.getElementById("lectRoom_mhead"); // table head부분 가져옴
    let tr_list = document.getElementsByClassName("lectRoom_mtr"); // table body에 있는 tr부분 다 가져옴.
    let selectAttend = String(document.getElementById("lectRoom_select_attend").value); // 선택된 출결 select를 string형으로 형변환
    // let selectHw = String(document.getElementById("lectRoom_select_hw").value); // 선택된 과제 select를 string형으로 형변환
    var i;

    //tr_list 수(tr 수)만큼 for문 돌린다.
    for (i = 0; i < tr_list.length; i++) {
        var attend = String(document.getElementsByClassName("lectRoom_attend")[i].innerHTML); // 테이블 안 출결을 다 가져와야 함.
    //     var hw = String(document.getElementsByClassName("lectRoom_hw")[i].innerHTML); // 테이블 안 과제를 다 가져와야 함.

        // 출결과 과제라는 옵션과 선택된 select가 같으면
        if ("출결" === selectAttend) {
            tr_head.style.display = "table-header-group"; // 이거 해야 테이블 형태 안무너짐 // 테이블 헤드 부분
            tr_list[i].style.display = "table-row"; // 테이블 내용 부분

        }

        else if (attend === selectAttend) {
            tr_head.style.display = "table-header-group"; // 이거 해야 테이블 형태 안무너짐 // 테이블 헤드 부분
            tr_list[i].style.display = "table-row"; // 테이블 내용 부분
        }

        else {
            tr_list[i].style.display = "none"; // 테이블 내용 부분
            tr_head.style.display = "table-header-group"; // 이거 해야 테이블 형태 안무너짐 // 테이블 헤드 부분

        }

    }

}

// 강의자 관점 출결관리 페이지에 필터
function lectRoom_manage_assign() {
    let tr_head = document.getElementById("lectRoom_mhead"); // table head부분 가져옴
    let tr_list = document.getElementsByClassName("lectRoom_mtr"); // table body에 있는 tr부분 다 가져옴.
    let selectHw = String(document.getElementById("lectRoom_select_hw").value); // 선택된 과제 select를 string형으로 형변환
    var i;

    //tr_list 수(tr 수)만큼 for문 돌린다.
    for (i = 0; i < tr_list.length; i++) {
        // var attend = String(document.getElementsByClassName("lectRoom_attend")[i].innerHTML); // 테이블 안 출결을 다 가져와야 함.
        var hw = String(document.getElementsByClassName("lectRoom_hw")[i].innerHTML); // 테이블 안 과제를 다 가져와야 함.

        // 출결과 과제라는 옵션과 선택된 select가 같으면
        if ("과제" === selectHw) {
            tr_head.style.display = "table-header-group"; // 이거 해야 테이블 형태 안무너짐 // 테이블 헤드 부분
            tr_list[i].style.display = "table-row"; // 테이블 내용 부분

        }

        else if (hw === selectHw) {
            tr_head.style.display = "table-header-group"; // 이거 해야 테이블 형태 안무너짐 // 테이블 헤드 부분
            tr_list[i].style.display = "table-row"; // 테이블 내용 부분
        }

        else {
            tr_list[i].style.display = "none"; // 테이블 내용 부분
            tr_head.style.display = "table-header-group"; // 이거 해야 테이블 형태 안무너짐 // 테이블 헤드 부분

        }

    }

}

function FilterFormSubmit() {
    const formElement = $("#filter-form")
    formElement.attr("method", "GET")
    formElement.submit()
}

function ManageFormSubmit() {
    const manage_mode = $("#manage-mode").val();

    if (manage_mode == null) {
        alert('적용할 상태를 선택하세요!');
    } else {
        let manage_mode_str = $("#manage-mode option:checked").text()

        var checked_list = [];
        $("input:checkbox[name^=is_checked]:checked").each(function () {
            checked_list.push(this.value);
        });

        if (checked_list.length === 0) {
            alert('수강생을 선택하세요!');
        } else {
            if (confirm("총 " + checked_list.length + "명의 수강생을 " + manage_mode_str + " 처리 하시겠습니까?")) {
                const formElement = $("#manage-form");
                formElement.attr("method", "POST");
                return true;
            }
        }
    }
    return false
}

function StatusFormSubmit() {
    const status_mode = $("#status-mode").val();

    if (status_mode === '관리') {
        alert('적용할 수강 상태를 선택하세요!');
    } else {
        let status_mode_str = '';
        if (status_mode === '1') status_mode_str = '수강중';
        else status_mode_str = '수강정지';

        let checked_list = [];
        $("input:checkbox[name^=is_checked]:checked").each(function () {
            checked_list.push(this.value)
        })

        if (checked_list.length === 0) {
            alert('적용할 수강생을 선택하세요!');
        } else {
            if (confirm("총 " + checked_list.length + "명의 수강생을 " + status_mode_str + " 처리 하시겠습니까?")) {
                const status_form = $("#status-form")
                status_form.attr("method", "post");
                return true;
            }
        }
    }

    return false;
}

function AssignmentAorFormSubmit() {
    alert('해당 과제가 실패 처리 되었습니다.');

    const reject_reason = $("#modal-reject-reason").val();
    $("#reject_reason").val(reject_reason);
    $("#aor").val(-1);
    $("#assignment_aor").submit()
}

