// 핸드폰 번호를 입력하면, 하이픈이 입력되도록 하는 함수
function inputPhoneNumber(obj) {
    var number = obj.value.replace(/[^0-9]/g, "");
    var phone = "";

    if (number.length < 4) {
        return number;
    } else if (number.length < 7) {
        phone += number.substr(0, 3);
        phone += "-";
        phone += number.substr(3);
    } else if (number.length < 11) {
        phone += number.substr(0, 3);
        phone += "-";
        phone += number.substr(3, 3);
        phone += "-";
        phone += number.substr(6);
    } else {
        phone += number.substr(0, 3);
        phone += "-";
        phone += number.substr(3, 4);
        phone += "-";
        phone += number.substr(7);
    }
    obj.value = phone;
}



// search id이름을 가진 입력창에 키를 누르면 전공 리스트 중에서 조회하도록 만드는 함수.
function filter() {
    let search = document.getElementById("search").value.toLowerCase();
    let listInner = document.getElementsByClassName("listInner");

    for (let i = 0; i < listInner.length; i++) {
        colleges = listInner[i].getElementsByClassName("colleges");
        major_names = listInner[i].getElementsByClassName("major_names");
        if (colleges[0].innerHTML.toLowerCase().indexOf(search) != -1 ||
            major_names[0].innerHTML.toLowerCase().indexOf(search) != -1
        ) {
            listInner[i].style.display = "flex"
        } else {
            listInner[i].style.display = "none"
        }
    }
}

// 전공 검색창이 뜨게 하는 함수
function popUp() {
    document.getElementById("major-search-popup").style.display = "block";
}
// 전공 검색창이 사라지게 하는 함수
function popDown() {
    document.getElementById("major-search-popup").style.display = "none";
}
// 전공을 클릭하면 전공 입력창에 선택한 전공이 입력되도록 하는 함수
function printResult(major_no) {
    document.getElementById("user_major").value = document.getElementById("major_name_" + major_no.toString()).innerHTML;
    popDown();
}
