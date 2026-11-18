# tamagotchi-game

강아지 다마고치를 키우는 턴제 선택형 게임입니다. (프로그래밍 기초 조별과제)

## 실행 방법

Python 3.10 이상, tkinter가 필요합니다.

```bash
python3 main.py
```

로직 검증(tkinter 불필요):

```bash
python3 test_logic.py
```

## 구현 요소

| 요소 | 내용 | 위치 |
| --- | --- | --- |
| 스테이터스 바 | 건강 / 행복 / 친밀도 (0~10, ■□ 막대) | `main.py` `refresh()` |
| 상태창 | 배부름·감기 등 키워드 상태, 마우스 오버 시 효과·남은 턴 표시 | `data.py` `STATUSES`, `main.py` `Tooltip` |
| 선택지 | 매 턴 무작위 선택지 + 나이 고정 / 상태 조건 / 계절 선택지 | `data.py` `CHOICES`, `game_logic.py` |
| 나이 / 계절 | 선택마다 계절이 바뀌고 한 바퀴 돌면 1살 | `game_logic.py` `_advance_season()` |
| 다마고치 | 캔버스로 그린 강아지 (행복·건강에 따라 표정 변화) | `main.py` `draw_pet()` |
| 엔딩 | 스테이터스 바닥 / 잘못된 선택 / 자연사(7살~) / 10살 도달, 선택 기록 돌아보기 | `data.py` `ENDINGS` |

## 파일 구성

- `data.py` : 상태, 선택지, 엔딩 데이터 (내용을 추가하려면 여기만 수정)
- `game_logic.py` : 게임 규칙 (UI와 분리)
- `main.py` : tkinter 화면
- `test_logic.py` : 로직 시뮬레이션 테스트

## 선택지 추가 방법

`data.py`의 `CHOICES` 리스트에 딕셔너리를 추가하면 됩니다.

```python
{
    "id": "my_choice",
    "seasons": ["가을"],        # 선택: 등장 계절
    "requires": ["감기"],       # 선택: 이 상태가 있을 때만 등장
    "prompt": "상황 설명",
    "options": [
        {"text": "선택지 문구", "stats": {"happiness": 1},
         "add": {"신남": 2}, "result": "결과 문구"},
    ],
}
```
