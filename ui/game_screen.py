import tkinter as tk
import customtkinter as ctk
from models.game import BaseGame

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
DOOR_DEFAULT_BG = "#FFFFFF"
DOOR_DEFAULT_NUM = "#1E293B"
DOOR_SELECTED_BORDER = "#EB1D49"
DOOR_OPEN_GOAT_BG = "#F1F5F9"
DOOR_OPEN_GOAT_NUM = "#94A3B8"
DOOR_OPEN_PRIZE_BG = "#DCFCE7"
DOOR_OPEN_PRIZE_NUM = "#22C55E"
BAR_BG = "#1E293B"


class DoorButton(ctk.CTkFrame):
    """
    Visual card for a single door. Clicking handled via tkinter bindings
    (more reliable than overlaid transparent button on white background).
    Demonstrates: OOP, Encapsulation, CustomTkinter widgets
    """

    def __init__(self, parent, door, on_click=None):
        super().__init__(
            parent,
            fg_color=DOOR_DEFAULT_BG,
            corner_radius=14,
            border_width=0,
        )
        self.__door = door
        self.__on_click = on_click
        self._render()

    def __str__(self):
        return f"DoorButton(door={self.__door})"

    def _render(self):
        for w in self.winfo_children():
            w.destroy()

        door = self.__door
        clickable = (not door.is_open) and (not door.is_selected) and (self.__on_click is not None)

        if door.is_open:
            if door.has_prize:
                self.configure(fg_color=DOOR_OPEN_PRIZE_BG,
                               border_color=SUCCESS_COLOR, border_width=2)
                num_color = DOOR_OPEN_PRIZE_NUM
                sub = "Prize!"
                sub_color = SUCCESS_COLOR
            else:
                self.configure(fg_color=DOOR_OPEN_GOAT_BG,
                               border_color="#CBD5E1", border_width=1)
                num_color = DOOR_OPEN_GOAT_NUM
                sub = "Empty"
                sub_color = DOOR_OPEN_GOAT_NUM
        elif door.is_selected:
            # White card, red border, selected indicator dot at top-right
            self.configure(fg_color=DOOR_DEFAULT_BG,
                           border_color=DOOR_SELECTED_BORDER, border_width=2)
            num_color = DOOR_DEFAULT_NUM
            sub = ""
            sub_color = TEXT_MUTED

            # Small red dot indicator at top-right (like Figma design)
            dot = ctk.CTkFrame(
                self, width=10, height=10, corner_radius=5,
                fg_color=DOOR_SELECTED_BORDER, border_width=0,
            )
            dot.place(relx=1.0, rely=0.0, anchor="ne", x=-8, y=8)
        else:
            self.configure(fg_color=DOOR_DEFAULT_BG, border_width=0)
            num_color = DOOR_DEFAULT_NUM
            sub = ""
            sub_color = TEXT_MUTED

        # Number label — large, vertically centered
        num_label = ctk.CTkLabel(
            self,
            text=str(door.number),
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=num_color,
        )
        num_label.pack(expand=True, pady=(0, 4) if sub else 0)

        # Sub-label (Empty / Prize!)
        if sub:
            sub_label = ctk.CTkLabel(
                self,
                text=sub,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=sub_color,
            )
            sub_label.pack(pady=(0, 12))

        # Cursor and click bindings — bind to frame + every child
        if clickable:
            self._bind_click(door.number)
        else:
            self.configure(cursor="")

    def _bind_click(self, door_number: int):
        """Bind <Button-1> to frame and all children for reliable hit detection."""
        handler = lambda e, n=door_number: self.__on_click(n)
        self.configure(cursor="hand2")
        self.bind("<Button-1>", handler)
        for widget in self.winfo_children():
            widget.bind("<Button-1>", handler)
            for subwidget in widget.winfo_children():
                subwidget.bind("<Button-1>", handler)

    def set_clickable(self, on_click):
        """Update the on_click callback and re-render."""
        self.__on_click = on_click
        self._render()

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

        logo_canvas = tk.Canvas(
            header, width=54, height=48,
            bg="#050505", highlightthickness=0,
        )
        logo_canvas.pack(side="left", padx=(20, 4), pady=8)
        logo_canvas.create_text(4, 12, text="T  G",
                                font=("Arial", 9, "bold"),
                                fill=TEXT_PRIMARY, anchor="w")
        logo_canvas.create_text(4, 30, text="L  K",
                                font=("Arial", 9, "bold"),
                                fill=TEXT_PRIMARY, anchor="w")
        logo_canvas.create_oval(22, 14, 44, 36,
                                outline=TEXT_PRIMARY, width=1.5)

        ctk.CTkButton(
            header,
            text=self.__lang("game_screen", "back"),
            font=ctk.CTkFont(size=13),
            fg_color="transparent", hover_color=BORDER,
            text_color=TEXT_SECONDARY,
            anchor="w", width=90, height=36, corner_radius=8,
            command=self._go_back,
        ).pack(side="left", padx=(4, 8), pady=14)

        ctk.CTkLabel(
            header,
            text="THE MONTY HALL PARADOX",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=ACCENT,
        ).pack(side="left", padx=4)

        # Main layout
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True)

        # Left panel — scrollable
        left_outer = ctk.CTkFrame(
            main, fg_color=BG_PANEL,
            border_color=BORDER, border_width=1,
            corner_radius=0, width=296,
        )
        left_outer.pack(side="left", fill="y")
        left_outer.pack_propagate(False)

        self._left_scroll = ctk.CTkScrollableFrame(
            left_outer, fg_color="transparent",
            scrollbar_button_color=BORDER,
            scrollbar_button_hover_color=ACCENT,
            width=280,
        )
        self._left_scroll.pack(fill="both", expand=True)

        # Right door area
        self._right_area = ctk.CTkScrollableFrame(
            main, fg_color=BG,
            scrollbar_button_color=BORDER,
            scrollbar_button_hover_color=ACCENT,
        )
        self._right_area.pack(side="left", fill="both", expand=True)

    def _build_left_panel(self):
        l = self.__lang
        g = self.__game

        for w in self._left_scroll.winfo_children():
            w.destroy()

        # GAME INFO
        ctk.CTkLabel(
            self._left_scroll,
            text="GAME INFO",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=TEXT_MUTED,
            anchor="w",
        ).pack(fill="x", padx=20, pady=(20, 8))

        info_card = ctk.CTkFrame(
            self._left_scroll, fg_color=BG_CARD,
            corner_radius=12, border_color=BORDER, border_width=1,
        )
        info_card.pack(fill="x", padx=16)

        stat_rows = [
            (l("game_screen", "doors"), str(g.door_count)),
            (l("game_screen", "mode"), g.get_mode_label()),
            (l("game_screen", "rounds"), str(g.total_rounds)),
            (l("game_screen", "wins"), str(g.wins)),
            (l("game_screen", "win_rate"), f"{g.win_rate:.1f}%"),
        ]
        for i, (label, value) in enumerate(stat_rows):
            row = ctk.CTkFrame(info_card, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=5)
            ctk.CTkLabel(row, text=label,
                         font=ctk.CTkFont(size=12), text_color=TEXT_MUTED,
                         anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=value,
                         font=ctk.CTkFont(size=12, weight="bold"),
                         text_color=TEXT_PRIMARY, anchor="e").pack(side="right")
            if i < len(stat_rows) - 1:
                ctk.CTkFrame(info_card, fg_color=BORDER, height=1).pack(fill="x", padx=14)

        # Win rate bar
        bar_frame = ctk.CTkFrame(info_card, fg_color="transparent")
        bar_frame.pack(fill="x", padx=14, pady=(4, 14))
        bg_bar = ctk.CTkFrame(bar_frame, fg_color=BAR_BG, height=6, corner_radius=3)
        bg_bar.pack(fill="x")
        bg_bar.pack_propagate(False)
        ratio = min(g.win_rate / 100, 1.0)
        if ratio > 0:
            ctk.CTkFrame(bg_bar, fg_color=ACCENT, height=6, corner_radius=3).place(
                relx=0, rely=0, relwidth=ratio, relheight=1
            )

        # PRO TIP
        tip_card = ctk.CTkFrame(
            self._left_scroll, fg_color="#0A0A0A",
            corner_radius=12, border_color=BORDER, border_width=1,
        )
        tip_card.pack(fill="x", padx=16, pady=(14, 0))

        tip_hdr = ctk.CTkFrame(tip_card, fg_color="transparent")
        tip_hdr.pack(fill="x", padx=14, pady=(12, 4))
        ctk.CTkLabel(tip_hdr, text="★", font=ctk.CTkFont(size=10),
                     text_color=ACCENT).pack(side="left")
        ctk.CTkLabel(tip_hdr, text="  pro tip",
                     font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=ACCENT, anchor="w").pack(side="left")

        ctk.CTkLabel(
            tip_card,
            text="In the Monty Hall paradox, switching your choice always doubles your probability of winning!",
            font=ctk.CTkFont(size=11),
            text_color=TEXT_SECONDARY,
            wraplength=230, justify="left", anchor="w",
        ).pack(fill="x", padx=14, pady=(0, 12))

        # Action panel
        self._action_frame = ctk.CTkFrame(self._left_scroll, fg_color="transparent")
        self._action_frame.pack(fill="x", padx=16, pady=(14, 20))

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
                wraplength=240, justify="center",
            ).pack(pady=16)

        elif phase == "switch_or_keep":
            # Notification card — Monty revealed a door
            hint_card = ctk.CTkFrame(
                self._action_frame, fg_color="#100008",
                corner_radius=10, border_color=ACCENT, border_width=1,
            )
            hint_card.pack(fill="x", pady=(0, 12))
            ctk.CTkLabel(
                hint_card,
                text=l("game_screen", "phase_switch"),
                font=ctk.CTkFont(size=12),
                text_color=TEXT_SECONDARY,
                wraplength=220, justify="center",
            ).pack(padx=12, pady=12)

            # Instruction to click another door
            ctk.CTkLabel(
                self._action_frame,
                text=l("game_screen", "phase_switch_hint"),
                font=ctk.CTkFont(size=11),
                text_color=TEXT_MUTED,
                wraplength=230, justify="center",
            ).pack(pady=(0, 10))

            # Only "Keep" button — switching = clicking another door card
            ctk.CTkButton(
                self._action_frame,
                text=l("game_screen", "keep"),
                font=ctk.CTkFont(size=13),
                fg_color=BORDER, hover_color="#2D3748",
                text_color=TEXT_PRIMARY,
                height=44, corner_radius=10,
                command=self._on_keep,
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
                border_color=color, border_width=2,
            )
            result_card.pack(fill="x", pady=8)

            ctk.CTkLabel(
                result_card, text=title,
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=color,
            ).pack(pady=(14, 2))

            ctk.CTkLabel(
                result_card, text=switched_text,
                font=ctk.CTkFont(size=11),
                text_color=TEXT_MUTED,
            ).pack(pady=(0, 14))

            ctk.CTkButton(
                self._action_frame,
                text=l("game_screen", "new_round"),
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color=ACCENT, hover_color=ACCENT_HOVER,
                text_color=TEXT_PRIMARY,
                height=44, corner_radius=10,
                command=self._new_round,
            ).pack(fill="x", pady=(8, 0))

            ctk.CTkButton(
                self._action_frame,
                text=l("game_screen", "finish"),
                font=ctk.CTkFont(size=13),
                fg_color=BORDER, hover_color="#2D3748",
                text_color=TEXT_SECONDARY,
                height=44, corner_radius=10,
                command=self._go_back,
            ).pack(fill="x", pady=(8, 0))

    def _render_doors(self):
        for w in self._right_area.winfo_children():
            w.destroy()
        self.__door_buttons.clear()

        doors = self.__game.doors
        phase = self.__game.phase
        n = len(doors)

        if n <= 6:
            cols = 3
        elif n <= 12:
            cols = 4
        else:
            cols = 5

        for i, door in enumerate(doors):
            row_idx, col = divmod(i, cols)

            # Determine click callback per door based on phase
            if phase == "select":
                # All closed doors are clickable to select
                on_click = self._on_door_select if not door.is_open else None
            elif phase == "switch_or_keep":
                # Closed non-selected doors are clickable to switch to
                if not door.is_open and not door.is_selected:
                    on_click = self._on_door_switch
                else:
                    on_click = None
            else:
                on_click = None

            btn = DoorButton(self._right_area, door, on_click=on_click)
            btn.grid(row=row_idx, column=col, padx=14, pady=14,
                     sticky="nsew", ipadx=10, ipady=20)
            btn.configure(width=130, height=175)
            self.__door_buttons.append(btn)

        for c in range(cols):
            self._right_area.columnconfigure(c, weight=1)

    def _render_phase(self):
        self._build_left_panel()
        self._render_doors()

    # --- Callbacks ---

    def _on_door_select(self, door_number: int):
        """Player selects a door (phase: select → switch_or_keep)."""
        self.__game.select_door(door_number)
        self._render_phase()

    def _on_door_switch(self, door_number: int):
        """Player clicks another door to switch to it (phase: switch_or_keep → result)."""
        result = self.__game.switch_door(door_number)
        self.__last_result = result
        self._save_round(switched=True, won=result)
        self._render_phase()

    def _on_keep(self):
        """Player keeps their current door."""
        result = self.__game.keep_door()
        self.__last_result = result
        self._save_round(switched=False, won=result)
        self._render_phase()

    def _save_round(self, switched: bool, won: bool):
        self.__db.update_session_stats(
            self.__session_id,
            self.__game.total_rounds,
            self.__game.wins,
        )
        self.__db.add_round(
            self.__session_id,
            self.__game.total_rounds,
            switched=switched,
            won=won,
        )

    def _new_round(self):
        self.__last_result = None
        self.__game.new_round()
        self._render_phase()

    def _go_back(self):
        self.__db.update_session_stats(
            self.__session_id,
            self.__game.total_rounds,
            self.__game.wins,
        )
        self.__app.show_main_screen()
