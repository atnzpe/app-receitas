# ARQUIVO: src/utils/theme.py
import flet as ft

# =================================================================================
# PALETAS DE CORES
# =================================================================================

# Tema Claro
light_color_scheme = ft.ColorScheme(
    primary=ft.Colors.ORANGE_700,
    on_primary=ft.Colors.WHITE,
    primary_container=ft.Colors.ORANGE_100,
    on_primary_container=ft.Colors.ORANGE_900,
    surface=ft.Colors.GREY_50,
    on_surface=ft.Colors.GREY_900,
    on_surface_variant=ft.Colors.GREY_700,
    error=ft.Colors.RED_700,
    on_error=ft.Colors.WHITE,
    outline=ft.Colors.GREY_500,
)

# Tema Escuro
dark_color_scheme = ft.ColorScheme(
    primary=ft.Colors.ORANGE_400,
    on_primary=ft.Colors.BLACK,
    primary_container=ft.Colors.ORANGE_900,
    on_primary_container=ft.Colors.ORANGE_100,
    surface="#121212",
    on_surface=ft.Colors.WHITE,
    on_surface_variant=ft.Colors.GREY_400,
    error=ft.Colors.RED_300,
    on_error=ft.Colors.BLACK,
    outline=ft.Colors.GREY_600,
)


class AppFonts:
    TITLE_LARGE = 32
    TITLE_MEDIUM = 24
    BODY_LARGE = 18
    BODY_MEDIUM = 16
    BODY_SMALL = 14


class AppDimensions:
    FIELD_MAX_WIDTH = 600
    BORDER_RADIUS = 12
    PAGE_PADDING = 20
    CARD_ELEVATION = 4
    ICON_SIZE_MEDIUM = 28
    ICON_CONTAINER_SIZE = 56
    ICON_CONTAINER_BORDER_RADIUS = 28
    SMALL_SPACING = 8
    MEDIUM_SPACING = 16
    LARGE_SPACING = 24
    FOOTER_HEIGHT = 50
    FOOTER_ICON_SIZE = 18
    SCROLLBAR_THICKNESS = 10  # [UX] Mais grossa para facilitar o clique
    SCROLLBAR_RADIUS = 5


# [CONFIGURAÇÃO GLOBAL DE SCROLLBAR]
# Blindagem: ThumbVisibility=True força a barra a aparecer sempre.
global_scrollbar_theme = ft.ScrollbarTheme(
    thumb_visibility=True,
    thickness=10,
    radius=5,
    thumb_color={
        ft.ControlState.HOVERED: ft.Colors.ORANGE_800,
        ft.ControlState.DEFAULT: ft.Colors.ORANGE_400,
    },
    track_visibility=True,
    track_color={
        ft.ControlState.DEFAULT: ft.Colors.with_opacity(0.1, ft.Colors.GREY),
    },
     # Trilha visível para contexto
    interactive=True
)


class AppThemes:
    light_theme = ft.Theme(
        color_scheme=light_color_scheme,
        visual_density=ft.VisualDensity.ADAPTIVE_PLATFORM_DENSITY,
        use_material3=True,
        scrollbar_theme=global_scrollbar_theme
    )
    dark_theme = ft.Theme(
        color_scheme=dark_color_scheme,
        visual_density=ft.VisualDensity.ADAPTIVE_PLATFORM_DENSITY,
        use_material3=True,
        scrollbar_theme=global_scrollbar_theme
    )


CARD_COLORS = {
    "Receitas": {"bg_light": ft.Colors.RED_100, "fg_light": ft.Colors.RED_800, "bg_dark": ft.Colors.RED_900, "fg_dark": ft.Colors.RED_100},
    "Cadastros": {"bg_light": ft.Colors.BLUE_100, "fg_light": ft.Colors.BLUE_800, "bg_dark": ft.Colors.BLUE_900, "fg_dark": ft.Colors.BLUE_100},
    "Discovery": {"bg_light": ft.Colors.AMBER_100, "fg_light": ft.Colors.AMBER_900, "bg_dark": ft.Colors.AMBER_900, "fg_dark": ft.Colors.AMBER_100},
    "Mercado": {"bg_light": ft.Colors.GREEN_100, "fg_light": ft.Colors.GREEN_800, "bg_dark": ft.Colors.GREEN_900, "fg_dark": ft.Colors.GREEN_100},
    "Lista": {"bg_light": ft.Colors.PURPLE_100, "fg_light": ft.Colors.PURPLE_800, "bg_dark": ft.Colors.PURPLE_900, "fg_dark": ft.Colors.PURPLE_100},
}
