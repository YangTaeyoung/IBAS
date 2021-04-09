// delete_list에 적용되어 있음
// select 값 설정했을때 필터
function staff_select() {
    var tr_head = document.getElementById("staff-del-list-head"); // table head부분 가져옴
    var tr_list = document.getElementsByClassName("staff-del-list-tr"); // table body에 있는 tr부분 다 가져옴.
    var selectString = String(document.getElementById("staff-select").value); // 선택된 select를 string형으로 형변환

    //tr_list 수(tr 수)만큼 for문 돌린다.
    for (i = 0; i < tr_list.length; i++) {
        var progress = String(document.getElementsByClassName("staff-progress")[i].innerHTML); // 테이블 안 상태를 다 가져와야 함.

        // 학년이라는 옵션과 선택된 select가 같으면
        if ("선택" === selectString) {
            tr_head.style.display = "table-row"; // 이거 해야 테이블 형태 안무너짐 // 테이블 헤드 부분
            tr_list[i].style.display = "table-row"; // 테이블 내용 부분

        // option 안 학년과 선택된 select가 같으면
        } else if (progress === selectString) {
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

// member_list에 적용되어 있음.
// select 값 설정했을때 필터
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