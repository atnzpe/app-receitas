# ARQUIVO: src/viewmodels/category_viewmodel.py
import flet as ft
from typing import List
from src.core.logger import get_logger
from src.database.category_queries import CategoryQueries
from src.models.recipe_model import Category
from src.models.user_model import User

logger = get_logger("src.viewmodels.category")

class CategoryViewModel:
    def __init__(self, page: ft.Page):
        self.page = page
        self.db = CategoryQueries()
        self.categories: List[Category] = []
        self.user: User = self.page.data.get("logged_in_user")
        
        # Referências UI
        self.list_view = None
        self.dialog = None
        self.name_field = None

    def initialize(self):
        self.load_data(update_ui=False)

    def load_data(self, update_ui=True):
        if not self.user: return
        try:
            self.categories = self.db.get_all_categories_for_user(self.user.id)
            self._populate_list()
            if update_ui and self.list_view:
                self.list_view.update()
        except Exception as e:
            logger.error(f"Erro load: {e}")

    def _populate_list(self):
        if not self.list_view: return
        self.list_view.controls.clear()
        
        if not self.categories:
            self.list_view.controls.append(ft.Text("Nenhuma categoria.", color="grey"))
            return

        for cat in self.categories:
            self.list_view.controls.append(self._create_tile(cat))

    def _create_tile(self, cat: Category):
        is_mine = cat.user_id == self.user.id
        icon = ft.Icons.VERIFIED if not cat.user_id else ft.Icons.LABEL
        color = ft.Colors.BLUE if not cat.user_id else ft.Colors.ORANGE
        
        return ft.ListTile(
            leading=ft.Icon(icon, color=color),
            title=ft.Text(cat.name, weight="bold"),
            subtitle=ft.Text("Sistema" if not cat.user_id else "Pessoal", size=12),
            on_click=lambda e, c=cat: self.navigate_to_recipes(c),
            trailing=ft.Row([
                ft.IconButton(
                    icon=ft.Icons.STAR if cat.is_favorite else ft.Icons.STAR_BORDER,
                    icon_color=ft.Colors.AMBER if cat.is_favorite else ft.Colors.GREY,
                    tooltip="Favoritar Categoria",
                    on_click=lambda e, c=cat: self.toggle_favorite(c)
                ),
                ft.IconButton(
                    ft.Icons.DELETE, icon_color="red", 
                    visible=is_mine,
                    on_click=lambda e, id=cat.id: self.delete_category(id)
                ) if is_mine else ft.Container()
            ], width=100)
        )

    def navigate_to_recipes(self, cat: Category):
        logger.info(f"Navegando para receitas da categoria: {cat.name}")
        self.page.data["filter_category_id"] = cat.id
        self.page.data["filter_category_name"] = cat.name
        self.page.push_route("/discovery") # Usa push_route padronizado

    def toggle_favorite(self, cat: Category):
        try:
            # [CORREÇÃO] Chamada correta ao método CASCADE
            status = self.db.toggle_favorite_cascade(cat.id, self.user.id)
            msg = "Categoria e receitas favoritas!" if status else "Removido dos favoritos."
            
            self.page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=ft.Colors.GREEN if status else ft.Colors.GREY)
            self.page.snack_bar.open = True
            
            # Recarrega para atualizar ícone visualmente
            self.load_data(update_ui=True)
            
        except Exception as e:
            logger.error(f"Erro fav: {e}")
            self.page.snack_bar = ft.SnackBar(ft.Text("Erro ao favoritar."), bgcolor=ft.Colors.RED)
            self.page.snack_bar.open = True
            self.page.update()

    # --- CRUD Auxiliar ---
    def open_dialog(self, e):
        if self.name_field: self.name_field.value = ""
        if self.dialog:
            self.dialog.open = True
            self.page.update()

    def close_dialog(self, e=None):
        if self.dialog:
            self.dialog.open = False
            self.page.update()

    def save_category(self, e):
        if not self.name_field.value: return
        if self.db.add_category(self.name_field.value, self.user.id):
            self.close_dialog()
            self.load_data()
        else:
            self.name_field.error_text = "Erro/Duplicado."
            self.name_field.update()

    def delete_category(self, cat_id: int):
        if self.db.delete_category(cat_id, self.user.id):
            self.load_data()