function chkDelete(lect_no) {
    if (confirm("정말 삭제하시겠습니까?")) {
        document.getElementById("lect_delete_form_" + lect_no).submit()
    }
}