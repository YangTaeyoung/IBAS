function login_isFailed(flag) // 비정상적인 경로를 통해 로그인한 경우 (해킹 시도)
{
    if(flag) {
        alert("비 정상적인 경로로 접근하셨습니다.")
    }
}
