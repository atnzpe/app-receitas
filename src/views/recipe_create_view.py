# ARQUIVO: src/views/recipe_create_view.py
import flet as ft
from src.viewmodels.recipe_viewmodel import RecipeViewModel
from src.services.intelligence_service import IntelligenceService
from src.database.category_queries import CategoryQueries


def RecipeCreateView(page: ft.Page) -> ft.View:
    vm = RecipeViewModel(page)
    user = page.data.get("logged_in_user")

    # Busca categorias para o Dropdown
    cat_db = CategoryQueries()
    categories = cat_db.get_user_categories(user.id)

    # --- CAMPOS DE TEXTO ---
    tf_title = ft.TextField(label="Título da Receita", border_radius=10)
    tf_time = ft.TextField(label="Tempo (min)", width=150,
                           keyboard_type=ft.KeyboardType.NUMBER, border_radius=10)
    tf_servings = ft.TextField(label="Porções", width=150, border_radius=10)

    dd_category = ft.Dropdown(
        label="Categoria",
        options=[ft.dropdown.Option(str(c['id']), c['name'])
                 for c in categories],
        border_radius=10,
        expand=True
    )

    tf_instructions = ft.TextField(
        label="Modo de Preparo", multiline=True, min_lines=5, border_radius=10)
    tf_add_instructions = ft.TextField(
        label="Dicas Extras", multiline=True, border_radius=10)
    tf_source = ft.TextField(
        label="Fonte / Origem (URL ou Livro)", border_radius=10, prefix_icon=ft.Icons.LINK)
    tf_image = ft.TextField(label="URL da Imagem",
                            border_radius=10, prefix_icon=ft.Icons.IMAGE)

    # --- INGREDIENTES ---
    tf_ing_name = ft.TextField(
        label="Ingrediente", expand=True, height=40, text_size=14)
    tf_ing_qty = ft.TextField(label="Qtd", width=80, height=40, text_size=14)
    tf_ing_unit = ft.TextField(label="Unid", width=80, height=40, text_size=14)

    ingredients_list_view = ft.ListView(height=200, spacing=5)

    def _render_ingredients():
        ingredients_list_view.controls.clear()
        for i, ing in enumerate(vm.temp_ingredients):
            ingredients_list_view.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text(
                            f"{ing.name} ({ing.quantity} {ing.unit})", expand=True),
                        ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_400,
                                      on_click=lambda e, idx=i: _remove_ingredient(idx))
                    ]),
                    bgcolor=ft.Colors.GREY_50, padding=5, border_radius=5
                )
            )
        page.update()

    def _add_ingredient(e):
        if vm.add_temp_ingredient(tf_ing_name.value, tf_ing_qty.value, tf_ing_unit.value):
            tf_ing_name.value = ""
            tf_ing_qty.value = ""
            tf_ing_unit.value = ""
            tf_ing_name.focus()
            _render_ingredients()

    def _remove_ingredient(index):
        vm.remove_temp_ingredient(index)
        _render_ingredients()

    # --- FUNÇÕES DE INTELIGÊNCIA ---
    def show_import_dialog(e):
        tf_url = ft.TextField(
            label="Link", hint_text="https://tudogostoso...", autofocus=True)

        def confirm(e):
            if not tf_url.value:
                return
            page.snack_bar = ft.SnackBar(ft.Text("Baixando..."))
            page.snack_bar.open = True
            page.update()

            err, data = vm.import_from_url(tf_url.value)
            dlg.open = False

            if err:
                page.snack_bar = ft.SnackBar(
                    ft.Text(f"Erro: {err}"), bgcolor="red")
            elif data:
                tf_title.value = data.get('title', '')
                tf_time.value = data.get('preparation_time', '')
                tf_servings.value = data.get('servings', '')
                tf_instructions.value = data.get('instructions', '')
                tf_add_instructions.value = data.get(
                    'additional_instructions', '')
                tf_source.value = data.get('source', '')
                tf_image.value = data.get('image_path', '')
                _render_ingredients()  # Renderiza ingredientes importados

                page.snack_bar = ft.SnackBar(
                    ft.Text("Importado! Revise os dados."), bgcolor="green")
            page.update()

        dlg = ft.AlertDialog(title=ft.Text("Importar Site"), content=tf_url,
                             actions=[ft.ElevatedButton("Importar", on_click=confirm)])
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def start_voice(e):
        page.snack_bar = ft.SnackBar(
            ft.Text("Ouvindo... Fale os ingredientes! 🎤"))
        page.snack_bar.open = True
        page.update()

        text = IntelligenceService.listen_dictation()

        if text.startswith("ERRO"):
            page.snack_bar = ft.SnackBar(ft.Text(text), bgcolor="orange")
        elif text:
            parts = text.replace(" e ", ",").split(",")
            count = 0
            for p in parts:
                if vm.add_temp_ingredient(p.strip(), "", "") is None:
                    count += 1
            _render_ingredients()  # Atualiza visualmente
            page.snack_bar = ft.SnackBar(
                ft.Text(f"{count} ingredientes detectados!"), bgcolor="green")
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text("Não entendi o áudio."), bgcolor="grey")
        page.snack_bar.open = True
        page.update()

    def save_action(e):
        success, msg = vm.save_recipe(
            tf_title.value, tf_time.value, tf_servings.value,
            tf_instructions.value, tf_add_instructions.value,
            tf_source.value, tf_image.value, dd_category.value
        )
        color = ft.Colors.GREEN if success else ft.Colors.RED

        if success:
            page.snack_bar = ft.SnackBar(content=ft.Text(msg), bgcolor=color)
            page.snack_bar.open = True
            page.go("/my_recipes")
        else:
            page.dialog = ft.AlertDialog(
                title=ft.Text("Atenção"), content=ft.Text(msg))
            page.dialog.open = True
            page.update()

    # --- VERIFICAÇÃO DE EDIÇÃO ---
    existing_data = vm.load_editing_data()
    page_title_text = "Nova Receita"
    if existing_data:
        page_title_text = "Editar Receita"
        tf_title.value = existing_data['title']
        tf_time.value = str(existing_data['preparation_time'])
        tf_servings.value = existing_data['servings']
        tf_instructions.value = existing_data['instructions']
        tf_add_instructions.value = existing_data['additional_instructions']
        tf_source.value = existing_data['source']
        tf_image.value = existing_data['image_path']
        dd_category.value = str(existing_data['category_id'])
        _render_ingredients()

    # --- VIEW ---
    return ft.View(
        route="/create_recipe",
        appbar=ft.AppBar(
            title=ft.Text(page_title_text),
            bgcolor=ft.Colors.WHITE,
            center_title=True,
            leading=ft.IconButton(ft.Icons.ARROW_BACK,
                                  on_click=lambda _: page.go("/my_recipes"))
        ),
        controls=[
            ft.SafeArea(
                # [CORREÇÃO CRÍTICA] expand=True adicionado ao Container pai
                expand=True,
                content=ft.Container(
                    padding=20,
                    # [CORREÇÃO CRÍTICA] expand=True adicionado ao Container
                    expand=True,
                    content=ft.Column([
                        # Cabeçalho com Botão de Importar
                        ft.Row([
                            ft.Text("Dados Básicos", size=18,
                                    weight=ft.FontWeight.BOLD),
                            ft.Row([
                                ft.ElevatedButton("Importar Link", icon=ft.Icons.DOWNLOAD,
                                                  on_click=show_import_dialog,
                                                  bgcolor=ft.Colors.BLUE_50, color=ft.Colors.BLUE_800,
                                                  style=ft.ButtonStyle(elevation=0)),
                                ft.IconButton(
                                    ft.Icons.MIC, icon_color="blue", tooltip="Voz", on_click=start_voice),
                            ])
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                        tf_title,
                        ft.Row([tf_time, tf_servings, dd_category]),
                        tf_source,
                        tf_image,
                        ft.Divider(),

                        ft.Text("Ingredientes", size=18,
                                weight=ft.FontWeight.BOLD),
                        ft.Row([tf_ing_name, tf_ing_qty, tf_ing_unit,
                                ft.IconButton(ft.Icons.ADD_CIRCLE, icon_color=ft.Colors.GREEN, icon_size=30, on_click=_add_ingredient)]),

                        ft.Container(
                            content=ingredients_list_view,
                            bgcolor=ft.Colors.WHITE, border=ft.Border.all(1, ft.Colors.GREY_300), border_radius=10, padding=10
                        ),

                        ft.Divider(),
                        ft.Text("Instruções", size=18,
                                weight=ft.FontWeight.BOLD),
                        tf_instructions,
                        tf_add_instructions,

                        ft.Container(height=20),

                        # O BOTÃO SALVAR ESTÁ AQUI
                        ft.ElevatedButton("Salvar Receita", on_click=save_action,
                                          bgcolor=ft.Colors.ORANGE_600, color=ft.Colors.WHITE,
                                          height=50, width=float('inf')),

                        # Espaço extra no final para garantir scroll confortável
                        ft.Container(height=50),

                    ], scroll=ft.ScrollMode.AUTO, expand=True)  # A Coluna tem scroll e expande
                )
            )
        ],
        bgcolor=ft.Colors.WHITE
    )
