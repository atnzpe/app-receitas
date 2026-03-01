# ARQUIVO: src/views/recipe_create_view.py
import flet as ft
import asyncio
from src.viewmodels.recipe_viewmodel import RecipeViewModel
from src.services.intelligence_service import IntelligenceService
from src.database.category_queries import CategoryQueries
from src.core.logger import get_logger

# Configuração de Logs
logger = get_logger("src.views.recipe_create")


def RecipeCreateView(page: ft.Page) -> ft.View:
    """
    VIEW DE CRIAÇÃO/EDIÇÃO DE RECEITA (VERSÃO BLINDADA)
    - Compatível com PDF, Imagem e Web
    - Blindado contra falhas de OCR/PDF/Erro UI
    """
    logger.info(">>> [INIT] RecipeCreateView V33 (Service Safe Mode)")

    vm = RecipeViewModel(page)
    user = page.data.get("logged_in_user")

    # --- ELEMENTOS VISUAIS ---
    loading_bar_top = ft.ProgressBar(visible=False, color="orange")

    # --- HELPER: SNACKBAR (BLINDADO) ---
    def show_msg(msg, color="blue"):
        try:
            page.snack_bar = ft.SnackBar(ft.Text(str(msg)), bgcolor=color)
            page.snack_bar.open = True
            page.update()
        except Exception as e:
            logger.warning(f"SnackBar ignorado: {e}")

    # --- HELPER: UPDATE SEGURO (BLINDADO) ---
    def safe_update(control=None):
        try:
            if control:
                if control.page:
                    control.update()
            else:
                page.update()
        except Exception as e:
            logger.warning(f"Safe update ignorado: {e}")

    # --- LÓGICA DE PROCESSAMENTO DE ARQUIVO ---
    def process_file_path(file_path):
        logger.info(f"Processando: {file_path}")
        loading_bar_top.visible = True
        safe_update()

        try:
            ext = file_path.split('.')[-1].lower()
            raw_text = ""
            if ext == "pdf":
                raw_text = IntelligenceService.read_pdf(file_path)
            else:
                raw_text = IntelligenceService.read_image(file_path)

            if raw_text and not raw_text.startswith("ERRO"):
                data = IntelligenceService.parse_raw_text(raw_text)
                populate_fields(data, update_ui=True)
                show_msg("Sucesso!", "green")
            else:
                show_msg("Falha na leitura.", "red")

        except Exception as ex:
            logger.error(f"Erro pipeline: {ex}", exc_info=True)
            show_msg(f"Erro: {ex}", "red")
        finally:
            loading_bar_top.visible = False
            safe_update()

    # --- FILE PICKER (BLINDADO PARA AWAIT) ---
    #file_picker = ft.FilePicker()
    #if file_picker not in page.overlay:
        #page.overlay.append(file_picker)  # CORREÇÃO: adicionar file_picker no overlay para funcionar

    #async def upload_click(e):
    #    e.control.disabled = True
    #    e.control.update()
    #
    #    result = await file_picker.pick_files(
    #        allow_multiple=False,
    #        allowed_extensions=["pdf", "png", "jpg", "jpeg"]
    #    )

    #    e.control.disabled = False
    #    e.control.update()

    #    if result and result.files:
    #        await process_file_path(result.files[0].path)

    # --- FORMULÁRIO ---
    input_style = {
        "border_radius": 12,
        "bgcolor": ft.Colors.WHITE,
        "border_color": ft.Colors.OUTLINE_VARIANT,
        "content_padding": 15,
        "text_size": 14
    }

    tf_title = ft.TextField(
        label="Título *", prefix_icon=ft.Icons.TITLE, **input_style)
    tf_time = ft.TextField(label="Minutos", width=140,
                           keyboard_type=ft.KeyboardType.NUMBER, prefix_icon=ft.Icons.TIMER, **input_style)
    tf_servings = ft.TextField(
        label="Porções", width=140, prefix_icon=ft.Icons.PEOPLE, **input_style)
    tf_source = ft.TextField(
        label="Fonte / URL", prefix_icon=ft.Icons.LINK, **input_style)
    tf_image = ft.TextField(
        label="URL Imagem", prefix_icon=ft.Icons.IMAGE, **input_style)
    tf_instructions = ft.TextField(
        label="Preparo *", multiline=True, min_lines=5, **input_style)
    tf_add_instructions = ft.TextField(
        label="Dicas", multiline=True, **input_style)

    cat_db = CategoryQueries()
    try:
        cats = cat_db.get_user_categories(user.id)
    except Exception:
        cats = []

    dd_category = ft.Dropdown(
        label="Categoria *",
        options=[ft.dropdown.Option(str(c['id']), c['name']) for c in cats],
        expand=True,
        **input_style
    )

    # --- INGREDIENTES ---
    tf_ing_name = ft.TextField(
        label="Nome (ex: Farinha)", expand=True, height=50, bgcolor="white", border_radius=8)
    tf_ing_qty = ft.TextField(label="Qtd", width=80,
                              height=50, bgcolor="white", border_radius=8)
    tf_ing_unit = ft.TextField(
        label="Unid", width=80, height=50, bgcolor="white", border_radius=8)
    ingredients_col = ft.Column(spacing=5)

    def _render_ingredients(update_ui=True):
        ingredients_col.controls.clear()
        if not vm.temp_ingredients:
            ingredients_col.controls.append(
                ft.Text("Nenhum ingrediente.", size=12, color="grey"))
        else:
            for i, ing in enumerate(vm.temp_ingredients):
                ingredients_col.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.CIRCLE, size=8,
                                    color=ft.Colors.ORANGE_400),
                            ft.Text(f"{ing.name}",
                                    weight=ft.FontWeight.BOLD, expand=True),
                            ft.Text(
                                f"{ing.quantity} {ing.unit}".strip(), color="grey"),
                            ft.IconButton(ft.Icons.CLOSE, icon_color="red", icon_size=18,
                                          on_click=lambda e, idx=i: _remove_ing(idx))
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        bgcolor=ft.Colors.GREY_50,
                        padding=10,
                        border_radius=8
                    )
                )
        if update_ui:
            safe_update(ingredients_col)

    def _add_ing(e):
        if vm.add_temp_ingredient(tf_ing_name.value, tf_ing_qty.value, tf_ing_unit.value):
            tf_ing_name.value = ""
            tf_ing_qty.value = ""
            tf_ing_unit.value = ""
            tf_ing_name.focus()
            safe_update()
            _render_ingredients(update_ui=True)
        else:
            show_msg("Nome inválido", "red")

    def _remove_ing(index):
        vm.remove_temp_ingredient(index)
        _render_ingredients(update_ui=True)

    # --- POPULA CAMPOS (PDF, IMAGEM, WEB) ---
    def populate_fields(data, update_ui=False):
        if not data:
            return
        try:
            tf_title.value = data.get('title', '')
            if data.get('preparation_time'):
                tf_time.value = str(data.get('preparation_time'))
            if data.get('servings'):
                tf_servings.value = str(data.get('servings'))
            tf_instructions.value = data.get('instructions', '')
            if data.get('image_path'):
                tf_image.value = data.get('image_path')
            if data.get('source'):
                tf_source.value = data.get('source')

            if data.get('ingredients'):
                vm.temp_ingredients = []
                for ing in data['ingredients']:
                    vm.add_temp_ingredient(ing['name'], ing.get(
                        'quantity', ''), ing.get('unit', ''))

            _render_ingredients(update_ui=update_ui)
            if update_ui:
                safe_update()
        except Exception as e:
            logger.warning(f"Erro ao popular campos: {e}")

    # --- DIALOG IMPORT WEB ---
    def show_link_dialog(e):
        tf_link = ft.TextField(label="Link", autofocus=True)
        loading_web = ft.ProgressBar(visible=False, color="blue")
        dlg = ft.AlertDialog(
            title=ft.Text("Importar Web"),
            content=ft.Column(
                [ft.Text("Cole um link:"), tf_link, loading_web], tight=True, width=400),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: _close_dlg(dlg)),
                ft.Button("Importar", on_click=lambda e: _run_import(
                    tf_link.value, dlg, loading_web))
            ]
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def _close_dlg(dlg):
        dlg.open = False
        page.update()

    def _run_import(url, dlg, bar):
        if not url:
            return
        bar.visible = True
        dlg.update()
        err, data = vm.import_from_url(url)
        bar.visible = False
        dlg.open = False
        page.update()
        if err:
            show_msg(err, "red")
        else:
            populate_fields(data, update_ui=True)
            show_msg("Sucesso!", "green")
        page.update()

    # --- SAVE RECIPE ---
    async def btn_save_click(e):
        if not tf_title.value or not dd_category.value:
            show_msg("Preencha Título e Categoria.", "red")
            return
        success, msg = vm.save_recipe(
            tf_title.value, tf_time.value, tf_servings.value, tf_instructions.value,
            tf_add_instructions.value, tf_source.value, tf_image.value, dd_category.value
        )
        if success:
            show_msg(msg, "green")
            await page.push_route("/my_recipes")
        else:
            show_msg(msg, "red")

    # --- INIT DATA ---
    existing = vm.load_editing_data()
    pg_title = "Nova Receita"
    if existing:
        pg_title = "Editar Receita"
        populate_fields(existing, update_ui=False)
    else:
        _render_ingredients(update_ui=False)

    # --- VIEW LAYOUT ---
    return ft.View(
        route="/create_recipe",
        appbar=ft.AppBar(
            title=ft.Text(pg_title),
            bgcolor="white",
            leading=ft.IconButton(
                ft.Icons.ARROW_BACK, on_click=lambda _: asyncio.create_task(page.push_route("/my_recipes")))
        ),
        controls=[
            # NÃO adicionar file_picker aqui, pois já está no overlay
            ft.SafeArea(
                expand=True,
                content=ft.Container(
                    padding=20,
                    content=ft.Column([
                        loading_bar_top,
                        ft.Container(
                            padding=10,
                            border_radius=10,
                            bgcolor=ft.Colors.BLUE_50,
                            border=ft.Border.all(1, ft.Colors.BLUE_100),
                            content=ft.Row([
                                ft.Icon(ft.Icons.AUTO_AWESOME, color="blue"),
                                ft.Column([
                                    ft.Text("Inteligência",
                                            weight="bold", color="blue"),
                                    ft.Text("Web, PDF ou Foto",
                                            size=10, color="blue")
                                ], spacing=0, expand=True),
                                ft.IconButton(
                                    ft.Icons.PUBLIC, tooltip="Link Web", icon_color="blue", on_click=show_link_dialog),
                                #ft.IconButton(ft.Icons.UPLOAD_FILE, tooltip="Ler Arquivo", icon_color="blue",
                                #              on_click=lambda e: asyncio.create_task(upload_click(e))),
                                #ft.IconButton(ft.Icons.MIC, tooltip="Voz", icon_color="blue", on_click=lambda e: show_msg(
                                #    "Em breve", "orange"))
                            ])
                        ),
                        ft.Divider(height=20, color="transparent"),
                        tf_title,
                        ft.Row([dd_category, tf_time, tf_servings]),
                        ft.Divider(),
                        ft.Text("Ingredientes", size=16, weight="bold"),
                        ft.Row([tf_ing_name, tf_ing_qty, tf_ing_unit, ft.IconButton(
                            ft.Icons.ADD_CIRCLE, icon_color="green", on_click=_add_ing)]),
                        ft.Container(content=ingredients_col, border=ft.Border.all(
                            1, ft.Colors.GREY_300), border_radius=8, padding=10, bgcolor="white"),
                        ft.Divider(),
                        ft.Text("Instruções", size=16, weight="bold"),
                        tf_instructions, tf_add_instructions, tf_source, tf_image,
                        ft.Container(height=20),
                        ft.Button("Salvar Receita", on_click=lambda e: asyncio.create_task(btn_save_click(e)),
                                  bgcolor="orange", color="white", height=50, width=float("inf")),
                        ft.Container(height=50)
                    ], scroll=ft.ScrollMode.AUTO, expand=True)
                )
            )
        ],
        bgcolor="white"
    )