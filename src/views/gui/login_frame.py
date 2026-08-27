"""
Tela de Login do Sistema Bancário.
Interface centralizada com campos de CPF/Senha e navegação para cadastro.
"""
import customtkinter as ctk
from src.views.gui.theme import Theme
from src.views.gui.components import StyledEntry, StyledButton, StatusMessage


class LoginFrame(ctk.CTkFrame):
    """Frame de autenticação do cliente."""

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=Theme.BG_DARK)
        self.controller = controller

        # ── Container centralizado ──────────────────────────
        center = ctk.CTkFrame(self, fg_color="transparent")
        center.place(relx=0.5, rely=0.5, anchor="center")

        # ── Card principal ──────────────────────────────────
        card = ctk.CTkFrame(
            center,
            fg_color=Theme.BG_CARD,
            corner_radius=Theme.CORNER_RADIUS,
            border_width=1,
            border_color=Theme.BORDER,
        )
        card.pack(padx=40, pady=40)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=48, pady=48)

        # ── Logo e Título ───────────────────────────────────
        ctk.CTkLabel(
            inner, text="🏦", font=(Theme.FONT_FAMILY, 48)
        ).pack()

        ctk.CTkLabel(
            inner,
            text="Sistema de Gestão\nBancária",
            font=Theme.FONT_HEADING,
            text_color=Theme.TEXT,
            justify="center",
        ).pack(pady=(8, 0))

        ctk.CTkLabel(
            inner,
            text="Acesse sua conta de forma segura",
            font=Theme.FONT_SMALL,
            text_color=Theme.TEXT_MUTED,
        ).pack(pady=(4, 32))

        # ── Campo CPF ──────────────────────────────────────
        self.cpf_entry = StyledEntry(inner, "CPF", "Digite seu CPF")
        self.cpf_entry.pack(fill="x", pady=(0, 16))

        # ── Campo Senha ────────────────────────────────────
        self.senha_entry = StyledEntry(
            inner, "Senha", "Digite sua senha", show="●"
        )
        self.senha_entry.pack(fill="x", pady=(0, 8))

        # ── Mensagem de status ─────────────────────────────
        self.status = StatusMessage(inner)
        self.status.pack(fill="x", pady=(8, 8))

        # ── Botão Entrar ───────────────────────────────────
        StyledButton(
            inner,
            text="Entrar",
            variant="primary",
            command=self._fazer_login,
            width=320,
        ).pack(fill="x", pady=(8, 16))

        # ── Separador ─────────────────────────────────────
        sep_frame = ctk.CTkFrame(inner, fg_color="transparent")
        sep_frame.pack(fill="x", pady=(0, 16))

        ctk.CTkFrame(sep_frame, height=1, fg_color=Theme.BORDER).pack(
            side="left", fill="x", expand=True
        )
        ctk.CTkLabel(
            sep_frame,
            text="  ou  ",
            font=Theme.FONT_SMALL,
            text_color=Theme.TEXT_MUTED,
        ).pack(side="left")
        ctk.CTkFrame(sep_frame, height=1, fg_color=Theme.BORDER).pack(
            side="left", fill="x", expand=True
        )

        # ── Link para Cadastro ─────────────────────────────
        StyledButton(
            inner,
            text="Criar Nova Conta",
            variant="ghost",
            command=lambda: controller.show_frame("cadastro"),
            width=320,
        ).pack(fill="x")

        # ── Atalhos de teclado ─────────────────────────────
        self.cpf_entry.entry.bind("<Return>", lambda e: self.senha_entry.focus())
        self.senha_entry.entry.bind("<Return>", lambda e: self._fazer_login())

    def _fazer_login(self):
        """Processa a autenticação do cliente."""
        cpf = self.cpf_entry.get().strip()
        senha = self.senha_entry.get().strip()

        if not cpf or not senha:
            self.status.show_error("Preencha todos os campos.")
            return

        sucesso, msg, cliente = self.controller.service.autenticar(cpf, senha)

        if sucesso:
            self.status.show_success(msg)
            self.after(
                800, lambda: self.controller.show_frame("dashboard", cliente=cliente)
            )
        else:
            self.status.show_error(msg)

