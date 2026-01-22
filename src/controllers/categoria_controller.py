"""
Controller para gerenciamento de categorias
"""
from models.database import Categoria, db


class CategoriaController:
    """Controlador para operações com categorias"""
    
    @staticmethod
    def listar_todas(apenas_ativas=True):
        """Lista todas as categorias"""
        try:
            query = Categoria.select()
            if apenas_ativas:
                query = query.where(Categoria.ativo == True)
            return list(query.order_by(Categoria.nome))
        except Exception as e:
            print(f"Erro ao listar categorias: {e}")
            return []
    
    @staticmethod
    def buscar_por_id(categoria_id):
        """Busca categoria por ID"""
        try:
            return Categoria.get_by_id(categoria_id)
        except Exception as e:
            print(f"Erro ao buscar categoria: {e}")
            return None
    
    @staticmethod
    def buscar_por_nome(nome):
        """Busca categoria por nome"""
        try:
            return Categoria.get(Categoria.nome == nome)
        except Categoria.DoesNotExist:
            return None
        except Exception as e:
            print(f"Erro ao buscar categoria por nome: {e}")
            return None
    
    @staticmethod
    def criar(nome, descricao=''):
        """
        Cria uma nova categoria
        
        Args:
            nome (str): Nome da categoria
            descricao (str): Descrição da categoria
        
        Returns:
            tuple: (sucesso: bool, mensagem: str, categoria: Categoria)
        """
        try:
            # Validações
            if not nome or not nome.strip():
                return False, "Nome é obrigatório", None
            
            # Verificar se já existe
            if CategoriaController.buscar_por_nome(nome):
                return False, "Categoria já cadastrada", None
            
            # Criar categoria
            categoria = Categoria.create(
                nome=nome.strip(),
                descricao=descricao.strip() if descricao else '',
                ativo=True
            )
            
            return True, "Categoria criada com sucesso!", categoria
            
        except Exception as e:
            return False, f"Erro ao criar categoria: {str(e)}", None
    
    @staticmethod
    def atualizar(categoria_id, nome=None, descricao=None):
        """
        Atualiza uma categoria
        
        Args:
            categoria_id (int): ID da categoria
            nome (str): Novo nome (opcional)
            descricao (str): Nova descrição (opcional)
        
        Returns:
            tuple: (sucesso: bool, mensagem: str)
        """
        try:
            categoria = Categoria.get_by_id(categoria_id)
            
            if nome is not None:
                if not nome.strip():
                    return False, "Nome não pode ser vazio"
                
                # Verificar duplicação
                existe = CategoriaController.buscar_por_nome(nome)
                if existe and existe.id != categoria_id:
                    return False, "Já existe outra categoria com este nome"
                
                categoria.nome = nome.strip()
            
            if descricao is not None:
                categoria.descricao = descricao.strip()
            
            categoria.save()
            return True, "Categoria atualizada com sucesso!"
            
        except Categoria.DoesNotExist:
            return False, "Categoria não encontrada"
        except Exception as e:
            return False, f"Erro ao atualizar categoria: {str(e)}"
    
    @staticmethod
    def excluir(categoria_id):
        """
        Exclui (inativa) uma categoria
        
        Args:
            categoria_id (int): ID da categoria
        
        Returns:
            tuple: (sucesso: bool, mensagem: str)
        """
        try:
            categoria = Categoria.get_by_id(categoria_id)
            
            # Verificar se tem produtos associados
            if categoria.produtos.count() > 0:
                return False, "Não é possível excluir categoria com produtos associados"
            
            categoria.ativo = False
            categoria.save()
            
            return True, "Categoria excluída com sucesso!"
            
        except Categoria.DoesNotExist:
            return False, "Categoria não encontrada"
        except Exception as e:
            return False, f"Erro ao excluir categoria: {str(e)}"