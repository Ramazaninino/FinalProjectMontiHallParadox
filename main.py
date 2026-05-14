

import customtkinter as ctk
from database.db_manager import DatabaseManager
from utils.language import Language
from utils.theme import Theme

# Configure CustomTkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class App(ctk.CTk):
    """
    Main application window.
    Demonstrates: OOP, Encapsulation, CustomTkinter CTk
    """

    def __init__(self):
        super().__init__()

        # Core services
        self.db = DatabaseManager()
        self.lang = Language("ru")
        self.theme = Theme("dark")

        # Update window bg when theme changes
        self.theme.on_change(self._on_theme_change)

        # Window setup
        self.title(self.lang("app_title"))
        self.geometry("1280x800")
        self.minsize(1024, 650)
        self.configure(fg_color=self.theme.BG)

        # Screen container
        self._container = ctk.CTkFrame(self, fg_color="transparent")
        self._container.pack(fill="both", expand=True)

        # Start on splash screen
        self.show_splash_screen()

    def _on_theme_change(self):
        self.configure(fg_color=self.theme.BG)

    def __str__(self):
        return f"App(title='{self.lang('app_title')}')"

    def __repr__(self):
        return f"App(db={self.db!r}, lang={self.lang!r})"

    def _clear(self):
        for widget in self._container.winfo_children():
            widget.destroy()

    def show_splash_screen(self):
        from ui.splash_screen import SplashScreen
        self._clear()
        SplashScreen(self._container, self).pack(fill="both", expand=True)

    def show_main_screen(self):
        from ui.main_screen import MainScreen
        self._clear()
        MainScreen(self._container, self).pack(fill="both", expand=True)

    def show_game_screen(self, game, session_id: int):
        from ui.game_screen import GameScreen
        self._clear()
        GameScreen(self._container, self, game, session_id).pack(fill="both", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
