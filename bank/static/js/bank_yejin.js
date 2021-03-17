//수정 아이콘을 클릭하면 등록 아이콘으로 바뀌고, 등록 아이콘을 클릭했을 때 메세지 뜨기

function bank_update() {

    document.getElementById('bank-date-1').disabled = false; // input창 disabled속성을 해제, disabled 속성을 거짓이라 둠.
    document.getElementById('bank-date-1').classList.add("bank-input-add");

    document.getElementById('bank-txt-1').disabled = false; // input창 disabled속성을 해제, disabled 속성을 거짓이라 둠.
    document.getElementById('bank-txt-1').classList.add("bank-input-add");

    document.getElementById('bank-earn-1').disabled = false; // input창 disabled속성을 해제, disabled 속성을 거짓이라 둠.
    document.getElementById('bank-earn-1').classList.add("bank-input-add");

    document.getElementById('bank-spend-1').disabled = false; // input창 disabled속성을 해제, disabled 속성을 거짓이라 둠.
    document.getElementById('bank-spend-1').classList.add("bank-input-add");

    document.getElementById('bank-money-1').disabled = false; // input창 disabled속성을 해제, disabled 속성을 거짓이라 둠.
    document.getElementById('bank-money-1').classList.add("bank-input-add");


    //아이콘 바꾸어 주기 위해 변수 선언. 수정 아이콘을 바꾸어 주어야 하므로 id로 update를 가져옴.
    var icon = document.getElementById('bank-update')
    // 아이콘 class 속성을 바꾸어 주어 아이콘 변경하기
    icon.setAttribute("class", "fa fa-check")

    //check 아이콘은 하나 뿐이므로 인덱스 0번 사용.
    var check_icon = document.getElementsByClassName('fa fa-check')[0]

    //check 아이콘 클릭 시 confirm 알림나옴.
    check_icon.onclick = function () {
        confirm("수정하시겠습니까?")
        }

}

// 아이콘 눌렀을 때 삭제 comfirm 알림 나옴.
function bank_del() {
    confirm('정말로 삭제하시겠습니까?')

}

function bank_add() {
    var conDiv = document.getElementById("conDiv");

    var dateDiv = document.createElement("div");
    var dateInput = document.createElement("input");

    var txtDiv = document.createElement("div");
    var txtInput = document.createElement("input");

    var earnDiv = document.createElement("div");
    var earnInput = document.createElement("input");

    var spendDiv = document.createElement("div");
    var spendInput = document.createElement("input");

    var moneyDiv = document.createElement("div");
    var moneyInput = document.createElement("input");

    var fileDiv = document.createElement("div");
    var fileInput = document.createElement("input");
    var fileLabel = document.createElement("label");


    dateInput.classList = "bank-input-add";
    dateInput.type = "date";
    dateInput.placeholder = "내용을 입력해주세요."

    txtInput.classList = "bank-input-add";
    txtInput.type = "text";
    txtInput.placeholder = "내용을 입력해주세요."

    earnInput.classList = "bank-input-add";
    earnInput.type = "text";
    earnInput.placeholder = "내용을 입력해주세요."

    spendInput.classList = "bank-input-add";
    spendInput.type = "text";
    spendInput.placeholder = "내용을 입력해주세요."

    moneyInput.classList = "bank-input-add";
    moneyInput.type = "text";
    moneyInput.placeholder = "내용을 입력해주세요.";

    fileLabel.classList = "input-file-button bank-margin-bottom_0 bank-margin-left_10";
    fileLabel.htmlFor = "input-file-2";
    fileLabel.innerHTML = "첨부";

    fileInput.type = "file";
    fileInput.id = "input-file-2.";
    fileInput.style.display = "none";

    dateDiv.classList = "bank-flex";
    txtDiv.classList = "bank-flex";
    earnDiv.classList = "bank-flex";
    spendDiv.classList = "bank-flex";
    moneyDiv.classList = "bank-flex";
    fileDiv.classList = "bank-flex";


    dateDiv.appendChild(dateInput);
    txtDiv.appendChild(txtInput);
    earnDiv.appendChild(earnInput);
    spendDiv.appendChild(spendInput);
    moneyDiv.appendChild(moneyInput);
    fileDiv.appendChild(fileInput);
    fileDiv.appendChild(fileLabel);



    conDiv.appendChild(dateDiv);
    conDiv.appendChild(txtDiv);
    conDiv.appendChild(earnDiv);
    conDiv.appendChild(spendDiv);
    conDiv.appendChild(moneyDiv);
    conDiv.appendChild(fileDiv);


}