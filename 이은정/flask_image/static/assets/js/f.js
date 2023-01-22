function f() {
  var check_b = document.getElementsByName("pre_toggle_2")[0];
  var size = document.getElementsByName("size")[0];
  if (check_b.checked) {
    size.style.display = "inline";
    console.log(check_b.checked);
  } else {
    size.style.display = "none";
  }
}
