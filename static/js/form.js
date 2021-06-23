// 폼 제출 시 사용하는 자바 스크립트, (폼 안에 버튼 태그를 넣기 어렵거나, a태그를 이용해 제출하는 경우)
function goSubmit(form_id, isCheck = false, msg = "") {
    if (isCheck) {
        if (confirm(msg)) {
            document.getElementById(form_id).submit();
        }
    } else {
        document.getElementById(form_id).submit();
    }
}

// 단순 페이지 이동, 및 이동 전 메시지를 지정할 수 있도록 하는 함수
function goPage(url, isCheck = false, msg = "") {
    if (isCheck) {
        if (confirm(msg)) {
            location.href = url;
        }
    } else {
        location.href = url;
    }
}