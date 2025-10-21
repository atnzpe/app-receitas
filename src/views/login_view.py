import flet as ft
from src.viewmodels.login_viewmodel import LoginViewModel
from src.views.components.app_footer import AppFooter
from src.utils.theme import AppDimensions, AppFonts

def LoginView(page: ft.Page) -> ft.View:
    """
    Retorna a ft.View para a rota de Login.
    (CORRIGIDO) Corrigido o problema de renderização (tela em branco)
    ao usar as cores de referência do Flet (ex: ft.Colors.SURFACE),
    que são mapeadas pelo tema global.
    """
    
    vm = LoginViewModel(page)
    
    # --- Controles do formulário (sem alterações) ---
    email_field = ft.TextField(
        label="Email",
        keyboard_type=ft.KeyboardType.EMAIL,
        prefix_icon=ft.Icons.EMAIL_OUTLINED
    )
    
    password_field = ft.TextField(
        label="Senha",
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.Icons.LOCK_OUTLINED
    )
    
    login_button = ft.ElevatedButton(
        text="Entrar",
        icon=ft.Icons.LOGIN,
        on_click=vm.on_login_click,
        width=float('inf')
    )
    
    register_button = ft.TextButton(
        text="Não tem uma conta? Registre-se aqui.",
        on_click=vm.on_navigate_to_register,
        width=float('inf')
    )
    
    vm.set_controls(email_field, password_field)

    # --- Card do formulário (CORRIGIDO) ---
    login_form_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("App de Receitas", size=AppFonts.TITLE_LARGE, weight=ft.FontWeight.BOLD),
                ft.Text("Faça login para continuar", size=AppFonts.BODY_MEDIUM, color=ft.Colors.GREY_700),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                email_field,
                password_field,
                login_button,
                register_button
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
        # O tema global irá mapear 'SURFACE' para a cor correta (clara ou escura).
        bgcolor=ft.Colors.SURFACE,
    )
    
    # --- Layout principal (sem alterações) ---
    main_content = ft.Column(
        controls=[
            ft.Container(
                content=ft.Row(
                    [login_form_card],
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
        route="/login",
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
