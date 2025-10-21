import flet as ft
from src.viewmodels.register_viewmodel import RegisterViewModel
from src.views.components.app_footer import AppFooter
from src.utils.theme import AppDimensions, AppFonts

def RegisterView(page: ft.Page) -> ft.View:
    """
    Retorna a ft.View para a rota de Registro.
    (CORRIGIDO) Corrigido o problema de renderização (tela em branco)
    ao usar as cores de referência do Flet.
    """
    
    vm = RegisterViewModel(page)
    
    # --- Controles do formulário (sem alterações) ---
    name_field = ft.TextField(
        label="Nome Completo",
        prefix_icon=ft.Icons.PERSON_OUTLINE
    )
    
    email_field = ft.TextField(
        label="Email",
        keyboard_type=ft.KeyboardType.EMAIL,
        prefix_icon=ft.Icons.EMAIL_OUTLINED
    )
    
    password_field = ft.TextField(
        label="Senha (mín. 6 caracteres)",
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.Icons.LOCK_OUTLINED
    )
    
    register_button = ft.ElevatedButton(
        text="Registrar",
        icon=ft.Icons.PERSON_ADD,
        on_click=vm.on_register_click,
        width=float('inf')
    )
    
    login_button = ft.TextButton(
        text="Já tem uma conta? Faça login.",
        on_click=vm.on_navigate_to_login,
        width=float('inf')
    )
    
    vm.set_controls(name_field, email_field, password_field)
    
    # --- Card do formulário (CORRIGIDO) ---
    register_form_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Criar Nova Conta", size=AppFonts.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                name_field,
                email_field,
                password_field,
                register_button,
                login_button
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=AppDimensions.FIELD_MAX_WIDTH,
        padding=AppDimensions.PAGE_PADDING,
        border_radius=AppDimensions.BORDER_RADIUS,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            offset=ft.Offset(0, 5),
        ),
        # (CORRIGIDO) Usando a cor de referência do Flet.
        bgcolor=ft.Colors.SURFACE,
    )
    
    # --- Layout principal (sem alterações) ---
    main_content = ft.Column(
        controls=[
            ft.Container(
                content=ft.Row(
                    [register_form_card],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                alignment=ft.alignment.center,
                expand=True,
                padding=ft.padding.symmetric(horizontal=AppDimensions.PAGE_PADDING)
            ),
            AppFooter()
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        expand=True,
        scroll=ft.ScrollMode.ADAPTIVE,
    )

    return ft.View(
        route="/register",
        controls=[
            ft.SafeArea(
                content=main_content,
                expand=True
            )
        ],
        padding=0,
        # (CORRIGIDO) Usando a cor de referência do Flet.
        bgcolor=page.theme.color_scheme.background,
    )
