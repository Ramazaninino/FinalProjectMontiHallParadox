import tkinter as tk
import customtkinter as ctk
from ui.main_screen import _draw_logo

BG = "#000000"
ACCENT = "#EB1D49"
TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "#94A3B8"


class SplashScreen(ctk.CTkFrame):
    """
    Welcome / splash screen matching Figma design:
    - Black background
    - Huge red bold title centered
    - 'Start a game' underlined link below
    - Logo icon top-left (T G / L K letters with overlapping circle)
    """

    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG)
        self.__app = app
        self._build()

    def _build(self):
        # Top-left logo
        logo_canvas = tk.Canvas(
            self, width=48, height=48,
            bg=BG, highlightthickness=0,
        )
        logo_canvas.place(x=20, y=16)
        _draw_logo(logo_canvas, BG, TEXT_PRIMARY)

        # Center content
        center = ctk.CTkFrame(self, fg_color="transparent")
        center.place(relx=0.5, rely=0.45, anchor="center")

        # Big red title
        ctk.CTkLabel(
            center,
            text="The Monty Hall\nParadox",
            font=ctk.CTkFont(family="Arial", size=82, weight="bold"),
            text_color=ACCENT,
            justify="center",
        ).pack()

        # Spacer
        ctk.CTkFrame(center, fg_color="transparent", height=48).pack()

        # "Start a game" button
        start_btn = ctk.CTkButton(
            center,
            text="Start a game",
            font=ctk.CTkFont(size=16),
            fg_color="transparent",
            hover_color="#1A1A1A",
            text_color=TEXT_PRIMARY,
            border_width=0,
            corner_radius=0,
            command=self.__app.show_main_screen,
            height=36,
        )
        start_btn.pack()

        # Underline
        ctk.CTkFrame(center, fg_color=TEXT_PRIMARY, height=1, width=120).pack()
