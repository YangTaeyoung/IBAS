// 대댓글창 삽입
function addReply() {
    // 답글달기 버튼 안보이게
    const btnAdd = document.getElementById('btnAdd');
    btnAdd.style.display = 'none';

    // 대댓글 입력창에 추가되는 모든걸 담는 div를 생성
    const reply_box = document.createElement('div');
    reply_box.classList.add("btnRemove");
    document.getElementById('comment_no_1').appendChild(reply_box);

    // 대댓글 입력창 윗쪽 구분선
    const line = document.createElement('div');
    line.classList.add("dlab-divider", "bg-gray-dark");
    reply_box.appendChild(line);

    // 대댓글 입력 form 태그
    const form = document.createElement('form');
    form.classList.add('comment-form');
    reply_box.appendChild(form);

    // 대댓글 창을 꾸미는 p태그
    const p = document.createElement('p');
    p.classList.add('comment-form-comment');
    form.appendChild(p);

    // 대댓글 입력란 text area
    const textarea = document.createElement('textarea');
    textarea.setAttribute('placeholder', '답글을 입력하세요!');
    textarea.setAttribute('row', '8');
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
    btn1.onclick = function (){
        reply_box.parentNode.removeChild(reply_box); // 생성된 답글쓰기 div 삭제
        btnAdd.style.display = 'inline-block'; // 숨겨둔 답글쓰기 버튼 보이게 하기
    }

    // 답글작성 버튼
    const btn2 = document.createElement('button');
    btn2.setAttribute('id', 're-comment-submit');
    btn2.setAttribute('type', 'submit');
    btn2.classList.add('site-button', 'radius-xl', 'm-l10', 'm-r15');
    btn2.innerText = "답글작성"
    btndiv.appendChild(btn2);

}

// 댓글수정
function correcting_comment(comment_id) {
    document.getElementById('correcting-' + comment_id).disabled = false; // input창 disabled속성을 해제.
    document.getElementById('correcting-' + comment_id).setAttribute("class", 'happy'); // input창 css 변경
    document.getElementById('correcting-' + comment_id).focus(); //마우스 포커스
}

// 댓글삭제
function comment_del(comment_id) {
    if (confirm('정말로 삭제하시겠습니까?')) {
        document.getElementById("comment-delete-" + comment_id).submit()
    }
}

