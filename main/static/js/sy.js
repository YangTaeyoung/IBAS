// 답글삽입
$(document).ready(function () {
            // 답글쓰기 버튼을 클릭하면, 해당 댓글 칸 아래에 답글작성란이 삽입되는 함수
            $('.btnAdd').click(function () {
                $('#comment_no_1').append( // id 때문에, 답글달기를 누른 댓글 칸 뒤에만 삽입됨. (추후 id를 comment.comment_id로 변경할것)
                    '<div class="btnRemove">' +
                    '<div class=" dlab-divider bg-gray-dark"></div>' +
                    '<div class="" id="respond"> ' +
                    '<form class="comment-form" id="commentform" method="post" action="#"> ' +
                    '<p class="comment-form-comment"> ' +
                    '<label for="comment">Comments</label> ' +
                    '<textarea rows="8" name="comment" placeholder="답글을 입력하세요!" id="comment"></textarea> ' +
                    '</p> ' +
                    '<p class="form-submit"> ' +
                    '<div class="extra-cell text-right"> ' +
                    '<button id="comment-delete" type="button" class="site-button red radius-xl m-l10"><i class="fa fa-trash m-r5"></i>작성취소</button>' +
                    '<button id="re-comment-submit" type="submit" class="site-button radius-xl m-l10 m-r15">답글작성</button>'+
                    '</div>' +
                    '</p> ' +
                    '</form> ' +
                    '</div>' +
                    '</div>'
                );
                // 답글달기 클릭 후 작성취소 버튼 클릭 시, 답글작성란이 사라지게 함
                $('#comment-delete').on('click', function () {
                    $('div').remove('.btnRemove'); // remove the button
                    $(".btnAdd").show();
                });
            });

            // $('#re-comment').click(function () {
            //     $("#comment_no_2").attr("disabled", false);
            //     $('.btnAdd').hide('fast')
            //     $('input#comment_no_2').addClass('happy')
            //     var len = $('#comment_no_2').val().length;
            //     $('#comment_no_2').focus();
            //     $('#comment_no_2')[0].setSelectionRange(len, len);
            //     $(this).text(" 등록하기").addClass('fa fa-check');
            // });

        }); // end ready

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

