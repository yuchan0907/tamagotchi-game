"""도트 강아지 이미지(images/*.png)를 만드는 도구 파일.

게임을 실행하는 데는 필요 없습니다. (이미 만들어진 PNG 파일을 게임이 불러다 씁니다)
이미지를 다시 만들거나 새 표정을 추가하고 싶을 때만 실행하세요.

    python tools/make_images.py

32x32 칸짜리 도트 그림을 그린 뒤, 5배로 키워서 160x160 PNG로 저장합니다.
외부 패키지 없이 파이썬 기본 기능만 사용합니다.
"""

import os
import struct
import zlib

SIZE = 32       # 도트 칸 수 (32 x 32)
SCALE = 5       # 저장할 때 확대 배율 (32 * 5 = 160px)

# ---------------------------------------------------------------- 색깔
OUT = "#4a2f17"        # 테두리
FUR = "#d9a66b"        # 털
EAR = "#8a5a2b"        # 귀
MUZZLE = "#f6e3c0"     # 주둥이 / 배
EYE = "#222222"
WHITE = "#ffffff"
PINK = "#ff8fb0"
TONGUE = "#f08a9a"
BLUE = "#6ec1ff"
RED = "#d9534f"
YELLOW = "#ffd84a"
CLOUD = "#9aa7b4"
FOOD = "#a0522d"

BG = "#fdf6e3"         # 미리보기 그림의 배경색


# ---------------------------------------------------------------- 그리기 도구
def new_grid():
    return [[None] * SIZE for _ in range(SIZE)]


def put(grid, x, y, color):
    """(x, y) 칸 하나에 색을 칠한다. 그림 밖이면 무시."""
    if 0 <= x < SIZE and 0 <= y < SIZE:
        grid[y][x] = color


def sym(grid, points, color):
    """점들을 칠하고, 좌우 대칭 위치에도 똑같이 칠한다."""
    for x, y in points:
        put(grid, x, y, color)
        put(grid, SIZE - 1 - x, y, color)


def rect(grid, x0, y0, x1, y1, color):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            put(grid, x, y, color)


def ellipse(grid, cx, cy, rx, ry, color):
    """중심 (cx, cy), 가로 반지름 rx, 세로 반지름 ry 인 타원을 채운다."""
    for y in range(SIZE):
        for x in range(SIZE):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1:
                grid[y][x] = color


def outline(grid, color):
    """그려진 칸과 맞닿은 빈 칸에 테두리를 칠한다."""
    marks = []
    for y in range(SIZE):
        for x in range(SIZE):
            if grid[y][x] is not None:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx = x + dx
                ny = y + dy
                if 0 <= nx < SIZE and 0 <= ny < SIZE and grid[ny][nx] is not None:
                    marks.append((x, y))
                    break
    for x, y in marks:
        grid[y][x] = color


def draw_pattern(grid, x, y, rows, color):
    """문자열 도안('1'인 칸만 칠함)을 (x, y) 위치에 그린다."""
    for row_index in range(len(rows)):
        for col_index in range(len(rows[row_index])):
            if rows[row_index][col_index] == "1":
                put(grid, x + col_index, y + row_index, color)


HEART = ["01010",
         "11111",
         "01110",
         "00100"]

SPARKLE = ["010",
           "111",
           "010"]

SWEAT = ["010",
         "010",
         "111"]


# ---------------------------------------------------------------- 몸 / 얼굴 부품
def draw_tail(grid, kind, puppy, fur):
    if kind == "none":
        return
    if puppy:
        points = [(22, 25), (23, 24), (24, 23), (24, 22)]
    elif kind == "up":
        points = [(23, 22), (24, 21), (25, 20), (26, 19), (26, 18),
                  (23, 21), (24, 20), (25, 19)]
    else:
        points = [(23, 23), (24, 24), (25, 25), (25, 26), (23, 24), (24, 25)]
    for x, y in points:
        put(grid, x, y, fur)


def draw_body(grid, spec):
    puppy = spec.get("puppy", False)
    fur = spec.get("fur", FUR)
    muzzle = spec.get("muzzle", MUZZLE)

    if puppy:
        ellipse(grid, 15.5, 25, 6, 4.5, fur)
        rect(grid, 11, 27, 13, 29, fur)
        rect(grid, 18, 27, 20, 29, fur)
        rect(grid, 11, 29, 13, 29, muzzle)
        rect(grid, 18, 29, 20, 29, muzzle)
    else:
        ellipse(grid, 15.5, 23.5, 7.5, 6, fur)
        if spec.get("big_belly"):
            ellipse(grid, 15.5, 25.5, 5.5, 4.5, muzzle)
        else:
            ellipse(grid, 15.5, 25.5, 4.5, 4, muzzle)
        rect(grid, 11, 26, 14, 29, fur)
        rect(grid, 17, 26, 20, 29, fur)
        rect(grid, 11, 29, 14, 29, muzzle)
        rect(grid, 17, 29, 20, 29, muzzle)


def draw_head(grid, spec):
    puppy = spec.get("puppy", False)
    fur = spec.get("fur", FUR)
    muzzle = spec.get("muzzle", MUZZLE)
    ear = spec.get("ear", EAR)

    head_y = 13 if puppy else 11
    ellipse(grid, 7, head_y - 1, 3, 5.5, ear)             # 왼쪽 귀
    ellipse(grid, 24, head_y - 1, 3, 5.5, ear)            # 오른쪽 귀
    ellipse(grid, 15.5, head_y, 8.5, 7.5, fur)            # 얼굴
    ellipse(grid, 15.5, head_y + 3.5, 4.5, 3.5, muzzle)   # 주둥이


def draw_bowl(grid, food):
    """왼쪽 아래의 밥그릇."""
    if food:
        inside = FOOD
        rect(grid, 3, 26, 5, 26, FOOD)                    # 사료 더미
        put(grid, 4, 26, "#c68642")
    else:
        inside = "#5b3b2b"
    rect(grid, 2, 27, 6, 27, inside)
    rect(grid, 1, 28, 7, 28, "#e8826f")
    rect(grid, 2, 29, 6, 29, "#c0504d")
    rect(grid, 3, 30, 5, 30, "#c0504d")


def draw_nose(grid, dy, color):
    rect(grid, 15, 12 + dy, 16, 13 + dy, color)


def draw_eyes(grid, kind, dy):
    if kind in ("open", "sad", "wide"):
        if kind == "wide":
            sym(grid, [(11, 8 + dy), (12, 8 + dy), (11, 9 + dy), (12, 9 + dy),
                       (11, 10 + dy), (12, 10 + dy)], EYE)
            put(grid, 11, 8 + dy, WHITE)
            put(grid, 19, 8 + dy, WHITE)
            put(grid, 12, 10 + dy, WHITE)
            put(grid, 20, 10 + dy, WHITE)
        else:
            sym(grid, [(11, 9 + dy), (12, 9 + dy), (11, 10 + dy), (12, 10 + dy)], EYE)
            put(grid, 11, 9 + dy, WHITE)
            put(grid, 19, 9 + dy, WHITE)
        if kind == "sad":
            sym(grid, [(10, 8 + dy), (11, 8 + dy), (12, 7 + dy), (13, 7 + dy)], EAR)
    elif kind == "happy":      # ^ ^ 웃는 눈
        sym(grid, [(10, 10 + dy), (11, 9 + dy), (12, 9 + dy), (13, 10 + dy)], EYE)
    elif kind == "closed":     # - - 감은 눈
        sym(grid, [(10, 10 + dy), (11, 10 + dy), (12, 10 + dy), (13, 10 + dy)], EYE)
    elif kind == "closed_sad":  # 감은 눈 + 슬픈 눈썹
        sym(grid, [(10, 10 + dy), (11, 10 + dy), (12, 10 + dy), (13, 10 + dy)], EYE)
        sym(grid, [(10, 8 + dy), (11, 8 + dy), (12, 7 + dy), (13, 7 + dy)], EAR)
    elif kind == "senior":     # 감은 눈 + 하얀 눈썹
        sym(grid, [(10, 10 + dy), (11, 10 + dy), (12, 10 + dy), (13, 10 + dy)], EYE)
        sym(grid, [(10, 8 + dy), (11, 8 + dy), (12, 8 + dy), (13, 8 + dy)], WHITE)


def draw_mouth(grid, kind, dy):
    if kind == "neutral":
        sym(grid, [(15, 15 + dy)], EYE)
    elif kind == "smile":
        sym(grid, [(14, 15 + dy), (15, 16 + dy)], EYE)
    elif kind == "open":       # 활짝 웃는 입 + 혀
        rect(grid, 14, 15 + dy, 17, 16 + dy, EYE)
        rect(grid, 15, 16 + dy, 16, 17 + dy, TONGUE)
    elif kind == "frown":
        sym(grid, [(15, 16 + dy), (14, 17 + dy)], EYE)
    elif kind == "drool":      # 입 벌리고 침 흘리는 입
        rect(grid, 14, 15 + dy, 17, 16 + dy, EYE)
        rect(grid, 17, 17 + dy, 17, 18 + dy, "#bfe9ff")


# ---------------------------------------------------------------- 한 장 그리기
def build(spec):
    """spec(설명 딕셔너리)대로 32x32 도트 그림을 만들어 돌려준다."""
    grid = new_grid()
    puppy = spec.get("puppy", False)
    dy = 2 if puppy else 0
    fur = spec.get("fur", FUR)

    # 1단계: 몸 (테두리가 둘러지는 부분)
    if spec.get("wings"):
        ellipse(grid, 6, 22, 3.5, 5, WHITE)
        ellipse(grid, 25, 22, 3.5, 5, WHITE)
    draw_tail(grid, spec.get("tail", "down"), puppy, fur)
    draw_body(grid, spec)
    if "bowl" in spec:
        draw_bowl(grid, spec["bowl"] == "food")
    draw_head(grid, spec)
    outline(grid, OUT)

    # 2단계: 얼굴과 장식 (테두리 없음)
    draw_nose(grid, dy, spec.get("nose", EYE))
    draw_eyes(grid, spec.get("eyes", "open"), dy)
    draw_mouth(grid, spec.get("mouth", "smile"), dy)

    if spec.get("cheeks"):
        sym(grid, [(9, 12 + dy), (10, 12 + dy)], PINK)

    for i in range(spec.get("tears", 0)):
        sym(grid, [(11, 11 + dy + i)], BLUE)

    if spec.get("snot"):
        put(grid, 16, 14 + dy, "#bfe9ff")
        put(grid, 16, 15 + dy, "#bfe9ff")

    if spec.get("sweat"):
        draw_pattern(grid, 23, 1, SWEAT, BLUE)

    if spec.get("bandage"):
        rect(grid, 10, 6 + dy, 21, 7 + dy, WHITE)
        for x in (12, 15, 18):
            put(grid, x, 6 + dy, "#cfcfcf")
        rect(grid, 11, 26, 14, 27, WHITE)          # 앞다리 붕대
        put(grid, 12, 26, "#cfcfcf")
        put(grid, 13, 27, "#cfcfcf")

    if spec.get("cloud"):
        ellipse(grid, 11.5, 1.8, 4.5, 1.9, CLOUD)
        ellipse(grid, 19.5, 1.8, 4.5, 1.9, CLOUD)
        ellipse(grid, 15.5, 1.3, 5, 1.5, CLOUD)
        for x, y in [(10, 4), (21, 4), (6, 3), (25, 3)]:
            put(grid, x, y, BLUE)

    if spec.get("halo"):
        ellipse(grid, 15.5, 1, 6, 1.5, YELLOW)

    if spec.get("hearts"):
        draw_pattern(grid, 1, 1, HEART, PINK)
        draw_pattern(grid, 26, 1, HEART, PINK)

    if spec.get("sparkles"):
        for x, y in [(2, 2), (28, 2), (29, 13), (1, 13)]:
            draw_pattern(grid, x - 1, y - 1, SPARKLE, YELLOW)

    return grid


# ---------------------------------------------------------------- 이미지 목록
# 새 표정을 추가하려면 여기에 한 줄 추가하면 됩니다.
SPECS = {
    # --- 나이에 따른 기본 모습 ---
    "puppy": {"puppy": True, "eyes": "open", "mouth": "smile", "tail": "up"},
    "normal": {"eyes": "open", "mouth": "smile", "tail": "down"},
    "senior": {"fur": "#b9a88f", "muzzle": "#f2f2f2", "ear": "#7d6b55",
               "eyes": "senior", "mouth": "smile", "tail": "down"},

    # --- 스테이터스 / 상태에 따른 모습 ---
    "happy": {"eyes": "happy", "mouth": "open", "tail": "up", "cheeks": True},
    "sad": {"eyes": "sad", "mouth": "frown", "tail": "down", "tears": 2},
    "sick": {"fur": "#c9cfa3", "muzzle": "#eef0d8", "eyes": "sad", "mouth": "frown",
             "nose": RED, "snot": True, "sweat": True, "tail": "down"},
    "hungry": {"eyes": "sad", "mouth": "drool", "tail": "down", "bowl": "empty"},
    "full": {"eyes": "happy", "mouth": "smile", "tail": "up", "cheeks": True,
             "big_belly": True, "bowl": "food"},
    "excited": {"eyes": "wide", "mouth": "open", "tail": "up", "cheeks": True,
                "sparkles": True},
    "injured": {"eyes": "sad", "mouth": "frown", "tail": "down", "bandage": True,
                "tears": 1},
    "depressed": {"fur": "#a8aab8", "muzzle": "#e3e5ee", "ear": "#6f7185",
                  "eyes": "closed_sad", "mouth": "frown", "tail": "down", "cloud": True},

    # --- 엔딩 ---
    "ending_good": {"eyes": "happy", "mouth": "open", "tail": "up", "cheeks": True,
                    "hearts": True},
    "ending_angel": {"fur": "#f3ead8", "muzzle": "#ffffff", "ear": "#c9b99a",
                     "eyes": "happy", "mouth": "smile", "tail": "down",
                     "wings": True, "halo": True},
    "ending_lonely": {"fur": "#b9a58a", "ear": "#7d6b55", "eyes": "sad",
                      "mouth": "frown", "tail": "down", "tears": 2, "bowl": "empty"},
}


# ---------------------------------------------------------------- PNG 저장
def hex_to_rgba(color):
    if color is None:
        return (0, 0, 0, 0)
    return (int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16), 255)


def chunk(kind, data):
    body = kind + data
    return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body))


def write_png(path, grid, scale, background=None):
    """도트 그림을 scale배로 키워서 PNG 파일로 저장한다. (background가 있으면 배경을 채움)"""
    width = len(grid[0]) * scale
    height = len(grid) * scale
    raw = bytearray()
    for row in grid:
        line = bytearray([0])                       # PNG 한 줄의 시작 표시
        for color in row:
            if color is None and background is not None:
                color = background
            line += bytes(hex_to_rgba(color)) * scale
        for _ in range(scale):
            raw += line
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


def make_preview(path, grids, columns=7):
    """모든 이미지를 한 장에 모은 미리보기(README용)를 만든다."""
    cell = SIZE + 2
    rows = (len(grids) + columns - 1) // columns
    sheet = [[BG] * (cell * columns) for _ in range(cell * rows)]
    for i in range(len(grids)):
        ox = (i % columns) * cell + 1
        oy = (i // columns) * cell + 1
        for y in range(SIZE):
            for x in range(SIZE):
                if grids[i][y][x] is not None:
                    sheet[oy + y][ox + x] = grids[i][y][x]
    write_png(path, sheet, 4)


def main():
    folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images")
    os.makedirs(folder, exist_ok=True)

    grids = []
    for name in SPECS:
        grid = build(SPECS[name])
        grids.append(grid)
        write_png(os.path.join(folder, name + ".png"), grid, SCALE)
        print("만듦:", name + ".png")

    make_preview(os.path.join(folder, "preview.png"), grids)
    print("만듦: preview.png (이미지 모음 미리보기)")


if __name__ == "__main__":
    main()
