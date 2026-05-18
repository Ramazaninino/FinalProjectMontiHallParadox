class Theme:
    """
    Dark / Light theme manager — same observer pattern as Language.
    Demonstrates: OOP, Encapsulation, observer/callback pattern
    Week 14 (extra): UI theming
    """

    DARK = {
        "BG":           "#0D0D0D",
        "BG_CARD":      "#1A1A1A",
        "BG_PANEL":     "#111111",
        "BG_DEEP":      "#0A0A0A",
        "BORDER":       "#2A2A2A",
        "BORDER_DEEP":  "#333333",
        "HEADER_BG":    "#0D0D0D",
        "HINT_BG":      "#1A0008",
        "TEXT_PRIMARY":   "#FFFFFF",
        "TEXT_SECONDARY": "#888888",
        "TEXT_MUTED":     "#555555",
        "CHIP_BG":      "#242424",
        "BAR_BG":       "#2A2A2A",
        "BAR_BG_DEEP":  "#333333",
        "FIELD_BG":     "#1A1A1A",
        "SUCCESS":      "#22C55E",
        "DOOR_BG":      "#1A1A1A",
        "DOOR_NUM":     "#FFFFFF",
        "DOOR_BORDER":  "#2A2A2A",
    }

    LIGHT = {
        "BG":           "#FFFFFF",
        "BG_CARD":      "#FFFFFF",
        "BG_PANEL":     "#F7F7F7",
        "BG_DEEP":      "#F2F2F2",
        "BORDER":       "#EBEBEB",
        "BORDER_DEEP":  "#D0D0D0",
        "HEADER_BG":    "#FFFFFF",
        "HINT_BG":      "#FFF0F3",
        "TEXT_PRIMARY":   "#1A1A1A",
        "TEXT_SECONDARY": "#666666",
        "TEXT_MUTED":     "#AAAAAA",
        "CHIP_BG":      "#F2F2F2",
        "BAR_BG":       "#EBEBEB",
        "BAR_BG_DEEP":  "#D0D0D0",
        "FIELD_BG":     "#F7F7F7",
        "SUCCESS":      "#16A34A",
        "DOOR_BG":      "#FFFFFF",
        "DOOR_NUM":     "#1A1A1A",
        "DOOR_BORDER":  "#EBEBEB",
    }

    # Accent stays red in both themes
    ACCENT       = "#EB1D49"
    ACCENT_HOVER = "#C91540"

    def __init__(self, mode: str = "dark"):
        self.__mode: str = mode if mode in ("dark", "light") else "dark"
        self.__callbacks: list = []

    def __str__(self):
        return f"Theme(mode='{self.__mode}')"

    def __repr__(self):
        return f"Theme(mode='{self.__mode}')"

    def __getattr__(self, name: str):
        """Allow theme.BG, theme.BORDER_DEEP, etc. as direct attribute access."""
        try:
            mode = object.__getattribute__(self, "_Theme__mode")
        except AttributeError:
            mode = "dark"
        palette = Theme.DARK if mode == "dark" else Theme.LIGHT
        if name in palette:
            return palette[name]
        raise AttributeError(f"Theme has no color '{name}'")

    # ── Properties ────────────────────────────────────────────────────────

    @property
    def mode(self) -> str:
        return self.__mode

    @property
    def is_dark(self) -> bool:
        return self.__mode == "dark"

    # ── Actions ───────────────────────────────────────────────────────────

    def switch(self):
        """Toggle between dark and light, then notify observers."""
        self.__mode = "light" if self.__mode == "dark" else "dark"
        for cb in self.__callbacks:
            cb()

    # ── Observer pattern (same as Language) ──────────────────────────────

    def on_change(self, callback):
        if callback not in self.__callbacks:
            self.__callbacks.append(callback)

    def remove_callback(self, callback):
        if callback in self.__callbacks:
            self.__callbacks.remove(callback)

    def clear_callbacks(self):
        self.__callbacks.clear()
