// 네비게이션바 클릭했을 때 색 바뀌기
function clickMenu(idx) {
    // 메뉴 바 선택 관련
    var menuItemList = document.getElementsByClassName('menu-item'); // 메뉴 아이템 정보를 리스트 형식으로 받음.
    menuItemList[idx].style.fontWeight = 'bolder'; // 글씨체: 굵게
    menuItemList[idx].style.fontSize = '16px'; // 글씨 크기: 16px
    menuItemList[idx].style.color = '#091069'; // 글씨 색상: 남색
    for (i = 0; i < menuItemList.length; i++) {
        // 메뉴 아이템 순회, 다른 메뉴 아이템의 색상은 클릭 시에 아무런 문제가 없어야 하므로 클릭된 요소를 제외한 모든 메뉴를 일반 상태로 돌림
        if (i == idx) {
            // i 가 idx의 경우
            continue; // 넘어감
        }
        menuItemList[i].style.color = 'black'; // 글씨 색: 검정
        menuItemList[i].style.fontWeight = null; // 폰트 굵기: 일반
        menuItemList[i].style.fontSize = '15px'; // 폰트 크기: 15px
    }
    /*해당 메뉴에 맞는 내용 출력하는 곳*/
}

function create(){

    if (document.getElementById('create').style.display === '' ){
        document.getElementById('create').style.display='none';
    }
    else document.getElementById('create').style.display='';
}

function update() {
    document.getElementById('date').disabled = false;
    document.getElementById('history-txt').disabled = false;

    document.getElementById('date').focus();
    if (document.getElementById('date').disabled === false) {
        document.getElementById('date').style.textUnderlinePosition = 'solid'
        document.getElementById('history-txt').style.textUnderlinePosition = 'solid'
    }
    
    document.getElementById('update').value = '등록';
}


function del() {
    confirm('정말로 삭제하시겠습니까?');
    var del = document.getElementsByClassName('delete');

}


function introduce_add() {

    var modalBg = document.getElementById('introduce-modal-bg');

    modalBg.style.display = 'flex';

}

function introduce_close() {
    var modalBg = document.getElementById('introduce-modal-bg');

    modalBg.style.display = 'none';
}

// function create2() {
//     var divGroup = document.getElementById("divGroup");
//     var divDate = document.createElement("div");
//     var divTxt = document.createElement("div");
//     var divBtn = document.createElement("div");
//     var inputDate = document.createElement("input");
//     var inputTxt = document.createElement("input");
//     var inputRegister = document.createElement("input");
//
//
//     // <input type="submit" id="update" className="introduce-button-style" onClick="update()"
//     //        value="수정">
//
//     inputDate.setAttribute("type", "date" );
//     inputDate.setAttribute("class", "introduce-update-input-date ");
//     // inputDate.style.left = "20px";
//     inputDate.style.width = "160px";
//
//
//
//
//     inputTxt.setAttribute("type", "text");
//     inputTxt.setAttribute("class", "introduce-add-input-txt");
//     inputTxt.style.borderRadius = "18px";
//
//     inputRegister.setAttribute("type", "submit");
//     // inputRegister.setAttribute("id", "update");
//     inputRegister.setAttribute("class", "introduce-button-style");
//     // inputRegister.setAttribute("onclick", "update()");
//     inputRegister.setAttribute("value", "등록");
//
//
//     divDate.appendChild(inputDate);
//     divDate.setAttribute("class", "introduce-contact-flex-container");
//
//     divTxt.appendChild(inputTxt);
//
//     divBtn.appendChild(inputRegister);
//     divBtn.setAttribute("class", "introduce-contact-flex-container");
//
//     divGroup.appendChild(divDate);
//     divGroup.appendChild(divTxt);
//     divGroup.appendChild(divBtn);
//
// }
