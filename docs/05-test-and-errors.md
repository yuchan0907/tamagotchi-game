# 05. 테스트와 자주 발생하는 오류

수정한 뒤 확인하거나 오류가 났을 때 보는 문서임. [← README](../README.md)

## 테스트
```
python test_logic.py
```
화면 없이 실행되며 아래 내용을 검사함.

| 검사 | 내용 |
| --- | --- |
| `test_data` | 선택지 id 중복 없음, 존재하지 않는 상태 이름 없음, 답변이 1~3개 |
| `test_images` | 이미지 14장이 있고 PNG 형식이며 160x160 크기임, 엔딩 이미지 연결이 빠짐 없음 |
| `test_play` | 무작위로 2000판을 끝까지 플레이해 스테이터스가 0~10을 벗어나지 않고 무한 반복이 없는지 확인함 |

## 자주 발생하는 오류
| 증상 | 원인 | 해결 |
| --- | --- | --- |
| `No module named 'tkinter'` | tkinter가 설치되지 않음 | 윈도우/맥은 파이썬을 python.org에서 다시 설치함. 리눅스는 `sudo apt install python3-tk` |
| `KeyError: '상태이름'` | `add`나 `requires`에 `STATUSES`에 없는 이름을 씀 | 오타 확인 후 `test_logic.py`로 점검함 |
| `FileNotFoundError ... .png` | `images/`에 파일이 없거나 `IMAGE_NAMES`와 이름이 다름 | 파일 이름과 `IMAGE_NAMES`를 맞춤 |
| 한글이 깨져 보임 | 글꼴(`Malgun Gothic`)이 없는 운영체제임 | `main.py`의 `FONT` 글꼴 이름을 시스템 글꼴로 바꿈 (맥: `AppleGothic`) |
| 강아지 그림이 안 보임 | 그림을 `images` 딕셔너리에 보관하지 않음 | 불러온 이미지를 딕셔너리에 계속 보관함 |
| `IndexError: Cannot choose from an empty sequence` | 조건을 통과하는 선택지가 하나도 없음 | 조건 없는 일상 선택지를 충분히 유지함 |
| 들여쓰기 오류 | 탭과 공백이 섞임 | 공백 4칸으로 통일함 |
