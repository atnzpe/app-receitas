# 🍳 Guia Mestre de Receitas (App de Receitas Culinárias)

Este é um aplicativo multiplataforma (Desktop e Android) para organização e descoberta de receitas culinárias, construído com Python e Flet Framework.

O projeto segue uma arquitetura **MVVM (Model-View-ViewModel)** rigorosa e um design **Offline-First**, garantindo que o aplicativo funcione perfeitamente sem conexão com a internet, utilizando um banco de dados local SQLite.

**Visão Geral:** O objetivo é criar um organizador de receitas centralizado, permitindo importação de múltiplas fontes e descoberta baseada em ingredientes. As funcionalidades planejadas incluem gerenciamento completo (CRUD) de Receitas, Ingredientes, Categorias, Fornecedores (para listas de compras), Links de Mercados parceiros, e edição de perfil de usuário.

![Screenshot do Dashboard do App de Receitas no tema claro](https://i.imgur.com/your-dashboard-image.png)

## 🗺️ Roadmap do Projeto

Nosso plano de desenvolvimento detalhado e o status atual das Sprints estão em nosso [**ROADMAP.md**](ROADMAP.md).

## 🛠️ Stack de Tecnologia

* **Linguagem:** Python 3.10+
* **Framework UI:** Flet (baseado em Flutter)
* **Banco de Dados Local:** SQLite (Offline-First)
* **Segurança:** `bcrypt` para hashing de senhas.
* **Padrão de Arquitetura:** MVVM (Model-View-ViewModel)

## 🏛️ Arquitetura do Projeto

O código é estritamente separado nas seguintes camadas:

* `/src/models`: Data Models (dataclasses) para `User`, `Recipe`, etc.
* `/src/database`: Lógica de acesso ao banco de dados (conexão e queries).
* `/src/viewmodels`: Lógica de estado e apresentação (sem dependência direta de Flet).
* `/src/views`: Definição da UI (controles Flet) e componentes reutilizáveis.
* `/src/utils`: Código auxiliar (logging, temas, constantes de design).
* `/main.py`: Ponto de entrada, configuração e roteamento.

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