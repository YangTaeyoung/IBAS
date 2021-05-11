// ================================== nav 관련 js ========================================= //
// 네비게이션바 클릭했을 때 색 바뀌기
function clickMenu(idx) {
    var menuItemList = document.getElementsByClassName('menu-item'); // 메뉴 아이템 정보를 리스트 형식으로 받음.
    // 스타일 적용된 class 추가함.
    menuItemList[idx].classList.add('introduce-change-nav');
    for (i = 0; i < menuItemList.length; i++) {
        // 메뉴 아이템 순회, 다른 메뉴 아이템의 색상은 클릭 시에 아무런 문제가 없어야 하므로 클릭된 요소를 제외한 모든 메뉴를 일반 상태로 돌림
        if (i == idx) {
            // i 가 idx의 경우
            continue; // 넘어감
        }
        // 스타일 적용된 class 지워줌.
        menuItemList[i].classList.remove('introduce-change-nav');
    }
}