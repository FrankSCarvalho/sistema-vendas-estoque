# Sistema de Vendas e Estoque

Sistema profissional para controle de vendas e estoque desenvolvido com PySide6, SQLite e Peewee ORM.

## Funcionalidades

- ✅ Gestão de Produtos
- ✅ Controle de Estoque
- ✅ Cadastro de Clientes
- ✅ Registro de Vendas
- ✅ Relatórios Gerenciais
- ✅ Histórico de Movimentações

## Tecnologias Utilizadas

- **Python 3.x**
- **PySide6** - Interface gráfica
- **Peewee** - ORM para banco de dados
- **SQLite** - Banco de dados

## Estrutura do Projeto

```
sistema-vendas-estoque/
├── src/
│   ├── models/          # Modelos do banco de dados
│   ├── views/           # Interfaces gráficas
│   ├── controllers/     # Lógica de negócio
│   ├── utils/           # Utilitários
│   └── main.py          # Aplicação principal
├── tests/               # Testes automatizados
├── docs/                # Documentação
├── venv/                # Ambiente virtual
├── requirements.txt     # Dependências
└── README.md
```

## Instalação

### 1. Clonar o repositório

```bash
git clone [url-do-repositorio]
cd sistema-vendas-estoque
```

### 2. Criar ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Executar o sistema

```bash
python src/main.py
```

## Uso

### Criar tabelas do banco de dados

```bash
python src/models/database.py
```

### Executar testes

```bash
pytest tests/
```

## Desenvolvimento

Este projeto segue as melhores práticas de desenvolvimento:

- Arquitetura MVC (Model-View-Controller)
- Ambiente virtual isolado
- Controle de versão com Git
- Código modular e reutilizável
- Documentação completa

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT.

## Autor

Desenvolvido como projeto acadêmico de Análise e Desenvolvimento de Aplicativos.

## Roadmap

- [ ] Implementar CRUD completo de produtos
- [ ] Implementar sistema de vendas
- [ ] Adicionar gráficos e dashboards
- [ ] Implementar backup automático
- [ ] Adicionar exportação de relatórios em PDF
- [ ] Implementar sistema de permissões de usuário