$(document).ready(function () { // 함수를 작동시키는 트리거

            // 답글쓰기 버튼 클릭 시, 하단에 대댓글 입력창을 삽입하는 함수
            $('.btnAdd').click(function () {
                $('#comment-no-1').append( // comment-no-1은 임의의 id 값임. 백앤드에서 댓글 번호를 가져와야 함.
                    '<div class="btnRemove">' + // 작성 취소를 누를 때 사라지게 하기위해 btnRemove 클래스로를 지정.
                    '<div class=" dlab-divider bg-gray-dark"></div>' + // 댓글과 대댓글 사이 구분선
                    '<form class="comment-form" id="commentform" method="post" action="#"> ' +
                    '<p class="comment-form-comment"> ' +
                    '<label for="comment">Comments</label> ' +
                    '<textarea rows="8" name="comment" placeholder="답글을 입력하세요!" id="comment"></textarea> ' + // 대댓글 입력창
                    '</p> ' +
                    '<p class="form-submit"> ' +
                    '<div class="extra-cell text-right"> ' +
                    '<button id="comment-delete" type="button" class="site-button red radius-xl m-l10"><i class="fa fa-trash m-r5"></i>작성취소</button>' +
                    '<button id="re-comment-submit" type="submit" class="site-button radius-xl m-l10 m-r15">답글작성</button>'+
                    '</div>' +
                    '</p> ' +
                    '</form> ' +
                    '</div>'
                );

                // 답글쓰기 버튼 클릭 시 답글쓰기 버튼 사라지는 함수
                $(this).hide('fast');

                // 작성취소 클릭 시 대댓글 입력창이 사라지고, 답글쓰기 버튼이 다시 생기는 함수
                $('#comment-delete').on('click', function () {
                    $('div').remove('.btnRemove'); // remove the button
                    $(".btnAdd").show();
                });
            });

            // 댓글수정버튼 클릭하면, 댓글 수정할 수 있게하고 포커스가 마지막으로 가게끔
            $('#comment-no-1 .re-comment').click(function () { // 댓글수정버튼 클릭 시
                $("#comment-area").attr("disabled", false); // input 입력이 활성화
                $('#comment-no-1 .btnAdd').hide('fast') // 답글쓰기 버튼 가리기
                $('input#comment-area').addClass('comment-modify') // 댓글 수정하기 css 입힘

                // 댓글의 마지막으로 글자로 마우스 포커스가 가는 함수
                var len = $('#comment-area').val().length;
                $('#comment-area').focus();
                $('#comment-area')[0].setSelectionRange(len, len);

                // 수정하기 버튼을 등록하기로 바꾸고, 앞 이모티콘도 바꾸기
                $(this).text(" 등록하기").addClass('fa fa-check');
            });

        }); // end ready