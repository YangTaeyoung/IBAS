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
