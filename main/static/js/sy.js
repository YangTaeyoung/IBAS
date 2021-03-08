$(document).ready(function () {
            $('#comment-no-1').click(function () { // input 클래스 btnAdd를 클릭하면
                $('#comment_no_1').append( // div 클래스 인풋태그 뒤에 삽입
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
                ); // end append
                $(this).hide('fast');

                $('#comment-delete').on('click', function () {
                    $('div').remove('.btnRemove'); // remove the button
                    $(".btnAdd").show();
                });
            });

            $("input.autosize").on('keydown keyup', function () {
                $(this).height(1).height($(this).prop('scrollHeight') + 12);
            });// end click

            $('#re-comment').click(function () {
                $("#comment_no_2").attr("disabled", false);
                $('.btnAdd').hide('fast')
                $('input#comment_no_2').addClass('happy')
                var len = $('#comment_no_2').val().length;
                $('#comment_no_2').focus();
                $('#comment_no_2')[0].setSelectionRange(len, len);
                $(this).text(" 등록하기").addClass('fa fa-check');
            });

        }); // end ready