"""
Tela de Cadastro do Sistema Bancário.
Formulário completo com validação e seleção de tipo de conta.
"""
import customtkinter as ctk
from src.views.gui.theme import Theme
from src.views.gui.components import StyledEntry, StyledButton, StatusMessage


class CadastroFrame(ctk.CTkFrame):
    """Frame de cadastro de novo cliente."""

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
        card.pack(padx=40, pady=20)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=48, pady=36)

        # ── Header ─────────────────────────────────────────
        ctk.CTkLabel(inner, text="📋", font=(Theme.FONT_FAMILY, 36)).pack()

        ctk.CTkLabel(
            inner,
            text="Criar Nova Conta",
            font=Theme.FONT_HEADING,
            text_color=Theme.TEXT,
        ).pack(pady=(8, 0))

        ctk.CTkLabel(
            inner,
            text="Preencha seus dados para se cadastrar",
            font=Theme.FONT_SMALL,
            text_color=Theme.TEXT_MUTED,
        ).pack(pady=(4, 24))

        # ── Formulário ─────────────────────────────────────
        self.nome_entry = StyledEntry(
            inner, "Nome Completo", "Digite seu nome completo"
        )
        self.nome_entry.pack(fill="x", pady=(0, 12))

        self.cpf_entry = StyledEntry(
            inner, "CPF", "Somente números ou com pontuação"
        )
        self.cpf_entry.pack(fill="x", pady=(0, 12))

        self.senha_entry = StyledEntry(
            inner, "Senha", "Crie uma senha segura", show="●"
        )
        self.senha_entry.pack(fill="x", pady=(0, 12))

        self.confirmar_entry = StyledEntry(
            inner, "Confirmar Senha", "Repita sua senha", show="●"
        )
        self.confirmar_entry.pack(fill="x", pady=(0, 16))

        # ── Seleção de tipo de conta ───────────────────────
        tipo_frame = ctk.CTkFrame(inner, fg_color="transparent")
        tipo_frame.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            tipo_frame,
            text="Tipo de Conta",
            font=Theme.FONT_SMALL_BOLD,
            text_color=Theme.TEXT_SECONDARY,
            anchor="w",
        ).pack(fill="x", pady=(0, 8))

        self.tipo_var = ctk.StringVar(value="CORRENTE")

        radio_frame = ctk.CTkFrame(tipo_frame, fg_color="transparent")
        radio_frame.pack(fill="x")

        ctk.CTkRadioButton(
            radio_frame,
            text="  Conta Corrente",
            variable=self.tipo_var,
            value="CORRENTE",
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT,
            fg_color=Theme.PRIMARY,
            border_color=Theme.BORDER_LIGHT,
            hover_color=Theme.PRIMARY_HOVER,
        ).pack(side="left", padx=(0, 24))

        ctk.CTkRadioButton(
            radio_frame,
            text="  Conta Poupança",
            variable=self.tipo_var,
            value="POUPANCA",
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT,
            fg_color=Theme.PRIMARY,
            border_color=Theme.BORDER_LIGHT,
            hover_color=Theme.PRIMARY_HOVER,
        ).pack(side="left")

        # ── Mensagem de status ─────────────────────────────
        self.status = StatusMessage(inner)
        self.status.pack(fill="x", pady=(12, 8))

        # ── Botão Cadastrar ────────────────────────────────
        StyledButton(
            inner,
            text="Cadastrar",
            variant="success",
            command=self._cadastrar,
            width=360,
        ).pack(fill="x", pady=(8, 16))

        # ── Voltar ao Login ────────────────────────────────
        StyledButton(
            inner,
            text="← Voltar ao Login",
            variant="ghost",
            command=lambda: controller.show_frame("login"),
            width=360,
        ).pack(fill="x")

        # ── Atalho Enter ───────────────────────────────────
        self.confirmar_entry.entry.bind("<Return>", lambda e: self._cadastrar())

    def _cadastrar(self):
        """Processa o cadastro de novo cliente."""
        nome = self.nome_entry.get().strip()
        cpf = self.cpf_entry.get().strip()
        senha = self.senha_entry.get().strip()
        confirmar = self.confirmar_entry.get().strip()

        if not all([nome, cpf, senha, confirmar]):
            self.status.show_error("Preencha todos os campos.")
            return

        if senha != confirmar:
            self.status.show_error("As senhas não coincidem.")
            return

        if len(senha) < 3:
            self.status.show_error("A senha deve ter pelo menos 3 caracteres.")
            return

        sucesso, msg = self.controller.service.cadastrar_cliente(nome, cpf, senha)

        if not sucesso:
            self.status.show_error(msg)
            return

        # Abrir conta automaticamente
        tipo = self.tipo_var.get()
        self.controller.service.abrir_conta(cpf, tipo)

        self.status.show_success("Cadastro realizado! Redirecionando...")
        self.after(1500, lambda: self.controller.show_frame("login"))

