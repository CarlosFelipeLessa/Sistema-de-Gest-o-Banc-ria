"""
Componentes reutilizáveis da interface gráfica.
Widgets estilizados para manter consistência visual em toda a aplicação.
"""
import customtkinter as ctk
from src.views.gui.theme import Theme


class StyledEntry(ctk.CTkFrame):
    """Campo de entrada estilizado com label e efeitos de foco."""

    def __init__(self, parent, label_text, placeholder="", show=None, **kwargs):
        super().__init__(parent, fg_color="transparent")

        self.label = ctk.CTkLabel(
            self,
            text=label_text,
            font=Theme.FONT_SMALL_BOLD,
            text_color=Theme.TEXT_SECONDARY,
            anchor="w",
        )
        self.label.pack(fill="x", pady=(0, 6))

        entry_kwargs = {
            "placeholder_text": placeholder,
            "height": Theme.ENTRY_HEIGHT,
            "corner_radius": Theme.CORNER_RADIUS_SM,
            "font": Theme.FONT_BODY,
            "fg_color": Theme.BG_INPUT,
            "border_color": Theme.BORDER,
            "text_color": Theme.TEXT,
            "placeholder_text_color": Theme.TEXT_MUTED,
            "border_width": 1,
        }
        if show:
            entry_kwargs["show"] = show

        self.entry = ctk.CTkEntry(self, **entry_kwargs)
        self.entry.pack(fill="x")

        # Efeitos de foco
        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)

    def _on_focus_in(self, event):
        self.entry.configure(border_color=Theme.BORDER_FOCUS, border_width=2)
        self.label.configure(text_color=Theme.PRIMARY)

    def _on_focus_out(self, event):
        self.entry.configure(border_color=Theme.BORDER, border_width=1)
        self.label.configure(text_color=Theme.TEXT_SECONDARY)

    def get(self):
        return self.entry.get()

    def delete(self, first, last):
        self.entry.delete(first, last)

    def insert(self, index, text):
        self.entry.insert(index, text)

    def focus(self):
        self.entry.focus()


class StyledButton(ctk.CTkButton):
    """Botão estilizado com variantes visuais predefinidas."""

    VARIANTS = {
        "primary": {
            "fg_color": Theme.PRIMARY,
            "hover_color": Theme.PRIMARY_HOVER,
            "text_color": "#ffffff",
        },
        "success": {
            "fg_color": Theme.SUCCESS,
            "hover_color": "#059669",
            "text_color": "#ffffff",
        },
        "danger": {
            "fg_color": Theme.ERROR,
            "hover_color": "#dc2626",
            "text_color": "#ffffff",
        },
        "ghost": {
            "fg_color": "transparent",
            "hover_color": Theme.BG_CARD_HOVER,
            "text_color": Theme.TEXT_SECONDARY,
            "border_width": 1,
            "border_color": Theme.BORDER,
        },
        "outline": {
            "fg_color": "transparent",
            "hover_color": Theme.BG_CARD,
            "text_color": Theme.PRIMARY,
            "border_width": 2,
            "border_color": Theme.PRIMARY,
        },
    }

    def __init__(self, parent, text, variant="primary", **kwargs):
        style = self.VARIANTS.get(variant, self.VARIANTS["primary"]).copy()
        style.update(kwargs)

        defaults = {
            "height": Theme.BUTTON_HEIGHT,
            "corner_radius": Theme.CORNER_RADIUS_SM,
            "font": Theme.FONT_BUTTON,
        }
        defaults.update(style)

        super().__init__(parent, text=text, **defaults)


class ContaCard(ctk.CTkFrame):
    """Card de conta bancária para o dashboard."""

    def __init__(self, parent, conta, on_click=None, **kwargs):
        super().__init__(
            parent,
            fg_color=Theme.BG_CARD,
            corner_radius=Theme.CORNER_RADIUS,
            border_width=1,
            border_color=Theme.BORDER,
            **kwargs,
        )

        self.on_click = on_click
        self.conta = conta

        # Determinar informações do tipo de conta
        from src.models.conta import ContaCorrente

        if isinstance(conta, ContaCorrente):
            tipo_text = "Conta Corrente"
            tipo_icon = "🏦"
            tipo_color = Theme.PRIMARY
            detalhe = f"Limite: R$ {conta.limite:,.2f}"
        else:
            tipo_text = "Conta Poupança"
            tipo_icon = "💰"
            tipo_color = Theme.SUCCESS
            detalhe = f"Rendimento: {conta.taxa_rendimento * 100:.1f}% a.m."

        self.configure(cursor="hand2")

        # Frame interno com padding
        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=20, pady=20)

        # Ícone + Tipo
        header = ctk.CTkFrame(inner, fg_color="transparent")
        header.pack(fill="x")

        ctk.CTkLabel(
            header, text=tipo_icon, font=Theme.font(28), text_color=tipo_color
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text=tipo_text,
            font=Theme.FONT_SMALL_BOLD,
            text_color=tipo_color,
        ).pack(side="left", padx=(8, 0))

        # Número da conta
        ctk.CTkLabel(
            inner,
            text=f"Nº {conta.numero}",
            font=Theme.FONT_SMALL,
            text_color=Theme.TEXT_MUTED,
            anchor="w",
        ).pack(fill="x", pady=(10, 0))

        # Saldo
        saldo_color = Theme.SUCCESS if conta.saldo >= 0 else Theme.ERROR
        ctk.CTkLabel(
            inner,
            text=f"R$ {conta.saldo:,.2f}",
            font=Theme.font(22, "bold"),
            text_color=saldo_color,
            anchor="w",
        ).pack(fill="x", pady=(4, 0))

        # Detalhe
        ctk.CTkLabel(
            inner,
            text=detalhe,
            font=Theme.FONT_SMALL,
            text_color=Theme.TEXT_MUTED,
            anchor="w",
        ).pack(fill="x", pady=(2, 0))

        # Botão de acesso
        StyledButton(
            inner,
            text="Acessar Conta →",
            variant="outline",
            height=36,
            font=Theme.FONT_SMALL_BOLD,
            command=lambda: on_click(conta) if on_click else None,
        ).pack(fill="x", pady=(16, 0))

        # Efeito hover
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, event):
        self.configure(fg_color=Theme.BG_CARD_HOVER, border_color=Theme.PRIMARY)

    def _on_leave(self, event):
        self.configure(fg_color=Theme.BG_CARD, border_color=Theme.BORDER)


class NovaContaCard(ctk.CTkFrame):
    """Card com botão para abrir nova conta."""

    def __init__(self, parent, on_click=None, **kwargs):
        super().__init__(
            parent,
            fg_color=Theme.BG_CARD,
            corner_radius=Theme.CORNER_RADIUS,
            border_width=2,
            border_color=Theme.BORDER,
            **kwargs,
        )

        self.configure(cursor="hand2")
        self._on_click = on_click

        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.pack(expand=True, pady=30)

        ctk.CTkLabel(
            inner, text="＋", font=Theme.font(40, "bold"), text_color=Theme.TEXT_MUTED
        ).pack()

        ctk.CTkLabel(
            inner,
            text="Abrir Nova\nConta",
            font=Theme.FONT_BODY_BOLD,
            text_color=Theme.TEXT_MUTED,
            justify="center",
        ).pack(pady=(8, 0))

        # Click em todo o card
        self.bind("<Button-1>", lambda e: on_click() if on_click else None)
        inner.bind("<Button-1>", lambda e: on_click() if on_click else None)
        for child in inner.winfo_children():
            child.bind("<Button-1>", lambda e: on_click() if on_click else None)

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, event):
        self.configure(border_color=Theme.PRIMARY)

    def _on_leave(self, event):
        self.configure(border_color=Theme.BORDER)


class StatusMessage(ctk.CTkLabel):
    """Widget para exibir mensagens de sucesso ou erro com auto-hide."""

    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            text="",
            font=Theme.FONT_BODY_BOLD,
            corner_radius=Theme.CORNER_RADIUS_SM,
            fg_color="transparent",
            height=0,
            **kwargs,
        )
        self._after_id = None

    def show_success(self, message):
        """Exibe mensagem de sucesso com ícone verde."""
        if self._after_id:
            self.after_cancel(self._after_id)
        self.configure(
            text=f"  ✔  {message}  ",
            text_color=Theme.SUCCESS,
            fg_color=Theme.SUCCESS_BG,
            height=40,
        )
        self._after_id = self.after(5000, self.hide)

    def show_error(self, message):
        """Exibe mensagem de erro com ícone vermelho."""
        if self._after_id:
            self.after_cancel(self._after_id)
        self.configure(
            text=f"  ✖  {message}  ",
            text_color=Theme.ERROR,
            fg_color=Theme.ERROR_BG,
            height=40,
        )
        self._after_id = self.after(5000, self.hide)

    def hide(self):
        """Esconde a mensagem."""
        self.configure(text="", fg_color="transparent", height=0)
        self._after_id = None

