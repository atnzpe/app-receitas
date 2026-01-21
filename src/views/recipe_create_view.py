# ARQUIVO: src/views/recipe_create_view.py
# OBJETIVO: Tela de criação de receitas com Feedback Modal via Overlay (Blindado).
# FIX: Substituição de page.dialog por page.overlay para garantir visibilidade.

import flet as ft
from typing import Callable, Optional
from src.core.logger import get_logger
from src.viewmodels.recipe_viewmodel import RecipeViewModel
from src.viewmodels.category_viewmodel import CategoryViewModel
from src.utils.theme import AppDimensions

logger = get_logger("src.views.recipe_create")


def RecipeCreateView(page: ft.Page) -> ft.View:
    """
    Constrói e retorna a View de Criação de Receitas.
    Usa page.overlay para garantir que modais apareçam sobre qualquer View.
    """
    logger.debug("Inicializando RecipeCreateView com estratégia Overlay.")

    # 1. Inicialização
    try:
        viewModel = RecipeViewModel()
        categoryVM = CategoryViewModel(page)
    except Exception as e:
        logger.critical(f"Erro ao instanciar VMs: {e}", exc_info=True)
        raise e

    # 2. Referências
    tf_title = ft.Ref[ft.TextField]()
    dd_category = ft.Ref[ft.Dropdown]()
    tf_time = ft.Ref[ft.TextField]()
    tf_servings = ft.Ref[ft.TextField]()
    tf_instructions = ft.Ref[ft.TextField]()
    tf_add_instructions = ft.Ref[ft.TextField]()
    tf_source = ft.Ref[ft.TextField]()

    tf_ing_name = ft.Ref[ft.TextField]()
    tf_ing_qty = ft.Ref[ft.TextField]()
    tf_ing_unit = ft.Ref[ft.TextField]()
    lv_ingredients = ft.Ref[ft.ListView]()

    # Variável local para manter referência ao diálogo ativo
    # Isso evita problemas de Garbage Collection
    current_dialog: ft.AlertDialog = None

    # -------------------------------------------------------------------------
    # 3. Lógica de Feedback (Overlay Force)
    # -------------------------------------------------------------------------

    def _close_dialog(e):
        """Fecha o diálogo ativo e atualiza a página."""
        nonlocal current_dialog
        try:
            if current_dialog:
                logger.debug("Fechando diálogo via Overlay.")
                current_dialog.open = False
                page.update()
        except Exception as ex:
            logger.error(f"Erro ao fechar diálogo: {ex}")

    def _show_feedback_dialog(title: str, message: str, is_error: bool = False, on_ok: Optional[Callable] = None):
        """
        Exibe Modal usando page.overlay.append().
        Esta é a técnica mais robusta para garantir visibilidade em todas as versões do Flet.
        """
        nonlocal current_dialog

        action_type = "ERRO" if is_error else "SUCESSO"
        logger.info(f"Preparando Modal de {action_type}: {title}")

        try:
            icon_data = ft.Icons.ERROR_OUTLINE if is_error else ft.Icons.CHECK_CIRCLE_OUTLINE
            icon_color = ft.Colors.RED if is_error else ft.Colors.GREEN

            def on_ok_click(e):
                _close_dialog(e)
                if on_ok:
                    logger.info("Executando navegação pós-modal.")
                    on_ok(e)

            # Criação do componente
            dlg = ft.AlertDialog(
                title=ft.Row([
                    ft.Icon(icon_data, color=icon_color, size=30),
                    ft.Text(title)
                ], alignment=ft.MainAxisAlignment.START),
                content=ft.Text(message, size=16),
                actions=[
                    ft.TextButton("OK", on_click=on_ok_click)
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                # Impede fechar clicando fora se for sucesso (obriga o OK)
                modal=not is_error
            )

            # [CORREÇÃO BLINDADA]
            # 1. Armazena referência local
            current_dialog = dlg
            # 2. Injeta diretamente na raiz da página (Overlay)
            page.overlay.append(dlg)
            # 3. Abre
            dlg.open = True
            # 4. Atualiza a página inteira para renderizar o overlay
            page.update()

            logger.info("Modal injetado no page.overlay e atualizado.")

        except Exception as ex:
            logger.critical(
                f"FALHA CRÍTICA UI: Não foi possível renderizar o modal: {ex}", exc_info=True)

    # -------------------------------------------------------------------------
    # 4. Callbacks
    # -------------------------------------------------------------------------

    def _render_ingredients():
        if not lv_ingredients.current:
            return
        lv_ingredients.current.controls.clear()
        for i, ing in enumerate(viewModel.temp_ingredients):
            lv_ingredients.current.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.CIRCLE, size=8,
                                    color=ft.Colors.GREY),
                    title=ft.Text(ing.name, weight=ft.FontWeight.W_600),
                    subtitle=ft.Text(
                        f"{ing.quantity or ''} {ing.unit or ''}".strip()),
                    trailing=ft.IconButton(
                        ft.Icons.DELETE_OUTLINE,
                        data=i,
                        on_click=_on_remove_ingredient,
                        icon_color=ft.Colors.RED_400,
                        tooltip="Remover"
                    ),
                    dense=True
                )
            )
        lv_ingredients.current.update()

    def _on_add_ingredient(e):
        err = viewModel.add_temp_ingredient(
            name=tf_ing_name.current.value,
            qty=tf_ing_qty.current.value,
            unit=tf_ing_unit.current.value
        )
        if err:
            _show_feedback_dialog("Dados Inválidos", err, is_error=True)
            tf_ing_name.current.focus()
            return

        tf_ing_name.current.value = ""
        tf_ing_qty.current.value = ""
        tf_ing_unit.current.value = ""
        tf_ing_name.current.focus()
        page.update()
        _render_ingredients()

    def _on_remove_ingredient(e):
        try:
            idx = int(e.control.data)
            viewModel.remove_temp_ingredient(idx)
            _render_ingredients()
        except Exception:
            pass

    def _on_save_click(e):
        logger.info("Click Salvar Receita iniciado.")
        try:
            user = page.data.get("logged_in_user")
            if not user:
                _show_feedback_dialog("Sessão Expirada", "Faça login novamente.", is_error=True,
                                      on_ok=lambda _: page.go("/login"))
                return

            success = viewModel.save_recipe(
                user_id=user.id,
                title=tf_title.current.value,
                category_id=dd_category.current.value,
                instructions=tf_instructions.current.value,
                prep_time=tf_time.current.value,
                servings=tf_servings.current.value,
                add_instr=tf_add_instructions.current.value,
                source=tf_source.current.value
            )

            if success:
                logger.info("Sucesso lógico. Chamando modal via overlay...")
                _show_feedback_dialog(
                    "Sucesso!",
                    "Receita salva corretamente.",
                    is_error=False,
                    on_ok=lambda _: page.go("/my_recipes")
                )
            else:
                _show_feedback_dialog(
                    "Erro", "Falha ao salvar receita.", is_error=True)

        except Exception as ex:
            logger.error(f"Exceção no click salvar: {ex}")
            _show_feedback_dialog("Erro Crítico", str(ex), is_error=True)

    # 5. Layout
    try:
        categoryVM.load_data(update_ui=False)
        cat_options = [
            ft.dropdown.Option(key=str(c.id), text=c.name)
            for c in categoryVM.categories
        ]
    except:
        cat_options = []

    content_layout = ft.Column(
        scroll=ft.ScrollMode.HIDDEN,
        controls=[
            ft.Text("Nova Receita", size=24, weight=ft.FontWeight.BOLD),
            ft.Container(
                expand=True,
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=15,
                    controls=[
                        ft.TextField(
                            ref=tf_title, label="Título da Receita *", border=ft.InputBorder.UNDERLINE),
                        ft.Dropdown(ref=dd_category, label="Categoria",
                                    options=cat_options, border=ft.InputBorder.UNDERLINE),
                        ft.Row([
                            ft.TextField(ref=tf_time, label="Tempo (min)", width=120,
                                         keyboard_type=ft.KeyboardType.NUMBER, border=ft.InputBorder.UNDERLINE),
                            ft.TextField(ref=tf_servings, label="Rendimento",
                                         expand=True, border=ft.InputBorder.UNDERLINE),
                        ]),
                        ft.Divider(),
                        ft.Text("Ingredientes", size=16,
                                weight=ft.FontWeight.W_600, color=ft.Colors.PRIMARY),
                        ft.Row([
                            ft.TextField(ref=tf_ing_name, label="Item (ex: Arroz)",
                                         expand=2, height=50, content_padding=10),
                            ft.TextField(ref=tf_ing_qty, label="Qtd",
                                         width=70, height=50, content_padding=10),
                            ft.TextField(ref=tf_ing_unit, label="Unid",
                                         width=70, height=50, content_padding=10),
                            ft.IconButton(ft.Icons.ADD_CIRCLE, on_click=_on_add_ingredient,
                                          icon_color=ft.Colors.PRIMARY, icon_size=30)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Container(
                            content=ft.ListView(ref=lv_ingredients, spacing=0),
                            height=200,
                            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
                            border_radius=8,
                            padding=5
                        ),
                        ft.Divider(),
                        ft.TextField(
                            ref=tf_instructions, label="Modo de Preparo *", multiline=True, min_lines=5),
                        ft.TextField(ref=tf_add_instructions,
                                     label="Dicas Extras", multiline=True),
                        ft.TextField(
                            ref=tf_source, label="Fonte / Autor", prefix_icon=ft.Icons.LINK),
                        ft.Container(height=20),
                        ft.ElevatedButton(
                            content=ft.Row([ft.Icon(ft.Icons.SAVE), ft.Text(
                                "Salvar Receita")], alignment=ft.MainAxisAlignment.CENTER),
                            on_click=_on_save_click,
                            style=ft.ButtonStyle(
                                padding=20, shape=ft.RoundedRectangleBorder(radius=8))
                        )
                    ]
                )
            )
        ]
    )

    return ft.View(
        route="/create_recipe",
        controls=[ft.SafeArea(content=content_layout, expand=True)],
        appbar=ft.AppBar(
            leading=ft.IconButton(ft.Icons.ARROW_BACK,
                                  on_click=lambda _: page.go("/")),
            title=ft.Text("Nova Receita"),
            bgcolor=page.theme.color_scheme.surface
        ),
        bgcolor=page.theme.color_scheme.surface,
        scroll=ft.ScrollMode.AUTO
    )
