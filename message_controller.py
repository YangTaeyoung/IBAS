from django.contrib import messages


def alert(request, msg: str):
    messages.info(request, "<script>alert('" + msg + "')</script>")
