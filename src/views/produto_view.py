"""
Interface gráfica para cadastro de produtos
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QTableWidget, QTableWidgetItem, QLineEdit, QLabel,
                               QDialog, QFormLayout, QTextEdit, QComboBox,
                               QDoubleSpinBox, QSpinBox, QMessageBox, QHeaderView,
                               QGroupBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from controllers.produto_controller import ProdutoController
from models.database import Categoria


class DialogoProduto(QDialog):
    """Diálogo para criar/editar produto"""
    
    def __init__(self, parent=None, produto=None):
        super().__init__(parent)
        self.produto = produto
        self.setWindowTitle("Novo Produto" if not produto else "Editar Produto")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        self.configurar_ui()
        
        if produto:
            self.preencher_dados()
    
    def configurar_ui(self):
        """Configura a interface do diálogo"""
        layout = QVBoxLayout(self)
        
        # Formulário
        form_layout = QFormLayout()
        
        # Código
        self.txt_codigo = QLineEdit()
        self.txt_codigo.setMaxLength(50)
        form_layout.addRow("Código*:", self.txt_codigo)
        
        # Nome
        self.txt_nome = QLineEdit()
        self.txt_nome.setMaxLength(200)
        form_layout.addRow("Nome*:", self.txt_nome)
        
        # Descrição
        self.txt_descricao = QTextEdit()
        self.txt_descricao.setMaximumHeight(80)
        form_layout.addRow("Descrição:", self.txt_descricao)
        
        # Categoria
        self.cmb_categoria = QComboBox()
        self.carregar_categorias()
        form_layout.addRow("Categoria:", self.cmb_categoria)
        
        # Preço de Custo
        self.spin_preco_custo = QDoubleSpinBox()
        self.spin_preco_custo.setPrefix("R$ ")
        self.spin_preco_custo.setMaximum(999999.99)
        self.spin_preco_custo.setDecimals(2)
        form_layout.addRow("Preço de Custo*:", self.spin_preco_custo)
        
        # Preço de Venda
        self.spin_preco_venda = QDoubleSpinBox()
        self.spin_preco_venda.setPrefix("R$ ")
        self.spin_preco_venda.setMaximum(999999.99)
        self.spin_preco_venda.setDecimals(2)
        self.spin_preco_venda.valueChanged.connect(self.calcular_margem)
        form_layout.addRow("Preço de Venda*:", self.spin_preco_venda)
        
        # Margem de Lucro (apenas exibição)
        self.lbl_margem = QLabel("0.00%")
        self.lbl_margem.setStyleSheet("color: green; font-weight: bold;")
        form_layout.addRow("Margem de Lucro:", self.lbl_margem)
        
        # Estoque Atual
        self.spin_estoque_atual = QSpinBox()
        self.spin_estoque_atual.setMaximum(999999)
        if not self.produto:  # Apenas para novos produtos
            form_layout.addRow("Estoque Inicial:", self.spin_estoque_atual)
        
        # Estoque Mínimo
        self.spin_estoque_minimo = QSpinBox()
        self.spin_estoque_minimo.setMaximum(999999)
        form_layout.addRow("Estoque Mínimo:", self.spin_estoque_minimo)
        
        # Unidade de Medida
        self.cmb_unidade = QComboBox()
        self.cmb_unidade.addItems(["UN", "KG", "L", "M", "CX", "PC", "G", "ML"])
        form_layout.addRow("Unidade:", self.cmb_unidade)
        
        layout.addLayout(form_layout)
        
        # Nota sobre campos obrigatórios
        nota = QLabel("* Campos obrigatórios")
        nota.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(nota)
        
        # Botões
        layout_botoes = QHBoxLayout()
        layout_botoes.addStretch()
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        layout_botoes.addWidget(btn_cancelar)
        
        btn_salvar = QPushButton("Salvar")
        btn_salvar.setDefault(True)
        btn_salvar.clicked.connect(self.salvar)
        btn_salvar.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 20px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout_botoes.addWidget(btn_salvar)
        
        layout.addLayout(layout_botoes)
    
    def carregar_categorias(self):
        """Carrega categorias no combobox"""
        self.cmb_categoria.clear()
        self.cmb_categoria.addItem("Sem categoria", None)
        
        try:
            categorias = Categoria.select().where(Categoria.ativo == True)
            for cat in categorias:
                self.cmb_categoria.addItem(cat.nome, cat.id)
        except Exception as e:
            print(f"Erro ao carregar categorias: {e}")
    
    def calcular_margem(self):
        """Calcula e exibe a margem de lucro"""
        custo = self.spin_preco_custo.value()
        venda = self.spin_preco_venda.value()
        
        margem = ProdutoController.calcular_margem_lucro(custo, venda)
        self.lbl_margem.setText(f"{margem}%")
        
        # Alterar cor baseado na margem
        if margem < 0:
            self.lbl_margem.setStyleSheet("color: red; font-weight: bold;")
        elif margem < 20:
            self.lbl_margem.setStyleSheet("color: orange; font-weight: bold;")
        else:
            self.lbl_margem.setStyleSheet("color: green; font-weight: bold;")
    
    def preencher_dados(self):
        """Preenche o formulário com dados do produto"""
        if not self.produto:
            return
        
        self.txt_codigo.setText(self.produto.codigo)
        self.txt_nome.setText(self.produto.nome)
        self.txt_descricao.setPlainText(self.produto.descricao or "")
        
        if self.produto.categoria:
            index = self.cmb_categoria.findData(self.produto.categoria.id)
            if index >= 0:
                self.cmb_categoria.setCurrentIndex(index)
        
        self.spin_preco_custo.setValue(float(self.produto.preco_custo))
        self.spin_preco_venda.setValue(float(self.produto.preco_venda))
        self.spin_estoque_minimo.setValue(self.produto.estoque_minimo)
        
        index = self.cmb_unidade.findText(self.produto.unidade_medida)
        if index >= 0:
            self.cmb_unidade.setCurrentIndex(index)
    
    def salvar(self):
        """Salva o produto"""
        # Validações
        if not self.txt_codigo.text().strip():
            QMessageBox.warning(self, "Atenção", "Informe o código do produto!")
            self.txt_codigo.setFocus()
            return
        
        if not self.txt_nome.text().strip():
            QMessageBox.warning(self, "Atenção", "Informe o nome do produto!")
            self.txt_nome.setFocus()
            return
        
        # Preparar dados
        dados = {
            'codigo': self.txt_codigo.text().strip(),
            'nome': self.txt_nome.text().strip(),
            'descricao': self.txt_descricao.toPlainText().strip(),
            'categoria_id': self.cmb_categoria.currentData(),
            'preco_custo': self.spin_preco_custo.value(),
            'preco_venda': self.spin_preco_venda.value(),
            'estoque_minimo': self.spin_estoque_minimo.value(),
            'unidade_medida': self.cmb_unidade.currentText()
        }
        
        if not self.produto:
            dados['estoque_atual'] = self.spin_estoque_atual.value()
        
        # Salvar
        if self.produto:
            sucesso, mensagem = ProdutoController.atualizar(self.produto.id, dados)
        else:
            sucesso, mensagem, _ = ProdutoController.criar(dados)
        
        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.accept()
        else:
            QMessageBox.warning(self, "Erro", mensagem)


class ProdutoView(QWidget):
    """View principal para gerenciamento de produtos"""
    
    def __init__(self):
        super().__init__()
        self.configurar_ui()
        self.atualizar_tabela()
    
    def configurar_ui(self):
        """Configura a interface"""
        layout = QVBoxLayout(self)
        
        # Barra de ferramentas
        toolbar = QHBoxLayout()
        
        # Busca
        toolbar.addWidget(QLabel("Buscar:"))
        self.txt_busca = QLineEdit()
        self.txt_busca.setPlaceholderText("Digite o nome ou código do produto...")
        self.txt_busca.textChanged.connect(self.buscar)
        toolbar.addWidget(self.txt_busca)
        
        toolbar.addStretch()
        
        # Botões
        btn_novo = QPushButton("➕ Novo Produto")
        btn_novo.clicked.connect(self.novo_produto)
        btn_novo.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        toolbar.addWidget(btn_novo)
        
        btn_atualizar = QPushButton("🔄 Atualizar")
        btn_atualizar.clicked.connect(self.atualizar_tabela)
        toolbar.addWidget(btn_atualizar)
        
        layout.addLayout(toolbar)
        
        # Tabela de produtos
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(9)
        self.tabela.setHorizontalHeaderLabels([
            "ID", "Código", "Nome", "Categoria", "Preço Custo",
            "Preço Venda", "Estoque", "Est. Mín.", "Status"
        ])
        
        # Configurar tabela
        self.tabela.setAlternatingRowColors(True)
        self.tabela.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabela.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabela.verticalHeader().setVisible(False)
        
        # Ajustar colunas
        header = self.tabela.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        
        # Double click para editar
        self.tabela.doubleClicked.connect(self.editar_produto)
        
        layout.addWidget(self.tabela)
        
        # Botões de ação
        layout_acoes = QHBoxLayout()
        layout_acoes.addStretch()
        
        btn_editar = QPushButton("✏️ Editar")
        btn_editar.clicked.connect(self.editar_produto)
        layout_acoes.addWidget(btn_editar)
        
        btn_excluir = QPushButton("🗑️ Excluir")
        btn_excluir.clicked.connect(self.excluir_produto)
        btn_excluir.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        layout_acoes.addWidget(btn_excluir)
        
        layout.addLayout(layout_acoes)
        
        # Rodapé com informações
        self.lbl_total = QLabel()
        self.lbl_total.setStyleSheet("font-weight: bold; padding: 5px;")
        layout.addWidget(self.lbl_total)
    
    def atualizar_tabela(self, produtos=None):
        """Atualiza a tabela de produtos"""
        if produtos is None:
            produtos = ProdutoController.listar_todos()
        
        self.tabela.setRowCount(0)
        
        for produto in produtos:
            row = self.tabela.rowCount()
            self.tabela.insertRow(row)
            
            # Dados
            self.tabela.setItem(row, 0, QTableWidgetItem(str(produto.id)))
            self.tabela.setItem(row, 1, QTableWidgetItem(produto.codigo))
            self.tabela.setItem(row, 2, QTableWidgetItem(produto.nome))
            
            categoria = produto.categoria.nome if produto.categoria else "-"
            self.tabela.setItem(row, 3, QTableWidgetItem(categoria))
            
            self.tabela.setItem(row, 4, QTableWidgetItem(f"R$ {produto.preco_custo:.2f}"))
            self.tabela.setItem(row, 5, QTableWidgetItem(f"R$ {produto.preco_venda:.2f}"))
            
            # Estoque com cor
            item_estoque = QTableWidgetItem(str(produto.estoque_atual))
            if produto.estoque_atual <= produto.estoque_minimo:
                item_estoque.setBackground(Qt.GlobalColor.red)
                item_estoque.setForeground(Qt.GlobalColor.white)
            item_estoque.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabela.setItem(row, 6, item_estoque)
            
            self.tabela.setItem(row, 7, QTableWidgetItem(str(produto.estoque_minimo)))
            
            status = "Ativo" if produto.ativo else "Inativo"
            self.tabela.setItem(row, 8, QTableWidgetItem(status))
        
        # Atualizar rodapé
        self.lbl_total.setText(f"Total de produtos: {len(produtos)}")
    
    def buscar(self):
        """Busca produtos por nome ou código"""
        texto = self.txt_busca.text().strip().lower()
        
        if not texto:
            self.atualizar_tabela()
            return
        
        produtos = ProdutoController.listar_todos()
        filtrados = [
            p for p in produtos
            if texto in p.nome.lower() or texto in p.codigo.lower()
        ]
        
        self.atualizar_tabela(filtrados)
    
    def novo_produto(self):
        """Abre diálogo para novo produto"""
        dialogo = DialogoProduto(self)
        if dialogo.exec():
            self.atualizar_tabela()
    
    def editar_produto(self):
        """Edita o produto selecionado"""
        row = self.tabela.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Atenção", "Selecione um produto para editar!")
            return
        
        produto_id = int(self.tabela.item(row, 0).text())
        produto = ProdutoController.buscar_por_id(produto_id)
        
        if produto:
            dialogo = DialogoProduto(self, produto)
            if dialogo.exec():
                self.atualizar_tabela()
    
    def excluir_produto(self):
        """Exclui o produto selecionado"""
        row = self.tabela.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Atenção", "Selecione um produto para excluir!")
            return
        
        produto_nome = self.tabela.item(row, 2).text()
        
        resposta = QMessageBox.question(
            self,
            "Confirmar Exclusão",
            f"Deseja realmente excluir o produto '{produto_nome}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if resposta == QMessageBox.StandardButton.Yes:
            produto_id = int(self.tabela.item(row, 0).text())
            sucesso, mensagem = ProdutoController.excluir(produto_id)
            
            if sucesso:
                QMessageBox.information(self, "Sucesso", mensagem)
                self.atualizar_tabela()
            else:
                QMessageBox.warning(self, "Erro", mensagem)