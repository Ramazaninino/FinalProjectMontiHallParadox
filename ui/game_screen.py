import customtkinter as ctk
from models.game import BaseGame, ManualGame

BG = "#000000"
BG_PANEL = "#0A0A0A"
BG_CARD = "#0D1117"
BORDER = "#1E293B"
ACCENT = "#EB1D49"
ACCENT_HOVER = "#C91540"
TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "#94A3B8"
TEXT_MUTED = "#475569"
SUCCESS_COLOR = "#22C55E"
DOOR_CLOSED = "#111827"
DOOR_CLOSED_BORDER = "#1E293B"
DOOR_SELECTED_BORDER = ACCENT
DOOR_OPEN_GOAT = "#1A1A2E"
DOOR_OPEN_PRIZE = "#1A2E1A"
BAR_BG = "#1E293B"


class DoorButton(ctk.CTkFrame):
    """
    Visual representation of a single door as a clickable button.
    Demonstrates: OOP, Encapsulation, CustomTkinter widgets
    """

    def __init__(self, parent, door, lang, on_click=None):
        super().__init__(
            parent,
            fg_color=DOOR_CLOSED,
            border_color=DOOR_CLOSED_BORDER,
            border_width=2,
            corner_radius=12,
        )
        self.__door = door
        self.__lang = lang
        self.__on_click = on_click
        self.__btn: ctk.CTkButton | None = None
        self._render()

    def __str__(self):
        return f"DoorButton(door={self.__door})"

    def _render(self):
        for w in self.winfo_children():
            w.destroy()

        door = self.__door
        l = self.__lang

        if door.is_open:
            if door.has_prize:
                self.configure(fg_color=DOOR_OPEN_PRIZE, border_color=SUCCESS_COLOR)
                icon = l("game_screen", "door_open_prize")
                label = l("game_screen", "door_prize")
                text_color = SUCCESS_COLOR
            else:
                self.configure(fg_color=DOOR_OPEN_GOAT, border_color=BORDER)
                icon = l("game_screen", "door_open_goat")
                label = l("game_screen", "door_goat")
                text_color = TEXT_MUTED
        elif door.is_selected:
            self.configure(fg_color="#1A0008", border_color=ACCENT)
            icon = l("game_screen", "door_closed_icon")
            label = f"{l('game_screen', 'door_closed')} {door.number}"
            text_color = ACCENT
        else:
            self.configure(fg_color=DOOR_CLOSED, border_color=DOOR_CLOSED_BORDER)
            icon = l("game_screen", "door_closed_icon")
            label = f"{l('game_screen', 'door_closed')} {door.number}"
            text_color = TEXT_SECONDARY

        # Door icon
        ctk.CTkLabel(
            self, text=icon,
            font=ctk.CTkFont(size=28),
            text_color=text_color
        ).pack(pady=(10, 2))

        # Door number/label
        ctk.CTkLabel(
            self, text=label,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=text_color
        ).pack(pady=(0, 8))

        # Clickable overlay button (only for closed, non-open doors)
        if not door.is_open and self.__on_click:
            btn = ctk.CTkButton(
                self, text="",
                fg_color="transparent",
                hover_color="#FFFFFF11",
                command=lambda: self.__on_click(door.number),
                corner_radius=10,
                height=60
            )
            btn.place(relx=0, rely=0, relwidth=1, relheight=1)

    def refresh(self):
        self._render()


class GameScreen(ctk.CTkFrame):
    """
    Game play screen showing doors and controls.
    Demonstrates: OOP, Inheritance, Polymorphism, CustomTkinter layout
    """

    def __init__(self, parent, app, game: BaseGame, session_id: int):
        super().__init__(parent, fg_color=BG)
        self.__app = app
        self.__db = app.db
        self.__lang = app.lang
        self.__game = game
        self.__session_id = session_id
        self.__door_buttons: list[DoorButton] = []
        self.__last_result: bool | None = None
        self._build()
        self._render_phase()

    def __str__(self):
        return f"GameScreen(game={self.__game})"

    def _build(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="#050505", height=64)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkButton(
            header,
            text=self.__lang("game_screen", "back"),
            font=ctk.CTkFont(size=13),
            fg_color="transparent", hover_color=BORDER,
            text_color=TEXT_SECONDARY,
            anchor="w", width=90, height=36, corner_radius=8,
            command=self._go_back
        ).pack(side="left", padx=16, pady=14)

        ctk.CTkLabel(
            header,
            text="THE MONTY HALL PARADOX",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=ACCENT
        ).pack(side="left", padx=8)

        # Main layout: left panel + right door area
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=0, pady=0)

        # Left panel
        self._left_panel = ctk.CTkFrame(
            main, fg_color=BG_PANEL,
            border_color=BORDER, border_width=1,
            corner_radius=0, width=280
        )
        self._left_panel.pack(side="left", fill="y", padx=0, pady=0)
        self._left_panel.pack_propagate(False)

        # Right door area
        self._right_area = ctk.CTkScrollableFrame(
            main, fg_color=BG,
            scrollbar_button_color=BORDER,
            scrollbar_button_hover_color=ACCENT
        )
        self._right_area.pack(side="left", fill="both", expand=True, padx=0, pady=0)

        self._build_left_panel()

    def _build_left_panel(self):
        l = self.__lang
        g = self.__game

        for w in self._left_panel.winfo_children():
            w.destroy()

        # Game params section
        params = ctk.CTkFrame(self._left_panel, fg_color=BG_CARD, corner_radius=12,
                              border_color=BORDER, border_width=1)
        params.pack(fill="x", padx=16, pady=(20, 0))

        ctk.CTkLabel(params, text=l("game_screen", "params_title"),
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=TEXT_SECONDARY, anchor="w"
                     ).pack(fill="x", padx=14, pady=(12, 6))

        sep = ctk.CTkFrame(params, fg_color=BORDER, height=1)
        sep.pack(fill="x")

        stat_rows = [
            (l("game_screen", "doors"), str(g.door_count)),
            (l("game_screen", "mode"), g.get_mode_label()),
            (l("game_screen", "rounds"), str(g.total_rounds)),
            (l("game_screen", "wins"), str(g.wins)),
            (l("game_screen", "win_rate"), f"{g.win_rate:.1f}%"),
        ]
        for label, value in stat_rows:
            row = ctk.CTkFrame(params, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=5)
            ctk.CTkLabel(row, text=label, font=ctk.CTkFont(size=12),
                         text_color=TEXT_MUTED, anchor="w").pack(side="left")
            self._val_label = ctk.CTkLabel(row, text=value,
                                           font=ctk.CTkFont(size=12, weight="bold"),
                                           text_color=TEXT_PRIMARY, anchor="e")
            self._val_label.pack(side="right")

        # Win rate bar
        bar_frame = ctk.CTkFrame(params, fg_color="transparent")
        bar_frame.pack(fill="x", padx=14, pady=(4, 12))
        bg = ctk.CTkFrame(bar_frame, fg_color=BAR_BG, height=6, corner_radius=3)
        bg.pack(fill="x")
        bg.pack_propagate(False)
        ratio = min(g.win_rate / 100, 1.0)
        if ratio > 0:
            ctk.CTkFrame(bg, fg_color=ACCENT, height=6, corner_radius=3).place(
                relx=0, rely=0, relwidth=ratio, relheight=1
            )

        # Phase / action area
        self._action_frame = ctk.CTkFrame(self._left_panel, fg_color="transparent")
        self._action_frame.pack(fill="x", padx=16, pady=(16, 0))

        self._render_action_panel()

    def _render_action_panel(self):
        l = self.__lang
        for w in self._action_frame.winfo_children():
            w.destroy()

        phase = self.__game.phase

        if phase == "select":
            ctk.CTkLabel(
                self._action_frame,
                text=l("game_screen", "phase_select"),
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=TEXT_PRIMARY,
                wraplength=220, justify="center"
            ).pack(pady=16)

        elif phase == "switch_or_keep":
            ctk.CTkLabel(
                self._action_frame,
                text=l("game_screen", "phase_switch"),
                font=ctk.CTkFont(size=13),
                text_color=TEXT_SECONDARY,
                wraplength=220, justify="center"
            ).pack(pady=(12, 16))

            ctk.CTkButton(
                self._action_frame,
                text=l("game_screen", "switch"),
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color=ACCENT, hover_color=ACCENT_HOVER,
                text_color=TEXT_PRIMARY,
                height=44, corner_radius=10,
                command=self._on_switch
            ).pack(fill="x", pady=(0, 8))

            ctk.CTkButton(
                self._action_frame,
                text=l("game_screen", "keep"),
                font=ctk.CTkFont(size=13),
                fg_color=BORDER, hover_color="#2D3748",
                text_color=TEXT_PRIMARY,
                height=44, corner_radius=10,
                command=self._on_keep
            ).pack(fill="x")

        elif phase == "result":
            won = self.__last_result
            color = SUCCESS_COLOR if won else ACCENT
            title = l("game_screen", "won_title") if won else l("game_screen", "lost_title")
            switched_text = (
                l("game_screen", "switched_yes")
                if self.__game.last_switched
                else l("game_screen", "switched_no")
            )

            result_card = ctk.CTkFrame(
                self._action_frame,
                fg_color=BG_CARD, corner_radius=12,
                border_color=color, border_width=2
            )
            result_card.pack(fill="x", pady=8)

            ctk.CTkLabel(
                result_card, text=title,
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=color
            ).pack(pady=(14, 2))

            ctk.CTkLabel(
                result_card, text=switched_text,
                font=ctk.CTkFont(size=11),
                text_color=TEXT_MUTED
            ).pack(pady=(0, 14))

            ctk.CTkButton(
                self._action_frame,
                text=l("game_screen", "new_round"),
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color=ACCENT, hover_color=ACCENT_HOVER,
                text_color=TEXT_PRIMARY,
                height=44, corner_radius=10,
                command=self._new_round
            ).pack(fill="x", pady=(8, 0))

            ctk.CTkButton(
                self._action_frame,
                text=l("game_screen", "finish"),
                font=ctk.CTkFont(size=13),
                fg_color=BORDER, hover_color="#2D3748",
                text_color=TEXT_SECONDARY,
                height=44, corner_radius=10,
                command=self._go_back
            ).pack(fill="x", pady=(8, 0))

    def _render_doors(self):
        for w in self._right_area.winfo_children():
            w.destroy()
        self.__door_buttons.clear()

        doors = self.__game.doors
        n = len(doors)

        # Determine columns based on door count
        if n <= 6:
            cols = 3
        elif n <= 9:
            cols = 3
        elif n <= 12:
            cols = 4
        else:
            cols = 5

        door_size = 110

        # Phase: allow click only during "select"
        on_click = self._on_door_click if self.__game.phase == "select" else None

        for i, door in enumerate(doors):
            row, col = divmod(i, cols)
            btn = DoorButton(self._right_area, door, self.__lang, on_click=on_click)
            btn.grid(row=row, column=col, padx=12, pady=12, sticky="nsew",
                     ipadx=8, ipady=8)
            btn.configure(width=door_size, height=door_size + 20)
            self.__door_buttons.append(btn)

        for c in range(cols):
            self._right_area.columnconfigure(c, weight=1)

    def _render_phase(self):
        """Full redraw of left panel + doors."""
        self._build_left_panel()
        self._render_doors()

    def _on_door_click(self, door_number: int):
        self.__game.select_door(door_number)
        self._render_phase()

    def _on_switch(self):
        result = self.__game.switch_door()
        self.__last_result = result
        self._save_round(switched=True, won=result)
        self._render_phase()

    def _on_keep(self):
        result = self.__game.keep_door()
        self.__last_result = result
        self._save_round(switched=False, won=result)
        self._render_phase()

    def _save_round(self, switched: bool, won: bool):
        """Persist round result to database."""
        self.__db.update_session_stats(
            self.__session_id,
            self.__game.total_rounds,
            self.__game.wins
        )
        self.__db.add_round(
            self.__session_id,
            self.__game.total_rounds,
            switched=switched,
            won=won
        )

    def _new_round(self):
        self.__last_result = None
        self.__game.new_round()
        self._render_phase()

    def _go_back(self):
        # Save current stats before leaving
        self.__db.update_session_stats(
            self.__session_id,
            self.__game.total_rounds,
            self.__game.wins
        )
        self.__app.show_main_screen()
