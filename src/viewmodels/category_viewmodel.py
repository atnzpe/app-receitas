# ARQUIVO: src/viewmodels/category_viewmodel.py
# CÓDIGO COMPLETO E BLINDADO
from typing import List, Optional
import flet as ft

from src.core.logger import get_logger
from src.database import category_queries
from src.models.recipe_model import Category

logger = get_logger("src.viewmodels.category")


class CategoryViewModel:
    def __init__(self, page: ft.Page):
        self.page = page
        self.categories: List[Category] = []

        # Referências aos controles da UI (Injeção de Dependência)
        self.list_view: Optional[ft.ListView] = None
        self.dialog: Optional[ft.AlertDialog] = None
        self.name_field: Optional[ft.TextField] = None

        # Estado: Se tiver ID, é edição. Se None, é criação.
        self.editing_id: Optional[int] = None

    def initialize(self):
        """Método chamado ao montar a tela (Ciclo de vida)."""
        self.load_data()

    def load_data(self):
        """Busca dados atualizados e redesenha a lista."""
        try:
            self.categories = category_queries.get_all_categories()
            self._render_list()
        except Exception as e:
            logger.error(f"Erro na ViewModel ao carregar: {e}")
            self._show_snack("Erro ao carregar dados.", is_error=True)

    def _render_list(self):
        """Atualiza a UI da lista (ListView)."""
        if not self.list_view:
            return

        self.list_view.controls.clear()

        if not self.categories:
            self.list_view.controls.append(
                ft.Container(
                    content=ft.Text(
                        "Nenhuma categoria encontrada.", italic=True),
                    alignment=ft.alignment.center,
                    padding=20
                )
            )
        else:
            for cat in self.categories:
                # Criação dinâmica dos itens (ListTile)
                self.list_view.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.RESTAURANT_MENU,
                                        color=ft.Colors.ORANGE_400),
                        title=ft.Text(cat.name, weight=ft.FontWeight.W_500),
                        # Menu de Ações (Editar/Excluir)
                        trailing=ft.PopupMenuButton(
                            icon=ft.Icons.MORE_VERT,
                            items=[
                                ft.PopupMenuItem(
                                    text="Editar",
                                    icon=ft.Icons.EDIT,
                                    on_click=lambda e, c=cat: self.open_dialog(
                                        c)
                                ),
                                ft.PopupMenuItem(
                                    text="Excluir",
                                    icon=ft.Icons.DELETE,
                                    on_click=lambda e, id=cat.id: self.delete_category(
                                        id)
                                ),
                            ]
                        )
                    )
                )
        self.list_view.update()

    def open_dialog(self, category: Optional[Category] = None):
        """Prepara e abre o modal."""
        self.editing_id = category.id if category else None

        if self.name_field:
            self.name_field.value = category.name if category else ""
            self.name_field.error_text = None
            self.name_field.focus()

        if self.dialog:
            self.dialog.title = ft.Text(
                "Editar Categoria" if category else "Nova Categoria")
            self.dialog.open = True
            self.page.update()

    def close_dialog(self, e=None):
        if self.dialog:
            self.dialog.open = False
            self.page.update()

    def save_category(self, e):
        """Ação de Salvar (Decide se é Create ou Update)."""
        name = self.name_field.value.strip()

        # Validação de UI (Fail-Fast)
        if len(name) < 3:
            self.name_field.error_text = "Nome muito curto (mín. 3 letras)."
            self.name_field.update()
            return

        try:
            if self.editing_id:
                # Fluxo de Atualização
                if category_queries.update_category(self.editing_id, name):
                    self._show_snack("Categoria atualizada com sucesso!")
                else:
                    self.name_field.error_text = "Este nome já existe."
                    self.name_field.update()
                    return
            else:
                # Fluxo de Criação
                if category_queries.add_category(name):
                    self._show_snack("Categoria criada com sucesso!")
                else:
                    self.name_field.error_text = "Esta categoria já existe."
                    self.name_field.update()
                    return

            self.close_dialog()
            self.load_data()  # Refresh na lista

        except Exception as ex:
            logger.error(f"Erro ao salvar: {ex}")
            self._show_snack("Erro interno ao salvar.", is_error=True)

    def delete_category(self, cat_id: int):
        """Ação de Exclusão."""
        try:
            if category_queries.delete_category(cat_id):
                self._show_snack("Categoria removida.")
                self.load_data()
            else:
                self._show_snack("Erro ao remover.", is_error=True)
        except Exception as ex:
            logger.error(f"Erro ao deletar: {ex}")
            self._show_snack("Erro crítico ao deletar.", is_error=True)

    def _show_snack(self, text, is_error=False):
        """Feedback visual padrão."""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(text),
            bgcolor=ft.Colors.RED if is_error else ft.Colors.GREEN_700,
            behavior=ft.SnackBarBehavior.FLOATING
        )
        self.page.snack_bar.open = True
        self.page.update()
