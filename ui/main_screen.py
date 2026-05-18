import customtkinter as ctk
from tkinter import messagebox, filedialog
from utils.logo import get_logo

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
            height=300,
        )
        self.pack_propagate(False)
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
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=t.TEXT_PRIMARY,
            anchor="w",
        ).pack(fill="x", padx=16, pady=(14, 2))

        # Sub-line: wins / total
        total = int(s.get("total_games") or 0)
        wins  = int(s.get("wins") or 0)
        ctk.CTkLabel(
            self,
            text=f"{wins} {l('card', 'wins')} / {total} {l('card', 'games')}",
            font=ctk.CTkFont(size=11),
            text_color=t.TEXT_MUTED,
            anchor="w",
        ).pack(fill="x", padx=16, pady=(0, 8))

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
            text_color="#1A1A1A", anchor="e",
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
            text_color="#1A1A1A", anchor="e",
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
            text_color="#1A1A1A", anchor="e",
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

        export_btn = ctk.CTkButton(
            btn_row,
            text=l("card", "export"),
            font=ctk.CTkFont(size=12),
            fg_color=t.CHIP_BG, hover_color=t.BORDER,
            text_color=t.TEXT_SECONDARY,
            height=32, corner_radius=8,
        )
        export_btn.configure(command=lambda b=export_btn: self.__on_export(s["id"], b))
        export_btn.pack(side="left", padx=(0, 4))

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

        # ════════════════════════════════════════════════════════════
        # HEADER — same bg as main, red title, outline pill buttons
        # ════════════════════════════════════════════════════════════
        header = ctk.CTkFrame(self, fg_color=t.BG, height=72)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Logo — SVG asset, theme-aware
        logo_img = get_logo(is_dark=self._t.is_dark, size=(36, 39))
        ctk.CTkLabel(
            header, image=logo_img, text="",
            fg_color="transparent",
        ).pack(side="left", padx=(24, 0), pady=16)

        # Title — centered, RED
        ctk.CTkLabel(
            header,
            text=self.__lang("main_screen", "title"),
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            text_color=ACCENT,
        ).pack(side="left", expand=True)

        # ── Toolbar: outline pill buttons ─────────────────────────
        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right", padx=20, fill="y")

        btn_cfg = dict(
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            border_width=1,
            border_color=t.BORDER_DEEP,
            hover_color=t.CHIP_BG,
            text_color=t.TEXT_PRIMARY,
            height=34,
            corner_radius=17,
        )

        self._lang_btn = ctk.CTkButton(
            right, width=54,
            text=self.__lang("main_screen", "language"),
            command=self._toggle_language,
            **btn_cfg,
        )
        self._lang_btn.pack(side="right", pady=19)

        self._theme_btn = ctk.CTkButton(
            right, width=90,
            text=self._theme_btn_label(),
            command=self._toggle_theme,
            **btn_cfg,
        )
        self._theme_btn.pack(side="right", pady=19, padx=(0, 8))

        self._export_btn = ctk.CTkButton(
            right, width=84,
            text=self.__lang("main_screen", "export_all"),
            **btn_cfg,
        )
        self._export_btn.configure(command=self._export_all)
        self._export_btn.pack(side="right", pady=19, padx=(0, 8))

        # Thin separator under header
        ctk.CTkFrame(self, fg_color=t.BORDER, height=1).pack(fill="x")

        # Stats row
        self._stats_frame = ctk.CTkFrame(self, fg_color=t.BG)
        self._stats_frame.pack(fill="x")

        # Section header — "История игр" / "Game History"
        self._section_header = ctk.CTkFrame(self, fg_color="transparent")
        self._section_header.pack(fill="x", padx=28, pady=(16, 4))

        self._section_title_lbl = ctk.CTkLabel(
            self._section_header,
            text=self.__lang("main_screen", "subtitle"),
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=t.TEXT_PRIMARY,
            anchor="w",
        )
        self._section_title_lbl.pack(side="left")

        # Scrollable cards
        self._scroll = ctk.CTkScrollableFrame(
            self, fg_color=t.BG,
            scrollbar_button_color=t.BORDER,
            scrollbar_button_hover_color=ACCENT,
        )
        self._scroll.pack(fill="both", expand=True, padx=24, pady=(0, 80))

        # FAB — 56×56 red circle
        self._fab = ctk.CTkButton(
            self,
            text="+",
            font=ctk.CTkFont(size=24, weight="bold"),
            fg_color=ACCENT, hover_color=ACCENT_HOVER,
            text_color="#FFFFFF",
            width=56, height=56, corner_radius=28,
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
        from utils.logo import clear_cache
        clear_cache()
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
        if hasattr(self, "_section_title_lbl"):
            self._section_title_lbl.configure(text=self.__lang("main_screen", "subtitle"))
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
            fill="x", side="bottom", pady=(4, 0)
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

        total_rows = (len(sessions) + cols - 1) // cols
        for r in range(total_rows):
            self._scroll.rowconfigure(r, uniform="card_row")

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

    def _ask_save_path(self, default_name: str, ext: str) -> str | None:
        ext_map = {
            ".xlsx": [("Excel файл", "*.xlsx")],
            ".csv":  [("CSV файл", "*.csv")],
            ".json": [("JSON файл", "*.json")],
        }
        path = filedialog.asksaveasfilename(
            defaultextension=ext,
            filetypes=ext_map.get(ext, [("Все файлы", "*.*")]),
            initialfile=default_name,
            title=self.__lang("main_screen", "export_all"),
        )
        return path if path else None

    def _show_export_menu(self, anchor_widget, on_format, below: bool = False):
        """Show a small popup with CSV / Excel / JSON buttons near anchor_widget."""
        t = self._t
        l = self.__lang

        popup = ctk.CTkToplevel(self)
        popup.overrideredirect(True)
        popup.configure(fg_color=t.BG_CARD)
        popup.attributes("-topmost", True)

        anchor_widget.update_idletasks()
        x = anchor_widget.winfo_rootx()
        h = 110
        y = (anchor_widget.winfo_rooty() + anchor_widget.winfo_height() + 4
             if below else anchor_widget.winfo_rooty() - h - 4)
        popup.geometry(f"130x{h}+{x}+{y}")

        frame = ctk.CTkFrame(popup, fg_color=t.BG_CARD,
                             border_color=t.BORDER, border_width=1, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=1, pady=1)

        def pick(fmt):
            popup.destroy()
            on_format(fmt)

        for fmt_key, fmt in [("export_csv", "csv"), ("export_excel", "excel"), ("export_json", "json")]:
            ctk.CTkButton(
                frame,
                text=l("card", fmt_key),
                font=ctk.CTkFont(size=12),
                fg_color="transparent", hover_color=t.CHIP_BG,
                text_color=t.TEXT_PRIMARY, anchor="w",
                height=30, corner_radius=6,
                command=lambda f=fmt: pick(f),
            ).pack(fill="x", padx=6, pady=2)

        popup.bind("<FocusOut>", lambda e: popup.destroy())
        popup.focus_set()

    def _do_export(self, session_id: int | None, fmt: str):
        import datetime
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        base = f"session_{session_id}_{ts}" if session_id else f"all_sessions_{ts}"
        ext_map = {"csv": ".csv", "excel": ".xlsx", "json": ".json"}
        ext = ext_map[fmt]
        save_path = self._ask_save_path(base + ext, ext)
        if not save_path:
            return
        try:
            if fmt == "excel":
                self.__db.export_to_excel(session_id=session_id, filepath=save_path)
            elif fmt == "csv":
                self.__db.export_to_csv(session_id=session_id, filepath=save_path)
            elif fmt == "json":
                self.__db.export_to_json(session_id=session_id, filepath=save_path)
            messagebox.showinfo("Export", self.__lang("export_success", path=save_path))
        except Exception as e:
            messagebox.showerror(self.__lang("error"), str(e))

    def _export_session(self, session_id: int, anchor):
        self._show_export_menu(anchor, lambda fmt: self._do_export(session_id, fmt))

    def _export_all(self):
        self._show_export_menu(self._export_btn, lambda fmt: self._do_export(None, fmt),
                               below=True)

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
