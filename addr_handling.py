def go_board(board_type_no):
    return "<script>location.href='/board/" + str(board_type_no) + "/view/'</script>"


def go_board_detail(board_no):
    return "<script>location.href='/board/detail/" + str(board_no) + "'</script>"
