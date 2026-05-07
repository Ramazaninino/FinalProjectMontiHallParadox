import customtkinter as ctk
from tkinter import messagebox

BG = "#050505"
BG_CARD = "#0D1117"
BORDER = "#1E293B"
ACCENT = "#EB1D49"
ACCENT_HOVER = "#C91540"
TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "#94A3B8"
TEXT_MUTED = "#475569"
FIELD_BG = "#111827"


class NewGameDialog(ctk.CTkToplevel):
    """
    Dialog window for creating a new game session.
    Demonstrates: OOP, CustomTkinter (CTkToplevel, CTkEntry, CTkLabel,
                  CTkButton, CTkRadioButton, CTkSlider)
    """

    def __init__(self, parent, app):
        super().__init__(parent)
        self.__app = app
        self.__db = app.db
        self.__lang = app.lang
        self.__mode_var = ctk.StringVar(value="manual")
        self.__doors_var = ctk.IntVar(value=3)

        self.title(self.__lang("new_game", "title"))
        self.geometry("480x580")
        self.resizable(False, False)
        self.configure(fg_color=BG)
        self.grab_set()

        # Center on parent
        self.update_idletasks()
        px = parent.winfo_rootx() + (parent.winfo_width() - 480) // 2
        py = parent.winfo_rooty() + (parent.winfo_height() - 580) // 2
        self.geometry(f"+{px}+{py}")

        self._build()

    def __str__(self):
        return "NewGameDialog()"

    def _build(self):
        l = self.__lang

        # Title
        ctk.CTkLabel(
            self,
            text=l("new_game", "title"),
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=TEXT_PRIMARY
        ).pack(pady=(28, 20))

        # Content frame
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=32)

        # Game name
        ctk.CTkLabel(
            content, text=l("new_game", "name_label"),
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_SECONDARY, anchor="w"
        ).pack(fill="x", pady=(0, 4))

        self._name_entry = ctk.CTkEntry(
            content,
            placeholder_text=l("new_game", "name_placeholder"),
            font=ctk.CTkFont(size=13),
            fg_color=FIELD_BG, border_color=BORDER,
            text_color=TEXT_PRIMARY,
            placeholder_text_color=TEXT_MUTED,
            height=42, corner_radius=10
        )
        self._name_entry.pack(fill="x", pady=(0, 16))

        # Door count slider
        ctk.CTkLabel(
            content, text=l("new_game", "doors_label"),
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_SECONDARY, anchor="w"
        ).pack(fill="x", pady=(0, 4))

        slider_row = ctk.CTkFrame(content, fg_color="transparent")
        slider_row.pack(fill="x", pady=(0, 16))

        self._door_label = ctk.CTkLabel(
            slider_row,
            text="3",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=ACCENT,
            width=40
        )
        self._door_label.pack(side="left", padx=(0, 12))

        self._slider = ctk.CTkSlider(
            slider_row,
            from_=3, to=20,
            number_of_steps=17,
            variable=self.__doors_var,
            button_color=ACCENT,
            button_hover_color=ACCENT_HOVER,
            progress_color=ACCENT,
            fg_color=BORDER,
            command=self._on_slider_change
        )
        self._slider.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            slider_row,
            text="20",
            font=ctk.CTkFont(size=12),
            text_color=TEXT_MUTED,
            width=30
        ).pack(side="left", padx=(8, 0))

        # Game mode
        ctk.CTkLabel(
            content, text=l("new_game", "mode_label"),
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_SECONDARY, anchor="w"
        ).pack(fill="x", pady=(0, 8))

        mode_frame = ctk.CTkFrame(content, fg_color=FIELD_BG, corner_radius=10, border_color=BORDER, border_width=1)
        mode_frame.pack(fill="x", pady=(0, 16))

        ctk.CTkRadioButton(
            mode_frame,
            text=l("new_game", "mode_manual"),
            variable=self.__mode_var,
            value="manual",
            font=ctk.CTkFont(size=13),
            text_color=TEXT_PRIMARY,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            command=self._on_mode_change
        ).pack(side="left", padx=20, pady=14)

        ctk.CTkRadioButton(
            mode_frame,
            text=l("new_game", "mode_auto"),
            variable=self.__mode_var,
            value="auto",
            font=ctk.CTkFont(size=13),
            text_color=TEXT_PRIMARY,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            command=self._on_mode_change
        ).pack(side="left", padx=20, pady=14)

        # Auto games count (hidden by default, inside content)
        self._auto_frame = ctk.CTkFrame(content, fg_color="transparent")

        ctk.CTkLabel(
            self._auto_frame,
            text=l("new_game", "auto_games_label"),
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_SECONDARY, anchor="w"
        ).pack(fill="x", pady=(0, 4))

        self._auto_entry = ctk.CTkEntry(
            self._auto_frame,
            placeholder_text=l("new_game", "auto_games_placeholder"),
            font=ctk.CTkFont(size=13),
            fg_color=FIELD_BG, border_color=BORDER,
            text_color=TEXT_PRIMARY,
            placeholder_text_color=TEXT_MUTED,
            height=42, corner_radius=10,
        )
        self._auto_entry.pack(fill="x")
        self._auto_entry.insert(0, "1000")
        # not packed yet — shown only in auto mode

        # Buttons row
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=32, pady=(12, 28))

        ctk.CTkButton(
            btn_frame,
            text=l("new_game", "cancel"),
            font=ctk.CTkFont(size=13),
            fg_color=BORDER, hover_color="#2D3748",
            text_color=TEXT_SECONDARY,
            height=44, corner_radius=10,
            command=self.destroy
        ).pack(side="left", expand=True, fill="x", padx=(0, 8))

        ctk.CTkButton(
            btn_frame,
            text=l("new_game", "create"),
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=ACCENT, hover_color=ACCENT_HOVER,
            text_color=TEXT_PRIMARY,
            height=44, corner_radius=10,
            command=self._create_game
        ).pack(side="right", expand=True, fill="x", padx=(8, 0))

    def _on_slider_change(self, value):
        doors = int(value)
        self.__doors_var.set(doors)
        self._door_label.configure(text=str(doors))

    def _on_mode_change(self):
        if self.__mode_var.get() == "auto":
            self._auto_frame.pack(fill="x", pady=(0, 4))
        else:
            self._auto_frame.pack_forget()

    def _create_game(self):
        l = self.__lang
        name = self._name_entry.get().strip()
        if not name:
            messagebox.showerror(l("error"), l("new_game", "error_name"))
            return

        doors = self.__doors_var.get()
        if doors < 3 or doors > 20:
            messagebox.showerror(l("error"), l("new_game", "error_doors"))
            return

        mode = self.__mode_var.get()
        num_games = 0

        if mode == "auto":
            try:
                num_games = int(self._auto_entry.get().strip())
                if num_games < 1 or num_games > 100_000:
                    raise ValueError
            except ValueError:
                messagebox.showerror(l("error"), l("new_game", "error_auto_games"))
                return

        if mode == "manual":
            self._start_manual_game(name, doors)
        else:
            self._start_auto_game(name, doors, num_games)

    def _start_manual_game(self, name: str, doors: int):
        from models.game import ManualGame
        session_id = self.__db.create_session(name, doors, "manual")
        game = ManualGame(game_id=session_id, name=name, door_count=doors)
        # Store result for caller (MainScreen) to pick up after wait_window()
        self.pending_game = (game, session_id)
        self.pending_auto_results = None
        self.destroy()

    def _start_auto_game(self, name: str, doors: int, num_games: int):
        from models.game import AutoGame
        session_id = self.__db.create_session(name, doors, "auto", num_games)
        game = AutoGame(game_id=session_id, name=name, door_count=doors, num_games=num_games)
        results = game.simulate()
        self.__db.update_session_stats(session_id, results["total"], results["wins"])
        # Store results for caller to show after wait_window()
        self.pending_game = None
        self.pending_auto_results = (results, num_games, doors)
        self.destroy()

