# 02. 강아지 이미지 규칙

어떤 상황에 어떤 그림이 나오는지 정리한 문서임. [← README](../README.md)

이미지는 `images/` 폴더의 PNG 14장(160x160, 도트 그래픽)이고, 고르는 코드는 `game_logic.py`의 `pet_image_name()`임.

## 고르는 순서
위에 있는 조건일수록 우선순위가 높고, 처음 맞는 조건에서 바로 결정함.

| 순위 | 조건 | 이미지 |
| --- | --- | --- |
| 1 | 엔딩이 남 | 엔딩 이미지 (아래 표) |
| 2 | 부상 상태 | `injured` |
| 3 | 감기 상태 | `sick` |
| 4 | 우울 상태 | `depressed` |
| 5 | 배고픔 상태 | `hungry` |
| 6 | 신남 상태 | `excited` |
| 7 | 배부름 상태 | `full` |
| 8 | 건강 3 이하 | `sick` |
| 9 | 행복 3 이하 | `sad` |
| 10 | 행복 7 이상 | `happy` |
| 11 | 나이 0~1살 | `puppy` |
| 12 | 나이 7살 이상 | `senior` |
| 13 | 그 외 | `normal` |

## 엔딩 이미지
| 엔딩 | 이미지 |
| --- | --- |
| sick, natural_warm, natural_lonely | `ending_angel` |
| runaway, strayed | `ending_lonely` |
| ten_years | `ending_good` |

## 이미지 목록
`puppy`, `normal`, `senior`, `happy`, `sad`, `sick`, `hungry`, `full`, `excited`, `injured`, `depressed`, `ending_good`, `ending_angel`, `ending_lonely`
