# 06. 팀원과 같이 작업하는 방법 (Git)

팀원과 코드를 합칠 때 보는 문서임. [← README](../README.md)

## 기본 순서
```
git pull                       # 작업 시작 전에 최신 코드를 받음
(파일 수정)
git add .                      # 수정한 파일을 올릴 목록에 담음
git commit -m "무엇을 바꿨는지"   # 기록으로 저장함
git push                       # GitHub에 올림
```

## 규칙
- 작업 시작 전에는 항상 `git pull`을 먼저 실행함.
- 커밋 메시지에는 무엇을 바꿨는지 한 줄로 적음. (예: `겨울 선택지 추가`)
- 같은 파일을 동시에 고치지 않도록 역할을 나눔. 선택지는 `data.py`, 규칙은 `game_logic.py`, 화면은 `main.py`.
- push하기 전에 `python test_logic.py`로 테스트를 통과시킴.

## 충돌이 났을 때
같은 줄을 서로 고치면 `git pull` 때 충돌이 발생함.
1. 충돌한 파일을 열면 `<<<<<<<`, `=======`, `>>>>>>>` 표시가 있음.
2. 두 내용 중 남길 것을 정리하고 표시를 모두 지움.
3. `git add .` → `git commit` → `git push` 순서로 마무리함.

## push가 거절될 때
`rejected ... fetch first` 메시지는 GitHub에 내 컴퓨터에 없는 새 커밋이 있다는 뜻임. `git pull`을 한 뒤 다시 `git push`함.
