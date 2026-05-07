import json
import os


class Language:
    """
    JSON-based internationalization (i18n) system.
    Demonstrates: JSON data format, OOP, Encapsulation
    Week 14: MultiLanguage — JSON
    """

    LOCALES_DIR = "locales"
    SUPPORTED = ("ru", "en")

    def __init__(self, locale: str = "ru"):
        self.__locale = locale if locale in self.SUPPORTED else "ru"
        self.__data: dict = {}
        self.__callbacks: list = []
        self._load()

    def __str__(self):
        return f"Language(locale='{self.__locale}')"

    def __repr__(self):
        return f"Language(locale='{self.__locale}', keys={len(self.__data)})"

    @property
    def locale(self) -> str:
        return self.__locale

    def _load(self):
        path = os.path.join(self.LOCALES_DIR, f"{self.__locale}.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.__data = json.load(f)
        except FileNotFoundError:
            self.__data = {}

    def switch(self):
        """Toggle between ru and en."""
        self.__locale = "en" if self.__locale == "ru" else "ru"
        self._load()
        for cb in self.__callbacks:
            cb()

    def on_change(self, callback):
        """Register a callback to be called when language changes."""
        self.__callbacks.append(callback)

    def get(self, *keys: str, **fmt) -> str:
        """
        Retrieve a translation by dot-path keys.
        E.g. lang.get('game_screen', 'phase_select')
        Supports string formatting: lang.get('auto_result', 'conclusion', rate=66.7)
        """
        value = self.__data
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key, "")
            else:
                return ""

        if isinstance(value, str) and fmt:
            try:
                return value.format(**fmt)
            except KeyError:
                return value

        return value if isinstance(value, str) else ""

    def __call__(self, *keys: str, **fmt) -> str:
        """Shortcut: lang('key1', 'key2')"""
        return self.get(*keys, **fmt)
