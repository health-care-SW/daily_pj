### HTTP의 특징
- HTTP 메세지는 서버와 클라이언트에 의해 해석된다
- TCP/IP를 이용하는 응용프로토콜이다
- HTTP는 연결상태를 유지하지 않는 비연결성 프로토콜입니다. 클라이언트가 이전에 요청한 내용을 저장하지 않는다.
- 비연결성의 단점을 해결하기 위해 쿠키과 세션이 등장했다.
- 비연결성 프로토콜이기 때문에 요청/응답 방식으로 동작한다.
- 도메인 + 자윈위치, 도메인 + 자원의 식별자를 통해서 요청을 하고, 서버가 요청에 따른 HTML 문서 응답을 해줌

과거에는 로그인 등 현재에서 사용하는 어플리케이션을 생각하지 못했다. 그래서 클라이언트의 요청을 저장하지 않는 비 연결성 프로토콜로 제작되었다.

쿠키는 연결된 통신을 하기 원할 때, 