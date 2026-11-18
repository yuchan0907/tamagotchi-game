"""게임 데이터 파일.

상태, 선택지, 엔딩 같은 "내용"은 모두 이 파일에 정의되어 있음.
게임 내용 변경 시 이 파일만 수정하면 됨. (코드를 몰라도 수정 가능)
"""

STAT_NAMES = {
    "health": "건강",
    "happiness": "행복",
    "intimacy": "친밀도",
}
STAT_MAX = 10

SEASONS = ["봄", "여름", "가을", "겨울"]
MAX_AGE = 10  # 이 나이에 도달 시 게임 종료(엔딩)됨

INITIAL_STATS = {"health": 7, "happiness": 5, "intimacy": 3}

# ---------------------------------------------------------------------------
# 강아지 이미지 (images 폴더의 PNG 파일 이름이며 .png 는 제외함)
# ---------------------------------------------------------------------------
IMAGE_NAMES = [
    "puppy", "normal", "senior",                              # 나이별 기본 모습
    "happy", "sad", "sick", "hungry", "full", "excited",      # 상황별 모습
    "injured", "depressed",
    "ending_good", "ending_angel", "ending_lonely",           # 엔딩 모습
]

# 엔딩 키 -> 엔딩 시 표시할 이미지
ENDING_IMAGES = {
    "sick": "ending_angel",
    "runaway": "ending_lonely",
    "strayed": "ending_lonely",
    "heatstroke": "ending_angel",
    "poison": "ending_angel",
    "natural_warm": "ending_angel",
    "natural_lonely": "ending_angel",
    "bond": "ending_good",
    "joyful": "ending_good",
    "healthy": "ending_good",
    "ordinary": "ending_good",
}

# ---------------------------------------------------------------------------
# 상태창에 표시되는 세부 상태 정의
#   per_turn   : 매 턴마다 적용되는 스테이터스 변화 (+1은 증가, -1은 감소)
#   flavor     : 마우스 오버 시 표시되는 설명 문장
# (지속 턴 수는 선택지의 "add"에서 지정함. 예: "add": {"감기": 3})
# (예방접종은 특별 규칙이 적용되어 보유 중 감기에 걸리지 않음. game_logic.py에 구현됨)
# ---------------------------------------------------------------------------
STATUSES = {
    "배부름": {
        "per_turn": {"happiness": 1},
        "flavor": "배가 빵빵하다. 꼬리를 살랑살랑 흔든다.",
    },
    "배고픔": {
        "per_turn": {"happiness": -1},
        "flavor": "빈 밥그릇만 바라보고 있다.",
    },
    "감기": {
        "per_turn": {"health": -1},
        "flavor": "콜록콜록. 코가 촉촉하다 못해 흥건하다.",
    },
    "건강함": {
        "per_turn": {"health": 1},
        "flavor": "털에 윤기가 흐르고 눈이 반짝인다.",
    },
    "우울": {
        "per_turn": {"happiness": -1},
        "flavor": "구석에서 귀를 축 늘어뜨리고 있다.",
    },
    "신남": {
        "per_turn": {"happiness": 1},
        "flavor": "온 집 안을 빙글빙글 뛰어다닌다!",
    },
    "부상": {
        "per_turn": {"health": -1},
        "flavor": "한쪽 다리를 절뚝거린다.",
    },
    "예방접종": {
        "per_turn": {},
        "flavor": "주사는 무서웠지만, 이제 감기쯤은 문제없다.",
    },
}

# ---------------------------------------------------------------------------
# 엔딩
# ---------------------------------------------------------------------------
ENDINGS = {
    # --- 스테이터스 바닥 엔딩 ---
    "sick": {
        "title": "병마에 쓰러진 다마고치",
        "text": "건강을 돌보지 못한 다마고치는 끝내 일어나지 못했다. "
                "마지막까지 당신을 바라보던 눈빛이 오래도록 잊히지 않는다.",
        "good": False,
    },
    "runaway": {
        "title": "가출한 다마고치",
        "text": "어느 날 아침, 현관문 앞에는 빈 밥그릇만 남아 있었다. "
                "다마고치는 더 행복할 수 있는 곳을 찾아 떠났다.",
        "good": False,
    },
    "strayed": {
        "title": "남이 되어버린 우리",
        "text": "다마고치는 더 이상 당신을 보고 꼬리를 흔들지 않는다. "
                "같은 집에 살지만, 서로에게 낯선 존재가 되어버렸다.",
        "good": False,
    },
    # --- 매우 잘못된 선택 엔딩 ---
    "heatstroke": {
        "title": "한여름의 비극",
        "text": "'잠깐이면 되겠지'라는 생각이 돌이킬 수 없는 결과를 불렀다. "
                "뜨거운 차 안에서 다마고치는 다시 깨어나지 못했다.",
        "good": False,
    },
    "poison": {
        "title": "주워 먹은 것",
        "text": "길에서 주워 먹은 정체불명의 음식은 다마고치에게 치명적이었다. "
                "그날 밤, 다마고치는 조용히 눈을 감았다.",
        "good": False,
    },
    # --- 자연사 ---
    "natural_warm": {
        "title": "따뜻한 마지막 인사",
        "text": "노령에 접어든 다마고치는 당신의 품에서 평온하게 잠들었다. "
                "충분히 사랑받았다는 듯, 입가에는 미소가 걸려 있었다.",
        "good": True,
    },
    "natural_lonely": {
        "title": "쓸쓸한 노년",
        "text": "나이가 든 다마고치는 어느 날 조용히 숨을 거두었다. "
                "더 많이 안아줄 걸 그랬다는 후회가 밀려온다.",
        "good": False,
    },
    # --- 장수 엔딩 (MAX_AGE 도달) ---
    "bond": {
        "title": "영원한 단짝",
        "text": "열 번의 해를 함께 보낸 다마고치는 이제 당신의 가장 소중한 가족이다. "
                "눈빛만 봐도 서로의 마음을 알 수 있다.",
        "good": True,
    },
    "joyful": {
        "title": "행복한 개생",
        "text": "다마고치는 늘 신나게 뛰어놀며 열 살을 맞이했다. "
                "이 강아지의 인생은 웃음으로 가득했다.",
        "good": True,
    },
    "healthy": {
        "title": "철인 강아지",
        "text": "열 살이 되어서도 다마고치는 병원 한번 가지 않을 만큼 튼튼하다. "
                "동네 산책로의 전설이 되었다.",
        "good": True,
    },
    "ordinary": {
        "title": "평범하지만 소중한 날들",
        "text": "특별할 것은 없었지만, 다마고치와 함께한 열 해는 "
                "그 자체로 충분히 따뜻했다.",
        "good": True,
    },
}

# ---------------------------------------------------------------------------
# 선택지
#   id        : 선택지 이름표 (중복 불가)
#   prompt    : 화면에 표시되는 상황 설명
#   fixed_age : (선택) 이 나이가 되면 반드시 등장함 (1회)
#   min_age   : (선택) 이 나이 이상일 때만 등장함
#   seasons   : (선택) 이 계절에만 등장함  예: ["겨울"]
#   requires  : (선택) 이 상태를 보유한 경우에만 등장함  예: ["감기"]
#   forbids   : (선택) 이 상태를 보유하면 등장하지 않음
#   options   : 답변 목록 (버튼이 3개이므로 1~3개만 가능함)
#       stats  : 스테이터스 변화량
#       add    : {상태: 지속 턴}  (이미 있으면 지속 턴이 갱신됨)
#       remove : [상태, ...]
#       ending : 선택 즉시 엔딩이 발생함 (엔딩 키 지정)
# ---------------------------------------------------------------------------
CHOICES = [
    # ===== 특정 나이에 고정으로 등장 =====
    {
        "id": "age0_meet",
        "fixed_age": 0,
        "prompt": "작은 강아지가 눈을 떴다. 처음 만난 당신을 빤히 쳐다본다. 어떻게 할까?",
        "options": [
            {"text": "이름을 불러준다", "stats": {"intimacy": 2},
             "result": "다마고치가 고개를 갸웃하더니 꼬리를 흔들었다."},
            {"text": "조심스레 쓰다듬는다", "stats": {"intimacy": 1, "happiness": 1},
             "result": "따뜻한 손길에 다마고치가 눈을 사르르 감았다."},
            {"text": "따뜻한 우유를 먹인다", "stats": {"health": 1}, "add": {"배부름": 2},
             "result": "다마고치가 쪽쪽 소리를 내며 우유를 먹는다."},
        ],
    },
    {
        "id": "age1_bark",
        "fixed_age": 1,
        "prompt": "훌쩍 자란 다마고치가 짖는 연습을 하고 있다. '왕!' 하고 짖더니 스스로 놀란다.",
        "options": [
            {"text": "함께 짖어준다", "stats": {"happiness": 2, "intimacy": 1},
             "result": "둘이 한참을 짖으며 놀았다. 이웃집이 조금 시끄러웠을지도."},
            {"text": "조용히 시킨다", "stats": {"happiness": -1},
             "result": "다마고치가 시무룩해져서 입을 다물었다."},
            {"text": "잘했다며 간식을 준다", "stats": {"happiness": 1}, "add": {"배부름": 2},
             "result": "칭찬과 간식에 다마고치의 자신감이 올라갔다."},
        ],
    },
    {
        "id": "age3_teen",
        "fixed_age": 3,
        "prompt": "다마고치가 사춘기인지 말을 듣지 않는다. 아끼던 신발이 처참하게 물어뜯겨 있다.",
        "options": [
            {"text": "크게 혼낸다", "stats": {"happiness": -2, "intimacy": -1}, "add": {"우울": 2},
             "result": "다마고치가 귀를 접고 침대 밑으로 숨어버렸다."},
            {"text": "차분히 가르친다", "stats": {"intimacy": 1},
             "result": "다마고치가 고개를 숙이며 반성하는 듯 보였다."},
            {"text": "대신 씹을 장난감을 사준다", "stats": {"happiness": 1}, "add": {"신남": 2},
             "result": "새 장난감에 정신이 팔려 신발은 이미 잊은 듯하다."},
        ],
    },
    {
        "id": "age6_stairs",
        "fixed_age": 6,
        "prompt": "나이가 든 다마고치가 계단을 오르기 힘들어한다. 어떻게 할까?",
        "options": [
            {"text": "건강검진을 받으러 간다", "stats": {"health": 2}, "add": {"건강함": 3},
             "result": "검진 결과, 관리만 잘하면 아직 괜찮다고 한다."},
            {"text": "안아서 옮겨준다", "stats": {"intimacy": 2, "happiness": 1},
             "result": "다마고치가 당신의 품에 얼굴을 묻었다."},
            {"text": "운동이 필요하다며 계단 연습을 시킨다", "stats": {"health": -1}, "add": {"부상": 3},
             "result": "무리했는지 다마고치가 다리를 절뚝거린다."},
        ],
    },
    # ===== 상태 보유 시 등장 =====
    {
        "id": "cold_care",
        "requires": ["감기"],
        "prompt": "다마고치의 상태가 어딘가 나빠 보인다. 콜록거리며 힘없이 누워 있다. 어떻게 할까?",
        "options": [
            {"text": "지극정성으로 돌본다", "stats": {"intimacy": 1, "health": 1}, "add": {"감기": 1},
             "result": "밤새 곁을 지킨 덕에 증상이 많이 가라앉았다."},
            {"text": "병원에 데려간다", "stats": {"happiness": -1}, "remove": ["감기"], "add": {"건강함": 2},
             "result": "주사는 무서웠지만, 감기는 말끔히 나았다."},
            {"text": "자고 나면 낫겠지 하고 둔다", "stats": {"health": -1, "intimacy": -1}, "add": {"감기": 4},
             "result": "다마고치의 기침이 더 심해졌다."},
        ],
    },
    {
        "id": "hungry_care",
        "requires": ["배고픔"],
        "prompt": "다마고치가 배가 고파서 힘이 없어 보인다. 어떻게 할까?",
        "options": [
            {"text": "사료를 가득 준다", "stats": {"intimacy": 1}, "remove": ["배고픔"], "add": {"배부름": 2},
             "result": "허겁지겁 밥그릇을 비우는 모습이 안쓰러우면서도 귀엽다."},
            {"text": "조금만 더 참으라고 한다", "stats": {"health": -1, "happiness": -1},
             "result": "다마고치의 배에서 우렁찬 소리가 났다."},
        ],
    },
    {
        "id": "depressed_care",
        "requires": ["우울"],
        "prompt": "다마고치가 구석에서 꼼짝도 하지 않는다. 눈이 마주쳐도 꼬리를 흔들지 않는다.",
        "options": [
            {"text": "말없이 안아준다", "stats": {"intimacy": 2}, "remove": ["우울"],
             "result": "다마고치가 한참을 품에 안겨 있다가 천천히 꼬리를 흔들었다."},
            {"text": "간식으로 달랜다", "stats": {"happiness": 1, "health": -1}, "remove": ["우울"],
             "result": "기운은 났지만 간식을 너무 많이 먹은 것 같다."},
            {"text": "혼자 있고 싶은 걸 거라며 내버려둔다", "stats": {"happiness": -1, "intimacy": -1},
             "result": "다마고치는 밤새 창밖만 바라보았다."},
        ],
    },
    {
        "id": "injury_care",
        "requires": ["부상"],
        "prompt": "다마고치가 다리를 절뚝거린다. 어떻게 할까?",
        "options": [
            {"text": "동물병원에 데려간다", "stats": {"intimacy": 1, "happiness": -1}, "remove": ["부상"],
             "result": "간단한 치료를 받고 붕대를 감았다. 곧 나을 것이다."},
            {"text": "푹 쉬게 해준다", "stats": {"intimacy": 1}, "add": {"부상": 1},
             "result": "이틀간 얌전히 쉬었더니 많이 나아졌다."},
            {"text": "괜찮겠지 하고 평소처럼 산책한다", "stats": {"health": -1}, "add": {"부상": 4},
             "result": "다리가 더 아파졌는지 다마고치가 낑낑거린다."},
        ],
    },
    {
        "id": "senior_care",
        "min_age": 7,
        "prompt": "다마고치가 하루 종일 누워 있다. 예전 같은 활기는 없다.",
        "options": [
            {"text": "곁을 지켜준다", "stats": {"intimacy": 2, "happiness": 1},
             "result": "다마고치가 당신의 손에 턱을 올려놓았다."},
            {"text": "특식을 만들어 준다", "stats": {"health": 1, "happiness": 1}, "add": {"배부름": 2},
             "result": "오랜만에 그릇을 싹싹 비웠다."},
            {"text": "나이 탓이려니 하고 넘어간다", "stats": {"happiness": -1},
             "result": "다마고치는 한숨 같은 숨을 내쉬었다."},
        ],
    },
    # ===== 계절 선택지 =====
    {
        "id": "winter_cold",
        "seasons": ["겨울"],
        "prompt": "차가운 바람이 분다. 다마고치가 몸을 잔뜩 웅크리고 있다.",
        "options": [
            {"text": "따뜻한 옷을 입혀준다", "stats": {"intimacy": 1}, "add": {"건강함": 2},
             "result": "작은 패딩을 입은 다마고치가 뿌듯한 표정이다."},
            {"text": "눈밭에서 신나게 뛰어놀게 한다", "stats": {"happiness": 2}, "add": {"감기": 3},
             "result": "신나게 놀았지만, 코를 훌쩍이기 시작했다."},
            {"text": "그냥 둔다", "stats": {"health": -1}, "add": {"감기": 3},
             "result": "다마고치가 재채기를 했다. 감기에 걸린 것 같다."},
        ],
    },
    {
        "id": "summer_heat",
        "seasons": ["여름"],
        "prompt": "무더운 날이다. 다마고치가 혀를 길게 내밀고 헥헥거린다.",
        "options": [
            {"text": "시원한 물과 그늘을 마련해 준다", "stats": {"health": 1}, "add": {"건강함": 2},
             "result": "다마고치가 시원한 물을 벌컥벌컥 마셨다."},
            {"text": "물놀이를 시켜준다", "stats": {"happiness": 2, "intimacy": 1}, "add": {"신남": 2},
             "result": "첨벙첨벙! 물을 튀기며 한껏 신이 났다."},
            {"text": "차 안에 잠깐 두고 마트에 다녀온다", "ending": "heatstroke",
             "result": "'금방이면 되겠지.' 하지만 그 '금방'이 너무 길었다."},
        ],
    },
    {
        "id": "summer_thunder",
        "seasons": ["여름"],
        "prompt": "한밤중 천둥이 쳤다. 다마고치가 이불 속으로 파고들어 덜덜 떨고 있다.",
        "options": [
            {"text": "꼭 안고 달래준다", "stats": {"intimacy": 2},
             "result": "다마고치의 떨림이 서서히 잦아들었다."},
            {"text": "괜찮다며 방에 혼자 둔다", "stats": {"happiness": -2}, "add": {"우울": 2},
             "result": "다마고치는 밤새 잠들지 못했다."},
        ],
    },
    {
        "id": "autumn_leaves",
        "seasons": ["가을"],
        "prompt": "낙엽이 수북이 쌓인 공원. 다마고치가 낙엽 더미 앞에서 눈을 반짝인다.",
        "options": [
            {"text": "같이 낙엽 위를 뒹군다", "stats": {"happiness": 1, "intimacy": 1}, "add": {"신남": 2},
             "result": "낙엽투성이가 된 서로를 보며 한참을 웃었다."},
            {"text": "사진을 찍어준다", "stats": {"intimacy": 1},
             "result": "인생 사진이 나왔다. 앨범에 소중히 간직했다."},
        ],
    },
    {
        "id": "spring_flowers",
        "seasons": ["봄"],
        "prompt": "꽃이 활짝 핀 봄날, 다마고치가 꽃밭을 향해 달려간다.",
        "options": [
            {"text": "함께 꽃놀이를 즐긴다", "stats": {"happiness": 1, "intimacy": 1},
             "result": "꽃잎이 코에 붙은 채로 다마고치가 재채기를 했다."},
            {"text": "꽃을 먹지 못하게 말린다", "stats": {"health": 1, "happiness": -1},
             "result": "아쉬워하면서도 건강은 지켰다."},
        ],
    },
    {
        "id": "vaccine",
        "seasons": ["봄", "가을"],
        "forbids": ["예방접종"],
        "prompt": "동물병원에서 예방접종 안내 문자가 왔다. 어떻게 할까?",
        "options": [
            {"text": "예방접종을 맞히러 간다", "stats": {"happiness": -1}, "add": {"예방접종": 8},
             "result": "다마고치가 병원 문 앞에서 버텼지만, 무사히 주사를 맞았다."},
            {"text": "건강하니 괜찮을 거라며 넘긴다",
             "result": "문자를 읽음 처리하고 넘겼다."},
        ],
    },
    # ===== 일상 선택지 =====
    {
        "id": "hungry",
        "forbids": ["배부름", "배고픔"],
        "prompt": "다마고치가 빈 밥그릇 앞에서 낑낑거린다.",
        "options": [
            {"text": "사료를 준다", "stats": {"happiness": 1}, "add": {"배부름": 2},
             "result": "다마고치가 신나게 사료를 먹었다."},
            {"text": "간식을 잔뜩 준다", "stats": {"happiness": 2, "health": -1}, "add": {"배부름": 2},
             "result": "너무 신나서 먹다가 살짝 체한 것 같다."},
            {"text": "모른 척한다", "stats": {"happiness": -1, "intimacy": -1}, "add": {"배고픔": 3},
             "result": "다마고치가 서운한 눈으로 당신을 바라본다."},
        ],
    },
    {
        "id": "walk",
        "prompt": "다마고치가 리드줄을 입에 물고 현관 앞에 앉아 있다.",
        "options": [
            {"text": "산책을 나간다", "stats": {"health": 1, "happiness": 1, "intimacy": 1}, "add": {"신남": 2},
             "result": "동네를 한 바퀴 돌고 오니 둘 다 기분이 상쾌하다."},
            {"text": "귀찮다며 다음에 가자고 한다", "stats": {"happiness": -1}, "add": {"우울": 2},
             "result": "다마고치가 리드줄을 내려놓고 터덜터덜 돌아갔다."},
        ],
    },
    {
        "id": "ball",
        "prompt": "다마고치가 공을 물고 와서 당신의 발 앞에 내려놓는다.",
        "options": [
            {"text": "신나게 놀아준다", "stats": {"happiness": 2, "intimacy": 1}, "add": {"신남": 2},
             "result": "공을 열 번도 넘게 던졌다. 팔이 아프지만 행복하다."},
            {"text": "바쁘다며 쫓아낸다", "stats": {"happiness": -2, "intimacy": -1},
             "result": "다마고치가 공을 문 채로 멀어져 갔다."},
        ],
    },
    {
        "id": "neighbor_dog",
        "prompt": "이웃집 강아지가 놀러 왔다. 다마고치와 서로 냄새를 맡고 있다.",
        "options": [
            {"text": "같이 놀게 해준다", "stats": {"happiness": 2}, "add": {"신남": 2},
             "result": "둘이 거실을 가로지르며 한바탕 질주했다."},
            {"text": "낯선 강아지라 조심스러워 떨어뜨려 놓는다", "stats": {"intimacy": 1, "happiness": -1},
             "result": "다마고치가 아쉬운 듯 현관 쪽을 바라본다."},
        ],
    },
    {
        "id": "stranger_food",
        "prompt": "산책길, 바닥에 떨어진 정체불명의 음식을 발견한 다마고치가 눈을 반짝인다.",
        "options": [
            {"text": "줄을 당겨 막는다", "stats": {"happiness": -1},
             "result": "다마고치가 불만스러운 표정으로 따라왔다."},
            {"text": "대신 주머니 속 간식으로 시선을 돌린다", "stats": {"intimacy": 1},
             "result": "다마고치는 금세 바닥의 음식을 잊었다."},
            {"text": "그냥 먹게 둔다", "ending": "poison",
             "result": "말릴 틈도 없이 다마고치가 덥석 삼켜버렸다."},
        ],
    },
]
