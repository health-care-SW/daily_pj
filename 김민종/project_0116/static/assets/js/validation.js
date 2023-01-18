var inputID = document.getElementById("inputID");
var inputPassword = document.getElementById("inputPassword");
var inputEmail = document.getElementById("inputEmail");
var inputPhoneNum= document.getElementById("inputPhoneNum");
var button = document.getElementById("signin_button");
var chkbox = document.getElementById("chkbox");

inputID.addEventListener('keyup',activeEvent);
inputPassword.addEventListener('keyup',activeEvent);
inputEmail.addEventListener('keyup',activeEvent);
inputPhoneNum.addEventListener('keyup',activeEvent);


function activeEvent() {
    switch(!(inputEmail.value && inputID.value && inputPassword.value && inputPhoneNum.value && chkbox.checked)) {
        case true:
            button.disabled = true;
            break;
        case false:
            button.disabled = false;
            break;
    }
}

function chkLogin() {
	var id = document.getElementById("email");
	var pwd = document.getElementById("password");

    if(id.value.length < 2 || id.value.length > 10) {
        alert("아이디를 다시 입력해주세요")
        id.focus()
        id.select()
        return false;
    }
	if(pwd.value.length < 8){
		alert("비밀번호를 다시 입력해주세요.");
		pwd.select();
		pwd.focus();
		return false;
	}
    document.login.submit();
    // login_user();
}

function chkSignin(){
	var inputID = document.getElementById("inputID");
	var inputPassword = document.getElementById("inputPassword");
	var inputEmail = document.getElementById("inputEmail");
	var inputPhoneNum= document.getElementById("inputPhoneNum");
	
	if(inputID.value.length < 2 || inputID.value.length >10){
		alert("아이디은 최소 2글자에서 최대 10글자까지 입력하세요");
		inputID .select();
		inputID .focus(); 
		return false;
	}
	
	if(inputPassword.value.length < 8){
		alert("비밀번호는 최소8글자에서 이상 입력하세요.");
		inputID .select();
		inputID .focus();
		return false;
	}
	if(!inputEmail.value.includes("@")){
		alert("@ 이메일 형식을 지켜주세요");
		inputEmail .select();
		inputEmail .focus();
		return false;
	}    
	document.signin.submit();
}

function chkAddWriting(){
	var title = document.getElementById("title");
	var dsc = document.getElementById("description");
	var name = document.getElementById("name");
	var date= document.getElementById("date");
	
	if(title.value.length < 2 || name.value.length >20){
		alert("제목은 최소 2글자에서 최대 20글자까지 입력하세요");
		name.select();
		name.focus();
		return false;
	}
	if(dsc.value.length < 2){
		alert("내용은 최소 2글자이상 입력하세요");
		dsc.select();
		dsc.focus();
		return false;
	}
	
	document.newWrite.submit();
}

 /* Ajax를 이용해 login() 함수를 완성하세요. */
// function login_user() {
//     let user_id = $("#email").val()
//     let user_pw = $("#password").val()
// 	var d = {
// 		'id': user_id,
// 		'pwd': user_pw
// 	}
// 	$.ajax({
// 		url: '/login',
// 		type: 'post',
// 		contentType: 'application/json',
// 		data:  JSON.stringify(d),
// 		success: function (res) {
// 			if (res['result'] == 'success') {
// 				alert("로그인 성공")
// 				window.location.href = '/'
// 			} else {
// 				alert("로그인 실패!")
// 				window.location.reload()
// 			}
// 		}
// 	})
    
// }
