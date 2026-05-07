import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox

def _draw_logo(canvas, bg_color: str, fg_color: str):
    """Draw the T/G/L/K logo with a circle in the center on a tk.Canvas (48x48)."""
    canvas.configure(bg=bg_color)
    # Four letters at the four corners
    font = ("Arial", 11, "bold")
    canvas.create_text(10, 12, text="T", font=font, fill=fg_color, anchor="center")
    canvas.create_text(38, 12, text="G", font=font, fill=fg_color, anchor="center")
    canvas.create_text(10, 36, text="L", font=font, fill=fg_color, anchor="center")
    canvas.create_text(38, 36, text="K", font=font, fill=fg_color, anchor="center")
    # Circle centered on the canvas, overlapping all four letters
    canvas.create_oval(12, 6, 36, 42, outline=fg_color, width=1.5)


BG = "#000000"
BG_CARD = "#111111"
BORDER = "#222222"
ACCENT = "#EB1D49"
ACCENT_HOVER = "#C91540"
TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "#94A3B8"
TEXT_MUTED = "#475569"
CHIP_BG = "#1A1A1A"
BAR_BG = "#2A2A2A"


class GameCard(ctk.CTkFrame):
    """
    Card widget displaying a single game session's statistics.
    Demonstrates: OOP, Encapsulation, CustomTkinter widgets
    """

    def __init__(self, parent, session: dict, lang, on_play, on_delete, on_export):
        super().__init__(
            parent,
            fg_color=BG_CARD,
            border_color=BORDER,
            border_width=1,
            corner_radius=16,
        )
        self.__session = session
        self.__lang = lang
        self.__on_play = on_play
        self.__on_delete = on_delete
        self.__on_export = on_export
        self._build()

    def __str__(self):
        return f"GameCard(session_id={self.__session['id']}, name={self.__session['name']})"

    def _build(self):
        s = self.__session
        l = self.__lang
        win_rate = float(s.get("win_rate") or 0)
        mode_label = l("card", "mode_manual") if s["mode"] == "manual" else l("card", "mode_auto")

        # Card name
        ctk.CTkLabel(
            self,
            text=s["name"],
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_PRIMARY,
            anchor="w",
        ).pack(fill="x", padx=16, pady=(14, 8))

        # GAMES chip (full width)
        games_chip = ctk.CTkFrame(self, fg_color=CHIP_BG, corner_radius=10)
        games_chip.pack(fill="x", padx=16, pady=(0, 6))

        ctk.CTkLabel(
            games_chip, text="GAMES",
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color=TEXT_MUTED, anchor="w",
        ).pack(side="left", padx=(12, 4), pady=10)

        ctk.CTkLabel(
            games_chip, text=f"x{s['total_games']}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TEXT_PRIMARY, anchor="e",
        ).pack(side="right", padx=(4, 12), pady=10)

        # CARDS + TYPE chips side by side
        chips_row = ctk.CTkFrame(self, fg_color="transparent")
        chips_row.pack(fill="x", padx=16, pady=(0, 10))
        chips_row.columnconfigure(0, weight=1)
        chips_row.columnconfigure(1, weight=1)

        doors_chip = ctk.CTkFrame(chips_row, fg_color=CHIP_BG, corner_radius=10)
        doors_chip.grid(row=0, column=0, sticky="ew", padx=(0, 4))
        ctk.CTkLabel(
            doors_chip, text="CARDS",
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color=TEXT_MUTED, anchor="w",
        ).pack(side="left", padx=(10, 4), pady=10)
        ctk.CTkLabel(
            doors_chip, text=f"x{s['door_count']}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TEXT_PRIMARY, anchor="e",
        ).pack(side="right", padx=(4, 10), pady=10)

        type_chip = ctk.CTkFrame(chips_row, fg_color=CHIP_BG, corner_radius=10)
        type_chip.grid(row=0, column=1, sticky="ew", padx=(4, 0))
        ctk.CTkLabel(
            type_chip, text="TYPE",
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color=TEXT_MUTED, anchor="w",
        ).pack(side="left", padx=(10, 4), pady=10)
        ctk.CTkLabel(
            type_chip, text=mode_label,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TEXT_PRIMARY, anchor="e",
        ).pack(side="right", padx=(4, 10), pady=10)

        # Win rate row
        wr_row = ctk.CTkFrame(self, fg_color="transparent")
        wr_row.pack(fill="x", padx=16, pady=(0, 4))

        ctk.CTkLabel(
            wr_row, text=f"{win_rate:.0f}%",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=ACCENT, anchor="w",
        ).pack(side="left")

        ctk.CTkLabel(
            wr_row, text=l("card", "win_rate"),
            font=ctk.CTkFont(size=12),
            text_color=TEXT_SECONDARY, anchor="e",
        ).pack(side="left", padx=(6, 0), pady=(6, 0))

        # Progress bar
        bar_bg = ctk.CTkFrame(self, fg_color=BAR_BG, height=4, corner_radius=2)
        bar_bg.pack(fill="x", padx=16, pady=(0, 12))
        bar_bg.pack_propagate(False)
        ratio = min(win_rate / 100, 1.0)
        if ratio > 0:
            ctk.CTkFrame(bar_bg, fg_color=ACCENT, height=4, corner_radius=2).place(
                relx=0, rely=0, relwidth=ratio, relheight=1
            )

        # Separator
        ctk.CTkFrame(self, fg_color=BORDER, height=1).pack(fill="x")

        # Action buttons
        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(fill="x", padx=12, pady=10)

        if s["mode"] == "manual":
            ctk.CTkButton(
                btn_row,
                text=l("card", "play"),
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color=ACCENT, hover_color=ACCENT_HOVER,
                text_color=TEXT_PRIMARY,
                height=32, corner_radius=8,
                command=lambda sid=s: self.__on_play(sid),
            ).pack(side="left", padx=(0, 4))

        ctk.CTkButton(
            btn_row,
            text=l("card", "export"),
            font=ctk.CTkFont(size=12),
            fg_color=CHIP_BG, hover_color=BORDER,
            text_color=TEXT_SECONDARY,
            height=32, corner_radius=8,
            command=lambda sid=s["id"]: self.__on_export(sid),
        ).pack(side="left", padx=(0, 4))

        ctk.CTkButton(
            btn_row,
            text=l("card", "delete"),
            font=ctk.CTkFont(size=12),
            fg_color="transparent", hover_color="#2D0010",
            text_color=ACCENT, border_width=1, border_color=ACCENT,
            height=32, corner_radius=8,
            command=lambda sid=s: self.__on_delete(sid),
        ).pack(side="right")


class MainScreen(ctk.CTkFrame):
    """
    Main application screen showing game history and statistics.
    Demonstrates: OOP, CustomTkinter (ScrollableFrame, Label, Button, Frame)
    """

    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG)
        self.__app = app
        self.__db = app.db
        self.__lang = app.lang
        # Clear old stale callbacks before registering fresh one
        self.__lang.clear_callbacks()
        self.__lang.on_change(self._refresh)
        self._build()
        self._refresh()

    def __str__(self):
        return "MainScreen()"

    def _build(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="#050505", height=64)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Logo: T G on top-left/top-right, L K on bottom-left/bottom-right, circle center
        logo_canvas = tk.Canvas(
            header, width=48, height=48,
            bg="#050505", highlightthickness=0,
        )
        logo_canvas.pack(side="left", padx=(20, 8), pady=8)
        _draw_logo(logo_canvas, "#050505", TEXT_PRIMARY)

        # App title
        ctk.CTkLabel(
            header,
            text=self.__lang("main_screen", "title"),
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(side="left", padx=8)

        # Right controls
        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right", padx=20, fill="y")

        self._lang_btn = ctk.CTkButton(
            right,
            text=self.__lang("main_screen", "language"),
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=BORDER, hover_color="#333333",
            text_color=TEXT_PRIMARY,
            width=48, height=32, corner_radius=8,
            command=self._toggle_language,
        )
        self._lang_btn.pack(side="right", pady=16)

        self._export_btn = ctk.CTkButton(
            right,
            text=self.__lang("main_screen", "export_all"),
            font=ctk.CTkFont(size=12),
            fg_color=BORDER, hover_color="#333333",
            text_color=TEXT_SECONDARY,
            height=32, corner_radius=8,
            command=self._export_all,
        )
        self._export_btn.pack(side="right", pady=16, padx=(0, 8))

        # Global stats row
        self._stats_frame = ctk.CTkFrame(self, fg_color="#050505")
        self._stats_frame.pack(fill="x")

        # Scrollable cards
        self._scroll = ctk.CTkScrollableFrame(
            self, fg_color=BG,
            scrollbar_button_color=BORDER,
            scrollbar_button_hover_color=ACCENT,
        )
        self._scroll.pack(fill="both", expand=True, padx=24, pady=(16, 80))

        # FAB
        self._fab = ctk.CTkButton(
            self,
            text="+",
            font=ctk.CTkFont(size=28, weight="bold"),
            fg_color=ACCENT, hover_color=ACCENT_HOVER,
            text_color=TEXT_PRIMARY,
            width=64, height=64, corner_radius=32,
            command=self._open_new_game_dialog,
        )
        self._fab.place(relx=1.0, rely=1.0, anchor="se", x=-28, y=-28)

    def _refresh(self):
        if hasattr(self, "_lang_btn"):
            self._lang_btn.configure(text=self.__lang("main_screen", "language"))
        if hasattr(self, "_export_btn"):
            self._export_btn.configure(text=self.__lang("main_screen", "export_all"))
        self._draw_stats()
        self._draw_cards()

    def _draw_stats(self):
        for w in self._stats_frame.winfo_children():
            w.destroy()

        stats = self.__db.get_global_stats()
        l = self.__lang

        items = [
            (str(stats.get("total_sessions", 0)), l("main_screen", "total_sessions")),
            (str(stats.get("total_games", 0)), l("main_screen", "total_games")),
            (f"{stats.get('overall_win_rate', 0):.1f}%", l("main_screen", "win_rate")),
        ]

        for value, label in items:
            chip = ctk.CTkFrame(self._stats_frame, fg_color="transparent")
            chip.pack(side="left", padx=24, pady=12)
            ctk.CTkLabel(
                chip, text=value,
                font=ctk.CTkFont(size=22, weight="bold"),
                text_color=ACCENT,
            ).pack()
            ctk.CTkLabel(
                chip, text=label,
                font=ctk.CTkFont(size=10),
                text_color=TEXT_MUTED,
            ).pack()

        ctk.CTkFrame(self._stats_frame, fg_color=BORDER, height=1).pack(
            fill="x", side="bottom"
        )

    def _draw_cards(self):
        for w in self._scroll.winfo_children():
            w.destroy()

        sessions = self.__db.get_all_sessions()

        if not sessions:
            ctk.CTkLabel(
                self._scroll,
                text=self.__lang("main_screen", "no_games"),
                font=ctk.CTkFont(size=16),
                text_color=TEXT_MUTED,
            ).pack(expand=True, pady=80)
            return

        cols = 3
        for i, session in enumerate(sessions):
            row, col = divmod(i, cols)
            card = GameCard(
                self._scroll, session, self.__lang,
                on_play=self._play_session,
                on_delete=self._delete_session,
                on_export=self._export_session,
            )
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        for c in range(cols):
            self._scroll.columnconfigure(c, weight=1)

    def _open_new_game_dialog(self):
        from ui.new_game_dialog import NewGameDialog
        dialog = NewGameDialog(self, self.__app)
        dialog.grab_set()
        self.wait_window(dialog)
        # After dialog closes, check what it produced
        if not self.winfo_exists():
            return
        pending_game = getattr(dialog, "pending_game", None)
        if pending_game:
            game, session_id = pending_game
            self.__app.show_game_screen(game, session_id)
            return
        pending_auto = getattr(dialog, "pending_auto_results", None)
        if pending_auto:
            results, num_games, doors = pending_auto
            self._refresh()
            self._show_auto_results(results, num_games, doors)
            return
        self._refresh()

    def _play_session(self, session: dict):
        from models.game import ManualGame
        game = ManualGame(
            game_id=session["id"],
            name=session["name"],
            door_count=session["door_count"],
        )
        game._total_rounds = session["total_games"]
        game._wins = session["wins"]
        self.__app.show_game_screen(game, session["id"])

    def _delete_session(self, session: dict):
        msg = self.__lang("confirm_delete", "message", name=session["name"])
        if messagebox.askyesno(self.__lang("confirm_delete", "title"), msg):
            self.__db.delete_session(session["id"])
            self._refresh()

    def _export_session(self, session_id: int):
        try:
            path = self.__db.export_to_csv(session_id=session_id)
            messagebox.showinfo("Export", self.__lang("export_success", path=path))
        except Exception as e:
            messagebox.showerror(self.__lang("error"), str(e))

    def _export_all(self):
        try:
            path = self.__db.export_to_csv()
            messagebox.showinfo("Export", self.__lang("export_success", path=path))
        except Exception as e:
            messagebox.showerror(self.__lang("error"), str(e))

    def _show_auto_results(self, results: dict, num_games: int, doors: int):
        l = self.__lang
        dialog = ctk.CTkToplevel(self)
        dialog.title(l("auto_result", "title"))
        dialog.geometry("440x380")
        dialog.resizable(False, False)
        dialog.configure(fg_color="#050505")
        dialog.grab_set()

        dialog.update_idletasks()
        px = self.__app.winfo_x() + (self.__app.winfo_width() - 440) // 2
        py = self.__app.winfo_y() + (self.__app.winfo_height() - 380) // 2
        dialog.geometry(f"+{px}+{py}")

        ctk.CTkLabel(
            dialog, text=l("auto_result", "title"),
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(pady=(28, 16))

        info = ctk.CTkFrame(dialog, fg_color="#0D1117",
                            corner_radius=14, border_color=BORDER, border_width=1)
        info.pack(fill="x", padx=32, pady=8)

        rows = [
            (l("auto_result", "total"), str(results["total"])),
            (l("auto_result", "wins_label"), str(results["wins"])),
            (l("auto_result", "win_rate_label"), f"{results['win_rate']:.1f}%"),
        ]
        for label, value in rows:
            row = ctk.CTkFrame(info, fg_color="transparent")
            row.pack(fill="x", padx=16, pady=6)
            ctk.CTkLabel(row, text=label, font=ctk.CTkFont(size=12),
                         text_color=TEXT_SECONDARY, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=value, font=ctk.CTkFont(size=13, weight="bold"),
                         text_color=TEXT_PRIMARY, anchor="e").pack(side="right")

        bar_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        bar_frame.pack(fill="x", padx=32, pady=8)
        ctk.CTkLabel(bar_frame, text=f"{l('auto_result', 'win_rate_label')} {results['win_rate']:.1f}%",
                     font=ctk.CTkFont(size=11), text_color=ACCENT).pack(anchor="w")
        bg = ctk.CTkFrame(bar_frame, fg_color=BORDER, height=8, corner_radius=4)
        bg.pack(fill="x", pady=(4, 0))
        bg.pack_propagate(False)
        ctk.CTkFrame(bg, fg_color=ACCENT, height=8, corner_radius=4).place(
            relx=0, rely=0,
            relwidth=min(results["win_rate"] / 100, 1.0),
            relheight=1,
        )

        ctk.CTkLabel(
            dialog,
            text=l("auto_result", "conclusion", rate=results["win_rate"]),
            font=ctk.CTkFont(size=12),
            text_color=TEXT_SECONDARY,
            wraplength=380,
        ).pack(padx=32, pady=12)

        ctk.CTkButton(
            dialog,
            text=l("auto_result", "close"),
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=ACCENT, hover_color=ACCENT_HOVER,
            text_color=TEXT_PRIMARY,
            height=44, corner_radius=10,
            command=dialog.destroy,
        ).pack(padx=32, pady=(0, 24), fill="x")

    def _toggle_language(self):
        self.__lang.switch()
