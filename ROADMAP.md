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

## 🎯 Sprint 1: Autenticação e Roteamento (Próxima Etapa)

* **Status:** Próxima Etapa
* **Entregas:**
    * [ ] Adição da tabela `users` ao banco de dados com hash de senha.
    * [ ] Criação do Model `User`.
    * [ ] Implementação do `auth_queries.py` para o CRUD de Usuário.
    * [ ] Implementação do Roteador (`ft.Router`) no `main.py` para navegação.
    * [ ] Criação da `LoginView` e `RegisterView` com seus respectivos `ViewModels`.
    * [ ] Criação de testes unitários para a camada de autenticação.
    * [ ] Criação (atualização) dos documentos `README.md` e `ROADMAP.md`.

---

## 📋 Sprint 2: UI do Dashboard e Refatoração de Overlays (Pendente)

* **Status:** Pendente
* **Entregas:**
    * [ ] Refatoração do feedback de Login/Registro para usar `ft.SnackBar` (overlays).
    * [ ] Criação do componente de UI reutilizável `DashboardCard`.
    * [ ] Implementação da `DashboardView` com `ft.AppBar` e `ft.GridView` responsivo.
    * [ ] Implementação do `ft.AlertDialog` para feedback de funcionalidades futuras.

---

## 📋 Sprint 3: CRUD de Categorias (Pendente)

* **Status:** Pendente
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
        * (View/ViewModel para o formulário completo de cadastro de receitas)
        * (Queries para salvar/editar receitas e seus ingredientes associados)
    * [ ] **Feature: Importação de Receitas**
        * (Módulo de importação por Link - LLM)
        * (Módulo de importação por Foto - OCR)
        * (Módulo de importação por Voz - Speech-to-Text)
    * [ ] **Feature: Discovery (Sugestão de Receitas)**
    * [ ] **Feature: Lista de Compras**
    * [ ] **Infraestrutura**
        * (Integração com Firebase - Sincronização em Nuvem)
        * (Build Multiplataforma - Android/Windows)
        * (Integração Google Ads)