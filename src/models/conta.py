from src.models.transacao import Transacao

class Conta:
    def __init__(self, numero: int, titular_cpf: str, saldo: float = 0.0, extrato: list = None):
        self.numero = numero
        self.titular_cpf = titular_cpf
        self.saldo = saldo
        self.extrato = extrato if extrato is not None else []

    def depositar(self, valor: float, descricao: str = "Depósito") -> bool:
        if valor <= 0:
            return False
        self.saldo += valor
        transacao = Transacao(tipo="DEPOSITO", valor=valor, descricao=descricao)
        self.adicionar_transacao(transacao)
        return True

    def sacar(self, valor: float, descricao: str = "Saque") -> bool:
        if valor <= 0 or valor > self.saldo:
            return False
        self.saldo -= valor
        transacao = Transacao(tipo="SAQUE", valor=valor, descricao=descricao)
        self.adicionar_transacao(transacao)
        return True

    def adicionar_transacao(self, transacao: Transacao):
        self.extrato.append(transacao)

    def to_dict(self) -> dict:
        return {
            "numero": self.numero,
            "titular_cpf": self.titular_cpf,
            "saldo": self.saldo,
            "extrato": [t.to_dict() for t in self.extrato]
        }


class ContaCorrente(Conta):
    def __init__(self, numero: int, titular_cpf: str, saldo: float = 0.0, extrato: list = None, limite: float = 500.0):
        super().__init__(numero=numero, titular_cpf=titular_cpf, saldo=saldo, extrato=extrato)
        self.limite = limite

    def sacar(self, valor: float, descricao: str = "Saque") -> bool:
        saldo_disponivel = self.saldo + self.limite
        if valor <= 0 or valor > saldo_disponivel:
            return False
        self.saldo -= valor
        transacao = Transacao(tipo="SAQUE", valor=valor, descricao=descricao)
        self.adicionar_transacao(transacao)
        return True

    def to_dict(self) -> dict:
        dados = super().to_dict()
        dados["tipo"] = "CORRENTE"
        dados["limite"] = self.limite
        return dados

    @classmethod
    def from_dict(cls, dados: dict):
        extrato = [Transacao.from_dict(t) for t in dados.get("extrato", [])]
        return cls(
            numero=dados["numero"],
            titular_cpf=dados["titular_cpf"],
            saldo=dados["saldo"],
            extrato=extrato,
            limite=dados.get("limite", 500.0)
        )


class ContaPoupanca(Conta):
    def __init__(self, numero: int, titular_cpf: str, saldo: float = 0.0, extrato: list = None, taxa_rendimento: float = 0.005):
        super().__init__(numero=numero, titular_cpf=titular_cpf, saldo=saldo, extrato=extrato)
        self.taxa_rendimento = taxa_rendimento

    def render_juros(self) -> float:
        if self.saldo <= 0:
            return 0.0
        rendimento = self.saldo * self.taxa_rendimento
        self.saldo += rendimento
        transacao = Transacao(tipo="RENDIMENTO", valor=rendimento, descricao="Rendimento de Poupança")
        self.adicionar_transacao(transacao)
        return rendimento

    def to_dict(self) -> dict:
        dados = super().to_dict()
        dados["tipo"] = "POUPANCA"
        dados["taxa_rendimento"] = self.taxa_rendimento
        return dados

    @classmethod
    def from_dict(cls, dados: dict):
        extrato = [Transacao.from_dict(t) for t in dados.get("extrato", [])]
        return cls(
            numero=dados["numero"],
            titular_cpf=dados["titular_cpf"],
            saldo=dados["saldo"],
            extrato=extrato,
            taxa_rendimento=dados.get("taxa_rendimento", 0.005)
        )
