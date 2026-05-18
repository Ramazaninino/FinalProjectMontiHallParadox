import customtkinter as ctk
from models.game import BaseGame
from utils.logo import get_logo

ACCENT       = "#EB1D49"
ACCENT_HOVER = "#C91540"


class DoorButton(ctk.CTkFrame):
    """
    Visual card for a single door/card — matches Figma card design.
    Shows door NUMBER prominently; state label and indicator on top.
    Demonstrates: OOP, Encapsulation, CustomTkinter widgets
    """

    def __init__(self, parent, door, lang, theme, on_click=None, num_font_size=30):
        t = theme
        super().__init__(
            parent,
            fg_color=t.DOOR_BG,
            corner_radius=14,
            border_width=0,
        )
        self.__door         = door
        self.__lang         = lang
        self._t             = theme
        self.__on_click     = on_click
        self.__num_font_size = num_font_size
        self._render()

    def __str__(self):
        return f"DoorButton(door={self.__door})"

    def _render(self):
        for w in self.winfo_children():
            w.destroy()

        door = self.__door
        l    = self.__lang
        t    = self._t

        # ── Opened cards ───────────────────────────────────────────────────
        if door.is_open:
            if door.has_prize:
                self.configure(fg_color=t.SUCCESS, border_width=0, corner_radius=14)
                icon       = l("game_screen", "door_open_prize")   # 🏆
                icon_color = "#FFFFFF"
                sub        = l("game_screen", "door_prize")
                sub_color  = "#FFFFFF"
            else:
                self.configure(fg_color=t.CHIP_BG, border_width=1,
                               border_color=t.BORDER, corner_radius=14)
                icon       = l("game_screen", "door_open_goat")    # 🐐
                icon_color = t.TEXT_MUTED
                sub = (l("game_screen", "door_original_pick")
                       if door.was_original_pick
                       else l("game_screen", "door_goat"))
                sub_color  = t.TEXT_MUTED

            ctk.CTkLabel(
                self, text=icon,
                font=ctk.CTkFont(size=30),
                text_color=icon_color,
            ).place(relx=0.5, rely=0.38, anchor="center")

            ctk.CTkLabel(
                self, text=sub,
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=sub_color,
            ).place(relx=0.5, rely=0.74, anchor="center")

            self.configure(cursor="")
            return

        # ── Selected card (original first pick) — RED fill ────────────────
        if door.is_selected:
            self.configure(
                fg_color=ACCENT,
                border_width=0,
                corner_radius=14,
            )
            # Number in white
            ctk.CTkLabel(
                self, text=str(door.number),
                font=ctk.CTkFont(size=self.__num_font_size, weight="bold"),
                text_color="#FFFFFF",
            ).place(relx=0.5, rely=0.42, anchor="center")

            # Small white dot top-right
            dot = ctk.CTkFrame(
                self, width=10, height=10,
                corner_radius=5, fg_color="#FFFFFF", border_width=0,
            )
            dot.place(relx=1.0, rely=0.0, anchor="ne", x=-8, y=8)
            self.configure(cursor="")
            return

        # ── Closed, unselected — default state ─────────────────────────────
        self.configure(fg_color=t.DOOR_BG, border_color=t.DOOR_BORDER,
                       border_width=1, corner_radius=14)

        # Number (large, centered ~40% from top — matches Figma y≈90/225)
        ctk.CTkLabel(
            self, text=str(door.number),
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=t.DOOR_NUM,
        ).place(relx=0.5, rely=0.42, anchor="center")

        # Short decorative divider line at bottom
        line = ctk.CTkFrame(self, fg_color=t.DOOR_BORDER, height=2, corner_radius=1)
        line.place(relx=0.5, rely=0.80, anchor="center", relwidth=0.35)

        clickable = self.__on_click is not None
        if clickable:
            self._bind_click(door.number)
        else:
            self.configure(cursor="")

    def _bind_click(self, door_number: int):
        handler = lambda e, n=door_number: self.__on_click(n)
        self.configure(cursor="hand2")
        self.bind("<Button-1>", handler)
        for w in self.winfo_children():
            w.bind("<Button-1>", handler)
            for sw in w.winfo_children():
                sw.bind("<Button-1>", handler)

    def set_clickable(self, on_click):
        self.__on_click = on_click
        self._render()

    def refresh(self):
        self._render()


class GameScreen(ctk.CTkFrame):
    """
    Game screen — matches Figma layout exactly:
      Header 80px | Left panel 280px | Card grid | Bottom hint bar
    Demonstrates: OOP, Inheritance, Polymorphism, CustomTkinter layout
    """

    def __init__(self, parent, app, game: BaseGame, session_id: int):
        self._t = app.theme
        super().__init__(parent, fg_color=self._t.BG)
        self.__app         = app
        self.__db          = app.db
        self.__lang        = app.lang
        self.__game        = game
        self.__session_id  = session_id
        self.__door_buttons: list[DoorButton] = []
        self.__last_result: bool | None = None
        self._build()
        self._render_phase()

    def __str__(self):
        return f"GameScreen(game={self.__game})"

    # ── Build skeleton ─────────────────────────────────────────────────────

    def _build(self):
        t = self._t
        l = self.__lang

        # ════════════════════════════════════════════════════════════
        # HEADER  (80px — matches Figma frame height ~80)
        # ════════════════════════════════════════════════════════════
        header = ctk.CTkFrame(self, fg_color=t.BG, height=72)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Logo — SVG asset, theme-aware
        logo_img = get_logo(is_dark=self._t.is_dark, size=(36, 39))
        ctk.CTkLabel(
            header, image=logo_img, text="",
            fg_color="transparent",
        ).pack(side="left", padx=(20, 0), pady=16)

        # Back button — pill shape (h=36, r=18)
        ctk.CTkButton(
            header,
            text=l("game_screen", "back"),
            font=ctk.CTkFont(size=12),
            fg_color=t.CHIP_BG, hover_color=t.BORDER_DEEP,
            text_color=t.TEXT_SECONDARY,
            height=36, corner_radius=18, width=100,
            command=self._go_back,
        ).pack(side="left", padx=(12, 0), pady=22)

        # Title — centered in remaining header space
        ctk.CTkLabel(
            header,
            text=l("game_screen", "header_title"),
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color=ACCENT,
        ).pack(side="left", expand=True)

        # ════════════════════════════════════════════════════════════
        # MAIN  =  [spacer 20px] [left panel 280px] [card area]
        # ════════════════════════════════════════════════════════════
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True)

        # Left margin spacer (~matches Figma's 97px canvas offset, scaled)
        ctk.CTkFrame(main, fg_color="transparent", width=20).pack(side="left", fill="y")

        # ── Left panel (280px fixed) ──────────────────────────────────────
        left_outer = ctk.CTkFrame(main, fg_color="transparent", width=280)
        left_outer.pack(side="left", fill="y")
        left_outer.pack_propagate(False)

        self._left_scroll = ctk.CTkScrollableFrame(
            left_outer, fg_color="transparent",
            scrollbar_button_color=t.BORDER_DEEP,
            scrollbar_button_hover_color=ACCENT,
            width=268,
        )
        self._left_scroll.pack(fill="both", expand=True, pady=(16, 16))

        # ── Card play area (right, expands) ──────────────────────────────
        right_wrap = ctk.CTkFrame(main, fg_color="transparent")
        right_wrap.pack(side="left", fill="both", expand=True,
                        padx=(20, 20), pady=(16, 0))

        self._right_area = ctk.CTkFrame(right_wrap, fg_color="transparent")
        self._right_area.pack(fill="both", expand=True)

        # ── Bottom hint bar ───────────────────────────────────────────
        self._hint_bar = ctk.CTkFrame(self, fg_color=t.BG_DEEP, height=36)
        self._hint_bar.pack(fill="x", side="bottom")
        self._hint_bar.pack_propagate(False)
        self._hint_lbl = ctk.CTkLabel(
            self._hint_bar, text="",
            font=ctk.CTkFont(size=11),
            text_color=t.TEXT_MUTED,
        )
        self._hint_lbl.pack(expand=True)

    # ── Helpers ────────────────────────────────────────────────────────────

    def _get_phase_label(self) -> str:
        l = self.__lang
        phase = self.__game.phase
        if phase == "select":
            return l("game_screen", "phase_select_label")
        if phase == "switch_or_keep":
            return l("game_screen", "phase_switch_label")
        return l("game_screen", "phase_result_label")

    def _info_row(self, parent, label: str, value: str):
        """Simple label | value row used inside info card."""
        t = self._t
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(
            row, text=label,
            font=ctk.CTkFont(size=12), text_color=t.TEXT_SECONDARY, anchor="w",
        ).pack(side="left")
        ctk.CTkLabel(
            row, text=value,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=t.TEXT_PRIMARY, anchor="e",
        ).pack(side="right")

    # ── Left panel build ───────────────────────────────────────────────────

    def _build_left_panel(self):
        t = self._t
        l = self.__lang
        g = self.__game

        for w in self._left_scroll.winfo_children():
            w.destroy()

        # ════════════════════════════════════════
        # GAME INFO CARD
        # ════════════════════════════════════════
        info_card = ctk.CTkFrame(
            self._left_scroll,
            fg_color=t.BG_CARD,
            corner_radius=14,
            border_color=t.BORDER, border_width=1,
        )
        info_card.pack(fill="x", padx=4, pady=(4, 0))

        ctk.CTkLabel(
            info_card,
            text=l("game_screen", "game_info"),
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color=t.TEXT_MUTED, anchor="w",
        ).pack(fill="x", padx=16, pady=(12, 6))

        ctk.CTkFrame(info_card, fg_color=t.BORDER, height=1).pack(fill="x", padx=16)

        # Total Cards row
        self._info_row(info_card, l("game_screen", "total_cards"), str(g.door_count))

        # Mode row with badge
        is_auto   = g.get_mode() == "auto"
        mode_text = l("game_screen", "mode_auto_badge" if is_auto else "mode_manual_badge")
        mode_row  = ctk.CTkFrame(info_card, fg_color="transparent")
        mode_row.pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(
            mode_row, text=l("game_screen", "type_label"),
            font=ctk.CTkFont(size=11), text_color=t.TEXT_SECONDARY, anchor="w",
        ).pack(side="left")
        badge_bg   = "#2A1200" if t.is_dark else "#FFF3E0"
        badge_text = "#FF9800" if t.is_dark else "#B45309"
        mode_badge = ctk.CTkFrame(mode_row, fg_color=badge_bg, corner_radius=6)
        mode_badge.pack(side="right")
        ctk.CTkLabel(
            mode_badge, text=mode_text,
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=badge_text,
        ).pack(padx=8, pady=3)

        # Step row — phase as a colored chip
        step_row = ctk.CTkFrame(info_card, fg_color="transparent")
        step_row.pack(fill="x", padx=16, pady=(4, 12))
        ctk.CTkLabel(
            step_row, text=l("game_screen", "step_label"),
            font=ctk.CTkFont(size=11), text_color=t.TEXT_SECONDARY, anchor="w",
        ).pack(side="left")
        if t.is_dark:
            phase_color      = {"select": "#1E3A5F", "switch_or_keep": "#1A2E00", "result": "#2A0020"}
            phase_text_color = {"select": "#60A5FA", "switch_or_keep": "#86EFAC", "result": ACCENT}
        else:
            phase_color      = {"select": "#EBF5FF", "switch_or_keep": "#F0FFF4", "result": "#FFF0F3"}
            phase_text_color = {"select": "#1E4A8F", "switch_or_keep": "#166534", "result": ACCENT}
        ph = self.__game.phase
        step_chip = ctk.CTkFrame(
            step_row,
            fg_color=phase_color.get(ph, t.CHIP_BG),
            corner_radius=6,
        )
        step_chip.pack(side="right")
        ctk.CTkLabel(
            step_chip, text=self._get_phase_label(),
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=phase_text_color.get(ph, t.TEXT_PRIMARY),
        ).pack(padx=8, pady=3)

        # ════════════════════════════════════════
        # PRO TIP CARD
        # ════════════════════════════════════════
        tip_card = ctk.CTkFrame(
            self._left_scroll,
            fg_color=t.HINT_BG,
            corner_radius=14,
            border_color=ACCENT, border_width=1,
        )
        tip_card.pack(fill="x", padx=4, pady=(10, 0))

        tip_hdr = ctk.CTkFrame(tip_card, fg_color="transparent")
        tip_hdr.pack(fill="x", padx=14, pady=(10, 4))

        dot = ctk.CTkFrame(tip_hdr, fg_color=ACCENT, width=8, height=8, corner_radius=4)
        dot.pack(side="left", pady=2)
        dot.pack_propagate(False)

        ctk.CTkLabel(
            tip_hdr,
            text=f"  {l('game_screen', 'pro_tip_title').upper()}",
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color=ACCENT, anchor="w",
        ).pack(side="left")

        ctk.CTkLabel(
            tip_card,
            text=l("game_screen", "pro_tip_text"),
            font=ctk.CTkFont(size=11),
            text_color=t.TEXT_SECONDARY,
            wraplength=228, justify="left", anchor="w",
        ).pack(fill="x", padx=14, pady=(0, 12))

        # ════════════════════════════════════════
        # DECISION or RESULT card (phase-dependent)
        # ════════════════════════════════════════
        if self.__game.phase == "switch_or_keep":
            self._build_decision_card()
        elif self.__game.phase == "result":
            self._build_result_card()

    def _build_decision_card(self):
        """Final Decision card — Figma: Background+Border 284×361 with Switch+Keep buttons."""
        t = self._t
        l = self.__lang

        card = ctk.CTkFrame(
            self._left_scroll,
            fg_color=t.BG_CARD if t.is_dark else t.BG_DEEP,
            corner_radius=14,
            border_color=t.BORDER, border_width=1,
        )
        card.pack(fill="x", padx=4, pady=(12, 0))

        # Title  ("Акыркы чечим" / "Final Decision")
        ctk.CTkLabel(
            card,
            text=l("game_screen", "decision_title"),
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=t.TEXT_PRIMARY, anchor="w",
        ).pack(fill="x", padx=22, pady=(20, 6))

        # Question text
        ctk.CTkLabel(
            card,
            text=l("game_screen", "decision_question"),
            font=ctk.CTkFont(size=11),
            text_color=t.TEXT_SECONDARY,
            wraplength=220, justify="left", anchor="w",
        ).pack(fill="x", padx=22, pady=(0, 14))

        ctk.CTkFrame(card, fg_color=t.BORDER_DEEP, height=1).pack(fill="x")

        btn_area = ctk.CTkFrame(card, fg_color="transparent")
        btn_area.pack(fill="x", padx=18, pady=16)

        # SWITCH button  (Figma: 218×60, red fill)
        ctk.CTkButton(
            btn_area,
            text=l("game_screen", "switch"),
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=ACCENT, hover_color=ACCENT_HOVER,
            text_color="#FFFFFF",
            height=56, corner_radius=12,
            command=self._on_switch_auto,
        ).pack(fill="x", pady=(0, 10))

        # KEEP button  (Figma: 218×60, secondary style)
        ctk.CTkButton(
            btn_area,
            text=l("game_screen", "keep"),
            font=ctk.CTkFont(size=14),
            fg_color=t.CHIP_BG, hover_color=t.BORDER_DEEP,
            text_color=t.TEXT_PRIMARY,
            height=56, corner_radius=12,
            command=self._on_keep,
        ).pack(fill="x")

    def _build_result_card(self):
        """Result card with win/loss title + Play Again + Finish buttons."""
        t    = self._t
        l    = self.__lang
        won  = self.__last_result
        color = t.SUCCESS if won else ACCENT
        title = l("game_screen", "won_title") if won else l("game_screen", "lost_title")
        switched_text = (l("game_screen", "switched_yes") if self.__game.last_switched
                         else l("game_screen", "switched_no"))

        card = ctk.CTkFrame(
            self._left_scroll,
            fg_color=t.BG_DEEP,
            corner_radius=14,
            border_color=color, border_width=2,
        )
        card.pack(fill="x", padx=4, pady=(12, 0))

        ctk.CTkLabel(
            card, text=title,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=color,
        ).pack(pady=(18, 4))
        ctk.CTkLabel(
            card, text=switched_text,
            font=ctk.CTkFont(size=11),
            text_color=t.TEXT_MUTED,
        ).pack(pady=(0, 12))

        ctk.CTkFrame(card, fg_color=t.BORDER_DEEP, height=1).pack(fill="x")

        btn_area = ctk.CTkFrame(card, fg_color="transparent")
        btn_area.pack(fill="x", padx=18, pady=16)

        ctk.CTkButton(
            btn_area,
            text=l("game_screen", "new_round"),
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=ACCENT, hover_color=ACCENT_HOVER,
            text_color="#FFFFFF",
            height=52, corner_radius=12,
            command=self._new_round,
        ).pack(fill="x", pady=(0, 10))

        ctk.CTkButton(
            btn_area,
            text=l("game_screen", "finish"),
            font=ctk.CTkFont(size=13),
            fg_color=t.CHIP_BG, hover_color=t.BORDER_DEEP,
            text_color=t.TEXT_SECONDARY,
            height=52, corner_radius=12,
            command=self._go_back,
        ).pack(fill="x")

    # ── Card grid render ───────────────────────────────────────────────────

    def _render_doors(self):
        t = self._t
        l = self.__lang
        for w in self._right_area.winfo_children():
            w.destroy()
        self.__door_buttons.clear()

        doors = self.__game.doors
        phase = self.__game.phase
        n     = len(doors)

        # ── Grid structure (fits in minsize window 1280×650) ──────────────
        # available_h = 650-80(hdr)-32(pady) = 538px
        # n ≤  9 → 3×3: 3×(158+16)=522px ✓
        # n ≤ 11 → 4×3: 3×(142+16)=474px ✓
        # n ≤ 15 → 5×3: 3×(124+16)=420px ✓
        # n ≤ 20 → 5×4: 4×(112+16)=512px ✓
        if n <= 9:
            cols, card_w, card_h = 3, 120, 158
        elif n <= 11:
            cols, card_w, card_h = 4, 104, 142
        elif n <= 15:
            cols, card_w, card_h = 5,  92, 124
        else:
            cols, card_w, card_h = 5,  86, 112

        # For exactly 3 doors: offset to middle row so cards appear centered
        row_offset = 1 if n == 3 else 0

        # ── Wrapper: pack(expand=True) centers without clipping ────────────
        wrapper = ctk.CTkFrame(self._right_area, fg_color="transparent")
        wrapper.pack(expand=True)   # centers both H and V, no fill/stretch

        # Silent spacer rows for n==3 (keeps the 3-row visual height)
        if n == 3:
            for ph_row in (0, 2):
                for ph_col in range(cols):
                    ph = ctk.CTkFrame(wrapper, fg_color="transparent",
                                      width=card_w, height=card_h)
                    ph.grid(row=ph_row, column=ph_col, padx=8, pady=8)
                    ph.grid_propagate(False)

        # Font size scales with card width: large cards→28, medium→24, small→20
        num_font = 28 if card_w >= 115 else (24 if card_w >= 90 else 20)

        # ── Door buttons ───────────────────────────────────────────────────
        for i, door in enumerate(doors):
            row_idx = row_offset + i // cols
            col     = i % cols

            if phase == "select":
                on_click = self._on_door_select if not door.is_open else None
            elif phase == "switch_or_keep":
                on_click = (self._on_door_switch
                            if not door.is_open and not door.is_selected else None)
            else:
                on_click = None

            btn = DoorButton(wrapper, door, self.__lang, t,
                             on_click=on_click, num_font_size=num_font)
            btn.configure(width=card_w, height=card_h)
            btn.grid(row=row_idx, column=col, padx=8, pady=8)
            self.__door_buttons.append(btn)


    def _render_phase(self):
        self._build_left_panel()
        self._render_doors()
        self._update_hint()

    def _update_hint(self):
        l = self.__lang
        phase = self.__game.phase
        if phase == "select":
            text = l("game_screen", "phase_select")
        elif phase == "switch_or_keep":
            text = f"⚡  {l('game_screen', 'phase_switch')}  ·  {l('game_screen', 'phase_switch_hint')}"
        else:
            text = l("game_screen", "hint_make_decision") if self.__last_result is None else ""
        self._hint_lbl.configure(text=text)

    # ── Callbacks ──────────────────────────────────────────────────────────

    def _on_door_select(self, door_number: int):
        self.__game.select_door(door_number)
        self._render_phase()

    def _on_door_switch(self, door_number: int):
        result = self.__game.switch_door(door_number)
        self.__last_result = result
        self._save_round(switched=True, won=result)
        self._render_phase()

    def _on_switch_auto(self):
        """Auto-switch to first available (unopened, unselected) door."""
        for door in self.__game.doors:
            if not door.is_open and not door.is_selected:
                result = self.__game.switch_door(door.number)
                self.__last_result = result
                self._save_round(switched=True, won=result)
                self._render_phase()
                return

    def _on_keep(self):
        result = self.__game.keep_door()
        self.__last_result = result
        self._save_round(switched=False, won=result)
        self._render_phase()

    def _save_round(self, switched: bool, won: bool):
        self.__db.update_session_stats(
            self.__session_id, self.__game.total_rounds, self.__game.wins,
        )
        self.__db.add_round(
            self.__session_id, self.__game.total_rounds,
            switched=switched, won=won,
        )

    def _new_round(self):
        self.__last_result = None
        self.__game.new_round()
        self._render_phase()

    def _go_back(self):
        self.__db.update_session_stats(
            self.__session_id, self.__game.total_rounds, self.__game.wins,
        )
        self.__app.show_main_screen()
