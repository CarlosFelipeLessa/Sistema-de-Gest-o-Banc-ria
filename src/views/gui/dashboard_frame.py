"""
Dashboard do Cliente.
Exibe resumo das contas, cards interativos e ações rápidas.
"""
import customtkinter as ctk
from src.views.gui.theme import Theme
from src.views.gui.components import StyledButton, ContaCard, NovaContaCard, StatusMessage


class DashboardFrame(ctk.CTkFrame):
    """Frame principal do cliente autenticado."""

    def __init__(self, parent, controller, cliente=None):
        super().__init__(parent, fg_color=Theme.BG_DARK)
        self.controller = controller
        self.cliente = cliente

        # ── Header Bar ─────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, height=70, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)

        header_inner = ctk.CTkFrame(header, fg_color="transparent")
        header_inner.pack(fill="both", expand=True, padx=30)

        # Logo
        logo_frame = ctk.CTkFrame(header_inner, fg_color="transparent")
        logo_frame.pack(side="left", fill="y")

        ctk.CTkLabel(logo_frame, text="🏦", font=Theme.font(22)).pack(
            side="left", pady=15
        )
        ctk.CTkLabel(
            logo_frame,
            text="  Banco Digital",
            font=Theme.FONT_SUBHEADING,
            text_color=Theme.PRIMARY,
        ).pack(side="left", pady=15)

        # Lado direito — info do usuário + logout
        right_frame = ctk.CTkFrame(header_inner, fg_color="transparent")
        right_frame.pack(side="right", fill="y")

        ctk.CTkLabel(
            right_frame,
            text=f"Olá, {cliente.nome}!  👋",
            font=Theme.FONT_BODY_BOLD,
            text_color=Theme.TEXT,
        ).pack(side="left", padx=(0, 16), pady=15)

        StyledButton(
            right_frame,
            text="Sair",
            variant="ghost",
            width=80,
            height=36,
            font=Theme.FONT_SMALL_BOLD,
            command=self._logout,
        ).pack(side="left", pady=15)

        # ── Divider ────────────────────────────────────────
        ctk.CTkFrame(self, fg_color=Theme.BORDER, height=1).pack(fill="x")

        # ── Conteúdo Principal ─────────────────────────────
        content = ctk.CTkScrollableFrame(
            self, fg_color=Theme.BG_DARK, scrollbar_button_color=Theme.BORDER
        )
        content.pack(fill="both", expand=True, padx=30, pady=24)

        # Título da seção
        ctk.CTkLabel(
            content,
            text="Minhas Contas",
            font=Theme.FONT_HEADING,
            text_color=Theme.TEXT,
            anchor="w",
        ).pack(fill="x", pady=(0, 4))

        ctk.CTkLabel(
            content,
            text="Gerencie suas contas bancárias",
            font=Theme.FONT_SMALL,
            text_color=Theme.TEXT_MUTED,
            anchor="w",
        ).pack(fill="x", pady=(0, 20))

        # Mensagem de status
        self.status = StatusMessage(content)
        self.status.pack(fill="x", pady=(0, 12))

        # ── Grid de Cards de Contas ────────────────────────
        cards_frame = ctk.CTkFrame(content, fg_color="transparent")
        cards_frame.pack(fill="x")

        contas = controller.service.obter_contas_cliente(cliente.cpf)

        col = 0
        for conta in contas:
            card = ContaCard(cards_frame, conta, on_click=self._acessar_conta)
            card.grid(
                row=col // 3,
                column=col % 3,
                padx=(0, 16),
                pady=(0, 16),
                sticky="nsew",
            )
            cards_frame.grid_columnconfigure(col % 3, weight=1)
            col += 1

        # Card de nova conta
        nova_card = NovaContaCard(cards_frame, on_click=self._abrir_nova_conta_dialog)
        nova_card.grid(
            row=col // 3,
            column=col % 3,
            padx=(0, 16),
            pady=(0, 16),
            sticky="nsew",
        )
        cards_frame.grid_columnconfigure(col % 3, weight=1)

        # Preencher colunas restantes para manter o layout
        for i in range((col % 3) + 1, 3):
            cards_frame.grid_columnconfigure(i, weight=1)

        # ── Resumo do Patrimônio ───────────────────────────
        if contas:
            ctk.CTkFrame(content, fg_color=Theme.BORDER, height=1).pack(
                fill="x", pady=(20, 20)
            )

            total = sum(c.saldo for c in contas)
            total_color = Theme.SUCCESS if total >= 0 else Theme.ERROR

            summary = ctk.CTkFrame(
                content,
                fg_color=Theme.BG_CARD,
                corner_radius=Theme.CORNER_RADIUS,
                border_width=1,
                border_color=Theme.BORDER,
            )
            summary.pack(fill="x")

            summary_inner = ctk.CTkFrame(summary, fg_color="transparent")
            summary_inner.pack(fill="x", padx=24, pady=20)

            # Lado esquerdo — patrimônio
            left = ctk.CTkFrame(summary_inner, fg_color="transparent")
            left.pack(side="left")

            ctk.CTkLabel(
                left,
                text="PATRIMÔNIO TOTAL",
                font=Theme.FONT_SMALL_BOLD,
                text_color=Theme.TEXT_MUTED,
                anchor="w",
            ).pack(fill="x")

            ctk.CTkLabel(
                left,
                text=f"R$ {total:,.2f}",
                font=Theme.FONT_SALDO,
                text_color=total_color,
                anchor="w",
            ).pack(fill="x", pady=(4, 0))

            # Lado direito — info
            right = ctk.CTkFrame(summary_inner, fg_color="transparent")
            right.pack(side="right")

            ctk.CTkLabel(
                right,
                text=f"{len(contas)} conta(s) ativa(s)",
                font=Theme.FONT_BODY,
                text_color=Theme.TEXT_SECONDARY,
            ).pack()

    def _acessar_conta(self, conta):
        """Navega para a tela de operações da conta selecionada."""
        sucesso, msg, _ = self.controller.service.selecionar_conta(conta.numero)
        if sucesso:
            self.controller.show_frame("conta", conta=conta, cliente=self.cliente)
        else:
            self.status.show_error(msg)

    def _abrir_nova_conta_dialog(self):
        """Abre diálogo para criar nova conta bancária."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Abrir Nova Conta")
        dialog.geometry("420x340")
        dialog.configure(fg_color=Theme.BG_DARK)
        dialog.resizable(False, False)
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        # Centralizar o diálogo
        dialog.after(
            10,
            lambda: dialog.geometry(
                f"+{self.winfo_toplevel().winfo_x() + 300}"
                f"+{self.winfo_toplevel().winfo_y() + 150}"
            ),
        )

        inner = ctk.CTkFrame(
            dialog,
            fg_color=Theme.BG_CARD,
            corner_radius=Theme.CORNER_RADIUS,
            border_width=1,
            border_color=Theme.BORDER,
        )
        inner.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            inner,
            text="Abrir Nova Conta",
            font=Theme.FONT_HEADING,
            text_color=Theme.TEXT,
        ).pack(pady=(24, 4))

        ctk.CTkLabel(
            inner,
            text="Selecione o tipo de conta desejado",
            font=Theme.FONT_SMALL,
            text_color=Theme.TEXT_MUTED,
        ).pack(pady=(0, 24))

        tipo_var = ctk.StringVar(value="CORRENTE")

        ctk.CTkRadioButton(
            inner,
            text="  Conta Corrente  🏦",
            variable=tipo_var,
            value="CORRENTE",
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT,
            fg_color=Theme.PRIMARY,
            border_color=Theme.BORDER_LIGHT,
            hover_color=Theme.PRIMARY_HOVER,
        ).pack(anchor="w", padx=30, pady=(0, 10))

        ctk.CTkRadioButton(
            inner,
            text="  Conta Poupança  💰",
            variable=tipo_var,
            value="POUPANCA",
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT,
            fg_color=Theme.PRIMARY,
            border_color=Theme.BORDER_LIGHT,
            hover_color=Theme.PRIMARY_HOVER,
        ).pack(anchor="w", padx=30, pady=(0, 24))

        def confirmar():
            tipo = tipo_var.get()
            sucesso, msg, _ = self.controller.service.abrir_conta(
                self.cliente.cpf, tipo
            )
            dialog.destroy()
            if sucesso:
                self.status.show_success(msg)
                # Refresh dashboard
                self.after(
                    800,
                    lambda: self.controller.show_frame(
                        "dashboard", cliente=self.cliente
                    ),
                )
            else:
                self.status.show_error(msg)

        btns = ctk.CTkFrame(inner, fg_color="transparent")
        btns.pack(fill="x", padx=30, pady=(0, 24))

        StyledButton(
            btns, text="Confirmar", variant="success", command=confirmar
        ).pack(side="left", expand=True, fill="x", padx=(0, 8))

        StyledButton(
            btns, text="Cancelar", variant="ghost", command=dialog.destroy
        ).pack(side="left", expand=True, fill="x", padx=(8, 0))

    def _logout(self):
        """Desloga o cliente e volta ao login."""
        self.controller.service.deslogar()
        self.controller.show_frame("login")

