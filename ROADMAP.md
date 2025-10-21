# 🗺️ Roadmap do Projeto: Guia Mestre de Receitas

Este documento rastreia o progresso do desenvolvimento, onde estivemos, onde estamos e para onde vamos, com base no nosso Guia Mestre.

---

## ✅ Sprint 0: Fundação e Estrutura (Concluído)

* **Status:** Concluído
* **Entregas:**
    * [X] Definição da arquitetura MVVM.
    * [X] Criação da estrutura de diretórios (`src/models`, `src/views`, etc.).
    * [X] Configuração do banco de dados SQLite (`database.py`).
    * [X] Criação das tabelas iniciais (`categories`, `recipes`, `ingredients`).
    * [X] Definição dos Models iniciais (`Recipe`, `Ingredient`, `Category`).
    * [X] Implementação de testes unitários para a criação do banco de dados.

---

## ✅ Sprint 1: Autenticação e Roteamento (Concluído)

* **Status:** Concluído
* **Entregas:**
    * [X] Adição da tabela `users` ao banco de dados com hash de senha.
    * [X] Criação do Model `User`.
    * [X] Implementação do `auth_queries.py` para o CRUD de Usuário.
    * [X] Refatoração de segurança para usar `bcrypt` no hashing de senhas.
    * [X] Implementação do Roteador (`ft.Router`) no `main.py` para navegação.
    * [X] Criação da `LoginView` e `RegisterView` com seus respectivos `ViewModels`.
    * [X] Uso de `page.overlay` (via `SnackBar`) para feedback de login/registro.
    * [X] Criação de testes unitários para a camada de autenticação com `bcrypt`.

---

## ✅ Sprint 2: UI do Dashboard e Temas (Concluído)

* **Status:** Concluído
* **Entregas:**
    * [X] Implementação dos temas "claro" e "escuro" (baseado no `style.py` fornecido).
    * [X] Criação do componente de UI reutilizável `DashboardCard`.
    * [X] Implementação da `DashboardView` com `ft.AppBar` e `ft.GridView` responsivo.
    * [X] Adição do botão de troca de tema interativo.
    * [X] Implementação do `ft.AlertDialog` (overlay) para funcionalidades futuras.
    * [X] Criação do componente global `AppFooter` e integração em todas as telas (Mobile-First).
    * [X] Aplicação da regra `ft.SafeArea` para compatibilidade com APK.

---

## 🎯 Sprint 3: CRUD de Categorias (Próxima Etapa)

* **Status:** Próxima Etapa
* **Entregas:**
    * [ ] Criar a `CategoryView` para listar, adicionar, editar e excluir categorias.
    * [ ] Desenvolver o `CategoryViewModel` para gerenciar o estado da UI e a lógica de negócio.
    * [ ] Implementar as funções de acesso a dados em `src/database/queries.py` (CRUD de Categorias).
    * [ ] Conectar a navegação do Card "Cadastros" (no Dashboard) para a nova rota `/categories`.

---

## 📓 Backlog (Sprints Futuras)

* **Status:** Pendente
* **Entregas:**
    * [ ] **Feature: CRUD de Receitas (Manual)**
    * [ ] **Feature: Importação de Receitas (Link, Foto, Voz)**
    * [ ] **Feature: Discovery (Sugestão de Receitas)**
    * [ ] **Feature: Lista de Compras**
    * [ ] **Infraestrutura (Firebase, Build Multiplataforma, Google Ads)**