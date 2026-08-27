import sys


def main():
    if "--cli" in sys.argv:
        # ── Modo CLI (legado) ──────────────────────────────
        from src.services.banco_service import BancoService
        from src.views.cli_view import CLIView
        from rich.prompt import Prompt, FloatPrompt, IntPrompt
        from rich import print
        from pwinput import pwinput

        service = BancoService()
        view = CLIView()

        while True:
            opcao_inicial = view.menu_inicial()

            if opcao_inicial == "1":
                # Login
                view.limpar_tela()
                view.exibir_banner()
                cpf = Prompt.ask("[bold cyan]Digite seu CPF[/bold cyan]")
                print(f"[bold cyan]Digite sua senha[/bold cyan]", end="")
                senha = pwinput(": ")

                sucesso, msg, cliente = service.autenticar(cpf, senha)
                if not sucesso:
                    view.exibir_erro(msg)
                    view.pausar()
                    continue

                view.exibir_sucesso(msg)
                view.pausar()

                # Loop do Cliente Logado
                while service.cliente_autenticado:
                    opcao_cliente = view.menu_cliente(cliente.nome)

                    if opcao_cliente == "1":
                        # Selecionar Conta
                        contas = service.obter_contas_cliente(cliente.cpf)
                        if not contas:
                            view.exibir_erro(
                                "Você não possui contas. Abra uma nova conta primeiro."
                            )
                            view.pausar()
                            continue

                        view.exibir_tabela_contas(contas)
                        numero_conta = IntPrompt.ask(
                            "\nDigite o número da conta que deseja acessar"
                        )
                        sucesso_conta, msg_conta, conta = service.selecionar_conta(
                            numero_conta
                        )

                        if not sucesso_conta:
                            view.exibir_erro(msg_conta)
                            view.pausar()
                            continue

                        # Loop de Operações na Conta Ativa
                        while service.conta_ativa:
                            op_conta = view.menu_conta(service.conta_ativa)

                            if op_conta == "1":
                                # Depósito
                                valor = FloatPrompt.ask("Valor do depósito (R$)")
                                sucesso_op, msg_op = service.realizar_deposito(valor)
                                if sucesso_op:
                                    view.exibir_sucesso(msg_op)
                                else:
                                    view.exibir_erro(msg_op)
                                view.pausar()

                            elif op_conta == "2":
                                # Saque
                                valor = FloatPrompt.ask("Valor do saque (R$)")
                                sucesso_op, msg_op = service.realizar_saque(valor)
                                if sucesso_op:
                                    view.exibir_sucesso(msg_op)
                                else:
                                    view.exibir_erro(msg_op)
                                view.pausar()

                            elif op_conta == "3":
                                # Transferência
                                num_destino = IntPrompt.ask(
                                    "Número da conta de destino"
                                )
                                valor = FloatPrompt.ask(
                                    "Valor da transferência (R$)"
                                )
                                sucesso_op, msg_op = (
                                    service.realizar_transferencia(num_destino, valor)
                                )
                                if sucesso_op:
                                    view.exibir_sucesso(msg_op)
                                else:
                                    view.exibir_erro(msg_op)
                                view.pausar()

                            elif op_conta == "4":
                                # Extrato
                                view.exibir_extrato(service.conta_ativa)
                                view.pausar()

                            elif op_conta == "5":
                                # Rendimento Poupança
                                sucesso_op, msg_op = (
                                    service.aplicar_rendimento_poupanca()
                                )
                                if sucesso_op:
                                    view.exibir_sucesso(msg_op)
                                else:
                                    view.exibir_erro(msg_op)
                                view.pausar()

                            elif op_conta == "0":
                                service.conta_ativa = None

                    elif opcao_cliente == "2":
                        # Abrir Nova Conta
                        tipo = Prompt.ask(
                            "Qual tipo de conta deseja abrir? [1] Corrente | [2] Poupança",
                            choices=["1", "2"],
                            default="1",
                        )
                        tipo_nome = "CORRENTE" if tipo == "1" else "POUPANCA"
                        sucesso_abertura, msg_abertura, _ = service.abrir_conta(
                            cliente.cpf, tipo_nome
                        )
                        if sucesso_abertura:
                            view.exibir_sucesso(msg_abertura)
                        else:
                            view.exibir_erro(msg_abertura)
                        view.pausar()

                    elif opcao_cliente == "3":
                        # Listar Contas
                        contas = service.obter_contas_cliente(cliente.cpf)
                        view.limpar_tela()
                        view.exibir_banner()
                        view.exibir_tabela_contas(contas)
                        view.pausar()

                    elif opcao_cliente == "0":
                        service.deslogar()
                        view.exibir_sucesso("Logout realizado com sucesso.")
                        view.pausar()

            elif opcao_inicial == "2":
                # Cadastro de Novo Cliente
                view.limpar_tela()
                view.exibir_banner()
                nome = Prompt.ask("[bold cyan]Nome Completo[/bold cyan]")
                cpf = Prompt.ask(
                    "[bold cyan]CPF (somente números ou com pontuação)[/bold cyan]"
                )
                print(f"[bold cyan]Crie uma Senha[/bold cyan]", end="")
                senha = pwinput(": ")

                sucesso_cad, msg_cad = service.cadastrar_cliente(nome, cpf, senha)
                if sucesso_cad:
                    view.exibir_sucesso(msg_cad)
                    abrir = Prompt.ask(
                        "Deseja abrir sua primeira conta agora?",
                        choices=["s", "n"],
                        default="s",
                    )
                    if abrir == "s":
                        tipo = Prompt.ask(
                            "Tipo de conta: [1] Corrente | [2] Poupança",
                            choices=["1", "2"],
                            default="1",
                        )
                        tipo_str = "CORRENTE" if tipo == "1" else "POUPANCA"
                        _, msg_abertura, _ = service.abrir_conta(cpf, tipo_str)
                        view.exibir_sucesso(msg_abertura)
                else:
                    view.exibir_erro(msg_cad)
                view.pausar()

            elif opcao_inicial == "0":
                view.limpar_tela()
                view.exibir_banner()
                view.console.print(
                    "\n[bold cyan]Obrigado por utilizar o Sistema de Gestão Bancária. Até logo![/bold cyan]\n"
                )
                break
    else:
        # ── Modo GUI (padrão) ──────────────────────────────
        from src.views.gui.app import BancoApp

        app = BancoApp()
        app.mainloop()


if __name__ == "__main__":
    main()