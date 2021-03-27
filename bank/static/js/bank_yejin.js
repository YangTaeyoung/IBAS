//수정 아이콘을 클릭하면 등록 아이콘으로 바뀌고, 등록 아이콘을 클릭했을 때 메세지 뜨기

function bank_update() {
    // 각각의 인풋마다 숫자가 주어져야 함. for문 돌려야 하고, 태영이 오빠 방식 참고(main 폴더에서 yejin.js)하면 될 듯

    document.getElementById('bank-txt-1').disabled = false; // input창 disabled속성을 해제, disabled 속성을 거짓이라 둠.
    document.getElementById('bank-txt-1').classList.add("bank-input-add"); // class 추가하여 스타일 추가해줌.

    document.getElementById('bank-earn-1').disabled = false; // input창 disabled속성을 해제, disabled 속성을 거짓이라 둠.
    document.getElementById('bank-earn-1').classList.add("bank-input-add"); // class 추가하여 스타일 추가해줌.

    document.getElementById('bank-spend-1').disabled = false; // input창 disabled속성을 해제, disabled 속성을 거짓이라 둠.
    document.getElementById('bank-spend-1').classList.add("bank-input-add"); // class 추가하여 스타일 추가해줌.

    document.getElementById('bank-money-1').disabled = false; // input창 disabled속성을 해제, disabled 속성을 거짓이라 둠.
    document.getElementById('bank-money-1').classList.add("bank-input-add");// class 추가하여 스타일 추가해줌.


    //아이콘 바꾸어 주기 위해 변수 선언. 수정 아이콘을 바꾸어 주어야 하므로 id로 bank-update를 가져옴.
    // bank-update는 수정 버튼 아이콘 (i태그)의 id로 정의되어 있음.
    var icon = document.getElementById('bank-update')
    // 아이콘 class 속성을 바꾸어 주어 아이콘 변경하기
    icon.setAttribute("class", "fa fa-check")

    //check 아이콘은 하나 뿐이므로 인덱스 0번 사용.
    //지금은 하나 뿐인데, class 많아 질거니까 인덱스 역시 for문으로 돌려야 할듯
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


// select 값 설정했을때 연도도 바뀌고, 연도에 맞는 내용으로 정렬
function bank_select() {
    var select = document.getElementById("bank-select"); // select 태그 가져옴
    var selectTxt = select.options[select.selectedIndex].text; // 선택된 옵션의 글자를 가져옴
    var bankYear = document.getElementById("bank-year"); // 연도 글자 부분 h 태그를 가져옴

    // 연도 h태그 사이에 글자를 선택된 옵션으로 바꾸어 줌
    bankYear.innerHTML = selectTxt;


    //------------------------------- 연도에 맞는 자료 정렬----------------------------------------

    var dateValue = document.getElementById("bank-date-1").value; // date input id를 다 가져와야함
    var tr_head = document.getElementById("bank-tr-head"); // table head부분 가져옴
    var tr_1 = document.getElementById("bank-tr-1"); // table body에 있는 tr부분 가져옴. 숫자 부분 for문 돌려야 할듯...?

    var dateYear = String(dateValue.split("-")); // 가져온 값을 array형으로 나누고 string형으로 형변환
    var selectString = String(document.getElementById("bank-select").value); // 선택된 select를 string형으로 형변환

    // 연도와 select가 같지 않으면 안보이게
    if ((dateYear[0] + dateYear[1] + dateYear[2] + dateYear[3]) !== selectString) {
        // tr_0.style.display = "table";
        tr_1.style.display = "none";

    }
    // 연도와 select가 같으면 보이게
    else {
        tr_head.style.display = "table-cell"; // 이거 해야 테이블 형태 안무너짐
        tr_1.style.borderCollapse = "collapse"; //선 중복 방지 위함인데 수정해야 함. 선 중복된다..... 엉엉
        tr_1.style.display = "table";
    }

}
