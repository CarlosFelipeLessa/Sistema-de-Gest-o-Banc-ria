from typing import List, Dict, Optional, Tuple
from src.models.cliente import Cliente
from src.models.conta import Conta, ContaCorrente, ContaPoupanca
from src.storage.json_storage import JSONStorage

class BancoService:
    def __init__(self, storage: Optional[JSONStorage] = None):
        self.storage = storage or JSONStorage()
        self.clientes, self.contas = self.storage.carregar_dados()
        self.cliente_autenticado: Optional[Cliente] = None
        self.conta_ativa: Optional[Conta] = None

    def _salvar(self):
        """Salva o estado atual das listas no banco de dados JSON."""
        self.storage.salvar_dados(self.clientes, self.contas)

    def _gerar_proximo_numero_conta(self) -> int:
        """Gera um número sequencial único para novas contas."""
        if not self.contas:
            return 1001
        return max(self.contas.keys()) + 1

    def buscar_cliente_por_cpf(self, cpf: str) -> Optional[Cliente]:
        cpf_limpo = cpf.strip().replace(".", "").replace("-", "")
        for cliente in self.clientes:
            if cliente.cpf == cpf_limpo:
                return cliente
        return None

    def buscar_conta_por_numero(self, numero: int) -> Optional[Conta]:
        return self.contas.get(numero)

    def cadastrar_cliente(self, nome: str, cpf: str, senha: str) -> Tuple[bool, str]:
        if not nome.strip() or not cpf.strip() or not senha.strip():
            return False, "Todos os campos são obrigatórios."

        if self.buscar_cliente_por_cpf(cpf):
            return False, "Já existe um cliente cadastrado com este CPF."

        novo_cliente = Cliente(nome=nome, cpf=cpf, senha=senha)
        self.clientes.append(novo_cliente)
        self._salvar()
        return True, "Cliente cadastrado com sucesso!"

    def abrir_conta(self, cpf: str, tipo_conta: str) -> Tuple[bool, str, Optional[Conta]]:
        cliente = self.buscar_cliente_por_cpf(cpf)
        if not cliente:
            return False, "Cliente não encontrado.", None

        numero_conta = self._gerar_proximo_numero_conta()
        tipo_normalizado = tipo_conta.strip().upper()

        if tipo_normalizado in ["CORRENTE", "1"]:
            nova_conta = ContaCorrente(numero=numero_conta, titular_cpf=cliente.cpf)
        elif tipo_normalizado in ["POUPANCA", "POUPANÇA", "2"]:
            nova_conta = ContaPoupanca(numero=numero_conta, titular_cpf=cliente.cpf)
        else:
            return False, "Tipo de conta inválido. Escolha Corrente ou Poupança.", None

        self.contas[numero_conta] = nova_conta
        cliente.adicionar_conta(numero_conta)
        self._salvar()

        nome_tipo = "Corrente" if isinstance(nova_conta, ContaCorrente) else "Poupança"
        return True, f"Conta {nome_tipo} nº {numero_conta} aberta com sucesso!", nova_conta

    def autenticar(self, cpf: str, senha: str) -> Tuple[bool, str, Optional[Cliente]]:
        cliente = self.buscar_cliente_por_cpf(cpf)
        if not cliente:
            return False, "Cliente não encontrado.", None

        if not cliente.autenticar(senha):
            return False, "Senha incorreta.", None

        self.cliente_autenticado = cliente
        self.conta_ativa = None
        return True, f"Bem-vindo(a), {cliente.nome}!", cliente

    def deslogar(self):
        self.cliente_autenticado = None
        self.conta_ativa = None

    def obter_contas_cliente(self, cpf: str) -> List[Conta]:
        cliente = self.buscar_cliente_por_cpf(cpf)
        if not cliente:
            return []
        return [self.contas[num] for num in cliente.contas if num in self.contas]

    def selecionar_conta(self, numero_conta: int) -> Tuple[bool, str, Optional[Conta]]:
        if not self.cliente_autenticado:
            return False, "Nenhum cliente autenticado.", None

        if numero_conta not in self.cliente_autenticado.contas:
            return False, "Esta conta não pertence ao cliente autenticado.", None

        conta = self.buscar_conta_por_numero(numero_conta)
        if not conta:
            return False, "Conta não encontrada.", None

        self.conta_ativa = conta
        return True, f"Conta nº {numero_conta} selecionada com sucesso.", conta

    def realizar_deposito(self, valor: float) -> Tuple[bool, str]:
        if not self.conta_ativa:
            return False, "Nenhuma conta ativa selecionada."

        if valor <= 0:
            return False, "O valor do depósito deve ser maior que zero."

        sucesso = self.conta_ativa.depositar(valor, descricao="Depósito em Dinheiro/PIX")
        if sucesso:
            self._salvar()
            return True, f"Depósito de R$ {valor:.2f} realizado com sucesso!"
        return False, "Não foi possível realizar o depósito."

    def realizar_saque(self, valor: float) -> Tuple[bool, str]:
        if not self.conta_ativa:
            return False, "Nenhuma conta ativa selecionada."

        if valor <= 0:
            return False, "O valor do saque deve ser maior que zero."

        sucesso = self.conta_ativa.sacar(valor, descricao="Saque em Terminal")
        if sucesso:
            self._salvar()
            return True, f"Saque de R$ {valor:.2f} realizado com sucesso!"
        return False, "Saldo insuficiente para realizar o saque."

    def realizar_transferencia(self, numero_destino: int, valor: float) -> Tuple[bool, str]:
        if not self.conta_ativa:
            return False, "Nenhuma conta ativa selecionada."

        if self.conta_ativa.numero == numero_destino:
            return False, "A conta de destino não pode ser igual à conta de origem."

        if valor <= 0:
            return False, "O valor da transferência deve ser maior que zero."

        conta_destino = self.buscar_conta_por_numero(numero_destino)
        if not conta_destino:
            return False, f"Conta de destino nº {numero_destino} não encontrada."

        # Tenta debitar da conta de origem
        sucesso_debito = self.conta_ativa.sacar(valor, descricao=f"Transferência enviada para Conta {numero_destino}")
        if not sucesso_debito:
            return False, "Saldo insuficiente para transferir este valor."

        # Credita na conta de destino
        conta_destino.depositar(valor, descricao=f"Transferência recebida da Conta {self.conta_ativa.numero}")
        self._salvar()

        return True, f"Transferência de R$ {valor:.2f} para a Conta {numero_destino} realizada com sucesso!"

    def aplicar_rendimento_poupanca(self) -> Tuple[bool, str]:
        if not self.conta_ativa:
            return False, "Nenhuma conta ativa selecionada."

        if not isinstance(self.conta_ativa, ContaPoupanca):
            return False, "Rendimento aplicável apenas para Conta Poupança."

        rendimento = self.conta_ativa.render_juros()
        if rendimento > 0:
            self._salvar()
            return True, f"Rendimento de R$ {rendimento:.2f} aplicado com sucesso!"
        return False, "Saldo zerado ou negativo, nenhum rendimento aplicado."