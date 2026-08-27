import json
import os
from typing import Tuple, List, Dict
from src.models.cliente import Cliente
from src.models.conta import Conta, ContaCorrente, ContaPoupanca

class JSONStorage:
    def __init__(self, caminho_arquivo: str = "data/database.json"):
        self.caminho_arquivo = caminho_arquivo

    def carregar_dados(self) -> Tuple[List[Cliente], Dict[int, Conta]]:
        """Lê o arquivo JSON e reconstrói as instâncias de Cliente e Conta."""
        if not os.path.exists(self.caminho_arquivo):
            return [], {}

        try:
            with open(self.caminho_arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return [], {}

        # Reconstruindo lista de clientes
        clientes = [Cliente.from_dict(c) for c in dados.get("clientes", [])]

        # Reconstruindo dicionário de contas (chave = numero da conta)
        contas = {}
        for c in dados.get("contas", []):
            tipo = c.get("tipo")
            if tipo == "CORRENTE":
                conta_obj = ContaCorrente.from_dict(c)
            elif tipo == "POUPANCA":
                conta_obj = ContaPoupanca.from_dict(c)
            else:
                continue
            contas[conta_obj.numero] = conta_obj

        return clientes, contas

    def salvar_dados(self, clientes: List[Cliente], contas: Dict[int, Conta]) -> bool:
        """Salva a lista de clientes e dicionário de contas no arquivo JSON."""
        pasta = os.path.dirname(self.caminho_arquivo)
        if pasta and not os.path.exists(pasta):
            os.makedirs(pasta, exist_ok=True)

        lista_contas = list(contas.values()) if isinstance(contas, dict) else contas

        payload = {
            "clientes": [c.to_dict() for c in clientes],
            "contas": [c.to_dict() for c in lista_contas]
        }

        try:
            with open(self.caminho_arquivo, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False

