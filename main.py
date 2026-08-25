from src.models.transacao import *

if __name__ == "__main__":
    # Teste de criação
    t1 = Transacao(tipo="DEPOSITO", valor=150.0, descricao="Depósito inicial")
    print(t1)
    
    # Teste de conversão para dicionário (JSON)
    dicionario = t1.to_dict()
    print("Dicionário:", dicionario)
    
    # Teste de reconstrução
    t2 = Transacao.from_dict(dicionario)
    print("Reconstruído:", t2)