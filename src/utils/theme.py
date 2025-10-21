# CÓDIGO ALTERADO E COMENTADO
# -*- coding: utf-8 -*-

import flet as ft

# =================================================================================
# PALETAS DE CORES
# =================================================================================

light_color_scheme = ft.ColorScheme(
    primary=ft.Colors.BLUE_GREY_800,
    on_primary=ft.Colors.WHITE,
    primary_container=ft.Colors.BLUE_GREY_100,
    on_primary_container=ft.Colors.BLUE_GREY_900,
    secondary=ft.Colors.TEAL_600,
    on_secondary=ft.Colors.WHITE,
    background=ft.Colors.WHITE,
    on_background=ft.Colors.BLACK,  # Alto contraste
    surface=ft.Colors.GREY_50,
    on_surface=ft.Colors.BLACK,  # Alto contraste
    surface_variant=ft.Colors.GREY_200,  # Cor para Cards/Containers elevados
    on_surface_variant=ft.Colors.BLACK,
    error=ft.Colors.RED_700,
    on_error=ft.Colors.WHITE,
    error_container=ft.Colors.with_opacity(0.2, ft.Colors.RED_700),
    on_error_container=ft.Colors.RED_700,
    outline=ft.Colors.GREY_400,
)

dark_color_scheme = ft.ColorScheme(
    primary=ft.Colors.CYAN_ACCENT_400,
    on_primary=ft.Colors.BLACK,
    primary_container=ft.Colors.CYAN_800,
    on_primary_container=ft.Colors.CYAN_50,
    secondary=ft.Colors.TEAL_ACCENT_400,
    on_secondary=ft.Colors.BLACK,
    background="#121212",
    on_background=ft.Colors.WHITE,  # Alto contraste
    surface="#1e1e1e",  # Cor para Cards/Containers elevados
    on_surface=ft.Colors.WHITE,  # Alto contraste
    surface_variant=ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
    on_surface_variant=ft.Colors.WHITE,
    error=ft.Colors.RED_400,
    on_error=ft.Colors.BLACK,
    error_container=ft.Colors.with_opacity(0.2, ft.Colors.RED_400),
    on_error_container=ft.Colors.RED_400,
    outline=ft.Colors.GREY_700,
)

# =================================================================================
# TEMAS COMPLETOS
# =================================================================================


class AppThemes:
    light_theme = ft.Theme(
        color_scheme=light_color_scheme, visual_density=ft.VisualDensity.COMPACT
    )
    dark_theme = ft.Theme(
        color_scheme=dark_color_scheme, visual_density=ft.VisualDensity.COMPACT
    )


# =================================================================================
# FONTES E DIMENSÕES
# =================================================================================


class AppFonts:
    TITLE_LARGE = 32
    TITLE_MEDIUM = 28
    BODY_LARGE = 20
    BODY_MEDIUM = 16
    BODY_SMALL = 14


class AppDimensions:
    FIELD_MAX_WIDTH = 400
    BORDER_RADIUS = 10
    PAGE_PADDING = 15
    CARD_ELEVATION = 4
    # (NOVAS CONSTANTES) Para centralizar valores usados nos componentes
    ICON_SIZE_MEDIUM = 32
    ICON_CONTAINER_SIZE = 64
    ICON_CONTAINER_BORDER_RADIUS = 32  # Metade do ICON_CONTAINER_SIZE
    SMALL_SPACING = 5
    MEDIUM_SPACING = 10
    LARGE_SPACING = 20
    FOOTER_HEIGHT = 40
    FOOTER_ICON_SIZE = 16


# =================================================================================
# CONSTANTES DE CORES ESPECÍFICAS
# =================================================================================


# Cores dos cards do Dashboard
CARD_COLORS = {
    "Receitas": {
        "bg_light": ft.Colors.RED_100,
        "fg_light": ft.Colors.RED_600,
        "bg_dark": ft.Colors.with_opacity(0.4, ft.Colors.RED_900),
        "fg_dark": ft.Colors.RED_300,
    },
    "Cadastros": {
        "bg_light": ft.Colors.BLUE_100,
        "fg_light": ft.Colors.BLUE_600,
        "bg_dark": ft.Colors.with_opacity(0.4, ft.Colors.BLUE_900),
        "fg_dark": ft.Colors.BLUE_300,
    },
    "Discovery": {
        "bg_light": ft.Colors.YELLOW_100,
        "fg_light": ft.Colors.YELLOW_700,
        "bg_dark": ft.Colors.with_opacity(0.4, ft.Colors.YELLOW_900),
        "fg_dark": ft.Colors.YELLOW_300,
    },
    "Mercado": {
        "bg_light": ft.Colors.GREEN_100,
        "fg_light": ft.Colors.GREEN_600,
        "bg_dark": ft.Colors.with_opacity(0.4, ft.Colors.GREEN_900),
        "fg_dark": ft.Colors.GREEN_300,
    },
    "Lista": {
        "bg_light": ft.Colors.PURPLE_100,
        "fg_light": ft.Colors.PURPLE_600,
        "bg_dark": ft.Colors.with_opacity(0.4, ft.Colors.PURPLE_900),
        "fg_dark": ft.Colors.PURPLE_300,
    },
}
