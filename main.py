"""
Monty Hall Paradox — Student Final Project
Course: Introduction to Speciality (Semester II)
Instructor: Muratov Kanat

Topics covered:
  Week 2  — OOP: Functions, Classes, Objects
  Week 4  — Magic Methods: __str__, __repr__, __init__, __eq__, __len__
  Week 5  — OOP: Encapsulation, Inheritance, Polymorphism
  Week 6  — Desktop Application: CustomTkinter (Entry, Label, Button, Frame, Slider...)
  Week 10 — Database: sqlite3
  Week 11 — Desktop App + sqlite3 integration
  Week 12 — SQL: SELECT, LEFT JOIN, GROUP BY
  Week 13 — Data Formats: CSV export
  Week 14 — MultiLanguage: JSON-based i18n (ru / en)
"""

import customtkinter as ctk
from database.db_manager import DatabaseManager
from utils.language import Language

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

        # Window setup
        self.title(self.lang("app_title"))
        self.geometry("1280x800")
        self.minsize(1024, 650)
        self.configure(fg_color="#000000")

        # Screen container
        self._container = ctk.CTkFrame(self, fg_color="transparent")
        self._container.pack(fill="both", expand=True)

        # Start on main screen
        self.show_main_screen()

    def __str__(self):
        return f"App(title='{self.lang('app_title')}')"

    def __repr__(self):
        return f"App(db={self.db!r}, lang={self.lang!r})"

    def _clear(self):
        for widget in self._container.winfo_children():
            widget.destroy()

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
