# 🍳 Guia Mestre de Receitas

![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow) ![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Flet](https://img.shields.io/badge/Flet-Cross_Platform-purple) ![License](https://img.shields.io/badge/License-MIT-green)

Aplicativo profissional para organização e descoberta de receitas culinárias, desenvolvido com arquitetura **Offline-First**, foco em alta performance, integridade de dados e UX moderna.

**Conceito:** O app atua como uma rede social culinária, agregando receitas nativas e de múltiplos usuários, mas mantendo a estética e organização de um livro de receitas clássico e pessoal.

## 🚀 Visão do Produto

Um hub centralizado para gestão culinária que permite importar receitas, gerenciar despensa e planejar compras. O ecossistema integra tanto **receitas nativas** (curadoria do app) quanto **receitas da comunidade** (outros usuários).

O sistema é projetado para ser resiliente, funcionando sem internet e sincronizando quando possível em uma base de dados gratuita e sustentável (visão de futuro).

**Plataformas Alvo:**
* 🖥️ **Desktop:** Windows (`.exe`)
* 📱 **Mobile:** Android (`.apk`)

## 🗺️ Roadmap e Status

Acompanhe o progresso detalhado das Sprints e o cronograma de implementação acessando nosso [**ROADMAP.md**](ROADMAP.md).

## 🏛️ Arquitetura Técnica (Military Grade)

O projeto segue rigorosamente o padrão **MVVM (Model-View-ViewModel)** com uma camada de **Core** blindada para prevenção de erros ("Fail-Fast").

### Stack Tecnológico
* **Linguagem:** Python 3.10+
* **UI Framework:** [Flet](https://flet.dev) (Baseado em Flutter)
* **Banco de Dados:** SQLite (Transacional, FKs ativas)
* **Segurança:** `bcrypt` (Hashing), `Pydantic V2` (Validação de Dados)
* **Observabilidade:** Logs estruturados com rotação diária.

### Estrutura de Diretórios
```text
/src
|-- /core       # Núcleo blindado (Logger, Exceptions, Configs)
|-- /models     # Modelos de dados com validação Pydantic V2
|-- /database   # Persistência, Queries SQL otimizadas e Migrations
|-- /viewmodels # Lógica de estado e regras de negócio (sem UI direta)
|-- /views      # Interface do usuário (Widgets Flet e Componentes)
|-- /utils      # Temas, constantes e auxiliares
```

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