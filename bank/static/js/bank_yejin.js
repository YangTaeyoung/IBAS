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

        // 만약 date input의 연도랑 선택된 select의 글자가 같지 않으면 보이지 않고
        if (dateYear !== selectString) {
            tr_list[i].style.display = "none";
        }
        // 만약 date input의 연도랑 선택된 select의 글자가 같으면 보인다.
        else {
            tr_head.style.display = "table-row"; // 이거 해야 테이블 형태 안무너짐
            tr_list[i].style.display = "table-row";
        }

    }

}
