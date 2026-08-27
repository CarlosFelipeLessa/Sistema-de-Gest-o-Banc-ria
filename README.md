# 🏦 Sistema de Gestão Bancária e Financeira (CLI)

Sistema de terminal interativo para gestão de contas bancárias, clientes e transações financeiras, desenvolvido em **Python** utilizando **Programação Orientada a Objetos (POO)**, persistência em **JSON** e interface estilizada com a biblioteca **Rich**.

---

## 📌 Visão Geral do Projeto

O objetivo deste projeto é construir uma aplicação de console robusta e modular que simula o funcionamento de uma instituição bancária, aplicando boas práticas de engenharia de software, separação de responsabilidades em camadas e validação de regras de negócio.

---

## 🚀 Funcionalidades (MVP)

- **Gestão de Clientes e Contas:**
  - Cadastro de novos clientes com validação de dados básicos (Nome, CPF).
  - Abertura de contas (`Conta Corrente` e `Conta Poupança`).
  - Autenticação e seleção de conta ativa.

- **Operações Bancárias:**
  - **Depósito:** Crédito em conta com registro imediato no histórico.
  - **Saque:** Validação de saldo disponível e limite de cheque especial.
  - **Transferência:** Movimentação entre contas cadastradas com verificação de destino e saldo.
  - **Extrato Detalhado:** Tabela interativa formatada com `Rich`, exibindo data/hora, tipo de operação, descrição e valores coloridos (verde para entradas, vermelho para saídas).

- **Persistência de Dados:**
  - Leitura e gravação automática em arquivo `JSON` local a cada transação realizada.

---

## 🏗️ Arquitetura e Modelagem de Classes (POO)

O projeto segue a divisão em camadas para garantir baixo acoplamento e facilidade de manutenção:

```text
               ┌───────────────┐
               │    Cliente    │
               ├───────────────┤
               │ - nome: str   │
               │ - cpf: str    │
               │ - contas: []  │
               └───────┬───────┘
                       │ 1..*
                       ▼
               ┌───────────────┐
               │     Conta     │ (Base)
               ├───────────────┤
               │ - numero: int │
               │ - saldo: float│
               │ - extrato: [] │
               └───────┬───────┘
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
┌───────────────────┐     ┌───────────────────┐
│   ContaCorrente   │     │   ContaPoupanca   │
├───────────────────┤     ├───────────────────┤
│ - limite: float   │     │ - rendimento: flt │
└───────────────────┘     └───────────────────┘
```

### Detalhamento das Entidades:
* **`Transacao` (`src/models/transacao.py`):** Modela as movimentações financeiras com data/hora, tipo (`DEPOSITO`, `SAQUE`, `TRANSFERENCIA`), valor e descrição.
* **`Conta` (`src/models/conta.py`):** Classe base com métodos essenciais (`depositar`, `sacar`, `adicionar_transacao`).
* **`ContaCorrente` e `ContaPoupanca`:** Especializações que implementam regras específicas (como limite adicional ou rendimento).
* **`Cliente` (`src/models/cliente.py`):** Modela o titular e suas respectivas contas associadas.
* **`BancoService` (`src/services/banco_service.py`):** Centraliza as regras de negócio, autenticação e orquestração de transferências entre contas.
* **`JSONStorage` (`src/storage/json_storage.py`):** Gerencia a serialização (`to_dict`) e desserialização (`from_dict`) dos dados para o arquivo JSON.
* **`CLIView` (`src/views/cli_view.py`):** Responsável exclusivamente pela interface visual no terminal utilizando os componentes do `Rich` (`Panel`, `Table`, `Prompt`, `Console`).

---

## 📁 Estrutura do Repositório

```text
Sistema-de-Gest-o-Banc-ria/
│
├── data/
│   └── database.json          # Base de dados em JSON
│
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── transacao.py
│   │   ├── conta.py
│   │   └── cliente.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── banco_service.py
│   │
│   ├── storage/
│   │   ├── __init__.py
│   │   └── json_storage.py
│   │
│   └── views/
│       ├── __init__.py
│       └── cli_view.py
│
├── main.py                    # Ponto de entrada da aplicação
├── requirements.txt           # Dependências do projeto (rich)
├── .gitignore                 # Arquivos ignorados pelo Git
└── README.md                  # Documentação principal
```

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- **Rich** (Formatação avançada de terminal, tabelas e painéis)
- **JSON** (Persistência leve de dados)

---

## 📋 Como Executar o Projeto

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/CarlosFelipeLessa/Sistema-de-Gest-o-Banc-ria.git
   cd Sistema-de-Gest-o-Banc-ria
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv venv
   # No Windows:
   venv\Scripts\activate
   # No Linux/macOS:
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação:**
   ```bash
   python main.py
   ```

---

## 🎯 Roteiro de Desenvolvimento (Checklist)

- [x] **Etapa 1:** Criação da estrutura de pastas e arquivo `requirements.txt`.
- [x] **Etapa 2:** Implementação das classes de modelo (`Cliente`, `Conta`, `ContaCorrente`, `ContaPoupanca`, `Transacao`).
- [x] **Etapa 3:** Implementação da camada de armazenamento (`JSONStorage`).
- [x] **Etapa 4:** Implementação dos serviços de negócio e validações (`BancoService`).
- [x] **Etapa 5:** Construção das telas e tabelas com `Rich` (`CLIView`) e fluxo em `main.py`.
- [x] **Etapa 6:** Testes manuais de fluxo completo (depósito, saque, transferência, persistência).
- [ ] **Etapa 7:** Inserção de capturas de tela/GIF demonstrativo no `README.md`.
- [ ] **Etapa 8:** Criptografia de senhas adicionadas ao banco de dados usando hash.

