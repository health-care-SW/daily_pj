const check = document.getElementsByName("pre_toggle_2")[0];
const width = document.getElementsByName("width")[0];
const height = document.getElementsByName("height")[0];

function f () {
    console.log(check.checked);
    if (check.checked){
        width.style.display='inline';
        height.style.display='inline'
    } else {
        width.style.display='none';
        height.style.display='none'
    }
}

check.addEventListener("click", f)