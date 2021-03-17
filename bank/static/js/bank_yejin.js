//수정 아이콘을 클릭하면 등록 아이콘으로 바뀌고, 등록 아이콘을 클릭했을 때 메세지 뜨기

function bank_update() {

    document.getElementById('bank-date-1').disabled = false; // input창 disabled속성을 해제, disabled 속성을 거짓이라 둠.
    document.getElementById('bank-date-1').classList.add("bank-input-add");

    document.getElementById('bank-txt-1').disabled = false; // input창 disabled속성을 해제, disabled 속성을 거짓이라 둠.
    document.getElementById('bank-txt-1').classList.add("bank-input-add");

    document.getElementById('bank-earn-1').disabled = false; // input창 disabled속성을 해제, disabled 속성을 거짓이라 둠.
    document.getElementById('bank-earn-1').classList.add("bank-input-add");

    document.getElementById('bank-spend-1').disabled = false; // input창 disabled속성을 해제, disabled 속성을 거짓이라 둠.
    document.getElementById('bank-spend-1').classList.add("bank-input-add");

    document.getElementById('bank-money-1').disabled = false; // input창 disabled속성을 해제, disabled 속성을 거짓이라 둠.
    document.getElementById('bank-money-1').classList.add("bank-input-add");


    //아이콘 바꾸어 주기 위해 변수 선언. 수정 아이콘을 바꾸어 주어야 하므로 id로 update를 가져옴.
    var icon = document.getElementById('bank-update')
    // 아이콘 class 속성을 바꾸어 주어 아이콘 변경하기
    icon.setAttribute("class", "fa fa-check")

    //check 아이콘은 하나 뿐이므로 인덱스 0번 사용.
    var check_icon = document.getElementsByClassName('fa fa-check')[0]

    //check 아이콘 클릭 시 confirm 알림나옴.
    check_icon.onclick = function () {
        confirm("수정하시겠습니까?")
        }

}

// 아이콘 눌렀을 때 삭제 comfirm 알림 나옴.
function bank_del() {
    confirm('정말로 삭제하시겠습니까?')

}



function bank_select() {
    var select = document.getElementById("bank-select");
    var selectTxt = select.options[select.selectedIndex].text;
    var bankYear = document.getElementById("bank-year");

    bankYear.innerHTML = selectTxt;

    //-----------------------------------------------------------------------

    var dateValue = document.getElementById("bank-date-1").value;
    var tr_0 = document.getElementById("bank-tr-0");
    var tr_1 = document.getElementById("bank-tr-1");

    var dateYear = String(dateValue.split("-"));
    var selectString = String(document.getElementById("bank-select").value);

    if ((dateYear[0] + dateYear[1] + dateYear[2] + dateYear[3]) !== selectString) {
        // tr_0.style.display = "table";
        tr_1.style.display = "none";

    }
    else {
        tr_0.style.display = "table";
        tr_1.style.border = "none"; //이 스타일은 첫번째 row(제일 최근 row)만 지정해 주어야 함.
        tr_1.style.display = "table";
    }
    
}
