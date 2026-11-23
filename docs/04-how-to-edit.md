# 04. 코드 수정하는 방법

내용을 바꿀 때는 대부분 `data.py`만 수정하면 됨. [← README](../README.md)

## 선택지 추가
`data.py`의 `CHOICES` 리스트 안에 아래 형태를 추가함. `id`는 다른 선택지와 겹치면 안 됨.
```python
{
    "id": "my_choice",
    "seasons": ["여름"],            # (선택) 이 계절에만 등장함
    "prompt": "상황 설명 문장",
    "options": [
        {"text": "버튼 글자", "stats": {"happiness": 1}, "add": {"신남": 2},
         "result": "선택 후 나오는 문장"},
        {"text": "다른 버튼", "result": "아무 변화 없음"},
    ],
},
```
선택 가능한 항목: `fixed_age`, `min_age`, `seasons`, `requires`, `forbids`. 답변은 1~3개까지 가능함.

## 상태 추가
1. `STATUSES`에 `per_turn`(매 턴 효과)과 `flavor`(설명 문장)를 적음.
2. 선택지의 `add`에 `{"상태": 지속 턴}`으로 넣음.
3. 그림을 연결하려면 `game_logic.py`의 `pet_image_name()`에 `if` 한 줄을 추가함.

## 엔딩 추가
1. `data.py`의 `ENDINGS`에 `title`과 `text`를 추가함.
2. `ENDING_IMAGES`에 엔딩 키와 이미지를 연결함.
3. `game_logic.py`의 `check_stat_ending()` 또는 `advance_season()`에 발생 조건을 추가함.

## 이미지 추가
1. 160x160 PNG를 `images/`에 넣음.
2. `data.py`의 `IMAGE_NAMES`에 이름(`.png` 제외)을 추가함.
3. `pet_image_name()`에서 사용하도록 연결함.

## 숫자 바꾸기
| 바꾸고 싶은 것 | 위치 |
| --- | --- |
| 시작 스테이터스 | `data.py` `INITIAL_STATS` |
| 게임 종료 나이 | `data.py` `MAX_AGE` |
| 자연사 확률 | `game_logic.py` `advance_season()`의 `0.06` |
| 색 | `main.py` 위쪽 색 이름 상수 |
| 창 크기 | `main.py` `root.geometry("560x760")` |

수정한 뒤에는 `python test_logic.py`로 확인함. ([05-test-and-errors.md](05-test-and-errors.md))
