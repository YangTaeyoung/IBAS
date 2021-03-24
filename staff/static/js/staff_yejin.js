// select 값 설정했을때 연도도 바뀌고, 연도에 맞는 내용으로 정렬
function bank_select() {
    for (i = 0 ; i < 6; i++) {
        var staffTr = document.getElementById("staff-tr-" + i).value;

    }

    var staffSelect = document.getElementById("staff-select").value;


    var dateValue = document.getElementById("bank-date-1").value;
    var tr_0 = document.getElementById("bank-tr-0");
    var tr_1 = document.getElementById("bank-tr-1");
    //------------------------------- 연도에 맞는 자료 정렬----------------------------------------

    var dateValue = document.getElementById("bank-date-1").value; // date input id를 다 가져와야함
    var tr_head = document.getElementById("bank-tr-head"); // table head부분 가져옴
    var tr_1 = document.getElementById("bank-tr-1"); // table body에 있는 tr부분 가져옴. 숫자 부분 for문 돌려야 할듯...?

    var dateYear = String(dateValue.split("-"));
    var selectString = String(document.getElementById("bank-select").value);
    var dateYear = String(dateValue.split("-")); // 가져온 값을 array형으로 나누고 string형으로 형변환
    var selectString = String(document.getElementById("bank-select").value); // 선택된 select를 string형으로 형변환

    // 연도와 select가 같지 않으면 안보이게
    if ((dateYear[0] + dateYear[1] + dateYear[2] + dateYear[3]) !== selectString) {
        // tr_0.style.display = "table";
        tr_1.style.display = "none";

    }
    // 연도와 select가 같으면 보이게
    else {
        tr_0.style.display = "table";
        tr_1.style.border = "none"; //이 스타일은 첫번째 row(제일 최근 row)만 지정해 주어야 함.
        tr_head.style.display = "table-cell"; // 이거 해야 테이블 형태 안무너짐
        tr_1.style.borderCollapse = "collapse"; //선 중복 방지 위함인데 수정해야 함. 선 중복된다..... 엉엉
        tr_1.style.display = "table";
    }
}
