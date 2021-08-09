// ================================== register 관련 js ========================================= //
// 파일 확장자를 반환하는 함수 (.)포함
function getExtensionOfFilename(filename) {
    var _fileLen = filename.length;
    /**
     * lastIndexOf('.')
     * 뒤에서부터 '.'의 위치를 찾기위한 함수
     * 검색 문자의 위치를 반환한다.
     * 파일 이름에 '.'이 포함되는 경우가 있기 때문에 lastIndexOf() 사용
     */
    var _lastDot = filename.lastIndexOf('.');
    // 확장자 명만 추출한 후 소문자로 변경
    return filename.substring(_lastDot, _fileLen).toLowerCase();
}
// 이미지 파일인지 아닌지 확인하는 함수
function isImageFile(fileName) {
    ext = getExtensionOfFilename(fileName)
    console.log(ext);
    if (ext === ".jpg" || ext === ".png" || ext === ".bmp"|| ext === ".tif" || ext === ".gif")
    {
        return true;
    }
    return false;
}
// img태그를 쓸지 파일 아이콘을 쓸 지 결정하는 함수
function decisionIcon(contObj,filePath) {
    let imgObj;
    let fileIconObj;
    if (isImageFile(filePath)) {
        imgObj = document.createElement("img")
        imgObj.src = "/media/" + filePath;
        imgObj.alt = "현재 브라우저에서 지원하지 않습니다.";
        imgObj.className = "file-img height-100 width-100 img-bd";
        contObj.appendChild(imgObj);
    } else {
        fileIconObj = document.createElement("div");
        fileIconObj.className = "fa fa-file fa-3x file-img height-100 width-100 img-bd file-icon-p";
        contObj.appendChild(fileIconObj);
    }
}
function delImg(contObj) {
    contObj.remove();
}