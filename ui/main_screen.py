import customtkinter as ctk
from tkinter import messagebox

# Design tokens matching SVG design
BG = "#000000"
BG_CARD = "#0D1117"
BG_CARD2 = "#111827"
BORDER = "#1E293B"
ACCENT = "#EB1D49"
ACCENT_HOVER = "#C91540"
TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "#94A3B8"
TEXT_MUTED = "#475569"
SUCCESS = "#22C55E"
BAR_BG = "#1E293B"


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

        # Top row: name + mode badge
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=16, pady=(14, 0))

        ctk.CTkLabel(
            top, text=s["name"],
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=TEXT_PRIMARY, anchor="w"
        ).pack(side="left")

        badge = ctk.CTkFrame(top, fg_color=ACCENT, corner_radius=6)
        badge.pack(side="right")
        ctk.CTkLabel(
            badge, text=mode_label,
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=TEXT_PRIMARY, padx=8, pady=2
        ).pack()

        # Stats row: doors, games, wins
        stats = ctk.CTkFrame(self, fg_color="transparent")
        stats.pack(fill="x", padx=16, pady=(8, 0))

        self._stat_chip(stats, f"🚪 {s['door_count']}", l("card", "doors"))
        self._stat_chip(stats, f"🎮 {s['total_games']}", l("card", "games"))
        self._stat_chip(stats, f"🏆 {s['wins']}", l("card", "wins"))

        # Win rate bar
        bar_frame = ctk.CTkFrame(self, fg_color="transparent")
        bar_frame.pack(fill="x", padx=16, pady=(10, 0))

        ctk.CTkLabel(
            bar_frame,
            text=f"{l('card', 'win_rate')}: {win_rate:.1f}%",
            font=ctk.CTkFont(size=11),
            text_color=TEXT_SECONDARY, anchor="w"
        ).pack(fill="x")

        bar_bg = ctk.CTkFrame(bar_frame, fg_color=BAR_BG, height=6, corner_radius=3)
        bar_bg.pack(fill="x", pady=(4, 0))
        bar_bg.pack_propagate(False)

        fill_ratio = min(win_rate / 100, 1.0)
        if fill_ratio > 0:
            bar_fill = ctk.CTkFrame(bar_bg, fg_color=ACCENT, height=6, corner_radius=3)
            bar_fill.place(relx=0, rely=0, relwidth=fill_ratio, relheight=1)

        # Date
        ctk.CTkLabel(
            self,
            text=s.get("created_at", ""),
            font=ctk.CTkFont(size=10),
            text_color=TEXT_MUTED, anchor="w"
        ).pack(fill="x", padx=16, pady=(6, 0))

        # Action buttons
        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(fill="x", padx=16, pady=(10, 14))

        if s["mode"] == "manual":
            ctk.CTkButton(
                btn_row,
                text=l("card", "play"),
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color=ACCENT, hover_color=ACCENT_HOVER,
                text_color=TEXT_PRIMARY,
                height=32, corner_radius=8,
                command=lambda: self.__on_play(s)
            ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            btn_row,
            text=l("card", "export"),
            font=ctk.CTkFont(size=12),
            fg_color=BORDER, hover_color="#2D3748",
            text_color=TEXT_SECONDARY,
            height=32, corner_radius=8,
            command=lambda: self.__on_export(s["id"])
        ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            btn_row,
            text=l("card", "delete"),
            font=ctk.CTkFont(size=12),
            fg_color="transparent", hover_color="#2D0010",
            text_color=ACCENT, border_width=1, border_color=ACCENT,
            height=32, corner_radius=8,
            command=lambda: self.__on_delete(s)
        ).pack(side="right")

    def _stat_chip(self, parent, value: str, label: str):
        chip = ctk.CTkFrame(parent, fg_color=BORDER, corner_radius=8)
        chip.pack(side="left", padx=(0, 6))
        ctk.CTkLabel(
            chip, text=value,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=TEXT_PRIMARY, padx=8, pady=4
        ).pack()


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
        self.__lang.on_change(self._refresh)
        self._build()
        self._refresh()

    def __str__(self):
        return "MainScreen()"

    def _build(self):
        # Header bar
        header = ctk.CTkFrame(self, fg_color="#050505", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Logo area
        logo_frame = ctk.CTkFrame(header, fg_color="transparent")
        logo_frame.pack(side="left", padx=20, pady=0, fill="y")

        logo_circle = ctk.CTkFrame(
            logo_frame, fg_color="transparent",
            width=44, height=44,
            border_color=TEXT_SECONDARY, border_width=1,
            corner_radius=22
        )
        logo_circle.pack(side="left", pady=18)
        logo_circle.pack_propagate(False)
        ctk.CTkLabel(
            logo_circle, text="MH",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_PRIMARY
        ).place(relx=0.5, rely=0.5, anchor="center")

        # App title
        ctk.CTkLabel(
            header,
            text=self.__lang("main_screen", "title"),
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=ACCENT
        ).pack(side="left", padx=16, pady=0)

        # Right header controls
        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right", padx=20, fill="y")

        self._lang_btn = ctk.CTkButton(
            right,
            text=self.__lang("main_screen", "language"),
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=BORDER, hover_color="#2D3748",
            text_color=TEXT_PRIMARY,
            width=48, height=32, corner_radius=8,
            command=self._toggle_language
        )
        self._lang_btn.pack(side="right", pady=24)

        self._export_btn = ctk.CTkButton(
            right,
            text=self.__lang("main_screen", "export_all"),
            font=ctk.CTkFont(size=12),
            fg_color=BORDER, hover_color="#2D3748",
            text_color=TEXT_SECONDARY,
            height=32, corner_radius=8,
            command=self._export_all
        )
        self._export_btn.pack(side="right", pady=24, padx=(0, 8))

        # Stats summary row
        self._stats_frame = ctk.CTkFrame(self, fg_color="#050505")
        self._stats_frame.pack(fill="x", padx=0, pady=0)

        # Scrollable game cards area
        self._scroll = ctk.CTkScrollableFrame(
            self, fg_color=BG, scrollbar_button_color=BORDER,
            scrollbar_button_hover_color=ACCENT
        )
        self._scroll.pack(fill="both", expand=True, padx=24, pady=(16, 80))

        # FAB (+ button) bottom right
        self._fab = ctk.CTkButton(
            self,
            text="+",
            font=ctk.CTkFont(size=28, weight="bold"),
            fg_color=ACCENT, hover_color=ACCENT_HOVER,
            text_color=TEXT_PRIMARY,
            width=64, height=64, corner_radius=32,
            command=self._open_new_game_dialog
        )
        self._fab.place(relx=1.0, rely=1.0, anchor="se", x=-28, y=-28)

    def _refresh(self):
        """Reload and redraw all content (called on language change too)."""
        # Update language button text
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
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color=ACCENT
            ).pack()
            ctk.CTkLabel(
                chip, text=label,
                font=ctk.CTkFont(size=11),
                text_color=TEXT_MUTED
            ).pack()

        # Separator
        sep = ctk.CTkFrame(self._stats_frame, fg_color=BORDER, height=1)
        sep.pack(fill="x", side="bottom")

    def _draw_cards(self):
        for w in self._scroll.winfo_children():
            w.destroy()

        sessions = self.__db.get_all_sessions()

        if not sessions:
            ctk.CTkLabel(
                self._scroll,
                text=self.__lang("main_screen", "no_games"),
                font=ctk.CTkFont(size=16),
                text_color=TEXT_MUTED
            ).pack(expand=True, pady=80)
            return

        # Grid layout: 3 columns
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
        self._refresh()

    def _play_session(self, session: dict):
        """Continue playing a manual game session."""
        from models.game import ManualGame
        game = ManualGame(
            game_id=session["id"],
            name=session["name"],
            door_count=session["door_count"]
        )
        # Restore existing stats
        game._total_rounds = session["total_games"]
        game._wins = session["wins"]
        self.__app.show_game_screen(game, session["id"])

    def _delete_session(self, session: dict):
        msg = self.__lang("confirm_delete", "message", name=session["name"])
        if messagebox.askyesno(
            self.__lang("confirm_delete", "title"),
            msg,
            parent=self
        ):
            self.__db.delete_session(session["id"])
            self._refresh()

    def _export_session(self, session_id: int):
        try:
            path = self.__db.export_to_csv(session_id=session_id)
            messagebox.showinfo(
                "Export",
                self.__lang("export_success", path=path),
                parent=self
            )
        except Exception as e:
            messagebox.showerror(self.__lang("error"), str(e), parent=self)

    def _export_all(self):
        try:
            path = self.__db.export_to_csv()
            messagebox.showinfo(
                "Export",
                self.__lang("export_success", path=path),
                parent=self
            )
        except Exception as e:
            messagebox.showerror(self.__lang("error"), str(e), parent=self)

    def _toggle_language(self):
        self.__lang.switch()
