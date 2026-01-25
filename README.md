# **🍳 Guia Mestre de Receitas**

Aplicativo profissional para organização e descoberta de receitas culinárias, desenvolvido com arquitetura **Offline-First**, foco em alta performance, integridade de dados e UX moderna.

**Conceito:** O app atua como uma rede social culinária, agregando receitas nativas e de múltiplos usuários, mas mantendo a estética e organização de um livro de receitas clássico e pessoal.


## **🚀 Funcionalidades Entregues**

* 🔐 **Autenticação Segura:** Login e Registro com hash bcrypt.
* 📊 **Dashboard Interativo:** Navegação rápida e temas adaptáveis (Claro/Escuro).
* 🏷️ **Gestão de Categorias:** Sistema híbrido com categorias nativas (sistema) e personalizadas (usuário).
* 🥘 **Gestão Completa de Receitas (CRUD):**
  * Criação manual com ingredientes dinâmicos.
  * Edição e Exclusão segura (apenas para o autor).
  * Sistema de Favoritos integrado à listagem.
  * Feedback visual robusto (Modais e Alertas).

## **🏛️ Arquitetura Técnica (Military Grade)**

O projeto segue rigorosamente o padrão **MVVM (Model-View-ViewModel)** com uma camada de **Core** blindada para prevenção de erros ("Fail-Fast").

### **Stack Tecnológico**

* **Linguagem:** Python 3.10+
* **UI Framework:** [Flet](https://flet.dev) (Baseado em Flutter)
* **Banco de Dados Local:** SQLite (Transacional, FKs ativas)
* **Segurança:** bcrypt (Hashing), Pydantic V2 (Validação de Dados)
* **Observabilidade:** Logs estruturados com rotação diária.

### **Estrutura de Diretórios**

/src
|-- /core       # Núcleo blindado (Logger, Exceptions, Configs)
|-- /models     # Modelos de dados com validação Pydantic V2
|-- /database   # Persistência, Queries SQL otimizadas e Migrations
|-- /viewmodels # Lógica de estado e regras de negócio (sem UI direta)
|-- /views      # Interface do usuário (Widgets Flet e Componentes)
|-- /utils      # Temas, constantes e auxiliares

## **⚙️ Fluxo de Desenvolvimento (Git Flow)**

Adotamos um fluxo estrito para garantir a estabilidade do código:

1. **main (Production):** Código estável, versionado e pronto para deploy.
2. **homolog (Staging):** Branch de integração. Todo PR é testado aqui antes da main.
3. **feat/... (Development):** Branches efêmeras para novas funcionalidades.
4. **fix/... (Hotfixes):** Correções urgentes.

## **🏃 Como Executar (Ambiente de Dev)**

1. **Clone o repositório:**
   git clone [https://github.com/atnzpe/app-receitas.git](https://github.com/atnzpe/app-receitas.git)
   cd app-receitas

2. **Prepare o ambiente virtual:**

   # Windows

   python -m venv venv
   .\venv\Scripts\activate

   # Linux/Mac

   python3 -m venv venv
   source venv/bin/activate

3. **Instale as dependências:**
   pip install -r requirements.txt

4. **Execute a aplicação:**
   python main.py

5. **Execute os testes:**
   python -m unittest discover tests

## **🗺️ Roadmap e Status**

Acompanhe o progresso detalhado das Sprints e o cronograma de implementação acessando nosso [**ROADMAP.md**](ROADMAP.md).
