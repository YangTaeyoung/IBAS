// ================================== comment 관련 js ========================================= //
// 대댓글창 삽입
function addReply(comment_id, url, board_no, csrf_token) {
    // 답글달기 버튼 안보이게
    const btnAdd = document.getElementById('btnAdd-' + comment_id);
    btnAdd.style.display = 'none';

    // 대댓글 입력창에 추가되는 모든걸 담는 div를 생성
    const reply_box = document.createElement('div');
    reply_box.classList.add("btnRemove");


    // 대댓글 입력창 윗쪽 구분선
    const line = document.createElement('div');
    line.classList.add("dlab-divider", "bg-gray-dark");
    reply_box.appendChild(line);

    // 대댓글 입력 form 태그
    const form = document.createElement('form');
    form.classList.add('comment-form');
    form.id = "comment-ref-register-" + comment_id;
    form.action = url;
    form.method = "get";
    reply_box.appendChild(form);

    const inputCommentId = document.createElement("input");
    inputCommentId.type = "hidden";
    inputCommentId.name = "comment_ref"
    inputCommentId.value = comment_id;
    form.appendChild(inputCommentId);

    const inputBoardNo = document.createElement("input");
    inputBoardNo.type = "hidden";
    inputBoardNo.name = "board_no";
    inputBoardNo.value = board_no;
    form.appendChild(inputBoardNo);

    // 대댓글 창을 꾸미는 p태그
    const p = document.createElement('p');
    p.classList.add('comment-form-comment');
    form.appendChild(p);

    // 대댓글 입력란 text area
    const textarea = document.createElement('textarea');
    textarea.setAttribute('placeholder', '답글을 입력하세요!');
    textarea.setAttribute('row', '8');
    textarea.setAttribute("name", "comment_cont");
    p.appendChild(textarea);

    // 대댓글 작성취소 및 답글작성을 담는 버튼 div
    const btndiv = document.createElement('div');
    btndiv.classList.add('extra-cell', 'text-right');
    form.appendChild(btndiv);

    // 작성취소 버튼
    const btn1 = document.createElement('button');
    btn1.setAttribute('id', 'comment-delete');
    btn1.setAttribute('type', 'button');
    btn1.classList.add('site-button', 'radius-xl', 'm-l10', 'red');
    btn1.innerText = "작성취소";
    btndiv.appendChild(btn1);
    // 작성취소 버튼을 클릭하면, 대댓글을 담는 div는 사라지고, 가려진 답글쓰기 버튼도 다시 보임
    btn1.onclick = function () {
        reply_box.parentNode.removeChild(reply_box); // 생성된 답글쓰기 div 삭제
        btnAdd.style.display = 'inline-block'; // 숨겨둔 답글쓰기 버튼 보이게 하기
    }

    // 답글작성 버튼
    const btn2 = document.createElement('button');
    btn2.setAttribute('id', 're-comment-submit');
    btn2.setAttribute('type', 'submit');
    btn2.classList.add('site-button', 'radius-xl', 'm-l10', 'm-r15');
    btn2.innerText = "답글작성"
    btn2.addEventListener("click", event=>submitRef(comment_id));
    btndiv.appendChild(btn2);

    document.getElementById('comment_no_' + comment_id).appendChild(reply_box);
}

function  submitRef(comment_id)
{
    document.getElementById("form-ref-register"+comment_id).submit();
}

// // 댓글수정 (DB 적용 ver)
// // DB 버전은 총 세 군데 수정이 필요할 것으로 예상
// // 수정 1 (아래와 다른 부분)
// function correcting_comment(comment_id) {
//     // 수정2 (아래와 다른 부분)
//     const reply_comment = document.getElementById('correcting-' + comment_id);
//     reply_comment.disabled = false;
//     reply_comment.setAttribute('class', 'happy');
//
//     // 댓글수정 버튼 안보이게 하기
//     const correctingBtn = document.getElementById('correctingBtn');
//     correctingBtn.style.display = 'none';
//
//     // 댓글수정완료 버튼 생성
//     const correctingresultBtn = document.createElement('button');
//     correctingresultBtn.classList.add('comment-btn', 'm-r10');
//     const checkicon = document.createElement('i');
//     checkicon.classList.add('fa', 'fa-check', 'm-r10');
//     checkicon.innerText = " 수정완료";
//     correctingresultBtn.appendChild(checkicon);
//     // 수정완료 버튼 타입을 submit으로 지정
//     correctingresultBtn.setAttribute('type', 'submit');
//     // 수정 3 (아래와 다른부분)
//     document.getElementById('commentbtnDiv' + comment_id).appendChild(correctingresultBtn); // 아래와 다른부분
//
//     // 마우스포커스 맨 뒤로 가게 하기
//     var len = $(reply_comment).val().length;
//     $(reply_comment).focus();
//     $(reply_comment)[0].setSelectionRange(len, len);
// }
// 댓글수정 (DB 적용X - 테스트용 ver)
// 위에 주석처리된 것을 참고하여 수정
// 수정필요한 부분1
function comment_update(comment_id) {
    // 수정필요한 부분2
    const reply_comment = document.getElementById('correcting-no-' + comment_id);
    reply_comment.disabled = false;
    reply_comment.setAttribute('class', 'happy');

    // 댓글수정 버튼 안보이게 하기
    const correctingBtn = document.getElementById('correctingBtn-' + comment_id);
    correctingBtn.style.display = 'none';

    // 댓글수정완료 버튼 생성
    const correctingresultBtn = document.createElement('button');
    correctingresultBtn.classList.add('comment-btn', 'm-r10');
    const checkicon = document.createElement('i');
    checkicon.classList.add('fa', 'fa-check', 'm-r10');
    checkicon.innerText = " 수정완료";
    correctingresultBtn.appendChild(checkicon);
    // 수정완료 버튼 타입을 submit으로 지정
    correctingresultBtn.setAttribute('type', 'button');
    correctingresultBtn.addEventListener("click", event => submit_update(comment_id))
    // 수정필요한 부분3
    document.getElementById('form-comment-delete-' + comment_id).appendChild(correctingresultBtn);
    // 마우스포커스 맨 뒤로 가게 하기
    var len = $(reply_comment).val().length;
    $(reply_comment).focus();
    $(reply_comment)[0].setSelectionRange(len, len);
}

function submit_update(comment_id) {
    document.getElementById("form-comment-update-" + comment_id).submit();
}

// 댓글삭제
function comment_del(comment_id) {
    if (confirm('정말로 삭제하시겠습니까?')) // 삭제 할 지 묻고 동의 시
    {
        document.getElementById("form-comment-delete-" + comment_id).submit() // 삭제 폼을 전송
    }
}

