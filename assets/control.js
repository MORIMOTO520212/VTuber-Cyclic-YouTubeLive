function curtainOC(){
    // 幕の開閉
    element = document.getElementById("curtain");
    if(element.className == "curtain open"){
        element.className = "curtain close";
    }else{
        element.className = "curtain open";
    }
    return;
}