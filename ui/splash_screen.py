import customtkinter as ctk
from utils.logo import get_logo

ACCENT = "#EB1D49"


class SplashScreen(ctk.CTkFrame):
    """
    Welcome / splash screen.
    Demonstrates: OOP, CustomTkinter widgets
    Week 14: MultiLanguage — JSON
    """

    def __init__(self, parent, app):
        self._t = app.theme
        super().__init__(parent, fg_color=self._t.BG)
        self.__app = app
        self.__lang = app.lang
        self._build()

    def _build(self):
        t = self._t
        l = self.__lang

        # Top-left logo — SVG asset, theme-aware
        logo_lbl = ctk.CTkLabel(
            self, image=get_logo(is_dark=t.is_dark, size=(42, 45)),
            text="", fg_color="transparent",
        )
        logo_lbl.place(x=20, y=17)

        # Center content
        center = ctk.CTkFrame(self, fg_color="transparent")
        center.place(relx=0.5, rely=0.42, anchor="center")

        # Big red title
        ctk.CTkLabel(
            center,
            text=l("splash", "title"),
            font=ctk.CTkFont(family="Arial", size=82, weight="bold"),
            text_color=ACCENT,
            justify="center",
        ).pack()

        # Spacer
        ctk.CTkFrame(center, fg_color="transparent", height=48).pack()

        # Start button
        start_btn = ctk.CTkButton(
            center,
            text=l("splash", "start"),
            font=ctk.CTkFont(size=16),
            fg_color="transparent",
            hover_color=t.BG_CARD,
            text_color=t.TEXT_PRIMARY,
            border_width=0,
            corner_radius=0,
            command=self.__app.show_main_screen,
            height=36,
        )
        start_btn.pack()

        # Underline
        ctk.CTkFrame(center, fg_color=t.TEXT_PRIMARY, height=1, width=120).pack()
