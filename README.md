# 🐶 tamagotchi-game

강아지 다마고치를 키우는 턴제 선택형 게임임. (프로그래밍 기초 조별과제)

## 실행 방법

Python 3.8 이상 필요. 별도로 설치할 패키지는 없음. (tkinter는 Python에 기본 포함)

```
python main.py        # 게임 실행 (Mac/리눅스는 python3, 윈도우는 py)
python test_logic.py  # 게임 규칙 자동 테스트 (화면 없이 2000판 플레이)
```

## 문서 목차

자세한 설명은 `docs` 폴더에 나누어 정리함. 필요한 문서만 골라 읽으면 됨.

| 문서 | 제목 | 이런 때 읽음 |
| --- | --- | --- |
| [01-features.md](docs/01-features.md) | 구현 요소 | 게임에 어떤 기능이 있는지 알고 싶을 때 |
| [02-images.md](docs/02-images.md) | 강아지 이미지 규칙 | 어떤 상황에 어떤 그림이 나오는지 알고 싶을 때 |
| [03-code-reading.md](docs/03-code-reading.md) | 코드 구조와 읽는 순서 | 코드를 처음 읽을 때 |
| [04-how-to-edit.md](docs/04-how-to-edit.md) | 코드 수정하는 방법 | 선택지, 상태, 엔딩, 이미지를 추가하거나 숫자를 바꿀 때 |
| [05-test-and-errors.md](docs/05-test-and-errors.md) | 테스트와 자주 발생하는 오류 | 수정 후 확인하거나 오류가 났을 때 |
| [06-team-git.md](docs/06-team-git.md) | 팀원과 같이 작업하는 방법 (Git) | 팀원과 코드를 합칠 때 |

## 파일 구성

```
README.md              이 문서 (소개와 목차)
docs/                  세부 설명 문서
data.py                게임 "내용" (선택지, 상태, 엔딩 글, 이미지 목록)   ← 내용을 바꿀 땐 여기만!
game_logic.py          게임 "규칙" (턴 진행, 계절, 엔딩 판정, 이미지 고르기)
main.py                "화면" (tkinter로 그리기, 버튼)
test_logic.py          자동 테스트
images/                강아지 도트 이미지 (PNG)
tools/make_images.py   이미지를 만드는 도구 (게임 실행에는 필요 없음)
```
