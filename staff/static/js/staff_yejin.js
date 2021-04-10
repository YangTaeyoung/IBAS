// select 값 설정했을때 연도도 바뀌고, 연도에 맞는 내용으로 정렬
function staff_select() {
    for (i = 0 ; i < 6; i++) {
        ㄴ
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