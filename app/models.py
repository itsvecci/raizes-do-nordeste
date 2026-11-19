
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric, Text, DateTime
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    perfil = Column(String, default="CLIENTE", nullable=False)
    pontos = Column(Integer, default=0, nullable=False)

class ResgatePontos(Base):
    __tablename__ = "resgates_pontos"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    pontos_utilizados = Column(Integer, nullable=False)
    valor_desconto = Column(Numeric(10, 2), nullable=False)
    consentimento = Column(Boolean, nullable=False)
    data_resgate = Column(DateTime, nullable=False)

class Unidade(Base):
    __tablename__ = "unidades"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    endereco = Column(String, nullable=False)
    cidade = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    ativa = Column(Boolean, default=True, nullable=False)

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True)
    unidade_id = Column(Integer, ForeignKey("unidades.id"), nullable=False)
    nome = Column(String, nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)
    descricao = Column(String, nullable=True)
    disponivel = Column(Boolean, default=True, nullable=False)
    estoque = Column(Integer, default=0, nullable=False)    
    
class Pedido(Base):
    __tablename__ = "pedidos"

    status = Column(String, default="PENDENTE", nullable=False)
    valor_total = Column(Numeric(10, 2), default=0, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    id = Column(Integer, primary_key=True)
    unidade_id = Column(Integer, ForeignKey("unidades.id"), nullable=False)
    canal_pedido = Column(String, nullable=False)   
    pontos_creditados = Column(Integer, default=0, nullable=False)

class PedidoItem(Base):
    __tablename__ = "pedido_itens"

    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Numeric(10, 2), nullable=False)

class Pagamento(Base):
     __tablename__ = "pagamentos"

     id = Column(Integer, primary_key=True)
     pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
     valor = Column(Numeric(10, 2), nullable=False)
     status = Column(String, nullable=False)
     gateway = Column(String, nullable=False)
     payload_requisicao = Column(Text, nullable=False)
     payload_resposta = Column(Text, nullable=False)

class Promocao(Base):
    __tablename__ = "promocoes"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    desconto_percentual = Column(Numeric(10, 2), nullable=False)
    data_inicio = Column(DateTime, nullable=False)
    data_fim = Column(DateTime, nullable=False)
    ativa = Column(Boolean, default=True, nullable=False)