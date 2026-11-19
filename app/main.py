import json
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.schemas import UsuarioCadastro, UsuarioLogin, UnidadeCadastro, ProdutoCadastro, PedidoCadastro, PedidoItemCadastro, PedidoStatusUpdate, EstoqueUpdate, PagamentoCadastro, ResgatePontosCadastro, PromocaoCadastro, PagamentoResposta, PedidoResposta
from app.database import engine, Base, get_db
from app import models 
from app.security import gerar_hash_senha, verificar_senha
from app.auth import criar_token, verificar_token
from decimal import Decimal
from sqlalchemy.exc import IntegrityError
from typing import Literal

bearer_scheme = HTTPBearer()

app = FastAPI(
    title="Raízes do Nordeste",
    description="API de aprendizado do projeto",
    version="1.0.0"
)

@app.exception_handler(HTTPException)
def tratar_erro_http(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "erro": {
                "codigo": exc.status_code,
                "mensagem": exc.detail
            }
        },
        headers=exc.headers
    )

@app.exception_handler(RequestValidationError)
def tratar_erro_validacao(request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "erro": {
                "codigo": 422,
                "mensagem": "Erro de validação dos dados enviados",
                "detalhes": exc.errors()
            }
        }
    )


Base.metadata.create_all(bind=engine)


def obter_usuario_token(
    credenciais=Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credenciais.credentials

    dados = verificar_token(token)

    if dados is None:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )

    usuario_id = dados.get("sub")

    if usuario_id is None:
        raise HTTPException(
            status_code=401,
            detail="Token sem identificação de usuário",
            headers={"WWW-Authenticate": "Bearer"}
        )

    try:
        usuario_id_int = int(usuario_id)

    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Identificação de usuário inválida"
        )

    usuario = db.query(models.Usuario).filter(
        models.Usuario.id == usuario_id_int
    ).first()


    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return usuario


def exigir_admin(usuario: models.Usuario = Depends(obter_usuario_token)):
    if usuario.perfil != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso permitido apenas para administradores"
        )

    return usuario

@app.get("/admin")
def area_administrativa(
    usuario: models.Usuario = Depends(exigir_admin)
):
    return {
        "mensagem": "Acesso administrativo autorizado!",
        "usuario": usuario.nome,
        "perfil": usuario.perfil
    }


@app.get("/")
def inicio():
    return {
        "mensagem": "Minha API está funcionando!"
    }


@app.get("/unidades")
def listar_unidades(db: Session = Depends(get_db)):
    unidades = db.query(models.Unidade).all()

    lista_unidades = []

    for unidade in unidades:
        lista_unidades.append({
            "id": unidade.id,
            "nome": unidade.nome,
            "tipo": unidade.tipo,
            "cidade": unidade.cidade,
            "estado": unidade.estado,
            "endereco": unidade.endereco,
            "ativa": unidade.ativa
        })

    return {
        "unidades": lista_unidades
    }


@app.get("/produtos")
def listar_produtos(
    unidade_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    unidade = db.query(models.Unidade).filter(
        models.Unidade.id == unidade_id
    ).first()

    if unidade is None:
        raise HTTPException(
            status_code=404,
            detail="Unidade não encontrada"
        )

    if not unidade.ativa:
        raise HTTPException(
            status_code=400,
            detail="Esta unidade está inativa"
        )
 
    produtos = db.query(models.Produto).filter(
        models.Produto.unidade_id == unidade_id,
        models.Produto.disponivel == True,
        models.Produto.estoque > 0
    ).offset(skip).limit(limit).all()

    lista_produtos = []

    for produto in produtos:
        lista_produtos.append({
            "id": produto.id,
            "unidade_id": produto.unidade_id,
            "nome": produto.nome,
            "preco": float(produto.preco),
            "descricao": produto.descricao,
            "disponivel": produto.disponivel,
            "estoque": produto.estoque
        })

    return {
        "produtos": lista_produtos
    }

@app.delete("/produtos/{produto_id}")
def excluir_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(exigir_admin)
):
    produto = db.query(models.Produto).filter(
        models.Produto.id == produto_id  
    ).first()

    if produto is None:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )
    
    if not produto.disponivel:
        raise HTTPException(
            status_code=400,
            detail="Produto já está indisponível"
        )

    produto.disponivel = False

    db.commit()
    db.refresh(produto)

    return {
    "mensagem": "Produto desativado com sucesso!",
    "id": produto.id,
    "nome": produto.nome,
    "disponivel": produto.disponivel
    }

@app.get("/admin/produtos")
def listar_todos_produtos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),   
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(exigir_admin)
):
    produtos = db.query(models.Produto).offset(skip).limit(limit).all()


    lista_produtos = []

    for produto in produtos:
        lista_produtos.append({
        "id": produto.id,
        "unidade_id": produto.unidade_id,
        "nome": produto.nome,
        "preco": float(produto.preco),
        "descricao": produto.descricao,
        "disponivel": produto.disponivel,
        "estoque": produto.estoque
        })
    
    return {
        "produtos": lista_produtos
   
}

@app.get("/admin/promocoes")
def listar_todas_promocoes(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(exigir_admin)
):
    promocoes = db.query(models.Promocao).offset(skip).limit(limit).all()

    lista_promocoes = []
    for promocao in promocoes:
        lista_promocoes.append({
            "id": promocao.id,
            "nome": promocao.nome,
            "produto_id": promocao.produto_id,
            "desconto_percentual": float(promocao.desconto_percentual),
            "data_inicio": promocao.data_inicio,
            "data_fim": promocao.data_fim,
            "ativa": promocao.ativa,
        })

    return{"promocoes": lista_promocoes}


@app.get("/admin/pedidos")
def listar_todos_pedidos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    canal_pedido: Literal["APP", "TOTEM", "BALCAO", "PICKUP", "WEB"] | None = Query(None),
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(exigir_admin)
):
    consulta = db.query(models.Pedido)

    if canal_pedido is not None:
        consulta = consulta.filter(
            models.Pedido.canal_pedido == canal_pedido
        )

    pedidos = consulta.offset(skip).limit(limit).all()

    lista_pedidos = []

    for pedido in pedidos:
        lista_pedidos.append({
            "id": pedido.id,
            "unidade_id": pedido.unidade_id,
            "usuario_id": pedido.usuario_id,
            "canal_pedido": pedido.canal_pedido,
            "valor_total": float(pedido.valor_total),
            "status": pedido.status,
            "pontos_creditados": pedido.pontos_creditados,
        })

    return {
        "pedidos": lista_pedidos
    }


@app.get("/pedidos")
def listar_pedidos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    canal_pedido: Literal["APP", "TOTEM", "BALCAO", "PICKUP", "WEB"] | None = None,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(obter_usuario_token)
):
    pedidos = db.query(models.Pedido).filter(
    models.Pedido.usuario_id == usuario.id
    )

    if canal_pedido:
        pedidos = pedidos.filter(
            models.Pedido.canal_pedido == canal_pedido
        )

    pedidos = pedidos.offset(skip).limit(limit).all()

    lista_pedidos = []

    for pedido in pedidos:
        lista_pedidos.append({
            "id": pedido.id,
            "unidade_id": pedido.unidade_id,
            "canal_pedido": pedido.canal_pedido,
            "valor_total": float(pedido.valor_total),
            "status": pedido.status
        })

    return {
        "pedidos": lista_pedidos
    }

@app.get("/produtos/{produto_id}")
def buscar_produto(
    produto_id: int,
    db: Session = Depends(get_db)
):
    produto = db.query(models.Produto).filter(
        models.Produto.id == produto_id,
        models.Produto.disponivel == True,
        models.Produto.estoque > 0
    ).first()

    if produto is None:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    return {
        "id": produto.id,
        "unidade_id": produto.unidade_id,
        "nome": produto.nome,
        "preco": float(produto.preco),
        "descricao": produto.descricao,
        "disponivel": produto.disponivel
    }

@app.get("/pedidos/{pedido_id}")
def buscar_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(obter_usuario_token)
):
    pedido = db.query(models.Pedido).filter(
        models.Pedido.id == pedido_id,
        models.Pedido.usuario_id == usuario.id
    ).first()

    if pedido is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    itens = db.query(models.PedidoItem).filter(
        models.PedidoItem.pedido_id == pedido.id
    ).all()

    lista_itens = []

    for item in itens:

        produto = db.query(models.Produto).filter(
            models.Produto.id == item.produto_id
        ).first()

        lista_itens.append({
            "nome_produto": produto.nome,
            "id": item.id,
            "produto_id": item.produto_id,
            "quantidade": item.quantidade,
            "preco_unitario": float(item.preco_unitario)
        })

    return {
        "id": pedido.id,
        "unidade_id": pedido.unidade_id,
        "canal_pedido": pedido.canal_pedido,
        "valor_total": float(pedido.valor_total),
        "status": pedido.status,
        "itens": lista_itens
    }

@app.get("/fidelidade/pontos")
def consultar_pontos(
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(obter_usuario_token)
):
    return{
        "id": usuario.id,
        "nome": usuario.nome,
        "pontos": usuario.pontos
    }

@app.patch("/pedidos/{pedido_id}/status")
def atualizar_status_pedido(
    pedido_id: int,
    dados: PedidoStatusUpdate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(exigir_admin)
):
    pedido = db.query(models.Pedido).filter(
        models.Pedido.id == pedido_id
    ).first()

    if pedido is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    if pedido.status == "CANCELADO":
        raise HTTPException(
            status_code=400,
            detail="Não é possível atualizar o status de um pedido cancelado"
        )

    if pedido.status == "ENTREGUE":
        raise HTTPException(
            status_code=400,
            detail="Não é possível atualizar o status de um pedido entregue"
        )

    if pedido.status == "PENDENTE" and dados.status != "EM_PREPARO":
        raise HTTPException(
            status_code=400,
            detail="A mudança de status do pedido não é permitida"
        )

    elif pedido.status == "EM_PREPARO" and dados.status != "PRONTO":
        raise HTTPException(
            status_code=400,
            detail="A mudança de status do pedido não é permitida"
        )

    elif pedido.status == "PRONTO" and dados.status != "ENTREGUE":
        raise HTTPException(
            status_code=400,
            detail="A mudança de status do pedido não é permitida"
        )

    pontos_ganhos=0

    if dados.status == "ENTREGUE" and not pedido.pontos_creditados:
        cliente = db.query(models.Usuario).filter(
            models.Usuario.id == pedido.usuario_id
        ).first()

        if cliente is None:
            raise HTTPException(
                status_code=404,
                detail="Cliente não encontrado"   
            )

        pontos_ganhos = int(pedido.valor_total)
        cliente.pontos += pontos_ganhos
        pedido.pontos_creditados = True
  
    pedido.status = dados.status
    db.commit()
    db.refresh(pedido)

    return {
        "mensagem": "Status do pedido atualizado com sucesso!",
        "id": pedido.id,
        "unidade_id": pedido.unidade_id,
        "canal_pedido": pedido.canal_pedido,
        "valor_total": float(pedido.valor_total),
        "status": pedido.status,
        "pontos_creditados": pedido.pontos_creditados,
        "pontos_ganhos": pontos_ganhos
    }

@app.patch("/pedidos/{pedido_id}/cancelar")
def cancelar_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(obter_usuario_token)
):
    pedido = db.query(models.Pedido).filter(
        models.Pedido.id == pedido_id,
        models.Pedido.usuario_id == usuario.id
    ).first()

    if pedido is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    if pedido.status != "PENDENTE":
        raise HTTPException(
            status_code=400,
            detail="Só é possível cancelar pedidos pendentes"
        )

    try:

        itens = db.query(models.PedidoItem).filter(
            models.PedidoItem.pedido_id == pedido.id
        ).all()

        for item in itens:
            produto = db.query(models.Produto).filter(
                models.Produto.id == item.produto_id
            ).first()

            if produto is None:
                raise HTTPException(
                    status_code=404,
                    detail="Produto não encontrado durante o cancelamento do pedido"
                )

            produto.estoque = produto.estoque + item.quantidade
        
        pedido.status = "CANCELADO"
        db.commit()

    except Exception:
        db.rollback()
        raise

    db.refresh(pedido)

    return {
        "mensagem": "Pedido cancelado com sucesso!",
        "id": pedido.id,
        "unidade_id": pedido.unidade_id,
        "canal_pedido": pedido.canal_pedido,
        "valor_total": float(pedido.valor_total),
        "status": pedido.status,

    }

@app.patch("/produtos/{produto_id}/estoque")
def atualizar_estoque_produto(
    produto_id: int,
    dados: EstoqueUpdate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(exigir_admin)
):
    produto = db.query(models.Produto).filter(
        models.Produto.id == produto_id
    ).first()

    if produto is None:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    produto.estoque = dados.estoque
    db.commit()
    db.refresh(produto)

    return {
        "mensagem": "Estoque do produto atualizado com sucesso!",
        "id": produto.id,
        "unidade_id": produto.unidade_id,
        "nome": produto.nome,
        "preco": float(produto.preco),
        "descricao": produto.descricao,
        "disponivel": produto.disponivel,
        "estoque": produto.estoque
    }

@app.get("/unidades/{unidade_id}")
def buscar_unidade(
    unidade_id: int,
    db: Session = Depends(get_db)
):
    unidade = db.query(models.Unidade).filter(
        models.Unidade.id == unidade_id
    ).first()

    if unidade is None:
        raise HTTPException(
            status_code=404,
            detail="Unidade não encontrada"
        )

    return {
            "id": unidade.id,
            "nome": unidade.nome,
            "tipo": unidade.tipo,
            "cidade": unidade.cidade,
            "estado": unidade.estado,
            "endereco": unidade.endereco,
            "ativa": unidade.ativa
        }


@app.get("/usuarios/me")
def meu_perfil(
    usuario: models.Usuario = Depends(obter_usuario_token)
):
    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email
    }


@app.post("/unidades", status_code=201)
def cadastrar_unidade(
    dados: UnidadeCadastro,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(exigir_admin),
):
    unidade_existente = db.query(models.Unidade).filter(
        models.Unidade.nome == dados.nome
    ).first()

    if unidade_existente:
        raise HTTPException(
            status_code=409,
            detail="Nome da unidade já cadastrado"
        )

    nova_unidade = models.Unidade(
        tipo=dados.tipo,
        nome=dados.nome,
        endereco=dados.endereco,
        cidade=dados.cidade,
        estado=dados.estado,
    )


    db.add(nova_unidade)
    db.commit()
    db.refresh(nova_unidade)

    return {
        "mensagem": "Unidade cadastrada com sucesso!",
        "id": nova_unidade.id,
        "nome": nova_unidade.nome,
        "endereco": nova_unidade.endereco,
        "cidade": nova_unidade.cidade,
        "estado": nova_unidade.estado,
        "tipo": nova_unidade.tipo,
        "ativa": nova_unidade.ativa
    }


@app.post("/usuarios", status_code=201)
def cadastrar_usuario(
    dados: UsuarioCadastro,
    db: Session = Depends(get_db)
):
    usuario_existente = db.query(models.Usuario).filter(
        models.Usuario.email == dados.email
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=409,
            detail="E-mail já cadastrado"
        )

    novo_usuario = models.Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=gerar_hash_senha(dados.senha),
        perfil="CLIENTE"
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return {
        "mensagem": "Usuário cadastrado com sucesso!",
        "id": novo_usuario.id,
        "nome": novo_usuario.nome,
        "email": novo_usuario.email
    }


@app.post("/produtos", status_code=201)
def cadastrar_produto(
    dados: ProdutoCadastro,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(exigir_admin),
):
    unidade = db.query(models.Unidade).filter(
        models.Unidade.id == dados.unidade_id
    ).first()

    if not unidade:
        raise HTTPException(
            status_code=404,
            detail="Unidade não encontrada"
        )

    if not unidade.ativa:
        raise HTTPException(
            status_code=400,
            detail="A unidade associada ao produto está desativada"
        )

    produto_existente = db.query(models.Produto).filter(
        models.Produto.nome == dados.nome,
        models.Produto.unidade_id == dados.unidade_id
    ).first()

    if produto_existente:
        raise HTTPException(
            status_code=409,
            detail="Já existe um produto com esse nome nesta unidade"
        )

    novo_produto = models.Produto(
        unidade_id=dados.unidade_id,
        nome=dados.nome,
        preco=dados.preco,
        descricao=dados.descricao,
        estoque=dados.estoque
    )

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return {
        "mensagem": "Produto cadastrado com sucesso!",
        "id": novo_produto.id,
        "unidade_id": novo_produto.unidade_id,
        "nome": novo_produto.nome,
        "preco": novo_produto.preco,
        "descricao": novo_produto.descricao,
        "estoque": novo_produto.estoque
    }

@app.post("/promocoes", status_code=201)
def cadastrar_promocao(
    dados: PromocaoCadastro,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(exigir_admin)
):
    produto = db.query(models.Produto).filter(
        models.Produto.id == dados.produto_id
    ).first()

    if produto is None:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    if not produto.disponivel:
        raise HTTPException(
            status_code=400,
            detail="Não é possível criar promoção para um produto indisponível"
        )

    if dados.data_fim <= dados.data_inicio:
        raise HTTPException(
            status_code=400,
            detail="A data final deve ser posterior à data inicial"      
        )

    promocao = models.Promocao(
        nome=dados.nome,
        produto_id=dados.produto_id,
        desconto_percentual=dados.desconto_percentual,
        data_inicio=dados.data_inicio,
        data_fim=dados.data_fim
    )

    db.add(promocao)
    db.commit()
    db.refresh(promocao)

    return {
    "id": promocao.id,
    "nome": promocao.nome,
    "produto_id": promocao.produto_id,
    "desconto_percentual": float(promocao.desconto_percentual),
    "data_inicio": promocao.data_inicio,
    "data_fim": promocao.data_fim,
    "ativa": promocao.ativa,
    "mensagem": "Promoção cadastrada com sucesso!"
    }


@app.post("/pedidos", 
        status_code=201,
        response_model=PedidoResposta,
        responses={
            400: {"description": "Dados inconsistentes ou operação não permitida"},
            401: {"description": "Autenticação ausente, inválida ou expirada"},
            404: {"description": "Unidade ou produto não encontrado"},
            409: {"description": "Estoque insuficiente"},
            422: {"description": "Erro de validação dos dados enviados"}
        }
)
def cadastrar_pedido(
    dados: PedidoCadastro,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(obter_usuario_token)
):
    unidade = db.query(models.Unidade).filter(
        models.Unidade.id == dados.unidade_id
    ).first()

    if not unidade:
        raise HTTPException(
            status_code=404,
            detail="Unidade não encontrada"
        )

    if not unidade.ativa:
        raise HTTPException(
            status_code=400,
            detail="A unidade associada ao pedido está desativada"
        )

    novo_pedido = models.Pedido(
        unidade_id=dados.unidade_id,
        usuario_id=usuario.id,
        canal_pedido=dados.canal_pedido
    )                       
    produtos = db.query(models.Produto).filter(
        models.Produto.id.in_([item.produto_id for item in dados.itens])
    ).all()

    if len(dados.itens) != len(set(item.produto_id for item in dados.itens)):
        raise HTTPException(
            status_code=400,
            detail="Produtos duplicados no pedido"
        )

    if len(dados.itens) != len(produtos):
        raise HTTPException(
            status_code=404,
            detail="Um ou mais produtos não encontrados"
        )

    if any(produto.unidade_id != dados.unidade_id for produto in produtos):
        raise HTTPException(
            status_code=400,
            detail="Um ou mais produtos não pertencem à unidade especificada"
        )

    if any(not produto.disponivel for produto in produtos):
        raise HTTPException(
            status_code=400,
            detail="Um ou mais produtos não estão disponíveis"
        )

    if any(produto.estoque < item.quantidade for produto in produtos for item in dados.itens if produto.id == item.produto_id):
        raise HTTPException(
            status_code=409,
            detail="Um ou mais produtos não possuem estoque suficiente"
        )

    try:
        db.add(novo_pedido)
        db.flush()

        agora=datetime.now()
        valor_total = Decimal("0.00")
        for item in dados.itens:
            produto = next((p for p in produtos if p.id == item.produto_id), None)           
            if produto:
                promocao = db.query(models.Promocao).filter(
                    models.Promocao.produto_id == produto.id,
                    models.Promocao.ativa == True,
                    models.Promocao.data_inicio <= agora,
                    models.Promocao.data_fim >= agora,
                ).order_by(
                    models.Promocao.desconto_percentual.desc()
                ).first()

                preco_unitario = produto.preco

                if promocao:
                    fator_desconto = promocao.desconto_percentual / Decimal("100")
                    preco_unitario = (
                        produto.preco * (Decimal("1") - fator_desconto)
                    ).quantize(Decimal("0.01"))

                valor_total += preco_unitario * item.quantidade

                novo_item = models.PedidoItem(
                    pedido_id=novo_pedido.id,
                    produto_id=produto.id,
                    quantidade=item.quantidade,
                    preco_unitario=preco_unitario,
                )
                db.add(novo_item)
                produto.estoque -= item.quantidade

        novo_pedido.valor_total = valor_total

        db.commit()
        db.refresh(novo_pedido)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Erro ao cadastrar o pedido. Verifique os dados e tente novamente."
        )

    
    return {
        "mensagem": "Pedido cadastrado com sucesso!",
        "id": novo_pedido.id,
        "unidade_id": novo_pedido.unidade_id,
        "canal_pedido": novo_pedido.canal_pedido,
        "valor_total": float(novo_pedido.valor_total),
    }

@app.post("/pagamentos",
        status_code=201,
        response_model=PagamentoResposta,
        responses={
            400: {"description": "Pagamento não permitido ou já aprovado"},
            401: {"description": "Autenticação ausente, inválida ou expirada"},
            404: {"description": "Pedido não encontrado"},
            422: {"description": "Erro de validação dos dados enviados"}   

         }
)
def cadastrar_pagamento(
    dados: PagamentoCadastro,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(obter_usuario_token)
):
    pedido = db.query(models.Pedido).filter(
        models.Pedido.id == dados.pedido_id,
        models.Pedido.usuario_id == usuario.id
    ).first()

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    if pedido.status != "PENDENTE":
        raise HTTPException(
            status_code=400,
            detail="Só é possível realizar pagamentos em pedidos pendentes"
        )

    pagamento_existente = db.query(models.Pagamento).filter(
        models.Pagamento.pedido_id == pedido.id,
        models.Pagamento.status == "APROVADO"
    ).first()

    if dados.simular_recusa:
        payload_resposta = {
            "status":"RECUSADO",
            "mensagem":"Pagamento Recusado"
        }

    else:
        payload_resposta = {
            "status": "APROVADO",
            "mensagem": "Pagamento realizado com sucesso"
        }

    if pagamento_existente:
        raise HTTPException(
            status_code=400,
            detail="Este pedido já possui um pagamento aprovado"
        )

    valor_pagamento = pedido.valor_total

    payload_requisicao = {
        "pedido_id": pedido.id,
        "valor": str(valor_pagamento)
    }

    requisicao_json = json.dumps(payload_requisicao)
    resposta_json = json.dumps(payload_resposta)

    novo_pagamento = models.Pagamento(
        pedido_id = pedido.id,
        valor = valor_pagamento,
        status = payload_resposta["status"],
        gateway = "MOCK",
        payload_requisicao = requisicao_json,
        payload_resposta = resposta_json
    )
    db.add(novo_pagamento)
    db.commit()
    db.refresh(novo_pagamento)

    return {
        "id": novo_pagamento.id,
        "pedido_id": novo_pagamento.pedido_id,
        "valor": novo_pagamento.valor,
        "status": novo_pagamento.status,
        "gateway": novo_pagamento.gateway
    }

@app.post("/fidelidade/resgatar/{pedido_id}")
def resgatar_pontos(
    pedido_id: int,
    dados: ResgatePontosCadastro,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(obter_usuario_token)
):
    pedido = db.query(models.Pedido).filter(
        models.Pedido.id == pedido_id,
        models.Pedido.usuario_id == usuario.id
    ).first()

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    if pedido.status != "PENDENTE":
        raise HTTPException(
            status_code=400,
            detail="O resgate só é permitido em pedidos pendentes"
        )

    pagamento_existente = db.query(models.Pagamento).filter(
        models.Pagamento.pedido_id == pedido.id,
        models.Pagamento.status == "APROVADO"
    ).first()

    if pagamento_existente:
        raise HTTPException(
            status_code=400,
            detail="Não é possivel resgatar pontos de um pedido já pago"
        )

    if not dados.consentimento:
        raise HTTPException(
            status_code=400,
            detail="É necessario consentimento para resgatar pontos"
        )

    if usuario.pontos < dados.pontos_utilizados:
        raise HTTPException(
            status_code=400,
            detail="Saldo de pontos insuficiente"
        )
    resgate_existente = db.query(models.ResgatePontos).filter(
        models.ResgatePontos.pedido_id == pedido.id
    ).first()

    if resgate_existente:
        raise HTTPException(
            status_code=400,
            detail="Este pedido já possui um resgate de pontos"
        )

    valor_desconto = Decimal(dados.pontos_utilizados) / Decimal("10")

    if valor_desconto > pedido.valor_total:
        raise HTTPException(
            status_code=400,
            detail="O desconto não pode ser maior que o valor do pedido"
        )

    usuario.pontos -= dados.pontos_utilizados
    pedido.valor_total -= valor_desconto

    novo_resgate = models.ResgatePontos(
        usuario_id=usuario.id,
        pedido_id=pedido.id,
        pontos_utilizados=dados.pontos_utilizados,
        valor_desconto=valor_desconto,
        consentimento=dados.consentimento,
        data_resgate=datetime.now()
    )

    try:
        db.add(novo_resgate)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Não foi possivel registrar o resgate de pontos"

        )

    db.refresh(novo_resgate)

    return {
        "mensagem": "Pontos resgatados com sucesso!",
        "id": novo_resgate.id,
        "pedido_id": novo_resgate.pedido_id,
        "pontos_utilizados": novo_resgate.pontos_utilizados,
        "valor_desconto": novo_resgate.valor_desconto,
        "valor_final_pedido": pedido.valor_total,
        "saldo_pontos": usuario.pontos
    }

@app.post("/login")
def login(
    dados: UsuarioLogin,
    db: Session = Depends(get_db)
):
    usuario = db.query(models.Usuario).filter(
        models.Usuario.email == dados.email
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha incorretos"
        )

    senha_correta = verificar_senha(
        dados.senha,
        usuario.senha_hash
    )

    if not senha_correta:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha incorretos"
        )

    token = criar_token({
        "sub": str(usuario.id),
        "perfil": usuario.perfil
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.patch("/unidades/{unidade_id}/ativar")
def ativar_unidade(
    unidade_id: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(exigir_admin)
):
    unidade = db.query(models.Unidade).filter(
        models.Unidade.id == unidade_id
    ).first()

    if unidade is None:
        raise HTTPException(
            status_code=404,
            detail="Unidade não encontrada"
        )

    if unidade.ativa is True:
        raise HTTPException(
            status_code=400,
            detail="A unidade já está ativa"
        )

    unidade.ativa = True
    db.commit()

    return {
        "mensagem": "Unidade ativada com sucesso!",
        "id": unidade.id,
        "nome": unidade.nome,
        "ativa": unidade.ativa
    }


@app.patch("/produtos/{produto_id}/disponibilidade")
def alterar_disponibilidade_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(exigir_admin)
):
    produto = db.query(models.Produto).filter(
        models.Produto.id == produto_id
    ).first()

    if produto is None:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    if not produto.disponivel and produto.estoque == 0:
        raise HTTPException(
            status_code=400,
            detail="Não é possível reativar um produto sem estoque"
        )

    produto.disponivel = not produto.disponivel
    db.commit()
    db.refresh(produto)

    return {
        "mensagem": "Disponibilidade do produto alterada com sucesso!",
        "id": produto.id,
        "nome": produto.nome,
        "disponivel": produto.disponivel
    }


@app.put("/unidades/{unidade_id}")
def atualizar_unidade(
    unidade_id: int,
    dados: UnidadeCadastro,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(exigir_admin)
):
    unidade = db.query(models.Unidade).filter(
        models.Unidade.id == unidade_id
    ).first()

    if unidade is None:
        raise HTTPException(
            status_code=404,
            detail="Unidade não encontrada"
        )

    unidade_existente = db.query(models.Unidade).filter(
        models.Unidade.nome == dados.nome,
        models.Unidade.id != unidade_id
    ).first()

    if unidade_existente:
        raise HTTPException(
            status_code=409,
            detail="O nome já pertence a outra unidade"
        )

    unidade.nome = dados.nome
    unidade.tipo = dados.tipo
    unidade.endereco = dados.endereco
    unidade.cidade = dados.cidade
    unidade.estado = dados.estado
    db.commit()
    db.refresh(unidade)


    return {
            "id": unidade.id,
            "nome": unidade.nome,
            "tipo": unidade.tipo,
            "cidade": unidade.cidade,
            "estado": unidade.estado,
            "endereco": unidade.endereco,
            "ativa": unidade.ativa
        }


@app.put("/produtos/{produto_id}")
def atualizar_produto(
    produto_id: int,
    dados: ProdutoCadastro,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(exigir_admin)
):
    produto = db.query(models.Produto).filter(
        models.Produto.id == produto_id
    ).first()

    if produto is None:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )


    unidade = db.query(models.Unidade).filter(
        models.Unidade.id == dados.unidade_id
    ).first()

    if unidade is None:
        raise HTTPException(
            status_code=404,
            detail="Unidade não encontrada"
        )

    if not unidade.ativa:
        raise HTTPException(
            status_code=400,
            detail="A unidade associada ao produto está desativada"
        )

    produto_existente = db.query(models.Produto).filter(
        models.Produto.nome == dados.nome,
        models.Produto.id != produto_id,
        models.Produto.unidade_id == dados.unidade_id
    ).first()

    if produto_existente:
        raise HTTPException(
            status_code=409,
            detail="Já existe um produto com esse nome nesta unidade"
        )

    produto.unidade_id = dados.unidade_id
    produto.nome = dados.nome
    produto.preco = dados.preco
    produto.descricao = dados.descricao
    db.commit()
    db.refresh(produto)

    return {
        "id": produto.id,
        "unidade_id": produto.unidade_id,
        "nome": produto.nome,
        "preco": float(produto.preco),
        "descricao": produto.descricao,
        "disponivel": produto.disponivel
    }


@app.delete("/unidades/{unidade_id}")
def desativar_unidade(
    unidade_id: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(exigir_admin)
):
    unidade = db.query(models.Unidade).filter(
        models.Unidade.id == unidade_id
    ).first()

    if unidade is None:
        raise HTTPException(
            status_code=404,
            detail="Unidade não encontrada"
        )

    if unidade.ativa is False:
        raise HTTPException(
            status_code=400,
            detail="A unidade já foi desativada"
        )

    unidade.ativa = False
    db.commit()

    return {
        "mensagem": "Unidade desativada com sucesso!"
    }
