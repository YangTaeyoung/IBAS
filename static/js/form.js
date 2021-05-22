function goSubmit(form_id, isCheck = false, msg = "") {
    if (isCheck) {
        if (confirm(msg)) {
            document.getElementById(form_id).submit();
        }
    } else {
        document.getElementById(form_id).submit();
    }
}

