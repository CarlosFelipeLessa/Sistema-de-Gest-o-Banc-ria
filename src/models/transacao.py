from datetime import datetime

class Transacao:
    def __init__(self, tipo: str, valor: float, descricao: str = "", data_hora: str = None):
        self.tipo = tipo # Ex "Deposito", "Saque", "Transferencia"
        self.valor = valor
        self.descricao = descricao
        self.data_hora = data_hora or datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def to_dict(self) -> dict:
        """
        converte o objeto para dicionário para salver no JSON.
        """
        return{
            "tipo": self.tipo,
            "valor": self.valor,
            "descricao": self.descricao,
            "data_hora": self.data_hora
        }

    @classmethod
    def from_dict(cls,dados:dict):
        """
        Reconstrói uma instacia de transacao a partir de um dicionário do JSON.
        """
        return cls(
            tipo = dados["tipo"],
            valor = dados["valor"],
            descricao = dados.get("descricao",""),
            data_hora = dados.get("data_hora")
        )

    def __repr__(self):
        return f"<transacao {self.tipo}: R$ {self.valor:.2f} em {self.data_hora}>"


   