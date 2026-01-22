"""
Controller para gerenciamento de produtos
"""
from models.database import Produto, Categoria, MovimentacaoEstoque, db
from datetime import datetime
from decimal import Decimal


class ProdutoController:
    """Controlador para operações com produtos"""
    
    @staticmethod
    def listar_todos(apenas_ativos=True):
        """Lista todos os produtos"""
        try:
            query = Produto.select()
            if apenas_ativos:
                query = query.where(Produto.ativo == True)
            return list(query.order_by(Produto.nome))
        except Exception as e:
            print(f"Erro ao listar produtos: {e}")
            return []
    
    @staticmethod
    def buscar_por_id(produto_id):
        """Busca produto por ID"""
        try:
            return Produto.get_by_id(produto_id)
        except Exception as e:
            print(f"Erro ao buscar produto: {e}")
            return None
    
    @staticmethod
    def buscar_por_codigo(codigo):
        """Busca produto por código"""
        try:
            return Produto.get(Produto.codigo == codigo)
        except Produto.DoesNotExist:
            return None
        except Exception as e:
            print(f"Erro ao buscar produto por código: {e}")
            return None
    
    @staticmethod
    def criar(dados):
        """
        Cria um novo produto
        
        Args:
            dados (dict): Dicionário com os dados do produto
                - codigo: str
                - nome: str
                - descricao: str (opcional)
                - categoria_id: int (opcional)
                - preco_custo: float
                - preco_venda: float
                - estoque_atual: int
                - estoque_minimo: int
                - unidade_medida: str
        
        Returns:
            tuple: (sucesso: bool, mensagem: str, produto: Produto)
        """
        try:
            # Validações
            if not dados.get('codigo'):
                return False, "Código é obrigatório", None
            
            if not dados.get('nome'):
                return False, "Nome é obrigatório", None
            
            # Verificar se código já existe
            if ProdutoController.buscar_por_codigo(dados['codigo']):
                return False, "Código já cadastrado", None
            
            # Validar preços
            preco_custo = Decimal(str(dados.get('preco_custo', 0)))
            preco_venda = Decimal(str(dados.get('preco_venda', 0)))
            
            if preco_custo < 0:
                return False, "Preço de custo não pode ser negativo", None
            
            if preco_venda < 0:
                return False, "Preço de venda não pode ser negativo", None
            
            # Criar produto
            with db.atomic():
                produto = Produto.create(
                    codigo=dados['codigo'],
                    nome=dados['nome'],
                    descricao=dados.get('descricao', ''),
                    categoria=dados.get('categoria_id'),
                    preco_custo=preco_custo,
                    preco_venda=preco_venda,
                    estoque_atual=dados.get('estoque_atual', 0),
                    estoque_minimo=dados.get('estoque_minimo', 0),
                    unidade_medida=dados.get('unidade_medida', 'UN'),
                    ativo=True
                )
                
                # Registrar movimentação inicial se houver estoque
                if produto.estoque_atual > 0:
                    MovimentacaoEstoque.create(
                        produto=produto,
                        tipo='entrada',
                        quantidade=produto.estoque_atual,
                        estoque_anterior=0,
                        estoque_atual=produto.estoque_atual,
                        motivo='Estoque inicial',
                        observacoes='Cadastro do produto'
                    )
                
                return True, "Produto cadastrado com sucesso!", produto
                
        except Exception as e:
            return False, f"Erro ao criar produto: {str(e)}", None
    
    @staticmethod
    def atualizar(produto_id, dados):
        """
        Atualiza um produto existente
        
        Args:
            produto_id (int): ID do produto
            dados (dict): Dicionário com os dados a atualizar
        
        Returns:
            tuple: (sucesso: bool, mensagem: str)
        """
        try:
            produto = Produto.get_by_id(produto_id)
            
            # Validações
            if 'codigo' in dados and dados['codigo'] != produto.codigo:
                if ProdutoController.buscar_por_codigo(dados['codigo']):
                    return False, "Código já cadastrado para outro produto"
            
            if 'nome' in dados and not dados['nome']:
                return False, "Nome é obrigatório"
            
            # Validar preços se informados
            if 'preco_custo' in dados:
                preco_custo = Decimal(str(dados['preco_custo']))
                if preco_custo < 0:
                    return False, "Preço de custo não pode ser negativo"
                dados['preco_custo'] = preco_custo
            
            if 'preco_venda' in dados:
                preco_venda = Decimal(str(dados['preco_venda']))
                if preco_venda < 0:
                    return False, "Preço de venda não pode ser negativo"
                dados['preco_venda'] = preco_venda
            
            # Atualizar produto
            dados['atualizado_em'] = datetime.now()
            
            query = Produto.update(**dados).where(Produto.id == produto_id)
            query.execute()
            
            return True, "Produto atualizado com sucesso!"
            
        except Produto.DoesNotExist:
            return False, "Produto não encontrado"
        except Exception as e:
            return False, f"Erro ao atualizar produto: {str(e)}"
    
    @staticmethod
    def excluir(produto_id):
        """
        Exclui (inativa) um produto
        
        Args:
            produto_id (int): ID do produto
        
        Returns:
            tuple: (sucesso: bool, mensagem: str)
        """
        try:
            produto = Produto.get_by_id(produto_id)
            produto.ativo = False
            produto.save()
            
            return True, "Produto excluído com sucesso!"
            
        except Produto.DoesNotExist:
            return False, "Produto não encontrado"
        except Exception as e:
            return False, f"Erro ao excluir produto: {str(e)}"
    
    @staticmethod
    def ajustar_estoque(produto_id, quantidade, tipo, motivo, observacoes=''):
        """
        Ajusta o estoque de um produto
        
        Args:
            produto_id (int): ID do produto
            quantidade (int): Quantidade a adicionar (positivo) ou remover (negativo)
            tipo (str): 'entrada', 'saida' ou 'ajuste'
            motivo (str): Motivo da movimentação
            observacoes (str): Observações adicionais
        
        Returns:
            tuple: (sucesso: bool, mensagem: str)
        """
        try:
            with db.atomic():
                produto = Produto.get_by_id(produto_id)
                estoque_anterior = produto.estoque_atual
                
                # Validar estoque negativo
                if estoque_anterior + quantidade < 0:
                    return False, "Estoque não pode ficar negativo"
                
                # Atualizar estoque
                produto.estoque_atual += quantidade
                produto.atualizado_em = datetime.now()
                produto.save()
                
                # Registrar movimentação
                MovimentacaoEstoque.create(
                    produto=produto,
                    tipo=tipo,
                    quantidade=abs(quantidade),
                    estoque_anterior=estoque_anterior,
                    estoque_atual=produto.estoque_atual,
                    motivo=motivo,
                    observacoes=observacoes
                )
                
                return True, "Estoque ajustado com sucesso!"
                
        except Produto.DoesNotExist:
            return False, "Produto não encontrado"
        except Exception as e:
            return False, f"Erro ao ajustar estoque: {str(e)}"
    
    @staticmethod
    def listar_abaixo_estoque_minimo():
        """Lista produtos com estoque abaixo do mínimo"""
        try:
            query = Produto.select().where(
                (Produto.estoque_atual <= Produto.estoque_minimo) &
                (Produto.ativo == True)
            )
            return list(query.order_by(Produto.nome))
        except Exception as e:
            print(f"Erro ao listar produtos abaixo do estoque mínimo: {e}")
            return []
    
    @staticmethod
    def calcular_margem_lucro(preco_custo, preco_venda):
        """Calcula a margem de lucro percentual"""
        try:
            if preco_custo <= 0:
                return 0
            margem = ((preco_venda - preco_custo) / preco_custo) * 100
            return round(margem, 2)
        except:
            return 0