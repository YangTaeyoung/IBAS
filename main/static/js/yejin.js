// 네비게이션바 클릭했을 때 색 바뀌기
function clickMenu(idx) {
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
}


// function create(){
//
//     if (document.getElementById('create').style.display === '' ){
//         document.getElementById('create').style.display='none';
//     }
//     else document.getElementById('create').style.display='';
// }

//수정 아이콘을 클릭하면 등록 아이콘으로 바뀌고, 등록 아이콘을 클릭했을 때 메세지 뜨기
function introduce_update() {

    document.getElementById('date').disabled = false; // input창 disabled속성을 해제, disabled 속성을 거짓이라 둠.
    document.getElementById('history-txt').disabled = false;

    document.getElementById('date').setAttribute("class", 'introduce-js-input');
    //disabled 가 해제 되었을 때 class로 테두리 css를 지정해줌.
    document.getElementById('history-txt').setAttribute("class", 'introduce-js-textarea');
    //disabled 가 해제 되었을 때 class로 테두리 css를 지정해줌.
    document.getElementById('date').focus();
    //날짜 input 에 포커스

    //아이콘 바꾸어 주기 위해 변수 선언. 수정 아이콘을 바꾸어 주어야 하므로 id로 update를 가져옴.
    var icon = document.getElementById('update')
    // 아이콘 class 속성을 바꾸어 주어 아이콘 변경하기
    icon.setAttribute("class", "fa fa-check")

    //check 아이콘은 하나 뿐이므로 인덱스 0번 사용.
    var check_icon = document.getElementsByClassName('fa fa-check')[0]

    //check 아이콘 클릭 시 confirm 알림나옴.
    check_icon.onclick = function () {
        confirm("등록하시겠습니까?")
    }
}

// 아이콘 눌렀을 때 삭제 comfirm 알림 나옴.
function introduce_del() {
    confirm('정말로 삭제하시겠습니까?');
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

//네비게이션 바 색 바꾸기
//매개변수는 id. 매개변수 이름은 네비게이션 바 아이디와 동일.
function section_mouse_in(id){
    //id가 매개변수인 네비게이션바 요소를 찾음
    secObj = document.getElementById(id)
    //스타일 변경경    secObj.style.fontSize = "16px";
    secObj.style.fontWeight = "bolder";
    secObj.style.color = "#091069";
}
//네비게이션 바 색 원래대로 바꾸기
//매개변수는 id. 매개변수 이름은 네비게이션 바 아이디와 동일.
function section_mouse_out(id){
    // 네비게이션 바 id를 리스트로 만든다.
    secNameList = ["intro-a","intro-cm-a","his-a","con-a"];

    // i는 id 개수 만큼 돌려짐.
    for(i = 0; i < secNameList.length; i++)
    {
        //네비게이션 바 id 리스트와 매개변수로 받아온 id가 동일하지 않으면
        if(secNameList[i] !== id)
        {
            //원래대로 스타일 돌아온다.
            document.getElementById(secNameList[i]).style.fontSize = "15px";
            document.getElementById(secNameList[i]).style.color = "black";
            document.getElementById(secNameList[i]).style.fontWeight = "normal";
        }
    }
}

