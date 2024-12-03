from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base, relationship

engine = create_engine('sqlite:///PlatyPlus.sqlite3')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Categoria(Base):
    __tablename__ = 'categorias'
    id_categoria = Column(Integer, primary_key=True, unique=True)
    nome_categoria = Column(String(40), nullable=True, unique=True)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_categoria(self):
        dados_categoria = {
            'id_categoria': self.id_categoria,
            'nome_categoria': self.nome_categoria,
        }
        return dados_categoria

    def __repr__(self):
        return '<Categorias: {} {}>'.format(self.id_categoria,
                                            self.nome_categoria)


class Produto(Base):
    __tablename__ = 'produtos'
    produto_id = Column(Integer, primary_key=True, unique=True)
    nome_produto = Column(String(80), nullable=False, index=True)
    quantidade_produto = Column(Integer, nullable=False, index=True)
    codigo_produto = Column(String(40), nullable=False, index=True)
    id_categoria = Column(Integer, ForeignKey('categorias.id_categoria'))
    categorias = relationship(Categoria)
    preco_produto = Column(String(40), nullable=False, index=True)
    validade_produto = Column(String(10), nullable=False, index=True)

    # função para salvar no banco
    def save(self):
        db_session.add(self)
        db_session.commit()

    # função para deletar
    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_produto(self):
        dados_produto = {
            "produto_id": self.produto_id,
            "nome_produto": self.nome_produto,
            "quantidade_produto": self.quantidade_produto,
            "codigo_produto": self.codigo_produto,
            "id_categoria": self.id_categoria,
            "preco_produto": self.preco_produto,
            "validade_produto": self.validade_produto
        }
        return dados_produto

    def __repr__(self):
        return '<Produto: {} {} {} {} {} {} {}>'.format(self.produto_id,
                                                        self.nome_produto,
                                                        self.quantidade_produto,
                                                        self.codigo_produto,
                                                        self.id_categoria,
                                                        self.preco_produto,
                                                        self.validade_produto)


class Funcionario(Base):
    __tablename__ = 'funcionarios'
    funcionario_id = Column(Integer, primary_key=True, unique=True)
    nome_funcionario = Column(String(80), nullable=False, index=True)
    email_funcionario = Column(String(80), nullable=False, index=True)
    senha_funcionario = Column(String(80), nullable=False, index=True)

    # função para salvar no banco
    def save(self):
        db_session.add(self)
        db_session.commit()

    # função para deletar
    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_funcionario(self):
        dados_funcionario = {
            "funcionario_id": self.funcionario_id,
            "nome_funcionario": self.nome_funcionario,
            "email_funcionario": self.email_funcionario,
            "senha_funcionario": self.senha_funcionario
        }
        return dados_funcionario

    def __repr__(self):
        return '<Funcionario: {} {} {}>'.format(self.nome_funcionario,
                                                self.email_funcionario,
                                                self.senha_funcionario)


class Movimentacao(Base):
    __tablename__ = 'movimentacoes'
    id_movimentacao = Column(Integer, primary_key=True)
    data_de_movimentacao = Column(String(10), nullable=False, index=True)
    quantidade_movimentacao = Column(Integer, nullable=False, index=True)
    tipo_movimentacao = Column(Boolean, nullable=True)
    # chave estrangeira
    produto_id = Column(Integer, ForeignKey('produtos.produto_id'))
    produtos = relationship(Produto)
    funcionario_id = Column(Integer, ForeignKey('funcionarios.funcionario_id'))
    funcionarios = relationship(Funcionario)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_movimentacao(self):
        dados_movimentacao = {
            'id_movimentacao': self.id_movimentacao,
            'data_de_movimentacao': self.data_de_movimentacao,
            'quantidade_movimentacao': self.quantidade_movimentacao,
            'tipo_movimentacao': self.tipo_movimentacao,
            'produto_id': self.produto_id,
            'funcionario_id': self.funcionario_id
        }
        return dados_movimentacao

    def __repr__(self):
        return '<Produto: {} {} {} {} {} {}>'.format(self.id_movimentacao,
                                                     self.data_de_movimentacao,
                                                     self.quantidade_movimentacao,
                                                     self.tipo_movimentacao,
                                                     self.produto_id,
                                                     self.funcionario_id)

def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
