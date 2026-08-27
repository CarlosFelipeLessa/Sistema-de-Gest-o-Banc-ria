"""
Módulo de tema e estilos para a interface gráfica do Sistema Bancário.
Define cores, fontes e constantes visuais para toda a aplicação.
"""


class Theme:
    """Tema visual profissional para a aplicação bancária."""

    # ── Cores de Fundo ──────────────────────────────────────
    BG_DARK = "#0a0f1a"
    BG_CARD = "#111827"
    BG_CARD_HOVER = "#1a2332"
    BG_INPUT = "#0f172a"

    # ── Cores Primárias ─────────────────────────────────────
    PRIMARY = "#00b4d8"
    PRIMARY_HOVER = "#0096b7"
    PRIMARY_DARK = "#006d86"

    # ── Cores Semânticas ────────────────────────────────────
    SUCCESS = "#10b981"
    SUCCESS_BG = "#052e16"
    ERROR = "#ef4444"
    ERROR_BG = "#450a0a"
    WARNING = "#f59e0b"

    # ── Texto ───────────────────────────────────────────────
    TEXT = "#f8fafc"
    TEXT_SECONDARY = "#94a3b8"
    TEXT_MUTED = "#64748b"

    # ── Bordas ──────────────────────────────────────────────
    BORDER = "#1e293b"
    BORDER_LIGHT = "#334155"
    BORDER_FOCUS = "#00b4d8"

    # ── Destaques ───────────────────────────────────────────
    GOLD = "#f59e0b"

    # ── Fontes ──────────────────────────────────────────────
    FONT_FAMILY = "Segoe UI"

    @classmethod
    def font(cls, size=14, weight="normal"):
        """Retorna uma tupla de fonte com o tamanho e peso especificados."""
        if weight == "bold":
            return (cls.FONT_FAMILY, size, "bold")
        return (cls.FONT_FAMILY, size)

    # Presets de fonte
    FONT_TITLE = (FONT_FAMILY, 28, "bold")
    FONT_HEADING = (FONT_FAMILY, 22, "bold")
    FONT_SUBHEADING = (FONT_FAMILY, 16, "bold")
    FONT_BODY = (FONT_FAMILY, 14)
    FONT_BODY_BOLD = (FONT_FAMILY, 14, "bold")
    FONT_SMALL = (FONT_FAMILY, 12)
    FONT_SMALL_BOLD = (FONT_FAMILY, 12, "bold")
    FONT_BUTTON = (FONT_FAMILY, 14, "bold")
    FONT_SALDO = (FONT_FAMILY, 32, "bold")

    # ── Dimensões ───────────────────────────────────────────
    CORNER_RADIUS = 12
    CORNER_RADIUS_SM = 8
    BUTTON_HEIGHT = 45
    ENTRY_HEIGHT = 42
    CARD_PADDING = 24
    WINDOW_WIDTH = 1050
    WINDOW_HEIGHT = 680

