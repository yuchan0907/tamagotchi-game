"""다마고치 키우기 - 화면(tkinter) 파일.

실행 방법:  python main.py

이 파일은 "화면에 보여주기"만 담당합니다.
게임 규칙은 game_logic.py, 게임 내용(선택지 등)은 data.py 에 있습니다.
"""

import tkinter as tk
from tkinter import scrolledtext

import game_logic
from game_logic import game
from data import ENDINGS, MAX_AGE, STAT_MAX, STAT_NAMES

FONT = ("Malgun Gothic", 11)
FONT_BOLD = ("Malgun Gothic", 11, "bold")
FONT_BIG = ("Malgun Gothic", 16, "bold")

# 툴팁(마우스 오버 설명 창)을 저장해 두는 리스트. 창이 하나만 뜨게 관리한다.
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
    """index번째 선택지를 골라 한 턴 진행하고 화면을 새로 그린다."""
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
             justify="left", bg="#fffbe6", relief="solid", borderwidth=1,
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
    """캔버스에 강아지를 그린다. 행복도/건강에 따라 표정이 바뀐다."""
    canvas.delete("all")
    happiness = game["stats"]["happiness"]
    sick = game["stats"]["health"] <= 3 or "감기" in game["statuses"]

    if sick:
        fur = "#c9b79b"     # 아프면 털 색이 칙칙해짐
    else:
        fur = "#d9a66b"
    dark = "#8a5a2b"

    canvas.create_oval(60, 95, 165, 160, fill=fur, outline=dark, width=2)    # 몸
    canvas.create_oval(55, 25, 90, 75, fill=dark, outline=dark)              # 왼쪽 귀
    canvas.create_oval(130, 25, 165, 75, fill=dark, outline=dark)            # 오른쪽 귀
    canvas.create_oval(65, 30, 155, 110, fill=fur, outline=dark, width=2)    # 얼굴
    canvas.create_oval(88, 60, 100, 74, fill="black")                        # 왼쪽 눈
    canvas.create_oval(120, 60, 132, 74, fill="black")                       # 오른쪽 눈
    canvas.create_oval(103, 78, 117, 90, fill="black")                       # 코

    # 입 모양: 행복도에 따라 웃는 입 / 일자 입 / 슬픈 입
    if happiness >= 7:
        canvas.create_arc(95, 82, 125, 104, start=200, extent=140, style="arc", width=2)
    elif happiness >= 4:
        canvas.create_line(100, 98, 120, 98, width=2)
    else:
        canvas.create_arc(95, 96, 125, 116, start=20, extent=140, style="arc", width=2)


def draw_stat_bars():
    """■■■■□□□□□□ 모양의 스테이터스 바를 그린다."""
    for key in STAT_NAMES:
        value = game["stats"][key]
        bar = "■" * value + "□" * (STAT_MAX - value)
        stat_bar_labels[key].config(text=bar)
        stat_num_labels[key].config(text=f"{value}/{STAT_MAX}")


def draw_status_window():
    """상태창: 가지고 있는 상태를 작은 라벨로 나열한다."""
    # 이전에 그렸던 라벨 지우기
    for widget in status_frame.winfo_children():
        widget.destroy()

    if len(game["statuses"]) == 0:
        tk.Label(status_frame, text="(특별한 상태 없음)", font=FONT).pack(side="left")
        return

    for name in game["statuses"]:
        label = tk.Label(status_frame, text=name, font=FONT_BOLD,
                         bg="#f6e7c8", relief="ridge", padx=8, pady=2)
        label.pack(side="left", padx=3)
        label.bind("<Enter>", show_tooltip)     # 마우스를 올리면
        label.bind("<Leave>", hide_tooltip)     # 마우스를 내리면


def refresh():
    """화면 전체를 현재 game 상태에 맞게 다시 그린다."""
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
    """선택지 문장과 버튼을 보여준다."""
    choice = game["choice"]
    prompt_label.config(text="* " + choice["prompt"])

    options = choice["options"]
    click_functions = [click_1, click_2, click_3]

    # 버튼 3개를 일단 모두 숨긴 뒤, 필요한 개수만 다시 보여준다
    for button in buttons:
        button.pack_forget()
    for i in range(len(options)):
        buttons[i].config(text=f"{i + 1}. {options[i]['text']}", command=click_functions[i])
        buttons[i].pack(fill="x", pady=3)


def show_ending():
    """엔딩 문장과 버튼(돌아보기 / 새로 시작)을 보여준다."""
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
    """엔딩 후, 지금까지의 선택 기록을 새 창에 보여준다."""
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
# 4. 화면 배치 (프로그램이 시작할 때 한 번만 실행)
# ======================================================================
root = tk.Tk()
root.title("다마고치 키우기")
root.geometry("560x760")
root.configure(bg="#fdf6e3")

# 맨 위: 계절 / 나이 / 턴
header_label = tk.Label(root, font=FONT_BIG, bg="#fdf6e3")
header_label.pack(pady=(14, 4))

# 강아지 그림
canvas = tk.Canvas(root, width=220, height=170, bg="#fffdf5")
canvas.pack(pady=4)

# 스테이터스 바 (건강 / 행복 / 친밀도)
stat_frame = tk.Frame(root, bg="#fdf6e3")
stat_frame.pack(pady=6)
stat_bar_labels = {}
stat_num_labels = {}
row = 0
for key in STAT_NAMES:
    tk.Label(stat_frame, text=STAT_NAMES[key], font=FONT_BOLD, bg="#fdf6e3",
             width=7, anchor="w").grid(row=row, column=0)
    stat_bar_labels[key] = tk.Label(stat_frame, font=("Malgun Gothic", 12), bg="#fdf6e3")
    stat_bar_labels[key].grid(row=row, column=1)
    stat_num_labels[key] = tk.Label(stat_frame, font=FONT, bg="#fdf6e3", width=6)
    stat_num_labels[key].grid(row=row, column=2)
    row += 1

# 상태창
status_box = tk.LabelFrame(root, text=" 상태창 ", font=FONT_BOLD, bg="#fdf6e3", padx=8, pady=6)
status_box.pack(fill="x", padx=20, pady=6)
status_frame = tk.Frame(status_box, bg="#fdf6e3", height=34)
status_frame.pack(fill="x")
tk.Label(status_box, text="상태에 마우스를 올려보세요.", font=("Malgun Gothic", 9),
         bg="#fdf6e3", fg="gray").pack(anchor="w")

# 직전 선택의 결과 문장
result_label = tk.Label(root, font=FONT, bg="#fdf6e3", fg="#7a5c2e", wraplength=500,
                        justify="left", height=4, anchor="nw")
result_label.pack(fill="x", padx=24, pady=(4, 0))

# 선택지 영역
choice_frame = tk.Frame(root, bg="#fffdf5", highlightthickness=1)
choice_frame.pack(fill="both", expand=True, padx=20, pady=(4, 16))
prompt_label = tk.Label(choice_frame, font=FONT, bg="#fffdf5", wraplength=480, justify="left")
prompt_label.pack(padx=14, pady=(14, 8), anchor="w")

button_frame = tk.Frame(choice_frame, bg="#fffdf5")
button_frame.pack(fill="x", padx=14, pady=(0, 12))

# 선택지 버튼 3개 (선택지가 2개면 3번째 버튼은 숨겨짐)
buttons = []
for i in range(3):
    button = tk.Button(button_frame, font=FONT, wraplength=440, justify="left",
                       anchor="w", bg="#f6e7c8", padx=8, pady=6)
    buttons.append(button)


# ======================================================================
# 5. 게임 시작
# ======================================================================
start_new_game()
root.mainloop()
