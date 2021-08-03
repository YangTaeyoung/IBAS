let alert_msg_for_client = (response) => {
    if (response.status >= 500) {
        alert('서버 오류입니다.')
    } else if (response.status >= 400) {
        alert('유효하지 않은 값입니다.')
    }
}

export {alert_msg_for_client}