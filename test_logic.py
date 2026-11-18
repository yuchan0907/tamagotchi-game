"""게임 규칙이 오류 없이 돌아가는지 확인하는 테스트 파일.

실행 방법:  python test_logic.py
(화면(tkinter)은 필요 없습니다. 게임을 여러 번 자동으로 플레이해 봅니다.)
"""

import os
import random
import struct

import game_logic
from game_logic import game
from data import CHOICES, ENDING_IMAGES, ENDINGS, IMAGE_NAMES, STAT_MAX, STATUSES

IMAGE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")


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


def test_images():
    """이미지 파일이 모두 있고, PNG 파일이며, 크기가 160x160인지 검사한다."""
    for name in IMAGE_NAMES:
        path = os.path.join(IMAGE_FOLDER, name + ".png")
        assert os.path.exists(path), f"images/{name}.png 파일이 없습니다"
        with open(path, "rb") as f:
            header = f.read(24)
        assert header[:8] == b"\x89PNG\r\n\x1a\n", f"{name}.png 는 PNG 파일이 아닙니다"
        width, height = struct.unpack(">II", header[16:24])
        assert (width, height) == (160, 160), f"{name}.png 크기가 {width}x{height} 입니다"

    for key in ENDINGS:
        assert key in ENDING_IMAGES, f"ENDING_IMAGES에 '{key}' 엔딩이 없습니다"
        assert ENDING_IMAGES[key] in IMAGE_NAMES, f"'{key}' 엔딩의 이미지 이름이 없습니다"
    print("이미지 검사 통과")


# 플레이 중에 실제로 사용된 이미지 이름들
used_images = set()


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

        # 어떤 상황에서도 존재하는 이미지 이름이 나와야 한다
        used_images.add(game_logic.pet_image_name())
        assert game_logic.pet_image_name() in IMAGE_NAMES

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
test_images()
test_play()
print("플레이 중 사용된 이미지:", sorted(used_images))
test_vaccine()
print("모든 테스트 통과!")
