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

## **✅ Sprint 4: Core de Receitas (Concluído)**

**Foco:** O coração do aplicativo. Criar, Listar, Editar e Excluir.

* [x] **Database:** Schema expandido com tabelas `recipes`, `recipe_ingredients` e `favorite_recipes`.
* [x] **Model:** Validação Pydantic para Receitas e Ingredientes.
* [x] **UI - Cadastro & Edição:** Formulário híbrido inteligente com lista dinâmica de ingredientes.
* [x] **UI - Minhas Receitas (Listagem):**
  * [x] Tela `RecipeListView` em formato de lista responsiva.
  * [x] Botões de Ação Rápida: Editar (Dono), Excluir (Dono) e Favoritar (Global).
* [x] **Feedback Visual:** Implementação de Modais (Overlay) para ações críticas e feedback de status.

## **🚧 Sprint 5: Inteligência e Importação (PRÓXIMA ETAPA)**

**Foco:** Facilitar a entrada de dados com IA e Automação.

* [ ] **Importação via Link:** Extração inteligente de dados de sites de receitas (Web Scraping + LLM).
* [ ] **Leitura via OCR:** Extração de texto a partir de fotos de livros/cadernos.
* [ ] **Leitura via Voz:** Transcrição de áudio para texto (Speech-to-Text).

## **📅 Backlog (Planejamento Futuro)**

### **Sprint 6: Gestão de Compras e Mercados**

* Gerar Lista de Compras a partir de uma Receita.
* CRUD de Mercados/Fornecedores.

### **Sprint 7: Infraestrutura e Deploy (Nuvem)**

* Integração Firebase (Auth/Sync).
* CI/CD para Build Windows e Android.
