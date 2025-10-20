# CÓDIGO COMPLETO E COMENTADO
import flet as ft
from src.viewmodels.main_viewmodel import MainViewModel

class MainView(ft.UserControl):
    """
    A View principal (raiz) do aplicativo.
    
    Seguindo o MVVM:
    - A View é 'burra' (dumb). Ela apenas exibe os controles.
    - Ela instancia seu ViewModel.
    - Ela 'binda' (liga) seus controles às propriedades do ViewModel.
    - Ela lida com eventos de UI (ex: cliques) e os repassa
      para métodos no ViewModel.
    """
    
    def __init__(self):
        super().__init__()
        # 1. Instanciar o ViewModel
        # O ViewModel agora gerencia o estado desta View.
        self.view_model = MainViewModel()

    def build(self):
        """
        Constrói a interface gráfica da View (os controles Flet).
        """
        
        # 2. 'Bindar' (ligar) os controles às propriedades do ViewModel
        self.app_title = ft.Text(
            value=self.view_model.app_title, # BIND
            size=32, 
            weight=ft.FontWeight.BOLD
        )
        self.status_text = ft.Text(
            value=self.view_model.status_message # BIND
        )

        # Layout principal (placeholder inicial)
        return ft.Container(
            content=ft.Column(
                controls=[
                    self.app_title,
                    self.status_text,
                    ft.Divider(),
                    ft.Text("Próxima etapa: Implementar Autenticação e Roteamento."),
                    ft.Icon(ft.icons.RESTAURANT_MENU)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            alignment=ft.alignment.center,
            expand=True,
            padding=20
        )