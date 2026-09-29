"""Shared GreyScienx CSS tokens and Matplotlib styling helpers."""

from __future__ import annotations

import re
from pathlib import Path


DEFAULT_TOKENS = {
    "black": "#131200",
    "true-black": "#000000",
    "coral": "#f26157",
    "white": "#fbfffe",
    "grey-100": "#f0f1f2",
    "grey-300": "#cccccc",
    "grey-500": "#777777",
    "grey-700": "#3d3d3d",
}

TOKEN_PATTERN = re.compile(r"--([a-z0-9-]+)\s*:\s*(#[0-9a-fA-F]{6})\s*;")


def default_css_path() -> Path:
    return Path(__file__).resolve().parents[3] / "app" / "globals.css"


def load_tokens(css_path: str | Path | None = None) -> dict[str, str]:
    """Load supported print tokens from globals.css, with stable fallbacks."""
    path = Path(css_path) if css_path else default_css_path()
    tokens = dict(DEFAULT_TOKENS)
    if path.exists():
        discovered = dict(TOKEN_PATTERN.findall(path.read_text(encoding="utf-8")))
        for name in tokens:
            if name in discovered:
                tokens[name] = discovered[name].lower()
    return tokens


def _register_windows_fonts():
    from matplotlib import font_manager

    for name in ("segoeui.ttf", "segoeuib.ttf", "seguisb.ttf"):
        path = Path("C:/Windows/Fonts") / name
        if path.exists():
            font_manager.fontManager.addfont(str(path))


def configure_matplotlib(css_path: str | Path | None = None):
    """Apply GreyScienx editorial defaults and return resolved CSS tokens."""
    import matplotlib.pyplot as plt

    tokens = load_tokens(css_path)
    _register_windows_fonts()
    plt.rcParams.update(
        {
            "font.family": "Segoe UI",
            "font.size": 9.2,
            "axes.titlesize": 12.0,
            "axes.titleweight": "bold",
            "axes.labelsize": 9.0,
            "axes.edgecolor": tokens["black"],
            "axes.labelcolor": tokens["black"],
            "xtick.color": tokens["grey-700"],
            "ytick.color": tokens["grey-700"],
            "text.color": tokens["black"],
            "figure.facecolor": tokens["white"],
            "axes.facecolor": tokens["white"],
            "savefig.facecolor": tokens["white"],
        }
    )
    return tokens


def line_encodings(tokens: dict[str, str]):
    """Return redundant colour/line/marker encodings for up to three series."""
    return [
        {"color": tokens["coral"], "linestyle": "-", "marker": "o"},
        {"color": tokens["black"], "linestyle": (0, (5, 3)), "marker": "s"},
        {"color": tokens["grey-500"], "linestyle": (0, (1, 2)), "marker": "D"},
    ]


def add_figure_header(
    fig,
    title: str,
    subtitle: str | None = None,
    field: str = "GREYSCIENX / RESEARCH",
    tokens=None,
):
    """Add the standard coral rule, field label, title, and subtitle."""
    from matplotlib.patches import Rectangle

    tokens = tokens or load_tokens()
    fig.add_artist(
        Rectangle(
            (0.0, 0.978),
            1.0,
            0.022,
            transform=fig.transFigure,
            facecolor=tokens["coral"],
            edgecolor="none",
            clip_on=False,
        )
    )
    fig.text(
        0.055,
        0.945,
        field.upper(),
        color=tokens["coral"],
        fontsize=7.5,
        fontweight="bold",
        va="top",
    )
    fig.text(
        0.055,
        0.894,
        title,
        color=tokens["black"],
        fontsize=17.2,
        fontweight="bold",
        va="top",
    )
    if subtitle:
        fig.text(
            0.055,
            0.846,
            subtitle,
            color=tokens["grey-500"],
            fontsize=8.4,
            va="top",
        )


def style_axis(ax, tokens=None, grid_axis: str = "y"):
    """Apply quiet grids, black axes, and open top/right edges."""
    tokens = tokens or load_tokens()
    ax.grid(axis=grid_axis, color=tokens["grey-300"], linewidth=0.65, zorder=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(1.05)
    ax.spines["bottom"].set_linewidth(1.05)
    ax.tick_params(length=3, width=0.8)


def save_figure(fig, output: str | Path, dpi: int = 240):
    """Save a print-ready figure after creating its parent directory."""
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=dpi)
    return path
