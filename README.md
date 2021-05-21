# xml2yolo
fork from https://github.com/bjornstenger/xml2yolo

customize한 버전을 관리하기 위해 fork함.

참여 directory
1. tmp : labelImg를 통해 만들어낸 xml파일과 img 파일이 들어갈 directory
2. xml_backup : 작업이 끝난 후 xml파일이 백업될 directory
3. result : 최종 결과물이 들어갈 directory(yolov4 directory의 obj directory에 그대로 추가해주면 된다.)
4. obj : 작업이 끝난 전체 작업물이 저장될 directory
5. 
xml2yolo.py 실행시 train.txt 파일은 obj directory의 이미지 파일의 리스트를 학습 목록으로 만든다.(colab에서 학습할 데이터의 경로)
