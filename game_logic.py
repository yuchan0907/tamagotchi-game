"""다마고치 게임 로직 (UI와 무관한 순수 파이썬)."""

import random
from dataclasses import dataclass, field

from data import (
    CHOICES,
    ENDINGS,
    INITIAL_STATS,
    MAX_AGE,
    SEASONS,
    STAT_MAX,
    STAT_NAMES,
    STATUSES,
)


def clamp(value, low=0, high=STAT_MAX):
    return max(low, min(high, value))


def describe_status(name, remaining=None):
    """상태 이름 -> 마우스 오버 툴팁용 설명 문자열."""
    info = STATUSES[name]
    lines = []
    for stat, delta in info["per_turn"].items():
        verb = "증가" if delta > 0 else "감소"
        lines.append(f"매 턴마다 {STAT_NAMES[stat]}이(가) {abs(delta)} {verb}합니다")
    for immune in info.get("immune_to", []):
        lines.append(f"'{immune}' 상태에 걸리지 않습니다")
    if info.get("flavor"):
        lines.append("")
        lines.append(info["flavor"])
    if remaining is not None:
        lines.append("")
        lines.append(f"남은 턴 수 : {remaining}")
    return "\n".join(lines)


@dataclass
class TurnResult:
    result_text: str = ""
    stat_changes: dict = field(default_factory=dict)   # 선택지로 인한 변화
    log: list = field(default_factory=list)            # 상태 효과/계절 등 알림
    ending: str | None = None


class Game:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
        self.stats = dict(INITIAL_STATS)
        self.statuses = {}          # 상태 이름 -> 남은 턴 수
        self.age = 0
        self.season_index = 0
        self.turn = 0
        self.history = []           # 엔딩 후 돌아보기용 기록
        self.shown_fixed = set()
        self.recent_ids = []
        self.ending = None          # 엔딩 키
        self.current_choice = None
        self.current_choice_id = None
        self.next_choice()

    # ----- 조회 -----
    @property
    def season(self):
        return SEASONS[self.season_index]

    @property
    def is_over(self):
        return self.ending is not None

    def ending_info(self):
        return ENDINGS[self.ending] if self.ending else None

    # ----- 선택지 추첨 -----
    def _eligible(self, choice):
        if choice.get("fixed_age") is not None:
            return False
        if self.age < choice.get("min_age", 0) or self.age > choice.get("max_age", MAX_AGE):
            return False
        if "seasons" in choice and self.season not in choice["seasons"]:
            return False
        if any(s not in self.statuses for s in choice.get("requires", [])):
            return False
        if any(s in self.statuses for s in choice.get("forbids", [])):
            return False
        return True

    def next_choice(self):
        # 1) 이번 나이의 고정 선택지가 아직 안 나왔으면 우선 등장
        for choice in CHOICES:
            if choice.get("fixed_age") == self.age and choice["id"] not in self.shown_fixed:
                self.shown_fixed.add(choice["id"])
                self._set_choice(choice)
                return

        # 2) 조건에 맞는 선택지 중 가중치 추첨 (최근 3개는 제외)
        pool = [c for c in CHOICES if self._eligible(c)]
        fresh = [c for c in pool if c["id"] not in self.recent_ids]
        pool = fresh or pool
        weights = [c.get("weight", 3) for c in pool]
        self._set_choice(self.rng.choices(pool, weights=weights, k=1)[0])

    def _set_choice(self, choice):
        self.current_choice = choice
        self.current_choice_id = choice["id"]
        self.recent_ids = (self.recent_ids + [choice["id"]])[-3:]

    # ----- 상태 조작 -----
    def _add_status(self, name, turns, log):
        for owned in self.statuses:
            if name in STATUSES[owned].get("immune_to", []):
                log.append(f"'{owned}' 덕분에 '{name}' 상태를 막았다!")
                return
        self.statuses[name] = turns

    def _change_stat(self, stat, delta):
        before = self.stats[stat]
        self.stats[stat] = clamp(before + delta)
        return self.stats[stat] - before

    # ----- 턴 진행 -----
    def choose(self, index):
        """선택지 index를 고르고 한 턴을 진행한다. TurnResult를 반환."""
        if self.is_over:
            raise RuntimeError("이미 엔딩이 난 게임입니다.")

        choice = self.current_choice
        option = choice["options"][index]
        result = TurnResult(result_text=option.get("result", ""))

        # 1. 선택지 효과
        for stat, delta in option.get("stats", {}).items():
            result.stat_changes[stat] = self._change_stat(stat, delta)
        for name in option.get("remove", []):
            self.statuses.pop(name, None)
        for name, turns in option.get("add", {}).items():
            self._add_status(name, turns, result.log)

        # 2. 기록
        self.history.append({
            "turn": self.turn + 1,
            "age": self.age,
            "season": self.season,
            "prompt": choice["prompt"],
            "chosen": option["text"],
            "result": option.get("result", ""),
        })
        self.turn += 1

        # 3. 즉시 엔딩 (매우 잘못된 선택)
        if option.get("ending"):
            self.ending = option["ending"]
            result.ending = self.ending
            return result

        # 4. 상태 효과 발동 및 지속 턴 감소
        for name in list(self.statuses):
            for stat, delta in STATUSES[name]["per_turn"].items():
                self._change_stat(stat, delta)
                verb = "증가" if delta > 0 else "감소"
                result.log.append(f"[{name}] {STAT_NAMES[stat]} {abs(delta)} {verb}")
            self.statuses[name] -= 1
            if self.statuses[name] <= 0:
                del self.statuses[name]
                result.log.append(f"[{name}] 상태가 끝났다.")

        # 5. 스테이터스 바닥 엔딩
        ending = self._check_stat_ending()
        if not ending:
            # 6. 계절/나이 진행 후 엔딩 판정
            ending = self._advance_season(result)
        if ending:
            self.ending = ending
            result.ending = ending
        else:
            self.next_choice()
        return result

    def _check_stat_ending(self):
        if self.stats["health"] <= 0:
            return "sick"
        if self.stats["happiness"] <= 0:
            return "runaway"
        if self.stats["intimacy"] <= 0:
            return "strayed"
        return None

    def _advance_season(self, result):
        self.season_index += 1
        if self.season_index >= len(SEASONS):
            self.season_index = 0
            self.age += 1
            result.log.append(f"다마고치가 {self.age}살이 되었다!")
            if self.age >= MAX_AGE:
                return self._final_ending()
        result.log.append(f"계절이 {self.season}(으)로 바뀌었다.")

        # 노령 자연사 확률 (7살부터)
        if self.age >= 7:
            chance = 0.06 * (self.age - 6)
            if self.stats["health"] >= 7:
                chance *= 0.5
            if self.rng.random() < chance:
                warm = self.stats["intimacy"] >= 7
                return "natural_warm" if warm else "natural_lonely"
        return None

    def _final_ending(self):
        s = self.stats
        if s["intimacy"] >= 8:
            return "bond"
        if s["happiness"] >= 8:
            return "joyful"
        if s["health"] >= 8:
            return "healthy"
        return "ordinary"
