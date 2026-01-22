"""
Aplicação Principal - Sistema de Vendas e Estoque
"""
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from models.database import db, criar_tabelas
from views.produto_view import ProdutoView


class JanelaPrincipal(QMainWindow):
    """Janela principal do sistema"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Vendas e Estoque")
        self.setGeometry(100, 100, 1200, 700)
        
        # Inicializar banco de dados
        self.inicializar_banco()
        
        # Configurar interface
        self.configurar_ui()
    
    def inicializar_banco(self):
        """Inicializa o banco de dados"""
        try:
            db.connect()
            criar_tabelas()
            print("Banco de dados inicializado com sucesso!")
        except Exception as e:
            print(f"Erro ao inicializar banco de dados: {e}")
    
    def configurar_ui(self):
        """Configura a interface gráfica"""
        # Widget central
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        
        # Layout principal
        layout = QVBoxLayout(widget_central)
        
        # Abas
        self.abas = QTabWidget()
        layout.addWidget(self.abas)
        
        # Criar abas
        self.criar_aba_vendas()
        self.criar_aba_produtos()
        self.criar_aba_clientes()
        self.criar_aba_estoque()
        self.criar_aba_relatorios()
    
    def criar_aba_vendas(self):
        """Cria a aba de vendas"""
        aba_vendas = QWidget()
        layout = QVBoxLayout(aba_vendas)
        # Aqui virá a interface de vendas
        self.abas.addTab(aba_vendas, "💰 Vendas")
    
    def criar_aba_produtos(self):
        """Cria a aba de produtos"""
        self.aba_produtos = ProdutoView()
        self.abas.addTab(self.aba_produtos, "📦 Produtos")
    
    def criar_aba_clientes(self):
        """Cria a aba de clientes"""
        aba_clientes = QWidget()
        layout = QVBoxLayout(aba_clientes)
        # Aqui virá a interface de clientes
        self.abas.addTab(aba_clientes, "👥 Clientes")
    
    def criar_aba_estoque(self):
        """Cria a aba de estoque"""
        aba_estoque = QWidget()
        layout = QVBoxLayout(aba_estoque)
        # Aqui virá a interface de estoque
        self.abas.addTab(aba_estoque, "📊 Estoque")
    
    def criar_aba_relatorios(self):
        """Cria a aba de relatórios"""
        aba_relatorios = QWidget()
        layout = QVBoxLayout(aba_relatorios)
        # Aqui virá a interface de relatórios
        self.abas.addTab(aba_relatorios, "📈 Relatórios")
    
    def closeEvent(self, event):
        """Fecha a conexão com o banco ao fechar o aplicativo"""
        if not db.is_closed():
            db.close()
        event.accept()


def main():
    """Função principal"""
    app = QApplication(sys.argv)
    
    # Estilo da aplicação
    app.setStyle('Fusion')
    
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()