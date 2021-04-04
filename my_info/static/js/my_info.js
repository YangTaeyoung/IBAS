//역할 변경 select 중 회장을 선택했을 떄 나오는 알람.
function CheckSelect() {
    var ctrlSelect = document.getElementById("my_info_select"); //관련된 select문을 찾고
    if (ctrlSelect.selectedIndex === 1) { // 인덱스가 1번이면(회장을 선택하면)
        alert('회장을 선택하셨습니다. \n회장의 모든 권한을 선택한 사람에게 위임하게 됩니다.\n다수의 회장을 지명할 시 회장 위임이 이루어지지 않습니다.');
        // 알람이 나온다.
    }
}