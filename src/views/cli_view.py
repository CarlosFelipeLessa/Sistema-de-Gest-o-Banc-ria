from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, FloatPrompt, IntPrompt
from rich.align import Align
from rich.text import Text
from typing import List
from src.models.conta import Conta, ContaCorrente, ContaPoupanca

class CLIView:
    def __init__(self):
        self.console = Console()

    def limpar_tela(self):
        self.console.clear()

    def exibir_banner(self):
        banner_text = Text("🏦 SISTEMA DE GESTÃO BANCÁRIA", style="bold cyan")
        sub_text = Text("Python POO • Persistência JSON • Rich CLI", style="dim white")
        self.console.print(Panel(Align.center(banner_text + "\n" + sub_text), border_style="cyan"))

    def menu_inicial(self) -> str:
        self.limpar_tela()
        self.exibir_banner()
        opcoes = (
            "[bold cyan][1][/bold cyan] Entrar (Login)\n"
            "[bold cyan][2][/bold cyan] Cadastrar Novo Cliente\n"
            "[bold red][0][/bold red] Sair do Sistema"
        )
        self.console.print(Panel(opcoes, title="[bold white]Menu Inicial[/bold white]", border_style="blue"))
        return Prompt.ask("Escolha uma opção", choices=["1", "2", "0"], default="1")

    def menu_cliente(self, nome_cliente: str) -> str:
        self.limpar_tela()
        self.exibir_banner()
        opcoes = (
            "[bold cyan][1][/bold cyan] Acessar/Operar em uma Conta\n"
            "[bold cyan][2][/bold cyan] Abrir Nova Conta Bancária\n"
            "[bold cyan][3][/bold cyan] Listar Minhas Contas\n"
            "[bold red][0][/bold red] Deslogar (Voltar)"
        )
        titulo = f"[bold green]Cliente: {nome_cliente}[/bold green]"
        self.console.print(Panel(opcoes, title=titulo, border_style="green"))
        return Prompt.ask("Escolha uma opção", choices=["1", "2", "3", "0"], default="1")

    def menu_conta(self, conta: Conta) -> str:
        self.limpar_tela()
        self.exibir_banner()

        tipo_nome = "Conta Corrente" if isinstance(conta, ContaCorrente) else "Conta Poupança"
        info_extra = f" | Limite: R$ {conta.limite:.2f}" if isinstance(conta, ContaCorrente) else f" | Rendimento: {conta.taxa_rendimento*100:.1f}% a.m."
        
        cabecalho_conta = f"[bold yellow]{tipo_nome} nº {conta.numero}[/bold yellow]\n[bold green]Saldo Atual: R$ {conta.saldo:.2f}[/bold green]{info_extra}"
        self.console.print(Panel(cabecalho_conta, border_style="yellow"))

        opcoes = (
            "[bold cyan][1][/bold cyan] Realizar Depósito\n"
            "[bold cyan][2][/bold cyan] Realizar Saque\n"
            "[bold cyan][3][/bold cyan] Transferência (PIX/TED)\n"
            "[bold cyan][4][/bold cyan] Extrato Detalhado\n"
        )
        if isinstance(conta, ContaPoupanca):
            opcoes += "[bold cyan][5][/bold cyan] Simular Rendimento Mensal\n"
        opcoes += "[bold red][0][/bold red] Voltar ao Menu Anterior"

        self.console.print(Panel(opcoes, title="[bold white]Operações da Conta[/bold white]", border_style="blue"))
        opcoes_validas = ["1", "2", "3", "4", "5", "0"] if isinstance(conta, ContaPoupanca) else ["1", "2", "3", "4", "0"]
        return Prompt.ask("Escolha uma operação", choices=opcoes_validas, default="1")

    def exibir_tabela_contas(self, contas: List[Conta]):
        if not contas:
            self.console.print("[yellow]Você ainda não possui contas abertas neste banco.[/yellow]")
            return

        tabela = Table(title="Minhas Contas Bancárias", border_style="cyan", header_style="bold magenta")
        tabela.add_column("Número", justify="center", style="bold white")
        tabela.add_column("Tipo", justify="center")
        tabela.add_column("Saldo (R$)", justify="right", style="green")
        tabela.add_column("Detalhes", justify="left")

        for c in contas:
            tipo = "Corrente" if isinstance(c, ContaCorrente) else "Poupança"
            detalhe = f"Limite: R$ {c.limite:.2f}" if isinstance(c, ContaCorrente) else f"Rendimento: {c.taxa_rendimento*100:.1f}% a.m."
            tabela.add_row(str(c.numero), tipo, f"{c.saldo:.2f}", detalhe)

        self.console.print(tabela)

    def exibir_extrato(self, conta: Conta):
        self.limpar_tela()
        self.exibir_banner()

        tipo_nome = "Corrente" if isinstance(conta, ContaCorrente) else "Poupança"
        titulo = f"Extrato - {tipo_nome} nº {conta.numero}"
        tabela = Table(title=titulo, border_style="blue", header_style="bold cyan")

        tabela.add_column("Data/Hora", justify="center", style="dim white")
        tabela.add_column("Tipo", justify="center")
        tabela.add_column("Descrição", justify="left")
        tabela.add_column("Valor (R$)", justify="right")

        if not conta.extrato:
            tabela.add_row("-", "-", "Nenhuma movimentação realizada", "0.00")
        else:
            for t in conta.extrato:
                cor_tipo = "green" if t.tipo in ["DEPOSITO", "RENDIMENTO"] or "recebida" in t.descricao.lower() else "red"
                prefixo = "+" if cor_tipo == "green" else "-"
                tabela.add_row(
                    t.data_hora,
                    f"[{cor_tipo}]{t.tipo}[/{cor_tipo}]",
                    t.descricao,
                    f"[{cor_tipo}]{prefixo} R$ {t.valor:.2f}[/{cor_tipo}]"
                )

        self.console.print(tabela)
        self.console.print(f"\n[bold white]Saldo Atual:[/bold white] [bold green]R$ {conta.saldo:.2f}[/bold green]\n")

    def exibir_sucesso(self, mensagem: str):
        self.console.print(f"\n[bold green]✔ {mensagem}[/bold green]\n")

    def exibir_erro(self, mensagem: str):
        self.console.print(f"\n[bold red]✖ {mensagem}[/bold red]\n")

    def pausar(self):
        Prompt.ask("\nPressione [bold cyan]Enter[/bold cyan] para continuar...")