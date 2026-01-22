"""
Modelos de banco de dados usando Peewee ORM
"""
from peewee import *
from datetime import datetime
import os

# Caminho do banco de dados
DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'database.db')

# Configuração do banco de dados
db = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    """Modelo base para todas as tabelas"""
    class Meta:
        database = db


class Categoria(BaseModel):
    """Categorias de produtos"""
    nome = CharField(max_length=100, unique=True)
    descricao = TextField(null=True)
    ativo = BooleanField(default=True)
    criado_em = DateTimeField(default=datetime.now)
    
    class Meta:
        table_name = 'categorias'


class Produto(BaseModel):
    """Produtos do estoque"""
    codigo = CharField(max_length=50, unique=True)
    nome = CharField(max_length=200)
    descricao = TextField(null=True)
    categoria = ForeignKeyField(Categoria, backref='produtos', null=True)
    preco_custo = DecimalField(max_digits=10, decimal_places=2)
    preco_venda = DecimalField(max_digits=10, decimal_places=2)
    estoque_atual = IntegerField(default=0)
    estoque_minimo = IntegerField(default=0)
    unidade_medida = CharField(max_length=20, default='UN')
    ativo = BooleanField(default=True)
    criado_em = DateTimeField(default=datetime.now)
    atualizado_em = DateTimeField(default=datetime.now)
    
    class Meta:
        table_name = 'produtos'


class Cliente(BaseModel):
    """Clientes"""
    nome = CharField(max_length=200)
    cpf_cnpj = CharField(max_length=18, unique=True, null=True)
    email = CharField(max_length=100, null=True)
    telefone = CharField(max_length=20, null=True)
    endereco = TextField(null=True)
    ativo = BooleanField(default=True)
    criado_em = DateTimeField(default=datetime.now)
    
    class Meta:
        table_name = 'clientes'


class Venda(BaseModel):
    """Vendas realizadas"""
    numero_venda = CharField(max_length=50, unique=True)
    cliente = ForeignKeyField(Cliente, backref='vendas', null=True)
    data_venda = DateTimeField(default=datetime.now)
    valor_total = DecimalField(max_digits=10, decimal_places=2, default=0)
    desconto = DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_final = DecimalField(max_digits=10, decimal_places=2, default=0)
    forma_pagamento = CharField(max_length=50)
    status = CharField(max_length=20, default='finalizada')  # finalizada, cancelada
    observacoes = TextField(null=True)
    criado_em = DateTimeField(default=datetime.now)
    
    class Meta:
        table_name = 'vendas'


class ItemVenda(BaseModel):
    """Itens de cada venda"""
    venda = ForeignKeyField(Venda, backref='itens')
    produto = ForeignKeyField(Produto, backref='vendas')
    quantidade = IntegerField()
    preco_unitario = DecimalField(max_digits=10, decimal_places=2)
    subtotal = DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        table_name = 'itens_venda'


class MovimentacaoEstoque(BaseModel):
    """Histórico de movimentações de estoque"""
    produto = ForeignKeyField(Produto, backref='movimentacoes')
    tipo = CharField(max_length=20)  # entrada, saida, ajuste
    quantidade = IntegerField()
    estoque_anterior = IntegerField()
    estoque_atual = IntegerField()
    motivo = CharField(max_length=100)
    observacoes = TextField(null=True)
    data_movimentacao = DateTimeField(default=datetime.now)
    
    class Meta:
        table_name = 'movimentacoes_estoque'


def criar_tabelas():
    """Cria todas as tabelas no banco de dados"""
    with db:
        db.create_tables([
            Categoria,
            Produto,
            Cliente,
            Venda,
            ItemVenda,
            MovimentacaoEstoque
        ])
        print("Tabelas criadas com sucesso!")


def inserir_dados_exemplo():
    """Insere dados de exemplo para testes"""
    with db.atomic():
        # Categorias
        cat_alimentos = Categoria.create(nome='Alimentos', descricao='Produtos alimentícios')
        cat_bebidas = Categoria.create(nome='Bebidas', descricao='Bebidas em geral')
        
        # Produtos
        Produto.create(
            codigo='001',
            nome='Arroz 5kg',
            categoria=cat_alimentos,
            preco_custo=15.00,
            preco_venda=22.50,
            estoque_atual=50,
            estoque_minimo=10
        )
        
        Produto.create(
            codigo='002',
            nome='Feijão 1kg',
            categoria=cat_alimentos,
            preco_custo=6.00,
            preco_venda=9.50,
            estoque_atual=30,
            estoque_minimo=5
        )
        
        # Cliente
        Cliente.create(
            nome='João Silva',
            cpf_cnpj='123.456.789-00',
            email='joao@email.com',
            telefone='(11) 98765-4321'
        )
        
        print("Dados de exemplo inseridos com sucesso!")


if __name__ == '__main__':
    criar_tabelas()
    inserir_dados_exemplo()