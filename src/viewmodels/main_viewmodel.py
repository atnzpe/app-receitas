# CÓDIGO COMPLETO E COMENTADO
"""
ViewModel para a MainView.

O ViewModel é o cérebro da View. Ele contém a lógica de estado
e interage com as camadas de 'Queries' para buscar dados.

Princípio de Desacoplamento:
Este arquivo NUNCA deve importar 'flet' (ft).
A View importa o ViewModel, mas o ViewModel não conhece a View.
"""

class MainViewModel:
    """
    Coordena o estado e a lógica da visualização principal.
    """
    
    def __init__(self):
        """
        Inicializa o ViewModel.
        As propriedades aqui definirão o estado inicial da View.
        """
        # Propriedades de estado (que serão 'bindadas' pela View)
        self.app_title = "Guia Mestre de Receitas"
        self.status_message = "Estrutura MVVM inicializada."
        
        # Em Flet, para reatividade, a View observará estas propriedades
        # ou o ViewModel conterá referências aos controles (Flet)
        # para atualizá-los. Iniciaremos com o 'binding' simples.
        
        self.load_initial_data()

    def load_initial_data(self):
        """
        Método de exemplo para carregar dados na inicialização.
        """
        # Aqui é onde chamaríamos a camada de Queries, por exemplo:
        # from src.database import queries
        # self.categories_count = queries.get_categories_count()
        # self.status_message = f"{self.categories_count} categorias carregadas."
        
        print("MainViewModel: Dados iniciais carregados (simulação).")