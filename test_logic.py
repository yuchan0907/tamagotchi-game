"""게임 로직 검증용 시뮬레이션 (tkinter 불필요).

실행: python3 test_logic.py
"""

import random

from data import CHOICES, ENDINGS, MAX_AGE, STAT_MAX, STATUSES
from game_logic import Game, describe_status


def check_data():
    ids = [c["id"] for c in CHOICES]
    assert len(ids) == len(set(ids)), "선택지 id 중복"
    for c in CHOICES:
        assert c["options"], c["id"]
        for name in c.get("requires", []) + c.get("forbids", []):
            assert name in STATUSES, (c["id"], name)
        for o in c["options"]:
            for name in list(o.get("add", {})) + o.get("remove", []):
                assert name in STATUSES, (c["id"], name)
            if o.get("ending"):
                assert o["ending"] in ENDINGS, (c["id"], o["ending"])
    for name in STATUSES:
        describe_status(name, 2)  # 예외 없이 문자열 생성되는지
    for age in range(MAX_AGE):
        # 각 나이에 고정 선택지가 있다면 최대 1개
        assert sum(1 for c in CHOICES if c.get("fixed_age") == age) <= 1


def play_random(seed, policy):
    game = Game(seed=seed)
    rng = random.Random(seed * 7 + 1)
    steps = 0
    while not game.is_over:
        n = len(game.current_choice["options"])
        idx = rng.randrange(n) if policy == "random" else 0
        game.choose(idx)
        for v in game.stats.values():
            assert 0 <= v <= STAT_MAX
        for t in game.statuses.values():
            assert t > 0
        steps += 1
        assert steps < 500, "무한 루프 의심"
    return game


def main():
    check_data()

    counts = {}
    for seed in range(2000):
        for policy in ("random", "first"):
            g = play_random(seed, policy)
            counts[g.ending] = counts.get(g.ending, 0) + 1
            assert g.history  # 돌아보기 기록 존재
    print("엔딩 분포 (4000판):")
    for key, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {ENDINGS[key]['title']:<14} {n}")

    # 면역 동작 확인: 예방접종 상태에서는 감기에 걸리지 않아야 함
    g = Game(seed=1)
    g.statuses["예방접종"] = 5
    log = []
    g._add_status("감기", 3, log)
    assert "감기" not in g.statuses and log

    # 고정 선택지: 첫 턴은 나이 0 고정 선택지
    assert Game(seed=3).current_choice_id == "age0_meet"
    print("모든 검증 통과")


if __name__ == "__main__":
    main()
