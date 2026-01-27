# ARQUIVO: src/views/components/dashboard_card.py
import flet as ft


def DashboardCard(icon: str, title: str, description: str, color: str, on_click):
    """
    Componente de Card Responsivo.
    """
    return ft.Card(
        elevation=2,
        # [CORREÇÃO] Removido surface_tint_color para compatibilidade
        # Se quiser dar um tom de cor, podemos usar o Container interno, mas o padrão é mais seguro.

        # Container define o padding e clique, mas SEM height fixo
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        # Ícone como argumento posicional (sem 'name=')
                        content=ft.Icon(icon, size=40, color=color),
                        # Uso explícito de ft.Alignment(0, 0)
                        alignment=ft.Alignment(0, 0),
                        padding=ft.padding.only(bottom=10)
                    ),
                    ft.Text(
                        value=title,
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.ON_SURFACE
                    ),
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        value=description,
                        size=14,
                        color=ft.Colors.ON_SURFACE_VARIANT,
                        text_align=ft.TextAlign.CENTER,
                        # Garante que o texto quebre linha e não seja cortado
                        no_wrap=False,
                        selectable=False
                    )
                ],
                # Centraliza e ajusta ao tamanho do conteúdo
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True,
                spacing=5
            ),
            padding=20,
            border_radius=10,
            on_click=on_click,
            ink=True
        )
    )
