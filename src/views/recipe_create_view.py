# ARQUIVO: src/views/recipe_create_view.py
import flet as ft
from typing import Callable, Optional
from src.core.logger import get_logger
from src.viewmodels.recipe_viewmodel import RecipeViewModel
from src.viewmodels.category_viewmodel import CategoryViewModel
from src.utils.theme import AppDimensions

logger = get_logger("src.views.recipe_create")


def RecipeCreateView(page: ft.Page) -> ft.View:
    logger.debug("Inicializando RecipeCreateView.")

    # 1. Inicialização
    try:
        viewModel = RecipeViewModel()
        categoryVM = CategoryViewModel(page)
    except Exception as e:
        logger.critical(f"Erro init: {e}")
        raise e

    # 1.1 Verificação de Edição
    edit_id = page.data.get("editing_recipe_id")
    initial_data = None
    page_title_text = "Nova Receita"

    if edit_id:
        logger.info(f"Modo EDIÇÃO detectado para ID: {edit_id}")
        initial_data = viewModel.load_recipe_for_edit(edit_id)
        if initial_data:
            page_title_text = "Editar Receita"
            page.data["editing_recipe_id"] = None

    # 2. Referências
    tf_title = ft.Ref[ft.TextField]()
    tf_image = ft.Ref[ft.TextField]()  # [NOVO]
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

    current_dialog: ft.AlertDialog = None

    # 3. Lógica de Feedback
    def _close_dialog(e):
        nonlocal current_dialog
        if current_dialog:
            current_dialog.open = False
            page.update()

    def _show_feedback_dialog(title: str, message: str, is_error: bool = False, on_ok: Optional[Callable] = None):
        nonlocal current_dialog
        icon_data = ft.Icons.ERROR_OUTLINE if is_error else ft.Icons.CHECK_CIRCLE_OUTLINE
        icon_color = ft.Colors.RED if is_error else ft.Colors.GREEN

        def on_ok_click(e):
            _close_dialog(e)
            if on_ok:
                on_ok(e)

        dlg = ft.AlertDialog(
            title=ft.Row([ft.Icon(icon_data, color=icon_color, size=30), ft.Text(
                title)], alignment=ft.MainAxisAlignment.START),
            content=ft.Text(message, size=16),
            actions=[ft.TextButton("OK", on_click=on_ok_click)],
            actions_alignment=ft.MainAxisAlignment.END,
            modal=not is_error
        )
        current_dialog = dlg
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    # 4. Callbacks
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
                        ft.Icons.DELETE_OUTLINE, data=i, on_click=_on_remove_ingredient, icon_color=ft.Colors.RED_400),
                    dense=True
                )
            )
        lv_ingredients.current.update()

    def _on_add_ingredient(e):
        err = viewModel.add_temp_ingredient(
            tf_ing_name.current.value, tf_ing_qty.current.value, tf_ing_unit.current.value)
        if err:
            _show_feedback_dialog("Inválido", err, is_error=True)
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
            viewModel.remove_temp_ingredient(int(e.control.data))
            _render_ingredients()
        except:
            pass

    def _on_save_click(e):
        try:
            user = page.data.get("logged_in_user")
            if not user:
                _show_feedback_dialog(
                    "Sessão", "Logue novamente.", is_error=True, on_ok=lambda _: page.go("/login"))
                return

            success = viewModel.save_recipe(
                user_id=user.id,
                title=tf_title.current.value,
                category_id=dd_category.current.value,
                instructions=tf_instructions.current.value,
                prep_time=tf_time.current.value,
                servings=tf_servings.current.value,
                add_instr=tf_add_instructions.current.value,
                source=tf_source.current.value,
                image_path=tf_image.current.value  # [NOVO]
            )

            if success:
                _show_feedback_dialog(
                    "Sucesso", "Receita salva!", is_error=False, on_ok=lambda _: page.go("/my_recipes"))
            else:
                _show_feedback_dialog(
                    "Erro", "Falha ao salvar.", is_error=True)

        except Exception as ex:
            _show_feedback_dialog("Erro", str(ex), is_error=True)

    # 5. Layout e Preenchimento Inicial
    try:
        categoryVM.load_data(update_ui=False)
        cat_options = [ft.dropdown.Option(
            key=str(c.id), text=c.name) for c in categoryVM.categories]
    except:
        cat_options = []

    # Valores Iniciais
    val_title = initial_data['title'] if initial_data else ""
    val_image = initial_data.get('image_path', "") if initial_data else ""
    val_cat = str(initial_data['category_id']
                  ) if initial_data and initial_data['category_id'] else None
    val_time = str(initial_data['preparation_time']
                   ) if initial_data and initial_data['preparation_time'] else ""
    val_servings = initial_data['servings'] if initial_data else ""
    val_instr = initial_data['instructions'] if initial_data else ""
    val_add = initial_data['additional_instructions'] if initial_data else ""
    val_source = initial_data['source'] if initial_data else ""

    # [IMPORTANTE] Container interno recebe o padding para não quebrar o SafeArea
    content_layout = ft.Container(
        padding=20,
        content=ft.Column(
            scroll=ft.ScrollMode.HIDDEN,
            controls=[
                ft.Text(page_title_text, size=24, weight=ft.FontWeight.BOLD),
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        spacing=15,
                        controls=[
                            ft.TextField(
                                ref=tf_title, label="Título *", value=val_title, border=ft.InputBorder.UNDERLINE),

                            # [NOVO] Campo de Imagem
                            ft.TextField(
                                ref=tf_image,
                                label="URL da Imagem",
                                value=val_image,
                                prefix_icon=ft.Icons.IMAGE,
                                border=ft.InputBorder.UNDERLINE,
                                hint_text="https://exemplo.com/foto.jpg"
                            ),

                            ft.Dropdown(ref=dd_category, label="Categoria", value=val_cat,
                                        options=cat_options, border=ft.InputBorder.UNDERLINE),

                            ft.Row([
                                ft.TextField(ref=tf_time, label="Tempo (min)", value=val_time, width=120,
                                             keyboard_type=ft.KeyboardType.NUMBER, border=ft.InputBorder.UNDERLINE),
                                ft.TextField(ref=tf_servings, label="Rendimento", value=val_servings,
                                             expand=True, border=ft.InputBorder.UNDERLINE),
                            ]),

                            ft.Divider(),
                            ft.Text(
                                "Ingredientes", size=16, weight=ft.FontWeight.W_600, color=ft.Colors.PRIMARY),

                            ft.Row([
                                ft.TextField(
                                    ref=tf_ing_name, label="Item", expand=2, height=50, content_padding=10),
                                ft.TextField(
                                    ref=tf_ing_qty, label="Qtd", width=70, height=50, content_padding=10),
                                ft.TextField(
                                    ref=tf_ing_unit, label="Unid", width=70, height=50, content_padding=10),
                                ft.IconButton(
                                    ft.Icons.ADD_CIRCLE, on_click=_on_add_ingredient, icon_color=ft.Colors.PRIMARY, icon_size=30)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                            ft.Container(
                                content=ft.ListView(
                                    ref=lv_ingredients, spacing=0),
                                height=200, border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT), border_radius=8, padding=5
                            ),

                            ft.Divider(),
                            ft.TextField(ref=tf_instructions, label="Modo de Preparo *",
                                         value=val_instr, multiline=True, min_lines=5),
                            ft.TextField(
                                ref=tf_add_instructions, label="Dicas Extras", value=val_add, multiline=True),
                            ft.TextField(ref=tf_source, label="Fonte",
                                         value=val_source, prefix_icon=ft.Icons.LINK),

                            ft.Container(height=20),
                            ft.ElevatedButton(
                                content=ft.Row([ft.Icon(ft.Icons.SAVE), ft.Text(
                                    "Salvar")], alignment=ft.MainAxisAlignment.CENTER),
                                on_click=_on_save_click,
                                style=ft.ButtonStyle(
                                    padding=20, shape=ft.RoundedRectangleBorder(radius=8))
                            )
                        ]
                    )
                )
            ]
        )
    )

    if initial_data:
        lv_initial_controls = []
        for i, ing in enumerate(viewModel.temp_ingredients):
            lv_initial_controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.CIRCLE, size=8,
                                    color=ft.Colors.GREY),
                    title=ft.Text(ing.name, weight=ft.FontWeight.W_600),
                    subtitle=ft.Text(
                        f"{ing.quantity or ''} {ing.unit or ''}".strip()),
                    trailing=ft.IconButton(
                        ft.Icons.DELETE_OUTLINE, data=i, on_click=_on_remove_ingredient, icon_color=ft.Colors.RED_400),
                    dense=True
                )
            )
        lv_ingredients.current.controls = lv_initial_controls

    return ft.View(
        route="/create_recipe",
        # [CORREÇÃO] SafeArea sem padding
        controls=[ft.SafeArea(content=content_layout, expand=True)],
        appbar=ft.AppBar(
            leading=ft.IconButton(ft.Icons.ARROW_BACK,
                                  on_click=lambda _: page.go("/my_recipes")),
            title=ft.Text(page_title_text),
            bgcolor=page.theme.color_scheme.surface
        ),
        bgcolor=page.theme.color_scheme.surface,
        scroll=ft.ScrollMode.AUTO
    )
