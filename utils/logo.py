import os
import customtkinter as ctk
from PIL import Image

_ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")

_cache: dict[str, ctk.CTkImage] = {}


def get_logo(is_dark: bool, size: tuple[int, int] = (42, 45)) -> ctk.CTkImage:
    """Return a CTkImage of the logo for the current theme."""
    key = f"{'dark' if is_dark else 'light'}_{size}"
    if key in _cache:
        return _cache[key]

    dark_path  = os.path.join(_ASSETS, "logo_dark.png")
    light_path = os.path.join(_ASSETS, "logo_light.png")
    img = Image.open(dark_path if is_dark else light_path)

    # Use the same image for both slots — CTkImage auto-picks by CTk appearance
    # mode (always "dark" in our app), so we bypass that by setting both to the
    # already-correct variant for our custom theme.
    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=size)
    _cache[key] = ctk_img
    return ctk_img


def clear_cache():
    _cache.clear()
