"""
Tela de Operações da Conta.
Interface com abas para depósito, saque, transferência, extrato e rendimento.
"""
import customtkinter as ctk
from src.views.gui.theme import Theme
from src.views.gui.components import StyledEntry, StyledButton, StatusMessage
from src.models.conta import ContaCorrente, ContaPoupanca


class ContaFrame(ctk.CTkFrame):
    """Frame de operações bancárias na conta selecionada."""

    def __init__(self, parent, controller, conta=None, cliente=None):
        super().__init__(parent, fg_color=Theme.BG_DARK)
        self.controller = controller
        self.conta = conta
        self.cliente = cliente

        # Informações do tipo de conta
        is_corrente = isinstance(conta, ContaCorrente)
        tipo_text = "Conta Corrente" if is_corrente else "Conta Poupança"
        tipo_icon = "🏦" if is_corrente else "💰"
        tipo_color = Theme.PRIMARY if is_corrente else Theme.SUCCESS

        # ── Header ─────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, height=80, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)

        header_inner = ctk.CTkFrame(header, fg_color="transparent")
        header_inner.pack(fill="both", expand=True, padx=30)

        # Botão Voltar
        StyledButton(
            header_inner,
            text="← Voltar",
            variant="ghost",
            width=100,
            height=36,
            font=Theme.FONT_SMALL_BOLD,
            command=self._voltar,
        ).pack(side="left", pady=20)

        # Info da conta (centralizado)
        info_frame = ctk.CTkFrame(header_inner, fg_color="transparent")
        info_frame.pack(side="left", expand=True, pady=10)

        ctk.CTkLabel(
            info_frame,
            text=f"{tipo_icon}  {tipo_text} Nº {conta.numero}",
            font=Theme.FONT_SUBHEADING,
            text_color=tipo_color,
        ).pack()

        saldo_color = Theme.SUCCESS if conta.saldo >= 0 else Theme.ERROR
        self.saldo_label = ctk.CTkLabel(
            info_frame,
            text=f"Saldo: R$ {conta.saldo:,.2f}",
            font=Theme.FONT_BODY_BOLD,
            text_color=saldo_color,
        )
        self.saldo_label.pack()

        # Detalhe extra
        if is_corrente:
            detalhe = f"Limite disponível: R$ {conta.limite:,.2f}"
        else:
            detalhe = f"Rendimento: {conta.taxa_rendimento * 100:.1f}% a.m."

        ctk.CTkLabel(
            info_frame,
            text=detalhe,
            font=Theme.FONT_SMALL,
            text_color=Theme.TEXT_MUTED,
        ).pack()

        # ── Divider ────────────────────────────────────────
        ctk.CTkFrame(self, fg_color=Theme.BORDER, height=1).pack(fill="x")

        # ── Abas de Navegação ──────────────────────────────
        tabs_frame = ctk.CTkFrame(
            self, fg_color=Theme.BG_CARD, height=50, corner_radius=0
        )
        tabs_frame.pack(fill="x")
        tabs_frame.pack_propagate(False)

        tabs_inner = ctk.CTkFrame(tabs_frame, fg_color="transparent")
        tabs_inner.pack(fill="both", expand=True, padx=30)

        self.tab_buttons = {}
        operations = [
            ("deposito", "💳 Depósito"),
            ("saque", "💸 Saque"),
            ("transferencia", "🔄 Transferência"),
            ("extrato", "📊 Extrato"),
        ]
        if isinstance(conta, ContaPoupanca):
            operations.append(("rendimento", "📈 Rendimento"))

        for op_key, op_text in operations:
            btn = ctk.CTkButton(
                tabs_inner,
                text=op_text,
                fg_color="transparent",
                hover_color=Theme.BG_CARD_HOVER,
                text_color=Theme.TEXT_SECONDARY,
                font=Theme.FONT_SMALL_BOLD,
                height=40,
                corner_radius=Theme.CORNER_RADIUS_SM,
                command=lambda k=op_key: self._show_operation(k),
            )
            btn.pack(side="left", padx=(0, 4), pady=5)
            self.tab_buttons[op_key] = btn

        ctk.CTkFrame(self, fg_color=Theme.BORDER, height=1).pack(fill="x")

        # ── Área de Conteúdo ───────────────────────────────
        self.content_area = ctk.CTkFrame(self, fg_color=Theme.BG_DARK)
        self.content_area.pack(fill="both", expand=True, padx=30, pady=24)

        # Exibir operação padrão
        self._show_operation("deposito")

    def _show_operation(self, op_key):
        """Alterna entre as operações disponíveis."""
        # Atualizar estilo das abas
        for key, btn in self.tab_buttons.items():
            if key == op_key:
                btn.configure(fg_color=Theme.PRIMARY, text_color="#ffffff")
            else:
                btn.configure(fg_color="transparent", text_color=Theme.TEXT_SECONDARY)

        # Limpar área de conteúdo
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # Construir a operação selecionada
        builders = {
            "deposito": self._build_deposito,
            "saque": self._build_saque,
            "transferencia": self._build_transferencia,
            "extrato": self._build_extrato,
            "rendimento": self._build_rendimento,
        }
        builder = builders.get(op_key)
        if builder:
            builder()

    def _build_operation_form(self, title, icon, fields, button_text, on_submit):
        """Helper para construir formulários de operação consistentes."""
        card = ctk.CTkFrame(
            self.content_area,
            fg_color=Theme.BG_CARD,
            corner_radius=Theme.CORNER_RADIUS,
            border_width=1,
            border_color=Theme.BORDER,
        )
        card.pack(fill="x")

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=32, pady=28)

        # Título
        ctk.CTkLabel(
            inner,
            text=f"{icon}  {title}",
            font=Theme.FONT_SUBHEADING,
            text_color=Theme.TEXT,
            anchor="w",
        ).pack(fill="x", pady=(0, 20))

        # Campos do formulário
        entries = {}
        last_entry = None
        for field in fields:
            entry = StyledEntry(inner, field["label"], field.get("placeholder", ""))
            entry.pack(fill="x", pady=(0, 12))
            entries[field["key"]] = entry
            last_entry = entry

        # Mensagem de status
        status = StatusMessage(inner)
        status.pack(fill="x", pady=(8, 8))

        # Botão de ação
        StyledButton(
            inner,
            text=button_text,
            variant="primary",
            command=lambda: on_submit(entries, status),
        ).pack(fill="x", pady=(8, 0))

        # Bind Enter no último campo
        if last_entry:
            last_entry.entry.bind("<Return>", lambda e: on_submit(entries, status))

        return entries, status

    def _build_deposito(self):
        """Constrói o formulário de depósito."""

        def on_submit(entries, status):
            try:
                valor = float(entries["valor"].get().replace(",", "."))
            except ValueError:
                status.show_error("Digite um valor numérico válido.")
                return

            sucesso, msg = self.controller.service.realizar_deposito(valor)
            if sucesso:
                status.show_success(msg)
                self._atualizar_saldo()
                entries["valor"].delete(0, "end")
            else:
                status.show_error(msg)

        self._build_operation_form(
            "Realizar Depósito",
            "💳",
            [
                {
                    "key": "valor",
                    "label": "Valor do Depósito (R$)",
                    "placeholder": "Ex: 100,00",
                }
            ],
            "✔  Confirmar Depósito",
            on_submit,
        )

    def _build_saque(self):
        """Constrói o formulário de saque."""

        def on_submit(entries, status):
            try:
                valor = float(entries["valor"].get().replace(",", "."))
            except ValueError:
                status.show_error("Digite um valor numérico válido.")
                return

            sucesso, msg = self.controller.service.realizar_saque(valor)
            if sucesso:
                status.show_success(msg)
                self._atualizar_saldo()
                entries["valor"].delete(0, "end")
            else:
                status.show_error(msg)

        entries, status = self._build_operation_form(
            "Realizar Saque",
            "💸",
            [
                {
                    "key": "valor",
                    "label": "Valor do Saque (R$)",
                    "placeholder": "Ex: 50,00",
                }
            ],
            "✔  Confirmar Saque",
            on_submit,
        )

        # Info de saldo disponível
        card = entries["valor"].winfo_parent()
        saldo_disponivel = self.conta.saldo
        info_text = f"Saldo disponível: R$ {saldo_disponivel:,.2f}"
        if isinstance(self.conta, ContaCorrente):
            total = saldo_disponivel + self.conta.limite
            info_text += f"  •  Com limite: R$ {total:,.2f}"

        ctk.CTkLabel(
            self.content_area,
            text=info_text,
            font=Theme.FONT_SMALL,
            text_color=Theme.TEXT_MUTED,
            anchor="w",
        ).pack(fill="x", pady=(8, 0))

    def _build_transferencia(self):
        """Constrói o formulário de transferência."""

        def on_submit(entries, status):
            try:
                num_destino = int(entries["destino"].get())
            except ValueError:
                status.show_error("Número da conta deve ser um valor inteiro.")
                return
            try:
                valor = float(entries["valor"].get().replace(",", "."))
            except ValueError:
                status.show_error("Digite um valor numérico válido.")
                return

            sucesso, msg = self.controller.service.realizar_transferencia(
                num_destino, valor
            )
            if sucesso:
                status.show_success(msg)
                self._atualizar_saldo()
                entries["destino"].delete(0, "end")
                entries["valor"].delete(0, "end")
            else:
                status.show_error(msg)

        self._build_operation_form(
            "Transferência Bancária",
            "🔄",
            [
                {
                    "key": "destino",
                    "label": "Conta de Destino",
                    "placeholder": "Número da conta (ex: 1002)",
                },
                {
                    "key": "valor",
                    "label": "Valor da Transferência (R$)",
                    "placeholder": "Ex: 200,00",
                },
            ],
            "✔  Confirmar Transferência",
            on_submit,
        )

    def _build_extrato(self):
        """Constrói a tabela de extrato detalhado."""
        card = ctk.CTkFrame(
            self.content_area,
            fg_color=Theme.BG_CARD,
            corner_radius=Theme.CORNER_RADIUS,
            border_width=1,
            border_color=Theme.BORDER,
        )
        card.pack(fill="both", expand=True)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=32, pady=28)

        ctk.CTkLabel(
            inner,
            text="📊  Extrato Detalhado",
            font=Theme.FONT_SUBHEADING,
            text_color=Theme.TEXT,
            anchor="w",
        ).pack(fill="x", pady=(0, 16))

        # ── Cabeçalho da Tabela ────────────────────────────
        header_frame = ctk.CTkFrame(
            inner, fg_color=Theme.BG_DARK, corner_radius=Theme.CORNER_RADIUS_SM
        )
        header_frame.pack(fill="x")

        header_inner = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_inner.pack(fill="x", padx=16, pady=10)

        col_widths = [("Data/Hora", 180), ("Tipo", 120), ("Descrição", 280), ("Valor", 140)]
        for col_text, width in col_widths:
            ctk.CTkLabel(
                header_inner,
                text=col_text,
                font=Theme.FONT_SMALL_BOLD,
                text_color=Theme.TEXT_MUTED,
                anchor="w",
                width=width,
            ).pack(side="left")

        # ── Corpo da Tabela com Scroll ─────────────────────
        body = ctk.CTkScrollableFrame(
            inner,
            fg_color="transparent",
            height=250,
            scrollbar_button_color=Theme.BORDER,
        )
        body.pack(fill="both", expand=True, pady=(4, 0))

        if not self.conta.extrato:
            empty_frame = ctk.CTkFrame(body, fg_color="transparent")
            empty_frame.pack(expand=True, pady=40)

            ctk.CTkLabel(
                empty_frame,
                text="📭",
                font=(Theme.FONT_FAMILY, 36),
            ).pack()

            ctk.CTkLabel(
                empty_frame,
                text="Nenhuma movimentação registrada",
                font=Theme.FONT_BODY,
                text_color=Theme.TEXT_MUTED,
            ).pack(pady=(8, 0))
        else:
            for i, t in enumerate(reversed(self.conta.extrato)):
                is_credit = t.tipo in [
                    "DEPOSITO",
                    "RENDIMENTO",
                ] or "recebida" in t.descricao.lower()
                cor = Theme.SUCCESS if is_credit else Theme.ERROR
                prefix = "+" if is_credit else "-"

                row_bg = Theme.BG_CARD if i % 2 == 0 else Theme.BG_DARK
                row = ctk.CTkFrame(
                    body, fg_color=row_bg, corner_radius=4, height=38
                )
                row.pack(fill="x", pady=1)
                row.pack_propagate(False)

                row_inner = ctk.CTkFrame(row, fg_color="transparent")
                row_inner.pack(fill="both", expand=True, padx=16)

                ctk.CTkLabel(
                    row_inner,
                    text=t.data_hora,
                    font=Theme.FONT_SMALL,
                    text_color=Theme.TEXT_MUTED,
                    anchor="w",
                    width=180,
                ).pack(side="left", fill="y")

                ctk.CTkLabel(
                    row_inner,
                    text=t.tipo,
                    font=Theme.FONT_SMALL_BOLD,
                    text_color=cor,
                    anchor="w",
                    width=120,
                ).pack(side="left", fill="y")

                ctk.CTkLabel(
                    row_inner,
                    text=t.descricao,
                    font=Theme.FONT_SMALL,
                    text_color=Theme.TEXT,
                    anchor="w",
                    width=280,
                ).pack(side="left", fill="y")

                ctk.CTkLabel(
                    row_inner,
                    text=f"{prefix} R$ {t.valor:,.2f}",
                    font=Theme.FONT_SMALL_BOLD,
                    text_color=cor,
                    anchor="e",
                    width=140,
                ).pack(side="left", fill="y")

        # ── Rodapé com Saldo ───────────────────────────────
        footer = ctk.CTkFrame(
            inner, fg_color=Theme.BG_DARK, corner_radius=Theme.CORNER_RADIUS_SM
        )
        footer.pack(fill="x", pady=(8, 0))

        footer_inner = ctk.CTkFrame(footer, fg_color="transparent")
        footer_inner.pack(fill="x", padx=16, pady=12)

        saldo_color = Theme.SUCCESS if self.conta.saldo >= 0 else Theme.ERROR

        ctk.CTkLabel(
            footer_inner,
            text="SALDO ATUAL",
            font=Theme.FONT_BODY_BOLD,
            text_color=Theme.TEXT,
            anchor="w",
        ).pack(side="left")

        ctk.CTkLabel(
            footer_inner,
            text=f"R$ {self.conta.saldo:,.2f}",
            font=Theme.font(18, "bold"),
            text_color=saldo_color,
            anchor="e",
        ).pack(side="right")

    def _build_rendimento(self):
        """Constrói o painel de rendimento da poupança."""
        card = ctk.CTkFrame(
            self.content_area,
            fg_color=Theme.BG_CARD,
            corner_radius=Theme.CORNER_RADIUS,
            border_width=1,
            border_color=Theme.BORDER,
        )
        card.pack(fill="x")

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=32, pady=28)

        ctk.CTkLabel(
            inner,
            text="📈  Simular Rendimento Mensal",
            font=Theme.FONT_SUBHEADING,
            text_color=Theme.TEXT,
            anchor="w",
        ).pack(fill="x", pady=(0, 20))

        # Informações da simulação
        info_frame = ctk.CTkFrame(
            inner, fg_color=Theme.BG_DARK, corner_radius=Theme.CORNER_RADIUS_SM
        )
        info_frame.pack(fill="x", pady=(0, 20))

        info_inner = ctk.CTkFrame(info_frame, fg_color="transparent")
        info_inner.pack(fill="x", padx=20, pady=16)

        dados = [
            ("Taxa mensal", f"{self.conta.taxa_rendimento * 100:.1f}%"),
            ("Saldo atual", f"R$ {self.conta.saldo:,.2f}"),
            (
                "Rendimento estimado",
                f"R$ {self.conta.saldo * self.conta.taxa_rendimento:,.2f}",
            ),
            (
                "Saldo após rendimento",
                f"R$ {self.conta.saldo * (1 + self.conta.taxa_rendimento):,.2f}",
            ),
        ]

        for label, valor in dados:
            row = ctk.CTkFrame(info_inner, fg_color="transparent")
            row.pack(fill="x", pady=2)

            ctk.CTkLabel(
                row,
                text=label,
                font=Theme.FONT_BODY,
                text_color=Theme.TEXT_SECONDARY,
                anchor="w",
            ).pack(side="left")

            cor = Theme.SUCCESS if "Rendimento" in label else Theme.TEXT
            ctk.CTkLabel(
                row,
                text=valor,
                font=Theme.FONT_BODY_BOLD,
                text_color=cor,
                anchor="e",
            ).pack(side="right")

        # Status
        status = StatusMessage(inner)
        status.pack(fill="x", pady=(0, 8))

        def aplicar():
            sucesso, msg = self.controller.service.aplicar_rendimento_poupanca()
            if sucesso:
                status.show_success(msg)
                self._atualizar_saldo()
            else:
                status.show_error(msg)

        StyledButton(
            inner, text="✔  Aplicar Rendimento", variant="success", command=aplicar
        ).pack(fill="x")

    def _atualizar_saldo(self):
        """Atualiza o saldo exibido no header."""
        saldo_color = Theme.SUCCESS if self.conta.saldo >= 0 else Theme.ERROR
        self.saldo_label.configure(
            text=f"Saldo: R$ {self.conta.saldo:,.2f}", text_color=saldo_color
        )

    def _voltar(self):
        """Volta ao dashboard do cliente."""
        self.controller.service.conta_ativa = None
        self.controller.show_frame("dashboard", cliente=self.cliente)

