---

### 3. 🗺️ Arquivo `ROADMAP.md` (Atualizado)

Este arquivo reflete o que já entregamos (Sprints 0-2) e detalha o trabalho imediato (Sprint 3).

**Ação:** Substitua o conteúdo do seu `ROADMAP.md` por este:

```markdown
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

---

## 🚧 Sprint 3: Gestão de Categorias (EM ANDAMENTO)

**Foco:** Implementar o CRUD completo para categorização das receitas.

* [ ] **Database:** Implementar `src/database/category_queries.py` (CRUD SQL).
* [ ] **ViewModel:** Criar `CategoryViewModel` com gestão de estado e validação Pydantic.
* [ ] **UI:** Criar `CategoryView` com:
  * Listagem (ListView/DataTable).
  * Modal de Adição/Edição.
  * Feedback visual via SnackBar.
* [ ] **Integração:** Conectar Card "Cadastros" -> Rota `/categories`.
* [ ] **Testes:** Unitários para queries de categoria.

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

### Sprint 7: Infraestrutura e Deploy

* Integração Firebase (Auth/Sync).
* CI/CD para Build Windows e Android.
