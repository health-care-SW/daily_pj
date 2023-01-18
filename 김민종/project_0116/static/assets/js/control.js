// window.onload = function() {
//     show_click.addEventListener("click", function () {
//         open_update();
//     });
//     cancel.addEventListener("click", function () {
//         cancel();
//     });
// }

function open_update() {
    var show_click = document.getElementById("show_area");
    var update = document.getElementById("update");
    var click_update = document.getElementById("click_update");
    var del_form = document.getElementById("del_form");
    var cancel = document.getElementById("cancel");
    var isClicked = false;
    isClicked = true;
    update.style.display = "inline";
    cancel.style.display = "inline";
    show_click.style.display = "none"
    del_form.style.display = "none"
    click_update.style.display = "inline";

}
function cancel() {
    var show_click = document.getElementById("show_area");
    var update = document.getElementById("update");
    var click_update = document.getElementById("click_update");
    var del_form = document.getElementById("del_form");
    var cancel = document.getElementById("cancel");
    update.style.display = "none";
    show_click.style.display = "inline"
    cancel.style.display = "none";
    del_form.style.display = "inline"
    click_update.style.display = "none";
}


function delete_writing(id) {
    if(confirm("글을 삭제하시겠습니까?") == true) {
        $.ajax({
            type: 'POST',
            url: '/delete_writing',
            data: id,
            dataType : 'text',
            contentType: "application/json",
            success: function(data){
                alert('글 삭제 완료')
                window.location.href="/community";
            },
            error: function(request, status, error){
                alert('ajax 통신 실패')
                alert(error);
            }
        })
    } else {
        return false
    }

}