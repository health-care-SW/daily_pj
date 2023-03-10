### FLASK PROJECT
---01.15.2023---
* db 조회 (app_data.py), 이미지 전처리 (app_image.py) 구현
* 절대경로 --> 상대경로 변경

---01.16.2023---
* blueprint로 api.py, app_data.py, app_image.py 묶어서 실행 (app.py)

---01.17.2023---
* 회원가입, 로그인, 로그아웃 구현 (jQuery, Ajax 사용 x)

---01.18.2023---
* 로그인 오류 시 오류 나타내게 변경
* 게시판 및 글 작성 기능 작업중 (app_post.py, post.html, content.html, ...)
* db 에러 --> sqlalchemy 2.5.1로 다운그레이드

---01.19.2023---
* 게시글 작성, 삭제 기능 구현
* sql 변경, 이미지 처리, 게시글 열람 및 작성 기능 로그인 해야 사용하도록 변경
* 로그인 여부에 따라 유저명 표시
* 프로필 페이지에 본인 작성글 출력

---01.20.2023---
* 게시글 수정 기능 구현
* 메인 페이지 작성
* css로 페이지 다듬기

### STREAMLIT PROJECT
---01.25.2023---
* 꿀벌 건강 상태 및 종 구분 과제로 진행
* 벌 사진 업로드 하여 테스트할 수 있도록 만드는 것이 목표

---01.26.2023---
* expander로 데이터프레임 & 그래프 숨기기
* 꿀벌 건강, 꿀벌 종 모델 저장하여 벌 사진 업로드시 결과 출력

---01.27.2023---
* 경구약제 5000종 조합 약제 이미지 크롭 전처리 및 학습, 모델 저장하여 약제 사진 업로드시 결과 출력
* gpu 인식 문제로 고생
* 전이학습
* 특정 약제만 결과로 나오는 치명적인 오류...

---01.28.2023---
* 경구약제 5000종 추가 전처리 -- 10장이 안되는 약제 6종 제외, 데이터 균형 조정
* 특정 약제만 결과로 나오는 오류 어느 정도 해결.
* streamlit-cropper 사용하여 이미지 크롭 기능 추가.
* 용량 문제로 bee_health_model, bee_species_model은 구글 드라이브에 업로드 
* (bee_health_model https://drive.google.com/file/d/1lDrWyNgVv0z2YBKcmrOTZlrzwx92v4c8/view?usp=share_link)
* (bee_species_model https://drive.google.com/file/d/1UW2zX0D9XosTVMeAzL7arPK2HF1K3PfG/view?usp=share_link)
