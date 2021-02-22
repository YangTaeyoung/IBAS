function clickBox(idx) {
    var menuItemList = document.getElementsByClassName('card');


    if (idx === 0) {
        // document.getElementById("explain-text-0").style.display = "block";
        // document.getElementById("explain-text-1").style.display = "none";
        menuItemList[0].style.border = "3px solid #091069";
        menuItemList[0].style.borderRadius = "3px";
        menuItemList[1].style.border = "";
        menuItemList[1].style.borderRadius = "";
        // document.getElementById("auth-btn-0").style.display = "block";
        // document.getElementById("auth-btn-1").style.display = "none";


    } else {
        // document.getElementById("explain-text-0").style.display = "none";
        // document.getElementById("explain-text-1").style.display = "block";
        menuItemList[1].style.border = "3px solid #091069";
        menuItemList[1].style.borderRadius = "3px";
        menuItemList[0].style.border = "";
        menuItemList[0].style.borderRadius = "";
        // document.getElementById("auth-btn-1").style.display = "block";
        // document.getElementById("auth-btn-0").style.display = "none";
    }

}



