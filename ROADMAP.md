# 🗺️ Roadmap do Projeto: Guia Mestre de Receitas

Este documento rastreia o progresso do desenvolvimento, onde estivemos, onde estamos e para onde vamos, com base no nosso Guia Mestre.

---

## ✅ Sprint 0: Fundação e Estrutura (Concluído)

* **Status:** Concluído
* **Entregas:** Arquitetura MVVM, Estrutura de diretórios, Configuração DB SQLite, Tabelas e Models iniciais, Testes DB.

---

## ✅ Sprint 1: Autenticação e Roteamento (Concluído)

* **Status:** Concluído
* **Entregas:** Tabela `users`, Model `User`, `auth_queries.py` (com `bcrypt`), Roteador (`ft.Router`), Views/ViewModels de Login/Registro, Feedback com Overlays (`SnackBar`), Testes de Autenticação.

---

## ✅ Sprint 2: UI do Dashboard e Temas (Concluído)

* **Status:** Concluído
* **Entregas:** Centralização de Estilos (`theme.py`), Temas claro/escuro, Componente `DashboardCard`, `DashboardView` (AppBar, GridView), Botão de troca de tema, `AlertDialog` para features futuras, Componente `AppFooter`, `SafeArea` (Mobile-First).

---

## 🎯 Sprint 3: CRUD de Cadastros Básicos (Próxima Etapa)

* **Status:** Próxima Etapa
* **Entregas:**
    * **CRUD Categorias:**
        * [ ] Criar a `CategoryView` (Listar, Adicionar, Editar, Excluir).
        * [ ] Desenvolver o `CategoryViewModel`.
        * [ ] Implementar `category_queries.py` (ou adicionar em `queries.py`).
        * [ ] Conectar navegação do Card "Cadastros" para a rota `/categories`.
    * **CRUD Fornecedores:**
        * [ ] Adicionar tabela `suppliers` ao `database.py` (nome, endereço, telefone/WhatsApp, email).
        * [ ] Criar o Model `Supplier`.
        * [ ] Criar a `SupplierView` (Listar, Adicionar, Editar, Excluir).
        * [ ] Desenvolver o `SupplierViewModel`.
        * [ ] Implementar `supplier_queries.py` (ou adicionar em `queries.py`).
        * [ ] Adicionar acesso ao CRUD de Fornecedores (provavelmente dentro da área "Cadastros").

---

## 📓 Backlog (Sprints Futuras - Prioridade a definir)

* **Status:** Pendente
* **Entregas:**
    * [ ] **Feature: CRUD de Receitas (Manual)**
        * Adicionar/Editar/Excluir Receitas (título, instruções, tempo, fonte, etc.).
        * View/ViewModel para formulário de cadastro/edição de receitas.
        * Queries para salvar/editar receitas.
    * [ ] **Feature: CRUD de Ingredientes (vinculado a Receitas)**
        * Adicionar/Editar/Excluir Ingredientes *dentro* de uma receita (nome, quantidade).
        * Atualizar View/ViewModel de Receitas para incluir gerenciamento de ingredientes.
        * Queries para salvar/editar/excluir ingredientes associados a uma receita.
    * [ ] **Feature: CRUD Usuário (Edição de Perfil)**
        * Permitir ao usuário logado alterar seu nome e senha (verificando senha atual).
        * View/ViewModel para edição de perfil.
        * Queries para atualização de dados do usuário.
    * [ ] **Feature: CRUD Mercado (Links Parceiros)**
        * Adicionar tabela `markets` (nome, url_link).
        * Criar Model `Market`.
        * View/ViewModel para gerenciar links de mercados (Adicionar/Editar/Excluir).
        * Queries para CRUD de mercados.
        * (Definir como o Card "Mercado" usará esses links).
    * [ ] **Feature: Importação de Receitas (Link, Foto, Voz)**
    * [ ] **Feature: Discovery (Sugestão de Receitas)**
    * [ ] **Feature: Lista de Compras** (Usará Fornecedores cadastrados)
    * [ ] **Infraestrutura (Firebase, Build Multiplataforma, Google Ads)**