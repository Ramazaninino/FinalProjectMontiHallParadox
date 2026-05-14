import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, filedialog


def _draw_logo(canvas, bg_color: str, fg_color: str):
    """Draw the T/G/L/K logo with a circle in the center on a tk.Canvas (48x48)."""
    canvas.configure(bg=bg_color)
    font = ("Arial", 11, "bold")
    canvas.create_text(10, 12, text="T", font=font, fill=fg_color, anchor="center")
    canvas.create_text(38, 12, text="G", font=font, fill=fg_color, anchor="center")
    canvas.create_text(10, 36, text="L", font=font, fill=fg_color, anchor="center")
    canvas.create_text(38, 36, text="K", font=font, fill=fg_color, anchor="center")
    canvas.create_oval(12, 6, 36, 42, outline=fg_color, width=1.5)

# Accent never changes between themes
ACCENT       = "#EB1D49"
ACCENT_HOVER = "#C91540"


class GameCard(ctk.CTkFrame):
    """
    Card widget displaying a single game session's statistics.
    Demonstrates: OOP, Encapsulation, CustomTkinter widgets
    """

    def __init__(self, parent, session: dict, lang, theme, on_play, on_delete, on_export):
        t = theme
        super().__init__(
            parent,
            fg_color=t.BG_CARD,
            border_color=t.BORDER,
            border_width=1,
            corner_radius=16,
        )
        self.__session = session
        self.__lang = lang
        self._t = theme
        self.__on_play = on_play
        self.__on_delete = on_delete
        self.__on_export = on_export
        self._build()

    def __str__(self):
        return f"GameCard(session_id={self.__session['id']}, name={self.__session['name']})"

    def _build(self):
        s = self.__session
        l = self.__lang
        t = self._t
        win_rate = float(s.get("win_rate") or 0)
        mode_label = l("card", "mode_manual") if s["mode"] == "manual" else l("card", "mode_auto")

        # Card name
        ctk.CTkLabel(
            self,
            text=s["name"],
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=t.TEXT_PRIMARY,
            anchor="w",
        ).pack(fill="x", padx=16, pady=(14, 8))

        # GAMES chip (full width)
        games_chip = ctk.CTkFrame(self, fg_color=t.CHIP_BG, corner_radius=10)
        games_chip.pack(fill="x", padx=16, pady=(0, 6))

        ctk.CTkLabel(
            games_chip, text=l("card", "chip_games"),
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color=t.TEXT_MUTED, anchor="w",
        ).pack(side="left", padx=(12, 4), pady=10)

        ctk.CTkLabel(
            games_chip, text=f"x{s['total_games']}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=t.TEXT_PRIMARY, anchor="e",
        ).pack(side="right", padx=(4, 12), pady=10)

        # CARDS + TYPE chips side by side
        chips_row = ctk.CTkFrame(self, fg_color="transparent")
        chips_row.pack(fill="x", padx=16, pady=(0, 10))
        chips_row.columnconfigure(0, weight=1)
        chips_row.columnconfigure(1, weight=1)

        doors_chip = ctk.CTkFrame(chips_row, fg_color=t.CHIP_BG, corner_radius=10)
        doors_chip.grid(row=0, column=0, sticky="ew", padx=(0, 4))
        ctk.CTkLabel(
            doors_chip, text=l("card", "chip_cards"),
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color=t.TEXT_MUTED, anchor="w",
        ).pack(side="left", padx=(10, 4), pady=10)
        ctk.CTkLabel(
            doors_chip, text=f"x{s['door_count']}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=t.TEXT_PRIMARY, anchor="e",
        ).pack(side="right", padx=(4, 10), pady=10)

        type_chip = ctk.CTkFrame(chips_row, fg_color=t.CHIP_BG, corner_radius=10)
        type_chip.grid(row=0, column=1, sticky="ew", padx=(4, 0))
        ctk.CTkLabel(
            type_chip, text=l("card", "chip_type"),
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color=t.TEXT_MUTED, anchor="w",
        ).pack(side="left", padx=(10, 4), pady=10)
        ctk.CTkLabel(
            type_chip, text=mode_label,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=t.TEXT_PRIMARY, anchor="e",
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
            text_color=t.TEXT_SECONDARY, anchor="e",
        ).pack(side="left", padx=(6, 0), pady=(6, 0))

        # Progress bar
        bar_bg = ctk.CTkFrame(self, fg_color=t.BAR_BG, height=4, corner_radius=2)
        bar_bg.pack(fill="x", padx=16, pady=(0, 12))
        bar_bg.pack_propagate(False)
        ratio = min(win_rate / 100, 1.0)
        if ratio > 0:
            ctk.CTkFrame(bar_bg, fg_color=ACCENT, height=4, corner_radius=2).place(
                relx=0, rely=0, relwidth=ratio, relheight=1
            )

        # Separator
        ctk.CTkFrame(self, fg_color=t.BORDER, height=1).pack(fill="x")

        # Action buttons
        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(fill="x", padx=12, pady=10)

        if s["mode"] == "manual":
            ctk.CTkButton(
                btn_row,
                text=l("card", "play"),
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color=ACCENT, hover_color=ACCENT_HOVER,
                text_color="#FFFFFF",
                height=32, corner_radius=8,
                command=lambda sid=s: self.__on_play(sid),
            ).pack(side="left", padx=(0, 4))

        ctk.CTkButton(
            btn_row,
            text=l("card", "export"),
            font=ctk.CTkFont(size=12),
            fg_color=t.CHIP_BG, hover_color=t.BORDER,
            text_color=t.TEXT_SECONDARY,
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
        self._t = app.theme
        super().__init__(parent, fg_color=self._t.BG)
        self.__app = app
        self.__db = app.db
        self.__lang = app.lang

        # Register observers — clear stale callbacks first
        self.__lang.clear_callbacks()
        self.__lang.on_change(self._refresh)

        self._t.clear_callbacks()
        self._t.on_change(self._on_theme_change)

        self._build()
        self._refresh()

    def __str__(self):
        return "MainScreen()"

    # ── Build ─────────────────────────────────────────────────────────────

    def _build(self):
        t = self._t

        # Header
        header = ctk.CTkFrame(self, fg_color=t.HEADER_BG, height=64)
        header.pack(fill="x")
        header.pack_propagate(False)

        logo_canvas = tk.Canvas(
            header, width=48, height=48,
            bg=t.HEADER_BG, highlightthickness=0,
        )
        logo_canvas.pack(side="left", padx=(20, 8), pady=8)
        _draw_logo(logo_canvas, t.HEADER_BG, "#FFFFFF")

        ctk.CTkLabel(
            header,
            text=self.__lang("main_screen", "title"),
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF",
        ).pack(side="left", padx=8)

        # Right controls
        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right", padx=20, fill="y")

        self._lang_btn = ctk.CTkButton(
            right,
            text=self.__lang("main_screen", "language"),
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=t.BORDER_DEEP, hover_color="#334155",
            text_color="#FFFFFF",
            width=48, height=32, corner_radius=8,
            command=self._toggle_language,
        )
        self._lang_btn.pack(side="right", pady=16)

        self._theme_btn = ctk.CTkButton(
            right,
            text=self._theme_btn_label(),
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=t.BORDER_DEEP, hover_color="#334155",
            text_color="#FFFFFF",
            width=90, height=32, corner_radius=8,
            command=self._toggle_theme,
        )
        self._theme_btn.pack(side="right", pady=16, padx=(0, 8))

        self._export_btn = ctk.CTkButton(
            right,
            text=self.__lang("main_screen", "export_all"),
            font=ctk.CTkFont(size=12),
            fg_color=t.BORDER_DEEP, hover_color="#334155",
            text_color="#FFFFFF",
            height=32, corner_radius=8,
            command=self._export_all,
        )
        self._export_btn.pack(side="right", pady=16, padx=(0, 8))

        # Global stats row
        self._stats_frame = ctk.CTkFrame(self, fg_color=t.HEADER_BG)
        self._stats_frame.pack(fill="x")

        # Scrollable cards
        self._scroll = ctk.CTkScrollableFrame(
            self, fg_color=t.BG,
            scrollbar_button_color=t.BORDER,
            scrollbar_button_hover_color=ACCENT,
        )
        self._scroll.pack(fill="both", expand=True, padx=24, pady=(16, 80))

        # FAB
        self._fab = ctk.CTkButton(
            self,
            text="+",
            font=ctk.CTkFont(size=28, weight="bold"),
            fg_color=ACCENT, hover_color=ACCENT_HOVER,
            text_color="#FFFFFF",
            width=64, height=64, corner_radius=32,
            command=self._open_new_game_dialog,
        )
        self._fab.place(relx=1.0, rely=1.0, anchor="se", x=-28, y=-28)

    # ── Theme helpers ─────────────────────────────────────────────────────

    def _theme_btn_label(self) -> str:
        key = "theme_to_light" if self._t.is_dark else "theme_to_dark"
        return self.__lang("main_screen", key)

    def _on_theme_change(self):
        """Rebuild the whole screen after theme switch (deferred to avoid widget-in-callback issues)."""
        self.after(0, self._do_rebuild)

    def _do_rebuild(self):
        self.configure(fg_color=self._t.BG)
        for w in self.winfo_children():
            w.destroy()
        self._build()
        self._refresh()

    # ── Refresh (language + theme button text) ────────────────────────────

    def _refresh(self):
        if hasattr(self, "_lang_btn"):
            self._lang_btn.configure(text=self.__lang("main_screen", "language"))
        if hasattr(self, "_export_btn"):
            self._export_btn.configure(text=self.__lang("main_screen", "export_all"))
        if hasattr(self, "_theme_btn"):
            self._theme_btn.configure(text=self._theme_btn_label())
        self._draw_stats()
        self._draw_cards()

    def _draw_stats(self):
        t = self._t
        for w in self._stats_frame.winfo_children():
            w.destroy()

        stats = self.__db.get_global_stats()
        l = self.__lang

        items = [
            (str(stats.get("total_sessions", 0)), l("main_screen", "total_sessions")),
            (str(stats.get("total_games", 0)),    l("main_screen", "total_games")),
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
                text_color=t.TEXT_MUTED,
            ).pack()

        ctk.CTkFrame(self._stats_frame, fg_color=t.BORDER, height=1).pack(
            fill="x", side="bottom"
        )

    def _draw_cards(self):
        t = self._t
        for w in self._scroll.winfo_children():
            w.destroy()

        sessions = self.__db.get_all_sessions()

        if not sessions:
            ctk.CTkLabel(
                self._scroll,
                text=self.__lang("main_screen", "no_games"),
                font=ctk.CTkFont(size=16),
                text_color=t.TEXT_MUTED,
            ).pack(expand=True, pady=80)
            return

        cols = 3
        for i, session in enumerate(sessions):
            row, col = divmod(i, cols)
            card = GameCard(
                self._scroll, session, self.__lang, self._t,
                on_play=self._play_session,
                on_delete=self._delete_session,
                on_export=self._export_session,
            )
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        for c in range(cols):
            self._scroll.columnconfigure(c, weight=1)

    # ── Navigation & actions ──────────────────────────────────────────────

    def _open_new_game_dialog(self):
        from ui.new_game_dialog import NewGameDialog
        dialog = NewGameDialog(self, self.__app)
        dialog.grab_set()
        self.wait_window(dialog)
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

    def _ask_save_path(self, default_name: str) -> str | None:
        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel файл", "*.xlsx"), ("Все файлы", "*.*")],
            initialfile=default_name,
            title=self.__lang("main_screen", "export_all"),
        )
        return path if path else None

    def _export_session(self, session_id: int):
        import datetime
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = self._ask_save_path(f"session_{session_id}_{ts}.xlsx")
        if not save_path:
            return
        try:
            self.__db.export_to_excel(session_id=session_id, filepath=save_path)
            messagebox.showinfo("Export", self.__lang("export_success", path=save_path))
        except Exception as e:
            messagebox.showerror(self.__lang("error"), str(e))

    def _export_all(self):
        import datetime
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = self._ask_save_path(f"all_sessions_{ts}.xlsx")
        if not save_path:
            return
        try:
            self.__db.export_to_excel(filepath=save_path)
            messagebox.showinfo("Export", self.__lang("export_success", path=save_path))
        except Exception as e:
            messagebox.showerror(self.__lang("error"), str(e))

    def _show_auto_results(self, results: dict, num_games: int, doors: int):
        t = self._t
        l = self.__lang
        dialog = ctk.CTkToplevel(self)
        dialog.title(l("auto_result", "title"))
        dialog.geometry("440x380")
        dialog.resizable(False, False)
        dialog.configure(fg_color=t.HEADER_BG)
        dialog.grab_set()

        dialog.update_idletasks()
        px = self.__app.winfo_x() + (self.__app.winfo_width() - 440) // 2
        py = self.__app.winfo_y() + (self.__app.winfo_height() - 380) // 2
        dialog.geometry(f"+{px}+{py}")

        ctk.CTkLabel(
            dialog, text=l("auto_result", "title"),
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=t.TEXT_PRIMARY,
        ).pack(pady=(28, 16))

        info = ctk.CTkFrame(dialog, fg_color=t.BG_DEEP,
                            corner_radius=14, border_color=t.BORDER_DEEP, border_width=1)
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
                         text_color=t.TEXT_SECONDARY, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=value, font=ctk.CTkFont(size=13, weight="bold"),
                         text_color=t.TEXT_PRIMARY, anchor="e").pack(side="right")

        bar_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        bar_frame.pack(fill="x", padx=32, pady=8)
        ctk.CTkLabel(bar_frame,
                     text=f"{l('auto_result', 'win_rate_label')} {results['win_rate']:.1f}%",
                     font=ctk.CTkFont(size=11), text_color=ACCENT).pack(anchor="w")
        bg = ctk.CTkFrame(bar_frame, fg_color=t.BORDER_DEEP, height=8, corner_radius=4)
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
            text_color=t.TEXT_SECONDARY,
            wraplength=380,
        ).pack(padx=32, pady=12)

        ctk.CTkButton(
            dialog,
            text=l("auto_result", "close"),
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=ACCENT, hover_color=ACCENT_HOVER,
            text_color="#FFFFFF",
            height=44, corner_radius=10,
            command=dialog.destroy,
        ).pack(padx=32, pady=(0, 24), fill="x")

    # ── Toggle handlers ───────────────────────────────────────────────────

    def _toggle_language(self):
        self.__lang.switch()

    def _toggle_theme(self):
        self._t.switch()
