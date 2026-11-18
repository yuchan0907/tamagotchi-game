"""다마고치 키우기 - 화면(tkinter) 파일.

실행 방법:  python main.py

이 파일은 "화면 표시"만 담당함.
게임 규칙은 game_logic.py, 게임 내용(선택지 등)은 data.py 에 있음.
"""

import os
import tkinter as tk
from tkinter import scrolledtext

import game_logic
from game_logic import game
from data import ENDINGS, IMAGE_NAMES, MAX_AGE, STAT_MAX, STAT_NAMES

# images 폴더 위치 (어느 폴더에서 실행해도 찾을 수 있도록 이 파일 기준으로 계산함)
IMAGE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")

# 불러온 이미지를 저장하는 딕셔너리 {"happy": 그림, ...}
# (딕셔너리에 계속 보관해야 tkinter가 그림을 화면에서 지우지 않음)
images = {}

FONT = ("Malgun Gothic", 11)
FONT_BOLD = ("Malgun Gothic", 11, "bold")
FONT_BIG = ("Malgun Gothic", 16, "bold")

# 색깔 설정: "#fdf6e3" 같은 숫자 코드 대신 brown, wheat 같은 이름으로 지정함.
# 색 변경 시 여기 이름만 바꾸면 화면 전체에 적용됨.
# 사용할 수 있는 색 이름 목록: https://www.tcl.tk/man/tcl8.6/TkCmd/colors.htm
BG_COLOR = "oldlace"          # 전체 배경 (크림색)
PANEL_COLOR = "floralwhite"   # 선택지가 나오는 칸의 배경
BUTTON_COLOR = "wheat"        # 선택지 버튼, 상태창 라벨
TIP_COLOR = "lightyellow"     # 마우스 오버 설명 창
TEXT_COLOR = "saddlebrown"    # 선택 결과 문장 글자색
GUIDE_COLOR = "gray"          # 안내 문구 글자색

# 툴팁(마우스 오버 설명 창)을 저장하는 리스트. 창이 하나만 뜨도록 관리함.
tooltip_windows = []


# ======================================================================
# 1. 버튼을 눌렀을 때 실행되는 함수들
# ======================================================================
def click_1():
    play_turn(0)


def click_2():
    play_turn(1)


def click_3():
    play_turn(2)


def play_turn(index):
    """index번째 선택지를 골라 한 턴 진행한 뒤 화면을 새로 그림."""
    result = game_logic.choose(index)

    lines = []
    if result["text"] != "":
        lines.append("▶ " + result["text"])
    for message in result["log"]:
        lines.append("   " + message)
    result_label.config(text="\n".join(lines))

    refresh()


def start_new_game():
    game_logic.new_game()
    result_label.config(text="새로운 다마고치가 태어났다!")
    refresh()


# ======================================================================
# 2. 마우스 오버 설명 창 (상태창)
# ======================================================================
def show_tooltip(event):
    hide_tooltip(event)
    status_name = event.widget.cget("text")     # 마우스를 올린 라벨의 글자 = 상태 이름

    window = tk.Toplevel(root)
    window.wm_overrideredirect(True)            # 제목 표시줄 없는 작은 창
    window.wm_geometry(f"+{event.x_root + 12}+{event.y_root + 12}")
    tk.Label(window, text=game_logic.status_description(status_name),
             justify="left", bg=TIP_COLOR, relief="solid", borderwidth=1,
             padx=10, pady=8, font=FONT).pack()
    tooltip_windows.append(window)


def hide_tooltip(event):
    for window in tooltip_windows:
        window.destroy()
    tooltip_windows.clear()


# ======================================================================
# 3. 화면 그리기
# ======================================================================
def draw_pet():
    """지금 상황에 맞는 강아지 이미지(images 폴더의 PNG)를 화면에 표시함."""
    name = game_logic.pet_image_name()     # 사용할 그림은 game_logic.py에서 결정함
    pet_label.config(image=images[name])


def draw_stat_bars():
    """■■■■□□□□□□ 7/10 모양의 스테이터스 바를 그림."""
    for key in STAT_NAMES:
        value = game["stats"][key]
        bar = "■" * value + "□" * (STAT_MAX - value)
        stat_labels[key].config(text=f"{bar}   {value}/{STAT_MAX}")


def draw_status_window():
    """상태창: 보유한 상태를 작은 라벨로 나열함."""
    # 이전에 그렸던 라벨 지우기
    for widget in status_frame.winfo_children():
        widget.destroy()

    if len(game["statuses"]) == 0:
        tk.Label(status_frame, text="(특별한 상태 없음)", font=FONT).pack(side="left")
        return

    for name in game["statuses"]:
        label = tk.Label(status_frame, text=name, font=FONT_BOLD,
                         bg=BUTTON_COLOR, relief="ridge", padx=8, pady=2)
        label.pack(side="left", padx=3)
        label.bind("<Enter>", show_tooltip)     # 마우스를 올렸을 때 실행
        label.bind("<Leave>", hide_tooltip)     # 마우스를 내렸을 때 실행


def refresh():
    """화면 전체를 현재 game 상태에 맞게 다시 그림."""
    header_label.config(
        text=f"{game_logic.season_name()}  ·  {game['age']}살 / {MAX_AGE}살  ·  {game['turn']}턴")
    draw_pet()
    draw_stat_bars()
    draw_status_window()

    if game["ending"] != "":
        show_ending()
    else:
        show_choice()


def show_choice():
    """선택지 문장과 버튼을 표시함."""
    choice = game["choice"]
    prompt_label.config(text="* " + choice["prompt"])

    options = choice["options"]
    click_functions = [click_1, click_2, click_3]

    # 버튼 3개를 모두 숨긴 뒤 필요한 개수만 다시 표시함
    for button in buttons:
        button.pack_forget()
    for i in range(len(options)):
        buttons[i].config(text=f"{i + 1}. {options[i]['text']}", command=click_functions[i])
        buttons[i].pack(fill="x", pady=3)


def show_ending():
    """엔딩 문장과 버튼(돌아보기 / 새로 시작)을 표시함."""
    info = ENDINGS[game["ending"]]
    if info["good"]:
        mark = "★"
    else:
        mark = "☆"
    prompt_label.config(text=f"{mark} 엔딩: {info['title']}\n\n{info['text']}")

    for button in buttons:
        button.pack_forget()
    buttons[0].config(text="우리의 선택들 돌아보기", command=show_history)
    buttons[1].config(text="새 다마고치 키우기", command=start_new_game)
    buttons[0].pack(fill="x", pady=3)
    buttons[1].pack(fill="x", pady=3)


def show_history():
    """엔딩 후 지금까지의 선택 기록을 새 창에 표시함."""
    window = tk.Toplevel(root)
    window.title("다마고치와 함께한 선택들")
    window.geometry("520x560")

    text_box = scrolledtext.ScrolledText(window, wrap="word", font=FONT)
    text_box.pack(fill="both", expand=True, padx=10, pady=10)

    for record in game["history"]:
        text_box.insert("end", f"[{record['turn']}턴 · {record['age']}살 {record['season']}]\n")
        text_box.insert("end", record["prompt"] + "\n")
        text_box.insert("end", "→ " + record["chosen"] + "\n")
        if record["result"] != "":
            text_box.insert("end", "   " + record["result"] + "\n")
        text_box.insert("end", "\n")

    text_box.config(state="disabled")     # 읽기 전용


# ======================================================================
# 4. 화면 배치 (프로그램 시작 시 한 번만 실행됨)
# ======================================================================
root = tk.Tk()
root.title("다마고치 키우기")
root.geometry("560x760")
root.configure(bg=BG_COLOR)

# 맨 위: 계절 / 나이 / 턴
header_label = tk.Label(root, font=FONT_BIG, bg=BG_COLOR)
header_label.pack(pady=(14, 4))

# images 폴더의 PNG 파일을 모두 불러옴 (창 생성 후에 실행해야 함)
for image_name in IMAGE_NAMES:
    images[image_name] = tk.PhotoImage(file=os.path.join(IMAGE_FOLDER, image_name + ".png"))

# 강아지 그림이 표시될 자리
pet_label = tk.Label(root, bg=BG_COLOR)
pet_label.pack(pady=4)

# 스테이터스 바 (건강 / 행복 / 친밀도)
stat_frame = tk.Frame(root, bg=BG_COLOR)
stat_frame.pack(pady=6)
stat_labels = {}      # {"health": 막대 라벨, ...}  (내용은 draw_stat_bars()가 채움)
row = 0
for key in STAT_NAMES:
    tk.Label(stat_frame, text=STAT_NAMES[key], font=FONT_BOLD, bg=BG_COLOR,
             width=7, anchor="w").grid(row=row, column=0)
    stat_labels[key] = tk.Label(stat_frame, font=FONT, bg=BG_COLOR)
    stat_labels[key].grid(row=row, column=1)
    row += 1

# 상태창
status_box = tk.LabelFrame(root, text=" 상태창 ", font=FONT_BOLD, bg=BG_COLOR, padx=8, pady=6)
status_box.pack(fill="x", padx=20, pady=6)
status_frame = tk.Frame(status_box, bg=BG_COLOR, height=34)
status_frame.pack(fill="x")
tk.Label(status_box, text="상태에 마우스를 올려보세요.", font=("Malgun Gothic", 9),
         bg=BG_COLOR, fg=GUIDE_COLOR).pack(anchor="w")

# 직전 선택의 결과 문장
result_label = tk.Label(root, font=FONT, bg=BG_COLOR, fg=TEXT_COLOR, wraplength=500,
                        justify="left", height=4, anchor="nw")
result_label.pack(fill="x", padx=24, pady=(4, 0))

# 선택지 영역
choice_frame = tk.Frame(root, bg=PANEL_COLOR, highlightthickness=1)
choice_frame.pack(fill="both", expand=True, padx=20, pady=(4, 16))
prompt_label = tk.Label(choice_frame, font=FONT, bg=PANEL_COLOR, wraplength=480, justify="left")
prompt_label.pack(padx=14, pady=(14, 8), anchor="w")

button_frame = tk.Frame(choice_frame, bg=PANEL_COLOR)
button_frame.pack(fill="x", padx=14, pady=(0, 12))

# 선택지 버튼 3개 (선택지가 2개면 3번째 버튼은 숨겨짐)
buttons = []
for i in range(3):
    button = tk.Button(button_frame, font=FONT, wraplength=440, justify="left",
                       anchor="w", bg=BUTTON_COLOR, padx=8, pady=6)
    buttons.append(button)


# ======================================================================
# 5. 게임 시작
# ======================================================================
start_new_game()
root.mainloop()
