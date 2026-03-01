# **🗺️ Roadmap do Projeto: Guia Mestre de Receitas**

> **Status do Projeto:** 🟡 Em Desenvolvimento (Sprint 5)
> **Versão Atual:** v0.5.0-beta

Este documento é a fonte única da verdade (SSOT) para o progresso do projeto.

---

## **✅ Fases Concluídas (Sprint 0 - 4)**

<details>
<summary><strong>Clique para expandir o histórico</strong></summary>

### **Sprint 0: Fundação "Military Grade"**
* [x] Arquitetura MVVM Blindada e Core (Logger, Exceptions).
* [x] Configuração SQLite Robusta e Models Pydantic V2.

### **Sprint 1: Autenticação e Segurança**
* [x] Login/Registro com Hashing (bcrypt) e validações visuais.

### **Sprint 2: Dashboard e UI System**
* [x] Roteamento Protegido, Tratamento Global de Erros e Temas (Claro/Escuro).

### **Sprint 3: Gestão de Categorias**
* [x] CRUD de Categorias com validação de duplicidade e Seeds iniciais.

### **Sprint 4: Core de Receitas**
* [x] Schema de banco complexo (Receitas + Ingredientes + Favoritos).
* [x] CRUD Completo (Criar, Editar, Excluir) com lista dinâmica de ingredientes.
* [x] Feedback visual (Snackbars e Modais).

</details>

---

## **🚧 Sprint 5: Inteligência, UX Refinada e Automação (ATUAL)**

**Objetivo:** Elevar a experiência do usuário (UX) e reduzir o atrito na entrada de dados.

### **5.1. Discovery e Navegação (UX)**
* [x] **Grid System:** Visualização em Cards responsivos (Discovery e Minhas Receitas).
* [x] **Filtros Avançados:** Busca combinada por Nome, Tempo Máximo e Porções.
* [x] **Feedback Visual:** Contador de resultados em tempo real.
* [x] **Scrollbar Nativa:** Implementação de rolagem fluida em listas extensas.
* [x] **Smart Back:** Navegação contextual (botão voltar recorda a origem).

### **5.2. Gestão de Conteúdo**
* [x] **Imagens:** Suporte a URLs externas no cadastro e renderização nos cards.
* [x] **Favoritos:** Lógica de favoritar/desfavoritar global para não-donos.
* [ x] **Refinamento de Detalhes:** Exibir explicitamente os campos "Dicas Extras" e "Fonte/Origem" na tela `RecipeDetailView`.

### **5.3. Módulo de Inteligência (Automação)**
* [x] **Importação via Link (Scraping):** * [ ] Extração de metadados (Schema.org) de sites externos.
    * [x] Preenchimento automático do formulário de criação.
* [ ] **OCR (Visão Computacional):** Extração de texto de fotos de livros culinários.
* [ ] **Voice-to-Text:** Ditado de ingredientes via microfone.

---

## **📅 Backlog (Planejamento Futuro)**

### **Sprint 6: Social e Lista de Compras**
* [ ] **Lista de Compras:** Gerar checklist interativo a partir dos ingredientes de uma receita.
* [ ] **Compartilhamento:** Gerar cartão/imagem da receita para WhatsApp/Instagram.
* [ ] **Gestão de Mercados:** CRUD simples de fornecedores/mercados.

### **Sprint 7: Infraestrutura Cloud (Scale-Up)**
* [ ] **Sincronização Híbrida:** Integração com Firebase (Auth Google e Firestore).
* [ ] **CI/CD:** Pipelines de build automatizado para Windows (.exe) e Android (.apk).