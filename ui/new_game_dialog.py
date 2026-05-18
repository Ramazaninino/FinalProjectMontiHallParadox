import customtkinter as ctk
from tkinter import messagebox

ACCENT       = "#EB1D49"
ACCENT_HOVER = "#C91540"


class NewGameDialog(ctk.CTkToplevel):
    """
    Dialog window for creating a new game session.
    Demonstrates: OOP, CustomTkinter (CTkToplevel, CTkEntry, CTkLabel, CTkButton)
    Week 14: MultiLanguage — JSON
    """

    def __init__(self, parent, app):
        super().__init__(parent)
        self.__app = app
        self.__db  = app.db
        self.__lang = app.lang
        self._t    = app.theme
        self.__mode_var = ctk.StringVar(value="auto")

        self.title(self.__lang("new_game", "title"))
        self.geometry("400x670")
        self.resizable(False, False)
        # Outer window matches main bg
        self.configure(fg_color=self._t.BG)
        self.grab_set()

        self.update_idletasks()
        px = parent.winfo_rootx() + (parent.winfo_width()  - 400) // 2
        py = parent.winfo_rooty() + (parent.winfo_height() - 670) // 2
        self.geometry(f"+{px}+{py}")

        self._build()

    def __str__(self):
        return "NewGameDialog()"

    # ── Build ─────────────────────────────────────────────────────────────

    def _build(self):
        t  = self._t
        l  = self.__lang

        # White floating card (always white in light, dark card in dark)
        card = ctk.CTkFrame(
            self,
            fg_color=t.BG_CARD,
            corner_radius=20,
            border_width=1,
            border_color=t.BORDER,
        )
        card.pack(fill="both", expand=True, padx=20, pady=20)

        # ── Red dot icon at top ──────────────────────────────────────
        dot = ctk.CTkFrame(
            card,
            fg_color=ACCENT,
            width=36, height=36,
            corner_radius=18,
        )
        dot.pack(pady=(20, 0))
        dot.pack_propagate(False)
        ctk.CTkLabel(
            dot, text="▶",
            font=ctk.CTkFont(size=13),
            text_color="#FFFFFF",
            fg_color="transparent",
        ).place(relx=0.55, rely=0.5, anchor="center")

        # ── Title + subtitle ─────────────────────────────────────────
        ctk.CTkLabel(
            card,
            text=l("new_game", "title"),
            font=ctk.CTkFont(family="Arial", size=20, weight="bold"),
            text_color=t.TEXT_PRIMARY,
        ).pack(pady=(10, 0))

        ctk.CTkLabel(
            card,
            text=l("new_game", "subtitle"),
            font=ctk.CTkFont(size=12),
            text_color=t.TEXT_MUTED,
        ).pack(pady=(2, 0))

        # ── Content area ──────────────────────────────────────────────
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=28, pady=(12, 0))

        # Game name
        ctk.CTkLabel(
            content, text=l("new_game", "name_label"),
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=t.TEXT_SECONDARY, anchor="w",
        ).pack(fill="x", pady=(0, 6))

        self._name_entry = ctk.CTkEntry(
            content,
            placeholder_text=l("new_game", "name_placeholder"),
            font=ctk.CTkFont(size=13),
            fg_color=t.FIELD_BG,
            border_color=t.BORDER,
            border_width=1,
            text_color=t.TEXT_PRIMARY,
            placeholder_text_color=t.TEXT_MUTED,
            height=40, corner_radius=10,
        )
        self._name_entry.pack(fill="x", pady=(0, 10))

        # Quantity of Cards label + input
        ctk.CTkLabel(
            content, text=l("new_game", "doors_label"),
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=t.TEXT_SECONDARY, anchor="w",
        ).pack(fill="x", pady=(0, 4))

        self._doors_entry = ctk.CTkEntry(
            content,
            placeholder_text="3",
            font=ctk.CTkFont(size=13),
            fg_color=t.FIELD_BG,
            border_color=t.BORDER,
            border_width=1,
            text_color=t.TEXT_PRIMARY,
            placeholder_text_color=t.TEXT_MUTED,
            height=40, corner_radius=10,
        )
        self._doors_entry.pack(fill="x", pady=(0, 2))
        self._doors_entry.insert(0, "3")

        ctk.CTkLabel(
            content,
            text=l("new_game", "error_doors"),
            font=ctk.CTkFont(size=10),
            text_color=t.TEXT_MUTED,
            anchor="w",
        ).pack(fill="x", pady=(0, 10))

        # Game Mode toggle
        ctk.CTkLabel(
            content, text=l("new_game", "mode_label"),
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=t.TEXT_SECONDARY, anchor="w",
        ).pack(fill="x", pady=(0, 6))

        toggle_bg = ctk.CTkFrame(
            content,
            fg_color=t.FIELD_BG,
            corner_radius=10,
            border_width=1,
            border_color=t.BORDER,
        )
        toggle_bg.pack(fill="x", pady=(0, 4))
        toggle_bg.columnconfigure(0, weight=1)
        toggle_bg.columnconfigure(1, weight=1)

        self._btn_auto = ctk.CTkButton(
            toggle_bg,
            text=f"⚡  {l('new_game', 'mode_auto')}",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=ACCENT, hover_color=ACCENT_HOVER,
            text_color="#FFFFFF",
            height=40, corner_radius=8,
            command=lambda: self._set_mode("auto"),
        )
        self._btn_auto.grid(row=0, column=0, padx=4, pady=4, sticky="ew")

        self._btn_manual = ctk.CTkButton(
            toggle_bg,
            text=f"✋  {l('new_game', 'mode_manual')}",
            font=ctk.CTkFont(size=13),
            fg_color="transparent", hover_color=t.CHIP_BG,
            text_color=t.TEXT_SECONDARY,
            height=40, corner_radius=8,
            command=lambda: self._set_mode("manual"),
        )
        self._btn_manual.grid(row=0, column=1, padx=4, pady=4, sticky="ew")

        # Auto games count (hidden when manual)
        self._auto_frame = ctk.CTkFrame(content, fg_color="transparent")
        ctk.CTkLabel(
            self._auto_frame,
            text=l("new_game", "auto_games_label"),
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=t.TEXT_SECONDARY, anchor="w",
        ).pack(fill="x", pady=(12, 6))
        self._auto_entry = ctk.CTkEntry(
            self._auto_frame,
            placeholder_text=l("new_game", "auto_games_placeholder"),
            font=ctk.CTkFont(size=13),
            fg_color=t.FIELD_BG,
            border_color=t.BORDER,
            border_width=1,
            text_color=t.TEXT_PRIMARY,
            placeholder_text_color=t.TEXT_MUTED,
            height=40, corner_radius=10,
        )
        self._auto_entry.pack(fill="x")
        self._auto_entry.insert(0, "1000")
        self._auto_frame.pack(fill="x")

        # ── Action buttons ─────────────────────────────────────────────
        actions = ctk.CTkFrame(card, fg_color="transparent")
        actions.pack(fill="x", padx=28, pady=(12, 20))

        ctk.CTkButton(
            actions,
            text=f"{l('new_game', 'create')}  →",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=ACCENT, hover_color=ACCENT_HOVER,
            text_color="#FFFFFF",
            height=46, corner_radius=12,
            command=self._create_game,
        ).pack(fill="x", pady=(0, 8))

        ctk.CTkButton(
            actions,
            text=l("new_game", "cancel"),
            font=ctk.CTkFont(size=13),
            fg_color="transparent", hover_color=t.CHIP_BG,
            text_color=ACCENT,
            height=32, corner_radius=8,
            command=self.destroy,
        ).pack(fill="x")

    # ── Helpers ───────────────────────────────────────────────────────────

    def _set_mode(self, mode: str):
        t = self._t
        self.__mode_var.set(mode)
        if mode == "auto":
            self._btn_auto.configure(fg_color=ACCENT, hover_color=ACCENT_HOVER,
                                     text_color="#FFFFFF", font=ctk.CTkFont(size=13, weight="bold"))
            self._btn_manual.configure(fg_color="transparent", hover_color=t.CHIP_BG,
                                       text_color=t.TEXT_SECONDARY, font=ctk.CTkFont(size=13))
            self._auto_frame.pack(fill="x")
        else:
            self._btn_manual.configure(fg_color=ACCENT, hover_color=ACCENT_HOVER,
                                       text_color="#FFFFFF", font=ctk.CTkFont(size=13, weight="bold"))
            self._btn_auto.configure(fg_color="transparent", hover_color=t.CHIP_BG,
                                     text_color=t.TEXT_SECONDARY, font=ctk.CTkFont(size=13))
            self._auto_frame.pack_forget()

    def _create_game(self):
        l = self.__lang
        name = self._name_entry.get().strip()
        if not name:
            messagebox.showerror(l("error"), l("new_game", "error_name"))
            return

        try:
            doors = int(self._doors_entry.get().strip())
            if doors < 3 or doors > 20:
                raise ValueError
        except ValueError:
            messagebox.showerror(l("error"), l("new_game", "error_doors"))
            return

        mode = self.__mode_var.get()

        if mode == "manual":
            self._start_manual_game(name, doors)
        else:
            try:
                num_games = int(self._auto_entry.get().strip())
                if num_games < 1 or num_games > 100_000:
                    raise ValueError
            except ValueError:
                messagebox.showerror(l("error"), l("new_game", "error_auto_games"))
                return
            self._start_auto_game(name, doors, num_games)

    def _start_manual_game(self, name: str, doors: int):
        from models.game import ManualGame
        session_id = self.__db.create_session(name, doors, "manual")
        game = ManualGame(game_id=session_id, name=name, door_count=doors)
        self.pending_game = (game, session_id)
        self.pending_auto_results = None
        self.destroy()

    def _start_auto_game(self, name: str, doors: int, num_games: int):
        from models.game import AutoGame
        session_id = self.__db.create_session(name, doors, "auto", num_games)
        game = AutoGame(game_id=session_id, name=name, door_count=doors, num_games=num_games)
        results = game.simulate()
        self.__db.update_session_stats(session_id, results["total"], results["wins"])
        self.pending_game = None
        self.pending_auto_results = (results, num_games, doors)
        self.destroy()
