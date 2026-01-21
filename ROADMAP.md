# **🗺️ Roadmap do Projeto: Guia Mestre de Receitas**

Este documento serve como a fonte única da verdade para o progresso do projeto.

## **✅ Sprint 0: Fundação "Military Grade" (Concluído)**
* [x] Definição da Arquitetura MVVM Blindada.
* [x] Implementação do src/core (Logger Central, Exceções Customizadas).
* [x] Configuração do SQLite com tratamento de erros robusto.
* [x] Migração de Models para **Pydantic V2**.

## **✅ Sprint 1: Autenticação e Segurança (Concluído)**
* [x] Tabela users com constraints de unicidade.
* [x] Hashing de senha seguro com bcrypt.
* [x] Queries de Auth com tratamento de IntegrityError.
* [x] Telas de Login e Registro com validação visual.
* [x] Testes unitários de autenticação.

## **✅ Sprint 2: Dashboard e UI System (Concluído)**
* [x] Sistema de Roteamento Protegido (ft.Router).
* [x] Barreira Global de Erros (Crash Handler UI).
* [x] UI do Dashboard Responsivo (Grid System).
* [x] Sistema de Temas (Claro/Escuro/Sistema) persistente na sessão.
* [x] Componentização (DashboardCard, AppFooter).

## **✅ Sprint 3: Gestão de Categorias (Concluído)**
* [x] **Database:** Implementado src/database/category_queries.py com Seed Data.
* [x] **ViewModel:** Criado CategoryViewModel com lógica de permissões e favoritos.
* [x] **UI:** Implementada CategoryView responsiva com Modal e FAB.
* [x] **Integração:** Card "Cadastros" conectado.
* [x] **Testes:** Unitários blindados contra duplicidade e segurança.

## **🚧 Sprint 4: Core de Receitas (EM ANDAMENTO)**
**Foco:** O coração do aplicativo. Criar, Listar, Editar e Excluir.

* [x] **Database:** Tabela recipes e recipe_ingredients criadas e populadas.
* [x] **Model:** Refinamento do Pydantic para Recipe e Ingredient.
* [x] **UI - Cadastro Manual:** Formulário completo com Lista Dinâmica de Ingredientes e Feedback Modal.
* [ ] **UI - Minhas Receitas (Listagem):**
    * [ ] Tela `RecipeListView` (Grid ou Lista).
    * [ ] Filtro: Minhas Receitas vs. Favoritas.
    * [ ] Navegação para Detalhes/Edição.
* [ ] **UI - Ações CRUD:**
    * [ ] Lógica de Delete (Apenas proprietário).
    * [ ] Lógica de Update (Apenas proprietário).
    * [ ] Lógica de Favoritar (Global).

## **📅 Backlog (Planejamento Futuro)**

### **Sprint 5: Inteligência e Importação (Diferencial Competitivo)**
* Importação via Link (Web Scraping).
* Leitura via OCR (Foto de livro de receitas).
* Leitura via Áudio/Voz (Speech-to-Text).

### **Sprint 6: Gestão de Compras e Mercados**
* Gerar Lista de Compras a partir de uma Receita.
* CRUD de Mercados/Fornecedores.

### **Sprint 7: Infraestrutura e Deploy (Nuvem)**
* Integração Firebase (Auth/Sync).
* CI/CD para Build Windows e Android.