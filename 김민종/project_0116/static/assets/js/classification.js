function classification() {

}

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById('preview').src = e.target.result;
            document.getElementById('preview').style.width = '400px';
            document.getElementById('preview').style.height = '400px';

        };
        reader.readAsDataURL(input.files[0]);
    } else {
        document.getElementById('preview').src = "";
    }
}
// 이미지 사이즈 체크박스 변경시 visibility 설정
function hide(e) {
    var box = document.getElementById("size");
    if (e.checked) {
        box.style.display = "block";
    } else {
        box.style.display = "none";
    }
}