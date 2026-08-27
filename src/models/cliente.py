class Cliente:
    def __init__(self, nome: str, cpf: str, senha: str, contas: list = None):
        self.nome = nome.strip().title()
        self.cpf = cpf.strip().replace(".", "").replace("-", "")
        self.senha = senha
        self.contas = contas if contas is not None else []

    def adicionar_conta(self, numero_conta: int):
        if numero_conta not in self.contas:
            self.contas.append(numero_conta)

    def autenticar(self, senha: str) -> bool:
        return self.senha == senha

    def to_dict(self) -> dict:
        return {
            "nome": self.nome,
            "cpf": self.cpf,
            "senha": self.senha,
            "contas": self.contas
        }

    @classmethod
    def from_dict(cls, dados: dict):
        return cls(
            nome=dados["nome"],
            cpf=dados["cpf"],
            senha=dados["senha"],
            contas=dados.get("contas", [])
        )

    def __repr__(self):
        return f"<Cliente {self.nome} (CPF: {self.cpf}) - Contas: {self.contas}>"



