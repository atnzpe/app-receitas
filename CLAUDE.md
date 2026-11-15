<!--
  Arquivo: CLAUDE.md
  Para que serve: as regras que o Claude Code segue ao trabalhar neste repositório (Guia Mestre de Receitas).
  É lido em toda conversa: fica curto e muda quando uma decisão mudar.
-->

# CLAUDE.md · Guia Mestre de Receitas

- **O que é:** app de receitas que **funciona sem internet**, em Python + Flet, com arquitetura **MVVM** (Model = dados, View = tela, ViewModel = a ponte entre os dois):
  login com senha protegida (bcrypt), categorias, receitas com ingredientes, favoritos e tema claro e escuro. Banco local SQLite.
- **Rumo (15/11/2026):** virar **app Android (APK) para celular**, depois do Quiz SFPC. O APK é gerado pelo GitHub Actions com `flet build apk`.
- **Pessoas:** Gleyson Atanazio (desenvolvedor e Scrum Master) e a PO e QA do time, que testa cada APK no celular antes de publicar.
- **Autonomia:** o Claude cria branch, commit, push e PR sem pedir. O merge e a publicação são do Gleyson.
- **Idioma:** tudo em português do Brasil, em linguagem simples, com todo termo técnico explicado.

## Onde está cada coisa

| O quê | Onde |
|---|---|
| Código (MVVM) | `src/` |
| Receitas que vêm com o app | `src/assets/native_recipes.json` |
| Testes automáticos | `tests/` |
| O que falta fazer (sprints) | [ROADMAP.md](ROADMAP.md) |
| O que aprendi | [APRENDIZADO.md](APRENDIZADO.md) |

## Definição de Pronto

1. Testes automáticos passando (`tests/`).
2. O app abre sem internet; no APK, a PO e QA marcou o teste como aprovado no painel do time.
3. O [ROADMAP.md](ROADMAP.md) e o [APRENDIZADO.md](APRENDIZADO.md) atualizados.

## Regras que não mudam

- **LGPD:** o banco local de cada pessoa fica só no aparelho dela; nenhum banco com dados de usuário entra no Git.
  Nenhuma senha, chave ou token no repositório nem dentro do APK.
- **Senha sempre com hash** (bcrypt): nunca guardar senha em texto.
- **Código comentado para qualquer pessoa entender** (regra inegociável do Gleyson): vale para todo arquivo criado ou alterado.
