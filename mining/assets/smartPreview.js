function smart_preview(list_id, status) {
    /*
        list_id: ユーザーID
        status:
          true - プレビュー
          false - 閉じる
    */
    if(status){
        document.getElementById(list_id).children[0].setAttribute("src", `https://www.youtube.com/embed/${channel_list[list_id]}?autoplay=1&mute=1&controls=0&modestbranding=0&showinfo=0`);
    }else{
        document.getElementById(list_id).children[0].setAttribute("src", "");
    }
}