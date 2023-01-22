//텍스트 작성과 삭제 즉시 실행함수
(function () {
  //span 요소 노드 가져오기
  const spanElement = document.querySelector("main h2 span");
  //화면에 표시할 문장 배열
  const txtArray = [
    "Web Publisher",
    "Front-End Developer",
    "Web UI Designer",
    "UX Designer",
    "Back-End Developer",
  ];
  //배열의 인덱스 초깃값
  let index = 0;
  //화면에 표시할 문장 배열에서 요소를 하나 가져온 뒤, 배열로 만들기
  let currentTxt = txtArray[index].split("");

  function writeTxt() {
    spanElement.textContent += currentTxt.shift();
    if (currentTxt.length != 0) {
      setTimeout(writeTxt, Math.floor(Math.random() * 100));
    } else {
      currentTxt = spanElement.textContent.split("");
      setTimeout(deleteTxt, 4000);
    }
  }

  function deleteTxt() {
    currentTxt.pop();
    spanElement.textContent = currentTxt.join("");
    if (currentTxt.length != 0) {
      setTimeout(deleteTxt, Math.floor(Math.random() * 100));
    } else {
      index = (index + 1) % txtArray.length;
      currentTxt = txtArray[index].split("");
      writeTxt();
    }
  }
  writeTxt();
})();

//스크롤이벤트
const headerElement = document.querySelector("header");
window.addEventListener("scroll", function () {
  requestAnimationFrame(scrollCheck);
});
function scrollCheck() {
  let browserScrollY = Window.scrollY ? window.scrollY : window.pageYOffset;
  if (browserScrollY > 0) {
    headerElement.classList.add("active");
  } else {
    headerElement.classList.remove("active");
  }
}

//애니메이션 스크롤 이동
const animationMove = function(selector) {
  //1.selector매개변수로 이동할 대상 요소 노드 가져오기
  const targetElement = document.querySelector(selector);
  //2.현재 웹 브라우저의 스크롤정보 (y값)
  const browserScrollY = window.pageYOffset;
  //3.이동할 대상의 위치 (y값)
  const targetScrollY =
    targetElement.getBoundingClientRect().top + browserScrollY;
  //4.스크롤 이동
  window.scrollTo({ top: targetScrollY, behavior: 'smooth' });
};

//스크롤 이벤트 연결하기
const scrollMoveElement = document.querySelectorAll(
  '[data-animation-scroll="true"]'
);
for (let i = 0; i < scrollMoveElement.length; i++) {
  scrollMoveElement[i].addEventListener('click', function(e) {
    const target = this.dataset.target;
    animationMove(target);
  });
}
