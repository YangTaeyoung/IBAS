// common
function validation_check_for_title() {
    let error = null; // if there are no any errors, error=null, or error =  '...'

    let title = $('input[name$="title"]').val().trim();  // Matches those that end with 'title'

    if (title.length == null || title.length === 0) {
        error="제목을 입력하세요!\n";
    } else if (title.length > 100) {
        error="제목이 너무 깁니다. 100자 이내로 작성하세요!\n";
    }

    return error;
}

// common
function validation_check_for_contents() {
    let error = "내용을 입력하세요!\n";

    // semmernote 가 생성한 iframe 태그 밑의 document 에 접근.
    let content_div = $('div.summernote-div').children().contents().find('div.note-editable');
    if(content_div.text().trim().length > 0) {
        error = null;
    }

    return error;
}

function validation_check_for_img_file_upload() {
    let error = '이미지 파일을 적어도 한개 이상 등록해주세요!\n';

    $("div.imageuploadify-details").each(function () {
        let file_type = $(this).children('span:eq(1)').text()
        if (file_type.includes("image")) {
            error = null;
            return false;
        }
    })

    let uploaded_image_files = $("img.file-img")
    if (uploaded_image_files != null && uploaded_image_files.length > 0) {
        return null;
    }

    return error;
}

function validation_check_for_common_things() {
    // common validation methods
    let array_of_validation_method = [
        validation_check_for_title,
        validation_check_for_contents,
    ]

    let errors = [];
    let error = null;
    for (let i = 0; i < array_of_validation_method.length; i++) {
        error = array_of_validation_method[i]();
        if (error != null) {
            errors.push(error);
        }
    }

    return errors;
}

function alert_or_submit(errors){
    // if there are any errors, not submit contest_form and alert all messages!
    if (errors.length > 0) {
        alert(errors.join(''));
        return false;
    } else {
        $("#overlay, #PleaseWait").show();
        return true;
    }
}

// for contest board
function validation_check_for_contest() {
    let errors = [];

    let errors_of_common_things = validation_check_for_common_things();
    if(errors_of_common_things.length > 0) {
        errors.push(...errors_of_common_things);
    }

    // validate contest_topic
    let contest_topic = $('input[name="contest_topic"]').val();
    if (contest_topic.trim().length === 0) {
        errors.push('공모전 주제를 입력하세요!\n');
    } else if (contest_topic.length > 500) {
        errors.push('공모전 주제는 최대 500자까지 입력 가능합니다!\n');
    }

    // validate contest_association
    let contest_association = $('input[name="contest_asso"]').val();
    if (contest_association.trim().length === 0) {
        errors.push('공모전 주체 기관을 입력하세요!\n');
    } else if (contest_association.length > 100) {
        errors.push('공모전 주체 기관은 최대 100자까지 입력 가능합니다!\n');
    }

    // validate contest_start && contest_deadline
    let contest_start = $('input[name="contest_start"]').val();
    let contest_deadline = $('input[name="contest_deadline"]').val();
    if (contest_start.length === 0) {
        errors.push('공모전 시작날짜를 입력하세요!\n');
    }
    if (contest_deadline.length === 0) {
        errors.push('공모전 마감날짜를 입력하세요!\n');
    }
    if (contest_start.length > 0 && contest_deadline.length > 0){
        contest_start = new Date(contest_start);
        contest_deadline = new Date(contest_deadline);
        if (contest_start >= contest_deadline) {
        errors.push('공모전 마감날짜는 시작날짜보다 뒤여야 합니다!\n');
        }
    }

    // validate whether some image files exist or not
    let img_file_error = validation_check_for_img_file_upload()
    if (img_file_error != null && img_file_error.length > 0) {
        errors.push(img_file_error);
    }

    return alert_or_submit(errors)

}


function validation_check_for_assignment_register() {
    let errors = validation_check_for_common_things();

    // validate assignment ref
    let lect_board_ref = $('#select-box').val()
    if (lect_board_ref === "강의 선택") {
        errors.push('과제를 등록할 강의를 선택하세요!\n')
    }

    // validate deadline
    let assignment_deadline = $('input[name="assignment_deadline"]').val()
    if (assignment_deadline.length === 0) {
        errors.push('과제 마감기한을 설정하세요!')
    }

    return alert_or_submit(errors);
}


// for board consist of only title and content, files are not necessary
function validation_check_for_board(is_activity=false) {
    let errors = validation_check_for_common_things();

    // 활동 게시판은 사진 필수
    if (is_activity) {
        let img_error = validation_check_for_img_file_upload();
        if (img_error != null && img_error.length > 0) {
            errors.push(img_error);
        }
    }
    
    return alert_or_submit(errors);
}

// for lecture, study
/*
    - lect_title
    - lect_curri
    - lect_intro
    - lect_day
    - lect_method
    - lect_limit_num
    - lect_deadline : 수정 시에는 과거 날짜 가능하지만, 등록 시에는 불가능
 */
function validation_check_for_lecture() {
    let errors = [];

    // validate lect_title && lect_curri
    let errors_of_common_things = validation_check_for_common_things();
    if(errors_of_common_things.length > 0) {
        errors.push(...errors_of_common_things);
    }


    // validate lect_intro
    let lect_introduce = $('textarea[name="lect_intro"]').val();
    if (lect_introduce.trim().length === 0) {
        errors.push('소개를 입력하세요!\n');
    } else if (lect_introduce.length > 300) {
        errors.push('소개는 300자 이하까지 입력 가능합니다!\n');
    }

    // validate lect_day
    let lect_day = $('input[name="day"]:checked');
    if (lect_day.length === 0 ) {
        errors.push('요일을 선택하세요!\n');
    }

    // validate lect_method
    let lect_or_study_or_hobby = $('div.dlab-bnr-inr-entry').text();
    // 강의나 스터디면, 진행 방식 및 장소링크 필수
    if (!(lect_or_study_or_hobby.includes('취미'))) {
        let lect_method = $('select[name="lect_method"]').val();
        if (lect_method.length === 0) {
            errors.push('진행 방식을 선택하세요!\n');
        } else {
            // validate lect_place_or_link
            let lect_place_or_link = $('input[name="lect_place_or_link"]').val().trim();
            if (lect_place_or_link.length === 0) {
                errors.push('장소나 링크를 기재해주세요!\n');
            } else if (lect_place_or_link.length > 1000) {
                errors.push('장소, 링크는 최대 1000자까지만 입력가능합니다.\n');
            }
        }
    }

    // validate lect_limit_num
    let lect_limit_num = $('input[name="lect_limit_num"]').val().trim();
    if (lect_limit_num <= '0') {
        errors.push('제한인원은 0보다 커야합니다!\n');
    }

    // validate lect_deadline
    let cur_status = $('input.site-button.btn-block.button-md').val();
    if (cur_status === '등록하기') {
        let lect_deadline = $('input[name="lect_deadline"]').val();
        if (lect_deadline.length === 0) {
            errors.push('신청 마감일을 입력하세요!\n');
        } else {
            lect_deadline = new Date(lect_deadline);
            let today = new Date();
            if (lect_deadline < today){
                errors.push('신청 마감일을 다시 설정하세요!\n')
            }
        }

        // 이미지 등록 필수
        let img_error = validation_check_for_img_file_upload();
        if (img_error != null && img_error.length > 0) {
            errors.push(img_error);
        }
    }
    
    return alert_or_submit(errors);
}

function disable_check_box() {
    let check_box = $('input:checkbox[id^="check"]')

    if ($(check_box[0]).attr('id').includes('*')) {
        $(check_box).each(function () {
            $(this).attr("disabled", true);
        });
        $('button.site-button').attr("disabled", true);
    }
}

function phone_check(uri) {
    const user_phone = $("#user_phone").val();
    let error_msg = $('#error_text_phone');
    if(/^\d{3}-\d{3,4}-\d{4}$/.test(user_phone)) {
        axios.get(uri, {
            params: {user_phone: user_phone},
            timeout: 1000
        })
            .then(() => {
                if(uri.includes('my_info')){
                    let form = $('form#update-phone-number');
                    form.attr('method', 'post');
                    form.attr('action', uri);
                    $(form).submit();
                }
                else {
                    $(error_msg).hide();
                }
            })
            .catch(res => {
                if(res.response.status === 400) {
                    $(error_msg).text("입력한 핸드폰 번호가 중복됩니다.").show(); // 에러메시지 출력
                } else {
                    $(error_msg).text("오류입니다. 잠시 후 다시 시도해주세요.").show();
                }
            })
    } else {
        $(error_msg).text("전화번호 형식에 맞지 않습니다.").show();
        return false;
    }
    return false;
}

function stu_check_for_join() {
    const user_stu = $('#user_stu').val();
    let error_msg = $('#error_text_stu');
    if(/\d{6,8}/.test(user_stu) && parseInt(user_stu) > 99999) {
        axios.get('/user/join/', {
            params: {user_stu: user_stu},
            timeout: 1000
        })
            .then(() => {
                $(error_msg).hide();
            })
            .catch(res => {
                console.log(res.response)
                if(res.response.status === 400) {
                    $(error_msg).text('이미 등록되어 있는 학번입니다.').show();
                } else {
                    $(error_msg).text("오류입니다. 잠시 후 다시 시도해주세요.").show();
                }
            })
    } else {
        $(error_msg).text('유효하지 않은 형식입니다.').show();
    }
}

function maxLengthCheck(object) {
    if (object.value.length > object.maxLength) {
        object.value = object.value.slice(0, object.maxLength);
    }
}

function validation_check_for_join_form() {
    let errors = [];

    const user_name = $('#user_name').val().trim();
    if(user_name == null || user_name.length === 0){
        errors.push('이름을 입력하세요!\n');
    }

    const user_phone = $('#user_phone').val();
    if(user_phone != null && user_phone.length > 0){
        if($('#error_text_phone').css('display') === 'block'){
            errors.push('핸드폰 번호를 확인하세요!\n');
        }
    } else {
        errors.push('핸드폰 번호를 입력하세요!\n');
    }

    const user_stu = $('#user_stu').val();
    if(user_stu != null && user_stu.length > 0) {
        if($('#error_text_stu').css('display') === 'block'){
            errors.push('학번을 확인하세요!\n');
        }
    } else {
        errors.push('학번을 입력하세요!\n');
    }

    const user_major = $('#user_major').val();
    if (user_major == null || user_major.length === 0) {
        errors.push('전공을 선택하세요!\n');
    }

    // const user_grade = $('#user_grade').val();
    // if (user_grade == null || user_grade.length === 0) {
    //     errors.push('학년을 선택하세요!\n');
    // }

    return alert_or_submit(errors);
}

