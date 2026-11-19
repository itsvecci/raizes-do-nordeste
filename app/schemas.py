from pydantic import BaseModel, EmailStr, Field
from typing import Literal
from datetime import datetime

class UsuarioCadastro(BaseModel):
    model_config = {
        "str_strip_whitespace": True
    }
    nome: str = Field(min_length=2)
    email: EmailStr
    senha: str = Field(min_length=8)

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class UnidadeCadastro(BaseModel):
    model_config = {
        "str_strip_whitespace": True
    }
    nome: str = Field(min_length=1)
    tipo: str = Field(min_length=1)
    endereco: str = Field(min_length=1)
    cidade: str = Field(min_length=1)
    estado: str = Field(min_length=1)

class ProdutoCadastro(BaseModel):
    model_config = {
        "str_strip_whitespace": True,
    }
    unidade_id: int
    nome: str = Field(min_length=1)
    preco: float = Field(gt=0)
    descricao: str | None = None
    estoque: int = Field(ge=0)

class PedidoItemCadastro(BaseModel):
    produto_id: int
    quantidade: int = Field(gt=0) 

class PedidoCadastro(BaseModel):
    unidade_id: int
    canal_pedido: Literal["APP", "TOTEM", "BALCAO", "PICKUP", "WEB"]
    itens: list[PedidoItemCadastro] = Field(min_length=1)

class PedidoStatusUpdate(BaseModel):
    status: Literal["PENDENTE", "EM_PREPARO", "PRONTO", "ENTREGUE", "CANCELADO"]

class EstoqueUpdate(BaseModel):
    estoque: int = Field(ge=0)

class PagamentoCadastro(BaseModel):
    pedido_id: int
    simular_recusa: bool = False

class ResgatePontosCadastro(BaseModel):
    pontos_utilizados: int = Field(gt=0)
    consentimento: bool 

class PromocaoCadastro(BaseModel):
    model_config = {
        "str_strip_whitespace": True
    }
    nome: str = Field(min_length=1)
    produto_id: int
    desconto_percentual: float = Field(gt=0, le=100)
    data_inicio: datetime
    data_fim: datetime
