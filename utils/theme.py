class Theme:
    """
    Dark / Light theme manager — same observer pattern as Language.
    Demonstrates: OOP, Encapsulation, observer/callback pattern
    Week 14 (extra): UI theming
    """

    DARK = {
        "BG":           "#000000",
        "BG_CARD":      "#111111",
        "BG_PANEL":     "#0A0A0A",
        "BG_DEEP":      "#0D1117",
        "BORDER":       "#222222",
        "BORDER_DEEP":  "#1E293B",
        "HEADER_BG":    "#050505",
        "HINT_BG":      "#100008",
        "TEXT_PRIMARY":   "#FFFFFF",
        "TEXT_SECONDARY": "#94A3B8",
        "TEXT_MUTED":     "#475569",
        "CHIP_BG":      "#1A1A1A",
        "BAR_BG":       "#2A2A2A",
        "BAR_BG_DEEP":  "#1E293B",
        "FIELD_BG":     "#111827",
        "SUCCESS":      "#22C55E",
        "DOOR_BG":      "#FFFFFF",
        "DOOR_NUM":     "#1E293B",
    }

    LIGHT = {
        "BG":           "#F8FAFC",
        "BG_CARD":      "#FFFFFF",
        "BG_PANEL":     "#EEF2F8",
        "BG_DEEP":      "#F1F5F9",
        "BORDER":       "#CBD5E1",
        "BORDER_DEEP":  "#94A3B8",
        "HEADER_BG":    "#1E293B",
        "HINT_BG":      "#FFF0F3",
        "TEXT_PRIMARY":   "#0F172A",
        "TEXT_SECONDARY": "#475569",
        "TEXT_MUTED":     "#94A3B8",
        "CHIP_BG":      "#E2E8F0",
        "BAR_BG":       "#CBD5E1",
        "BAR_BG_DEEP":  "#94A3B8",
        "FIELD_BG":     "#F1F5F9",
        "SUCCESS":      "#16A34A",
        "DOOR_BG":      "#FFFFFF",
        "DOOR_NUM":     "#1E293B",
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
