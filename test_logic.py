"""게임 규칙이 오류 없이 돌아가는지 확인하는 테스트 파일.

실행 방법:  python test_logic.py
(화면(tkinter)은 필요 없습니다. 게임을 여러 번 자동으로 플레이해 봅니다.)
"""

import random

import game_logic
from game_logic import game
from data import CHOICES, ENDINGS, STAT_MAX, STATUSES


def test_data():
    """data.py에 오타가 없는지 검사한다."""
    ids = []
    for choice in CHOICES:
        ids.append(choice["id"])
        assert 1 <= len(choice["options"]) <= 3, choice["id"] + ": 선택지 답변은 1~3개"

        for name in choice.get("requires", []) + choice.get("forbids", []):
            assert name in STATUSES, f"{choice['id']}: 없는 상태 '{name}'"

        for option in choice["options"]:
            for name in option.get("add", {}):
                assert name in STATUSES, f"{choice['id']}: 없는 상태 '{name}'"
            for name in option.get("remove", []):
                assert name in STATUSES, f"{choice['id']}: 없는 상태 '{name}'"
            if "ending" in option:
                assert option["ending"] in ENDINGS, f"{choice['id']}: 없는 엔딩"

    assert len(ids) == len(set(ids)), "선택지 id가 겹칩니다"
    print("data.py 검사 통과")


def play_one_game():
    """무작위로 선택지를 골라 엔딩까지 한 판 플레이한다."""
    game_logic.new_game()
    count = 0
    while game["ending"] == "":
        number_of_options = len(game["choice"]["options"])
        game_logic.choose(random.randrange(number_of_options))

        # 스테이터스는 항상 0~10 이어야 한다
        for value in game["stats"].values():
            assert 0 <= value <= STAT_MAX

        count += 1
        assert count < 500, "끝나지 않는 게임?"
    return game["ending"]


def test_play():
    results = {}
    for i in range(2000):
        ending = play_one_game()
        results[ending] = results.get(ending, 0) + 1

    print("2000판 플레이 결과 (엔딩별 횟수):")
    for key in results:
        print(f"  {ENDINGS[key]['title']} : {results[key]}")


def test_vaccine():
    """예방접종 상태에서는 감기에 안 걸려야 한다."""
    game_logic.new_game()
    game["statuses"]["예방접종"] = 5
    log = []
    game_logic.add_status("감기", 3, log)
    assert "감기" not in game["statuses"]
    print("예방접종 검사 통과")


test_data()
test_play()
test_vaccine()
print("모든 테스트 통과!")
