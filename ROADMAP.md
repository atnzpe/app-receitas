# 🗺️ Roadmap do Projeto: Guia Mestre de Receitas

Este documento serve como a fonte única da verdade para o progresso do projeto.

---

## ✅ Sprint 0: Fundação "Military Grade" (Concluído)
* [x] Definição da Arquitetura MVVM Blindada.
* [x] Implementação do `src/core` (Logger Central, Exceções Customizadas).
* [x] Configuração do SQLite com tratamento de erros robusto.
* [x] Migração de Models para **Pydantic V2**.

## ✅ Sprint 1: Autenticação e Segurança (Concluído)
* [x] Tabela `users` com constraints de unicidade.
* [x] Hashing de senha seguro com `bcrypt`.
* [x] Queries de Auth com tratamento de `IntegrityError`.
* [x] Telas de Login e Registro com validação visual.
* [x] Testes unitários de autenticação.

## ✅ Sprint 2: Dashboard e UI System (Concluído)
* [x] Sistema de Roteamento Protegido (`ft.Router`).
* [x] Barreira Global de Erros (Crash Handler UI).
* [x] UI do Dashboard Responsivo (Grid System).
* [x] Sistema de Temas (Claro/Escuro/Sistema) persistente na sessão.
* [x] Componentização (`DashboardCard`, `AppFooter`).

## ✅ Sprint 3: Gestão de Categorias (Concluído)
* [x] **Database:** Implementado `src/database/category_queries.py` com Seed Data.
* [x] **ViewModel:** Criado `CategoryViewModel` com lógica de permissões e favoritos.
* [x] **UI:** Implementada `CategoryView` responsiva com Modal e FAB.
* [x] **Integração:** Card "Cadastros" conectado.
* [x] **Testes:** Unitários blindados contra duplicidade e segurança.

---

## 🚧 Sprint 4: Gestão de Fornecedores e Mercados (PRÓXIMO)
**Foco:** Expandir o ecossistema para compras.

* [ ] **Database:** Tabela `markets` e `suppliers`.
* [ ] **UI:** Tela de listagem de mercados com link externo.
* [ ] **Feature:** Lista de Compras básica (Ingredientes -> Lista).
---

## 📅 Backlog (Planejamento Futuro)

### Sprint 4: Gestão de Fornecedores e Mercados

* CRUD de Fornecedores (para lista de compras).
* CRUD de Mercados Parceiros (Links).

### Sprint 5: Core de Receitas (Mestre-Detalhe)

* Cadastro complexo de Receita (Cabeçalho + Lista de Ingredientes).
* Lógica de conversão de unidades (ex: g para kg).

### Sprint 6: Inteligência e Importação

* Importação via Link (Web Scraping).
* Leitura via OCR/Voz.
* Leitura via importar PDF

### Sprint 7: Infraestrutura e Deploy

* Integração Firebase (Auth/Sync).
* CI/CD para Build Windows e Android.
