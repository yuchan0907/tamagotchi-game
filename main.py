"""다마고치 키우기 - tkinter GUI.

실행: python3 main.py
"""

import tkinter as tk
from tkinter import scrolledtext

from data import MAX_AGE, STAT_MAX, STAT_NAMES
from game_logic import Game, describe_status

BG = "#fdf6e3"
PANEL = "#fffdf5"
FG = "#3b3228"
ACCENT = "#e0a458"

FONT = ("Malgun Gothic", 11)
FONT_BOLD = ("Malgun Gothic", 11, "bold")
FONT_TITLE = ("Malgun Gothic", 16, "bold")
FONT_BAR = ("Malgun Gothic", 12)


class Tooltip:
    """위젯에 마우스를 올리면 설명 창을 띄운다."""

    def __init__(self, widget, text_func):
        self.widget = widget
        self.text_func = text_func
        self.tip = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event):
        self.hide()
        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{event.x_root + 12}+{event.y_root + 12}")
        tk.Label(
            self.tip, text=self.text_func(), justify="left", bg="#fffbe6", fg=FG,
            relief="solid", borderwidth=1, padx=10, pady=8, font=FONT,
        ).pack()

    def hide(self, _event=None):
        if self.tip is not None:
            self.tip.destroy()
            self.tip = None


class App:
    def __init__(self, root):
        self.root = root
        root.title("다마고치 키우기")
        root.configure(bg=BG)
        root.geometry("560x760")
        root.minsize(520, 720)

        self.game = None
        self.build_widgets()
        self.new_game()

    # ------------------------------------------------------------------ UI 구성
    def build_widgets(self):
        # 헤더 (계절 / 나이 / 턴)
        self.header = tk.Label(self.root, font=FONT_TITLE, bg=BG, fg=FG)
        self.header.pack(pady=(14, 4))

        # 다마고치 (캔버스로 직접 그린 강아지)
        self.canvas = tk.Canvas(self.root, width=220, height=170, bg=PANEL,
                                highlightthickness=1, highlightbackground=ACCENT)
        self.canvas.pack(pady=4)

        # 스테이터스 바
        self.stat_frame = tk.Frame(self.root, bg=BG)
        self.stat_frame.pack(pady=6)
        self.stat_labels = {}
        for row, (key, name) in enumerate(STAT_NAMES.items()):
            tk.Label(self.stat_frame, text=name, font=FONT_BOLD, bg=BG, fg=FG,
                     width=7, anchor="w").grid(row=row, column=0, padx=(0, 6))
            bar = tk.Label(self.stat_frame, font=FONT_BAR, bg=BG, fg=FG, anchor="w")
            bar.grid(row=row, column=1)
            num = tk.Label(self.stat_frame, font=FONT, bg=BG, fg=FG, width=6)
            num.grid(row=row, column=2)
            self.stat_labels[key] = (bar, num)

        # 상태창
        status_box = tk.LabelFrame(self.root, text=" 상태창 ", font=FONT_BOLD,
                                   bg=BG, fg=FG, padx=8, pady=6)
        status_box.pack(fill="x", padx=20, pady=6)
        self.status_inner = tk.Frame(status_box, bg=BG, height=34)
        self.status_inner.pack(fill="x")
        self.status_hint = tk.Label(status_box, text="상태에 마우스를 올려보세요.",
                                    font=("Malgun Gothic", 9), bg=BG, fg="#9a8c78")
        self.status_hint.pack(anchor="w")

        # 이전 턴 결과
        self.result_label = tk.Label(self.root, font=FONT, bg=BG, fg="#7a5c2e",
                                     wraplength=500, justify="left", height=4,
                                     anchor="nw")
        self.result_label.pack(fill="x", padx=24, pady=(4, 0))

        # 선택지
        self.choice_frame = tk.Frame(self.root, bg=PANEL, highlightthickness=1,
                                     highlightbackground=ACCENT)
        self.choice_frame.pack(fill="both", expand=True, padx=20, pady=(4, 16))
        self.prompt_label = tk.Label(self.choice_frame, font=FONT, bg=PANEL, fg=FG,
                                     wraplength=480, justify="left")
        self.prompt_label.pack(padx=14, pady=(14, 8), anchor="w")
        self.button_frame = tk.Frame(self.choice_frame, bg=PANEL)
        self.button_frame.pack(fill="x", padx=14, pady=(0, 12))

    # ------------------------------------------------------------------ 게임 흐름
    def new_game(self):
        self.game = Game()
        self.result_label.config(text="새로운 다마고치가 태어났다!")
        self.refresh()

    def on_choose(self, index):
        result = self.game.choose(index)
        lines = [f"▶ {result.result_text}"] if result.result_text else []
        lines += [f"  {entry}" for entry in result.log]
        self.result_label.config(text="\n".join(lines))
        self.refresh()

    # ------------------------------------------------------------------ 화면 갱신
    def refresh(self):
        g = self.game
        self.header.config(text=f"{g.season}  ·  {g.age}살 / {MAX_AGE}살  ·  {g.turn}턴")
        self.draw_pet()

        for key, (bar, num) in self.stat_labels.items():
            value = g.stats[key]
            bar.config(text="■" * value + "□" * (STAT_MAX - value))
            num.config(text=f"{value}/{STAT_MAX}")

        self.draw_statuses()

        for w in self.button_frame.winfo_children():
            w.destroy()

        if g.is_over:
            self.show_ending()
            return

        choice = g.current_choice
        self.prompt_label.config(text="* " + choice["prompt"])
        for i, option in enumerate(choice["options"]):
            tk.Button(
                self.button_frame, text=f"{i + 1}. {option['text']}", font=FONT,
                wraplength=440, justify="left", anchor="w", bg="#f6e7c8",
                activebackground=ACCENT, relief="groove", padx=8, pady=6,
                command=lambda idx=i: self.on_choose(idx),
            ).pack(fill="x", pady=3)

    def draw_statuses(self):
        for w in self.status_inner.winfo_children():
            w.destroy()
        if not self.game.statuses:
            tk.Label(self.status_inner, text="(특별한 상태 없음)", font=FONT,
                     bg=BG, fg="#9a8c78").pack(side="left")
            return
        for name, remaining in self.game.statuses.items():
            lbl = tk.Label(self.status_inner, text=name, font=FONT_BOLD, bg="#f6e7c8",
                           fg=FG, relief="ridge", padx=8, pady=2)
            lbl.pack(side="left", padx=3, pady=2)
            Tooltip(lbl, lambda n=name, r=remaining: describe_status(n, r))

    def draw_pet(self):
        c = self.canvas
        c.delete("all")
        g = self.game
        happy = g.stats["happiness"]
        sick = g.stats["health"] <= 3 or "감기" in g.statuses or "부상" in g.statuses

        fur = "#d9a66b" if not sick else "#c9b79b"
        dark = "#8a5a2b"

        # 꼬리
        c.create_arc(150, 85, 200, 135, start=-20, extent=140, style="arc",
                     outline=dark, width=6)
        # 몸
        c.create_oval(60, 95, 165, 160, fill=fur, outline=dark, width=2)
        # 다리
        c.create_oval(75, 140, 100, 165, fill=fur, outline=dark, width=2)
        c.create_oval(125, 140, 150, 165, fill=fur, outline=dark, width=2)
        # 귀
        c.create_oval(55, 25, 90, 75, fill=dark, outline=dark)
        c.create_oval(130, 25, 165, 75, fill=dark, outline=dark)
        # 얼굴
        c.create_oval(65, 30, 155, 110, fill=fur, outline=dark, width=2)
        # 눈
        if sick:
            c.create_line(88, 62, 98, 72, fill=FG, width=3)
            c.create_line(98, 62, 88, 72, fill=FG, width=3)
            c.create_line(122, 62, 132, 72, fill=FG, width=3)
            c.create_line(132, 62, 122, 72, fill=FG, width=3)
        else:
            c.create_oval(88, 60, 100, 74, fill=FG)
            c.create_oval(120, 60, 132, 74, fill=FG)
        # 코
        c.create_oval(103, 78, 117, 90, fill=FG)
        # 입 (행복도에 따라 표정 변화)
        if happy >= 7:
            c.create_arc(95, 82, 125, 104, start=200, extent=140, style="arc",
                         outline=FG, width=2)
        elif happy >= 4:
            c.create_line(100, 98, 120, 98, fill=FG, width=2)
        else:
            c.create_arc(95, 96, 125, 116, start=20, extent=140, style="arc",
                         outline=FG, width=2)

    # ------------------------------------------------------------------ 엔딩
    def show_ending(self):
        info = self.game.ending_info()
        mark = "★ " if info["good"] else "☆ "
        self.prompt_label.config(text=f"{mark}엔딩: {info['title']}\n\n{info['text']}")
        tk.Button(self.button_frame, text="우리의 선택들 돌아보기", font=FONT,
                  bg="#f6e7c8", relief="groove", pady=6,
                  command=self.show_history).pack(fill="x", pady=3)
        tk.Button(self.button_frame, text="새 다마고치 키우기", font=FONT,
                  bg="#f6e7c8", relief="groove", pady=6,
                  command=self.new_game).pack(fill="x", pady=3)

    def show_history(self):
        win = tk.Toplevel(self.root)
        win.title("다마고치와 함께한 선택들")
        win.geometry("520x560")
        win.configure(bg=BG)
        text = scrolledtext.ScrolledText(win, wrap="word", font=FONT, bg=PANEL, fg=FG)
        text.pack(fill="both", expand=True, padx=10, pady=10)

        text.tag_configure("head", font=FONT_BOLD, foreground="#7a5c2e")
        text.tag_configure("chosen", foreground="#2b6a4f")
        for rec in self.game.history:
            text.insert("end", f"[{rec['turn']}턴 · {rec['age']}살 {rec['season']}]\n", "head")
            text.insert("end", f"{rec['prompt']}\n")
            text.insert("end", f"→ {rec['chosen']}\n", "chosen")
            if rec["result"]:
                text.insert("end", f"   {rec['result']}\n")
            text.insert("end", "\n")
        text.config(state="disabled")


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
