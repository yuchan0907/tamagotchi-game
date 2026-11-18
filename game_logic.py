"""게임 규칙 파일 (화면과 무관한 부분임).

이 파일에는 "게임이 진행되는 방식"이 들어 있음.
- 새 게임 시작
- 선택지 뽑기
- 선택했을 때 스테이터스/상태 변화
- 계절/나이 흐름
- 엔딩 판정

게임의 현재 상태는 game 딕셔너리 하나에 모아서 관리함.
"""

import random

from data import (
    CHOICES, ENDING_IMAGES, ENDINGS, INITIAL_STATS, MAX_AGE, SEASONS, STAT_MAX,
    STAT_NAMES, STATUSES,
)

# 게임의 현재 상태를 담는 딕셔너리 (new_game() 호출 시 채워짐)
game = {}


# ----------------------------------------------------------------------
# 1. 새 게임
# ----------------------------------------------------------------------
def new_game():
    game.clear()
    game["stats"] = dict(INITIAL_STATS)   # 건강, 행복, 친밀도 (복사본)
    game["statuses"] = {}                 # 상태창: {"감기": 남은 턴 수, ...}
    game["age"] = 0                       # 나이
    game["season"] = 0                    # 0=봄, 1=여름, 2=가을, 3=겨울
    game["turn"] = 0                      # 지금까지 진행한 턴 수
    game["history"] = []                  # 엔딩 후 돌아보기용 기록
    game["shown_fixed"] = []              # 이미 나온 "나이 고정" 선택지 id
    game["last_id"] = ""                  # 바로 직전에 나온 선택지 id
    game["ending"] = ""                   # 엔딩 키 ("" 이면 아직 게임 중임)
    game["choice"] = None                 # 지금 화면에 나온 선택지
    pick_next_choice()


# ----------------------------------------------------------------------
# 2. 작은 도우미 함수들
# ----------------------------------------------------------------------
def limit(value):
    """스테이터스를 0 ~ 10 사이로 유지함."""
    if value < 0:
        return 0
    if value > STAT_MAX:
        return STAT_MAX
    return value


def change_stat(stat, delta):
    """스테이터스를 delta만큼 변경함. (0~10 범위 유지)"""
    game["stats"][stat] = limit(game["stats"][stat] + delta)


def season_name():
    return SEASONS[game["season"]]


def status_description(name):
    """상태 이름에 마우스를 올렸을 때 보여줄 설명 글을 만듦."""
    info = STATUSES[name]
    lines = []

    for stat, delta in info["per_turn"].items():
        if delta > 0:
            lines.append(f"매 턴마다 {STAT_NAMES[stat]}이(가) {delta} 증가합니다")
        else:
            lines.append(f"매 턴마다 {STAT_NAMES[stat]}이(가) {-delta} 감소합니다")

    if name == "예방접종":
        lines.append("'감기' 상태에 걸리지 않습니다")

    lines.append("")
    lines.append(info["flavor"])
    lines.append("")
    lines.append(f"남은 턴 수 : {game['statuses'][name]}")
    return "\n".join(lines)


def pet_image_name():
    """지금 상황에 맞는 강아지 이미지 이름을 반환함. (images 폴더의 파일 이름)

    위에 있는 조건일수록 우선순위가 높음.
    새 상태를 추가했다면 여기에 한 줄을 추가하여 이미지를 연결함.
    """
    # 엔딩이 났다면 엔딩 이미지 사용
    if game["ending"] != "":
        return ENDING_IMAGES[game["ending"]]

    statuses = game["statuses"]
    stats = game["stats"]

    # 상태창의 상태가 우선임
    if "부상" in statuses:
        return "injured"
    if "감기" in statuses:
        return "sick"
    if "우울" in statuses:
        return "depressed"
    if "배고픔" in statuses:
        return "hungry"
    if "신남" in statuses:
        return "excited"
    if "배부름" in statuses:
        return "full"

    # 다음은 스테이터스 기준
    if stats["health"] <= 3:
        return "sick"
    if stats["happiness"] <= 3:
        return "sad"
    if stats["happiness"] >= 7:
        return "happy"

    # 아무 상태도 없으면 나이에 맞는 기본 모습 사용
    if game["age"] <= 1:
        return "puppy"
    if game["age"] >= 7:
        return "senior"
    return "normal"


# ----------------------------------------------------------------------
# 3. 선택지 뽑기
# ----------------------------------------------------------------------
def can_appear(choice):
    """이 선택지가 지금 나올 수 있는지 검사함. (True / False)"""
    # 나이 고정 선택지는 일반 추첨에서 제외
    if "fixed_age" in choice:
        return False

    # 방금 나온 선택지는 연속으로 나오지 않게 제외
    if choice["id"] == game["last_id"]:
        return False

    # 나이 조건
    if "min_age" in choice and game["age"] < choice["min_age"]:
        return False

    # 계절 조건
    if "seasons" in choice and season_name() not in choice["seasons"]:
        return False

    # 꼭 있어야 하는 상태 (.get(키, 기본값): 키가 없으면 기본값 사용함)
    for name in choice.get("requires", []):
        if name not in game["statuses"]:
            return False

    # 있으면 안 되는 상태
    for name in choice.get("forbids", []):
        if name in game["statuses"]:
            return False

    return True


def pick_next_choice():
    """다음에 보여줄 선택지를 정하여 game["choice"]에 저장함."""
    # 1) 이번 나이에 고정으로 나와야 하는 선택지가 있으면 먼저 보여줌
    for choice in CHOICES:
        if choice.get("fixed_age") == game["age"]:
            if choice["id"] not in game["shown_fixed"]:
                game["shown_fixed"].append(choice["id"])
                game["choice"] = choice
                game["last_id"] = choice["id"]
                return

    # 2) 나올 수 있는 선택지를 모은 뒤 그중 하나를 무작위로 뽑음
    candidates = []
    for choice in CHOICES:
        if can_appear(choice):
            candidates.append(choice)

    chosen = random.choice(candidates)
    game["choice"] = chosen
    game["last_id"] = chosen["id"]


# ----------------------------------------------------------------------
# 4. 선택지를 골랐을 때 (한 턴 진행)
# ----------------------------------------------------------------------
def add_status(name, turns, log):
    """상태창에 상태를 추가함. (이미 있으면 남은 턴을 덮어씀)"""
    # 예방접종 상태에서는 감기에 걸리지 않음
    if name == "감기" and "예방접종" in game["statuses"]:
        log.append("예방접종 덕분에 '감기'를 막았다!")
        return
    game["statuses"][name] = turns


def apply_status_effects(log):
    """상태창에 있는 모든 상태의 효과를 발동한 뒤 남은 턴을 1 감소시킴."""
    # list(...)로 복사하여 반복하는 이유: 반복 중 딕셔너리에서 삭제하면 오류가 나기 때문임
    for name in list(game["statuses"]):
        for stat, delta in STATUSES[name]["per_turn"].items():
            change_stat(stat, delta)
            if delta > 0:
                log.append(f"[{name}] {STAT_NAMES[stat]} {delta} 증가")
            else:
                log.append(f"[{name}] {STAT_NAMES[stat]} {-delta} 감소")

        game["statuses"][name] -= 1
        if game["statuses"][name] <= 0:
            del game["statuses"][name]
            log.append(f"[{name}] 상태가 끝났다.")


def check_stat_ending():
    """스테이터스가 0이 되어 발생하는 엔딩이 있는지 검사함."""
    if game["stats"]["health"] <= 0:
        return "sick"
    if game["stats"]["happiness"] <= 0:
        return "runaway"
    if game["stats"]["intimacy"] <= 0:
        return "strayed"
    return ""


def final_ending():
    """MAX_AGE살까지 키웠을 때의 엔딩을 스테이터스 기준으로 결정함."""
    stats = game["stats"]
    if stats["intimacy"] >= 8:
        return "bond"
    if stats["happiness"] >= 8:
        return "joyful"
    if stats["health"] >= 8:
        return "healthy"
    return "ordinary"


def advance_season(log):
    """계절을 한 칸 진행하고 나이/엔딩을 처리함. 엔딩이 나면 엔딩 키를 반환함."""
    game["season"] += 1

    # 겨울(3) 다음은 봄(0)이며, 이때 한 살 증가함
    if game["season"] >= len(SEASONS):
        game["season"] = 0
        game["age"] += 1
        log.append(f"다마고치가 {game['age']}살이 되었다!")
        if game["age"] >= MAX_AGE:
            return final_ending()

    log.append(f"계절이 {season_name()}(으)로 바뀌었다.")

    # 7살부터 계절이 바뀔 때마다 자연사 확률이 적용됨
    if game["age"] >= 7:
        chance = 0.06 * (game["age"] - 6)      # 나이가 많을수록 확률 증가
        if game["stats"]["health"] >= 7:
            chance = chance / 2                # 건강하면 확률 절반
        if random.random() < chance:
            if game["stats"]["intimacy"] >= 7:
                return "natural_warm"
            return "natural_lonely"

    return ""


def choose(index):
    """플레이어가 index번째(0부터) 선택지를 골랐을 때 한 턴을 진행함.

    반환값: {"text": 결과 문장, "log": [알림 문장들]}
    엔딩이 나면 game["ending"]에 엔딩 키가 저장됨.
    """
    option = game["choice"]["options"][index]
    log = []

    # 1. 스테이터스 변화
    for stat, delta in option.get("stats", {}).items():
        change_stat(stat, delta)

    # 2. 상태 제거 / 추가
    for name in option.get("remove", []):
        game["statuses"].pop(name, None)      # 있으면 삭제하고, 없으면 그대로 넘어감
    for name, turns in option.get("add", {}).items():
        add_status(name, turns, log)

    # 3. 기록 남기기 (엔딩 후 돌아보기)
    game["turn"] += 1
    game["history"].append({
        "turn": game["turn"],
        "age": game["age"],
        "season": season_name(),
        "prompt": game["choice"]["prompt"],
        "chosen": option["text"],
        "result": option.get("result", ""),
    })

    result = {"text": option.get("result", ""), "log": log}

    # 4. 매우 잘못된 선택 -> 바로 엔딩
    if "ending" in option:
        game["ending"] = option["ending"]
        return result

    # 5. 상태 효과 발동
    apply_status_effects(log)

    # 6. 엔딩 검사: 스테이터스 -> 계절/나이
    ending = check_stat_ending()
    if ending == "":
        ending = advance_season(log)

    if ending != "":
        game["ending"] = ending
    else:
        pick_next_choice()

    return result
