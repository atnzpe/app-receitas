# CÓDIGO COMPLETO E COMENTADO
# -*- coding: utf-8 -*-

# =================================================================================
# MÓDULO DE ESTILOS E TEMAS GLOBAIS (theme.py)
#
# OBJETIVO: Centralizar todas as constantes de design da aplicação, como cores,
#           fontes, dimensões e estilos de componentes.
#           Baseado no 'style.py' fornecido pelo Arquiteto.
# =================================================================================

import flet as ft

# =================================================================================
# PALETAS DE CORES (Definidas pelo Arquiteto)
# =================================================================================

light_color_scheme = ft.ColorScheme(
    primary=ft.Colors.BLUE_GREY_800,
    on_primary=ft.Colors.WHITE,
    primary_container=ft.Colors.BLUE_GREY_100,
    on_primary_container=ft.Colors.BLUE_GREY_900,
    secondary=ft.Colors.TEAL_600,
    on_secondary=ft.Colors.WHITE,
    background=ft.Colors.WHITE,
    on_background=ft.Colors.BLACK87,
    surface=ft.Colors.GREY_50,
    on_surface=ft.Colors.BLACK87,
    error=ft.Colors.RED_700,
    on_error=ft.Colors.WHITE,
    error_container=ft.Colors.with_opacity(0.2, ft.Colors.RED_700),
    on_error_container=ft.Colors.RED_700,
)

dark_color_scheme = ft.ColorScheme(
    primary=ft.Colors.CYAN_ACCENT_400,
    on_primary=ft.Colors.BLACK,
    primary_container=ft.Colors.CYAN_800,
    on_primary_container=ft.Colors.CYAN_50,
    secondary=ft.Colors.TEAL_ACCENT_400,
    on_secondary=ft.Colors.BLACK,
    background="#121212",
    on_background=ft.Colors.WHITE,
    surface="#1e1e1e",
    on_surface=ft.Colors.WHITE,
    error=ft.Colors.RED_400,
    on_error=ft.Colors.BLACK,
    error_container=ft.Colors.with_opacity(0.2, ft.Colors.RED_400),
    on_error_container=ft.Colors.RED_400,
)

# =================================================================================
# TEMAS COMPLETOS (Definidos pelo Arquiteto)
# =================================================================================

class AppThemes:
    """
    Agrupa os objetos de Tema (ft.Theme) completos para fácil importação.
    """
    light_theme = ft.Theme(
        color_scheme=light_color_scheme,
        visual_density=ft.VisualDensity.COMPACT
    )
    dark_theme = ft.Theme(
        color_scheme=dark_color_scheme,
        visual_density=ft.VisualDensity.COMPACT
    )

# =================================================================================
# FONTES E DIMENSÕES (Definidos pelo Arquiteto)
# =================================================================================

class AppFonts:
    """
    Define os tamanhos de fonte padrão para a aplicação.
    """
    TITLE_LARGE = 32
    TITLE_MEDIUM = 28
    BODY_LARGE = 20
    BODY_MEDIUM = 16
    BODY_SMALL = 14

class AppDimensions:
    """
    Define dimensões e raios de borda reutilizáveis.
    """
    FIELD_MAX_WIDTH = 400
    BORDER_RADIUS = 10
    PAGE_PADDING = 15
    CARD_ELEVATION = 4

# =================================================================================
# CONSTANTES DE CORES ESPECÍFICAS (Definidas por nós)
# =================================================================================

# Cores dos cards do Dashboard
CARD_COLORS = {
    "Receitas": {
        "bg_light": ft.Colors.RED_100, "fg_light": ft.Colors.RED_600,
        "bg_dark": ft.Colors.with_opacity(0.4, ft.Colors.RED_900), "fg_dark": ft.Colors.RED_300
    },
    "Cadastros": {
        "bg_light": ft.Colors.BLUE_100, "fg_light": ft.Colors.BLUE_600,
        "bg_dark": ft.Colors.with_opacity(0.4, ft.Colors.BLUE_900), "fg_dark": ft.Colors.BLUE_300
    },
    "Discovery": {
        "bg_light": ft.Colors.YELLOW_100, "fg_light": ft.Colors.YELLOW_700,
        "bg_dark": ft.Colors.with_opacity(0.4, ft.Colors.YELLOW_900), "fg_dark": ft.Colors.YELLOW_300
    },
    "Mercado": {
        "bg_light": ft.Colors.GREEN_100, "fg_light": ft.Colors.GREEN_600,
        "bg_dark": ft.Colors.with_opacity(0.4, ft.Colors.GREEN_900), "fg_dark": ft.Colors.GREEN_300
    },
    "Lista": {
        "bg_light": ft.Colors.PURPLE_100, "fg_light": ft.Colors.PURPLE_600,
        "bg_dark": ft.Colors.with_opacity(0.4, ft.Colors.PURPLE_900), "fg_dark": ft.Colors.PURPLE_300
    },
}