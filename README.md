# 🍳 Guia Mestre de Receitas (App de Receitas Culinárias)

Este é um aplicativo multiplataforma (Desktop e Android) para organização e descoberta de receitas culinárias, construído com Python e Flet Framework.

O projeto segue uma arquitetura **MVVM (Model-View-ViewModel)** rigorosa e um design **Offline-First**, garantindo que o aplicativo funcione perfeitamente sem conexão com a internet, utilizando um banco de dados local SQLite.

## 🗺️ Roadmap do Projeto

Nosso plano de desenvolvimento e o status atual das Sprints estão detalhados em nosso [**ROADMAP.md**](ROADMAP.md).

## 🛠️ Stack de Tecnologia

* **Linguagem:** Python 3.10+
* **Framework UI:** Flet (baseado em Flutter)
* **Banco de Dados Local:** SQLite (Offline-First)
* **Segurança:** `bcrypt` para hashing de senhas.
* **Padrão de Arquitetura:** MVVM (Model-View-ViewModel)

## 🏛️ Arquitetura do Projeto

O código é estritamente separado nas seguintes camadas para garantir desacoplamento e testabilidade:

* `/src/models`: Contém os Data Models (dataclasses) que representam nossos dados (ex: `recipe_model.py`, `user_model.py`).
* `/src/database`: Contém a lógica de acesso ao banco de dados (`database.py` para conexão, `auth_queries.py` para autenticação).
* `/src/viewmodels`: Contém a lógica de estado e apresentação. O ViewModel *não conhece* a View (ex: `login_viewmodel.py`).
* `/src/views`: Contém a definição da UI (os controles Flet) e componentes reutilizáveis. A View *conhece* o ViewModel.
* `/main.py`: Ponto de entrada da aplicação, responsável pela configuração inicial e pelo roteamento de telas.

## 🏃 Como Executar o Projeto

1.  Clone o repositório:
    ```bash
    git clone [https://github.com/atnzpe/app-receitas.git](https://github.com/atnzpe/app-receitas.git)
    cd app-receitas
    ```

2.  Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4.  Execute o aplicativo:
    ```bash
    python main.py
    ```

5.  Execute os testes:
    ```bash
    python -m unittest discover tests
    ```