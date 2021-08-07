// common
function validation_check_for_file_upload() {
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

// common
function validation_check_for_title() {
    let error = null; // if there are no any errors, error=null, or error =  '...'

    let title = $('input[name$="title"]').val();  // Matches those that end with 'title'

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

    $.each($(content_div).children('p'), function() {
        if($(this).text().trim().length > 0) {
            error = null;
            return false;
        }
    });

    return error
}

function  validation_check_for_common_things() {
    // common validation methods
    let array_of_validation_method = [
        validation_check_for_title,
        validation_check_for_contents,
        validation_check_for_file_upload,
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


    // if there are any errors, not submit contest_form and alert all messages!
    if (errors.length > 0) {
        alert(errors.join(''));
        return false;
    } else {
        return true;
    }

}

