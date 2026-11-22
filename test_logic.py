"""게임 규칙이 오류 없이 동작하는지 확인하는 테스트 파일임.

실행 방법:  python test_logic.py
(화면(tkinter) 불필요. 게임을 여러 번 자동 플레이하여 확인함.)
"""

import os
import random
import struct

import game_logic
from game_logic import game
from data import CHOICES, ENDING_IMAGES, ENDINGS, IMAGE_NAMES, STAT_MAX, STATUSES

IMAGE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")


def test_data():
    """data.py에 오타가 없는지 검사함."""
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

    assert len(ids) == len(set(ids)), "선택지 id 중복됨"
    print("data.py 검사 통과")


def test_images():
    """이미지 파일의 존재 여부, PNG 형식, 160x160 크기를 검사함."""
    for name in IMAGE_NAMES:
        path = os.path.join(IMAGE_FOLDER, name + ".png")
        assert os.path.exists(path), f"images/{name}.png 파일 없음"
        with open(path, "rb") as f:
            header = f.read(24)
        assert header[:8] == b"\x89PNG\r\n\x1a\n", f"{name}.png PNG 형식이 아님"
        width, height = struct.unpack(">II", header[16:24])
        assert (width, height) == (160, 160), f"{name}.png 크기 오류 ({width}x{height})"

    for key in ENDINGS:
        assert key in ENDING_IMAGES, f"ENDING_IMAGES에 '{key}' 엔딩 누락됨"
        assert ENDING_IMAGES[key] in IMAGE_NAMES, f"'{key}' 엔딩의 이미지 이름 누락됨"
    print("이미지 검사 통과")


def play_one_game():
    """무작위로 선택지를 골라 엔딩까지 한 판 플레이함."""
    game_logic.new_game()
    count = 0
    while game["ending"] == "":
        number_of_options = len(game["choice"]["options"])
        game_logic.choose(random.randrange(number_of_options))

        # 스테이터스는 항상 0~10 범위여야 함
        for value in game["stats"].values():
            assert 0 <= value <= STAT_MAX

        # 어떤 상황에서도 존재하는 이미지 이름이 반환되어야 함
        assert game_logic.pet_image_name() in IMAGE_NAMES

        count += 1
        assert count < 500, "게임이 끝나지 않음"
    return game["ending"]


def test_play():
    results = {}
    for i in range(2000):
        ending = play_one_game()
        results[ending] = results.get(ending, 0) + 1

    print("2000판 플레이 결과 (엔딩별 횟수):")
    for key in results:
        print(f"  {ENDINGS[key]['title']} : {results[key]}")


test_data()
test_images()
test_play()
print("모든 테스트 통과!")
