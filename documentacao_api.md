# Documentação da API — Raízes do Nordeste

# Rotas iniciais

### Rota inicial — Verificar funcionamento da API

**Método:** GET  
**Rota:** `/`  
**Autenticação:** não exige autenticação.

**Corpo da requisição:** não exige corpo JSON.

**Resposta de sucesso — HTTP 200:**

```json
{
  "mensagem": "Minha API está funcionando!"
}
```

### Acesso à área administrativa

**Método:** GET  
**Rota:** `/admin`  
**Autenticação:** obrigatória — ADMIN.

**Corpo da requisição:** não exige corpo JSON.

**Resposta de sucesso — HTTP 200:**

```json
{
  "mensagem": "Acesso administrativo autorizado!",
  "usuario": "Administrador",
  "perfil": "ADMIN"
}
```

**Possíveis erros:**
- `401 Unauthorized`: usuário não autenticado.
- `403 Forbidden`: usuário autenticado sem permissão administrativa.

## 1. Autenticação e usuários

### 1.1 Cadastrar usuário

**Método:** POST  
**Rota:** `/usuarios`  
**Autenticação:** pública — não exige token.

**Corpo da requisição:**
```json
{
  "nome": "Cliente Exemplo",
  "email": "cliente@exemplo.com",
  "senha": "senha123"
}
```

**Campos obrigatórios:**

| Campo | Tipo | Validação |
|---|---|---|
| `nome` | texto | Mínimo de 2 caracteres. |
| `email` | texto | Deve possuir formato de e-mail válido. |
| `senha` | texto | Mínimo de 8 caracteres. |

**Resposta de sucesso — HTTP 201:**
```json
{
  "mensagem": "Usuário cadastrado com sucesso!",
  "id": 2,
  "nome": "Cliente Exemplo",
  "email": "cliente@exemplo.com"
}
```

**Possíveis erros:**
- `409 Conflict`: e-mail já cadastrado.
- `422 Unprocessable Entity`: dados inválidos ou campos obrigatórios ausentes.

**Regras de negócio:**
- Todo usuário cadastrado por essa rota recebe automaticamente o perfil `CLIENTE`.
- A senha é armazenada por meio de hash.
- A senha não é retornada na resposta da API.

### 1.2 Realizar login

**Método:** POST  
**Rota:** `/login`  
**Autenticação:** pública — não exige token.

**Corpo da requisição:**
```json id="n2m4pa"
{
  "email": "cliente@exemplo.com",
  "senha": "senha123"
}
```

**Campos obrigatórios:**

| Campo | Tipo | Validação |
|---|---|---|
| `email` | texto | Deve possuir formato de e-mail válido. |
| `senha` | texto | Senha cadastrada pelo usuário. |

**Resposta de sucesso — HTTP 200:**
```json id="a7v3qx"
{
  "access_token": "TOKEN_JWT_GERADO",
  "token_type": "bearer"
}
```

**Possível erro:**
- `401 Unauthorized`: e-mail ou senha incorretos.

**Regras de negócio:**
- O sistema verifica se o e-mail está cadastrado.
- A senha informada é comparada com o hash armazenado.
- Quando a autenticação é válida, o sistema gera um token JWT.
- O token contém o identificador e o perfil do usuário.
- O token deve ser utilizado nas rotas protegidas da API.

### 1.3 Consultar perfil do usuário autenticado

**Método:** GET  
**Rota:** `/usuarios/me`  
**Autenticação:** obrigatória — CLIENTE ou ADMIN.

**Parâmetros:** nenhum.

**Corpo da requisição:** não exige corpo JSON.

**Exemplo de requisição:**

`GET /usuarios/me`

**Resposta de sucesso — HTTP 200:**
```json id="m5n8qr"
{
  "id": 2,
  "nome": "Cliente Exemplo",
  "email": "cliente@exemplo.com"
}
```

## 2. Unidades

### 2.1. Cadastrar unidade

- **Método:** POST
- **Rota:** `/unidades`
- **Autorização:** Obrigatória — perfil ADMIN.
- **Sucesso:** HTTP 201 Created.
- **Descrição:** Cadastra uma nova unidade no sistema.

**Corpo da requisição:**

```json
{
  "nome": "Unidade Centro",
  "tipo": "FILIAL",
  "endereco": "Rua Exemplo, 100",
  "cidade": "Recife",
  "estado": "PE"
}
```

**Resposta de sucesso (HTTP 201)**
```json
{
  "mensagem": "Unidade cadastrada com sucesso!",
  "id": 1,
  "nome": "Unidade Centro",
  "endereco": "Rua Exemplo, 100",
  "cidade": "Recife",
  "estado": "PE",
  "tipo": "FILIAL",
  "ativa": true
}
```

**Regras e validações:**
- Todos os campos são obrigatórios.
- O nome deve possuir pelo menos um caractere.
- Não é permitido cadastrar outra unidade com o mesmo nome.
- Nome duplicado retorna HTTP 409 Conflict.

### 2.2 Listar unidades

**Método:** GET  
**Rota:** `/unidades`  
**Autenticação:** pública — não exige token.

**Parâmetros:** nenhum.

**Corpo da requisição:** não exige corpo JSON.

**Exemplo de requisição:**

`GET /unidades`

**Resposta de sucesso — HTTP 200:**
```json id="t7h3ks"
{
  "unidades": [
    {
      "id": 1,
      "nome": "Unidade Centro",
      "tipo": "FILIAL",
      "cidade": "Recife",
      "estado": "PE",
      "endereco": "Rua Exemplo, 100",
      "ativa": true
    }
  ]
}
```

**Regras de negócio:**
- A consulta é pública.
- Retorna todas as unidades cadastradas, independentemente de estarem ativas ou inativas.

### 2.3 Consultar unidade específica

**Método:** GET  
**Rota:** `/unidades/{unidade_id}`  
**Autenticação:** pública — não exige token.

**Parâmetro de rota:**
- `unidade_id`: identificador da unidade que será consultada.

**Exemplo de requisição:**

`GET /unidades/1`

**Resposta de sucesso — HTTP 200:**
```json id="h4k2mn"
{
  "id": 1,
  "nome": "Unidade Centro",
  "tipo": "FILIAL",
  "cidade": "Recife",
  "estado": "PE",
  "endereco": "Rua Exemplo, 100",
  "ativa": true
}
```

**Possível erro:**
- `404 Not Found`: unidade não encontrada.

**Regras de negócio:**
- A consulta é pública.
- Retorna os dados da unidade informada, independentemente de estar ativa ou inativa.

### 2.4 Atualizar unidade

**Método:** PUT  
**Rota:** `/unidades/{unidade_id}`  
**Autenticação:** obrigatória — ADMIN.

**Parâmetro de rota:**
- `unidade_id`: identificador da unidade que será atualizada.

**Corpo da requisição:**

```json
{
  "nome": "Raízes do Nordeste - Centro",
  "tipo": "FILIAL",
  "endereco": "Rua das Flores, 100",
  "cidade": "Itabira",
  "estado": "MG"
}
```

**Resposta de sucesso — HTTP 200:**

```json
{
  "mensagem": "Unidade atualizada com sucesso!",
  "id": 1,
  "nome": "Raízes do Nordeste - Centro",
  "tipo": "FILIAL",
  "endereco": "Rua das Flores, 100",
  "cidade": "Itabira",
  "estado": "MG"
}
```

**Possíveis erros:**
- `404 Not Found`: unidade não encontrada.
- `409 Conflict`: já existe uma unidade com esse nome.

**Regras de negócio:**
- Somente administradores podem atualizar unidades.
- Os campos nome, tipo, endereço, cidade e estado são atualizados.
- O estado de ativação da unidade não é alterado por essa operação.

### 2.5 Desativar unidade

**Método:** DELETE  
**Rota:** `/unidades/{unidade_id}`  
**Autenticação:** obrigatória — ADMIN.

**Parâmetro de rota:**
- `unidade_id`: identificador da unidade que será desativada.

**Corpo da requisição:** não exige corpo JSON.

**Exemplo de requisição:**

`DELETE /unidades/1`

**Resposta de sucesso — HTTP 200:**
```json
{
  "mensagem": "Unidade desativada com sucesso!"
}
```

**Possíveis erros:**
- `404 Not Found`: unidade não encontrada.
- `400 Bad Request`: unidade já foi desativada.

**Regras de negócio:**
- Somente administradores podem desativar unidades.
- A operação realiza exclusão lógica, alterando o campo `ativa` para `false`.
- O registro permanece armazenado no banco de dados.

### 2.6 Ativar unidade

**Método:** PATCH  
**Rota:** `/unidades/{unidade_id}/ativar`  
**Autenticação:** obrigatória — ADMIN.

**Parâmetro de rota:**
- `unidade_id`: identificador da unidade que será ativada.

**Corpo da requisição:** não exige corpo JSON.

**Exemplo de requisição:**

`PATCH /unidades/1/ativar`

**Resposta de sucesso — HTTP 200:**

```json id="m7c1xp"
{
  "mensagem": "Unidade ativada com sucesso!",
  "id": 1,
  "nome": "Raízes do Nordeste - Centro",
  "ativa": true
}
```

**Possíveis erros:**
- `404 Not Found`: unidade não encontrada.
- `400 Bad Request`: a unidade já está ativa.

**Regras de negócio:**
- Somente administradores podem ativar unidades.
- A operação altera o campo `ativa` para `true`.
- Uma unidade que já esteja ativa não pode ser ativada novamente.

## 3. Produtos e promoções

### 3.1 Cadastrar produto

- **Método:** POST
- **Endpoint:** `/produtos`
- **Autorização:** ADMIN (token JWT obrigatório)
- **Código de sucesso:** 201 – Created

**Descrição:**  
Cadastra um novo produto e o associa a uma unidade existente e ativa. O cadastro armazena o nome, preço, descrição e quantidade inicial em estoque.

**Corpo da requisição:**

```json
{
  "unidade_id": 1,
  "nome": "Cuscuz nordestino",
  "preco": 12.50,
  "descricao": "Cuscuz tradicional com manteiga",
  "estoque": 20
}
```

**Regras de validação:**
- A unidade informada deve existir.
- A unidade deve estar ativa.
- Não pode existir outro produto com o mesmo nome na mesma unidade.
- O nome deve ter pelo menos 1 caractere.
- O preço deve ser maior que zero.
- O estoque deve ser um número inteiro maior ou igual a zero.
- A descrição é opcional.

**Resposta de sucesso (201):**

```json
{
  "mensagem": "Produto cadastrado com sucesso!",
  "id": 1,
  "unidade_id": 1,
  "nome": "Cuscuz nordestino",
  "preco": 12.5,
  "descricao": "Cuscuz tradicional com manteiga",
  "estoque": 20
}
```

**Possíveis erros:**
- **400 – Bad Request:** a unidade está desativada.
- **404 – Not Found:** a unidade informada não foi encontrada.
- **409 – Conflict:** já existe um produto com esse nome na unidade.
- **422 – Unprocessable Entity:** os dados enviados não atendem às regras de validação.

### 3.2 Cadastrar promoção

- **Método:** POST
- **Rota:** `/promocoes`
- **Autorização:** obrigatória — perfil ADMIN.
- **Sucesso:** HTTP 201 Created.

**Corpo da requisição:**

```json
{
  "nome": "Promoção de lançamento",
  "produto_id": 1,
  "desconto_percentual": 10,
  "data_inicio": "2026-11-18T00:00:00",
  "data_fim": "2026-11-30T23:59:59"
}
```

**Regras e validações:**
- O produto informado deve existir.
- O produto precisa estar disponível.
- O desconto deve ser maior que 0 e menor ou igual a 100.
- A data final deve ser posterior à data inicial.
- Produto inexistente retorna HTTP 404.
- Produto indisponível ou período inválido retorna HTTP 400.

**Resposta de sucesso — HTTP 201:**

```json
{
  "mensagem": "Promoção cadastrada com sucesso!",
  "id": 1,
  "nome": "Promoção de lançamento",
  "produto_id": 1,
  "desconto_percentual": 10,
  "data_inicio": "2026-11-18T00:00:00",
  "data_fim": "2026-11-30T23:59:59",
  "ativa": true
}
```

### 3.3 Listar todas as promoções (administrativo)

**Método:** GET  
**Rota:** `/admin/promocoes`  
**Autenticação:** obrigatória — ADMIN.

**Parâmetros de consulta:**

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `skip` | inteiro | Não | Quantidade de registros ignorados. Padrão: 0. |
| `limit` | inteiro | Não | Quantidade máxima de promoções retornadas. Padrão: 10; máximo: 100. |

**Exemplo de requisição:**

`GET /admin/promocoes?skip=0&limit=10`

**Resposta de sucesso — HTTP 200:**
```json id="k0x3zv"
{
  "promocoes": [
    {
      "id": 1,
      "nome": "Promoção de exemplo",
      "produto_id": 1,
      "desconto_percentual": 15.0,
      "data_inicio": "2026-11-01T00:00:00",
      "data_fim": "2026-11-30T23:59:59",
      "ativa": true
    }
  ]
}
```

**Regras de negócio:**
- Somente administradores podem acessar essa rota.
- Retorna as promoções cadastradas, sem filtrar por situação de ativação.
- Permite controlar a quantidade de registros por meio da paginação.

### 3.4 Listar todos os produtos (administrativo)

**Método:** GET  
**Rota:** `/admin/produtos`  
**Autenticação:** obrigatória — ADMIN.

**Parâmetros de consulta:**

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `skip` | inteiro | Não | Quantidade de registros ignorados. Padrão: 0. |
| `limit` | inteiro | Não | Quantidade máxima de produtos retornados. Padrão: 10; máximo: 100. |

**Exemplo de requisição:**

`GET /admin/produtos?skip=0&limit=10`

**Resposta de sucesso — HTTP 200:**
```json id="j9d2la"
{
  "produtos": [
    {
      "id": 1,
      "unidade_id": 1,
      "nome": "Produto exemplo",
      "preco": 12.75,
      "descricao": "Descrição do produto",
      "disponivel": true,
      "estoque": 20
    }
  ]
}
```

**Regras de negócio:**
- Somente administradores podem acessar essa rota.
- Retorna todos os produtos cadastrados, sem filtrar disponibilidade ou estoque.
- Permite controlar a quantidade de registros por meio da paginação.

### 3.5 Listar produtos de uma unidade

**Método:** GET  
**Rota:** `/produtos`  
**Autenticação:** pública — não exige token.

**Parâmetros de consulta:**

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `unidade_id` | inteiro | Sim | Identificador da unidade. |
| `skip` | inteiro | Não | Quantidade de registros ignorados. Padrão: 0. |
| `limit` | inteiro | Não | Quantidade máxima de produtos retornados. Padrão: 10; máximo: 100. |

**Exemplo de requisição:**

`GET /produtos?unidade_id=1&skip=0&limit=10`

**Resposta de sucesso — HTTP 200:**
```json id="x7c2ma"
{
  "produtos": [
    {
      "id": 1,
      "unidade_id": 1,
      "nome": "Produto exemplo",
      "preco": 12.75,
      "descricao": "Descrição do produto",
      "disponivel": true,
      "estoque": 20
    }
  ]
}
```

**Possíveis erros:**
- `404 Not Found`: unidade não encontrada.
- `400 Bad Request`: unidade inativa.

**Regras de negócio:**
- A consulta é pública.
- Retorna somente produtos da unidade informada.
- Exibe apenas produtos disponíveis e com estoque maior que zero.
- Permite paginação dos resultados.

### 3.6 Consultar produto específico

**Método:** GET  
**Rota:** `/produtos/{produto_id}`  
**Autenticação:** pública — não exige token.

**Parâmetro de rota:**
- `produto_id`: identificador do produto que será consultado.

**Exemplo de requisição:**

`GET /produtos/1`

**Resposta de sucesso — HTTP 200:**
```json id="j4f7ma"
{
  "id": 1,
  "unidade_id": 1,
  "nome": "Produto exemplo",
  "preco": 12.75,
  "descricao": "Descrição do produto",
  "disponivel": true
}
```

**Possíveis erros:**
- `404 Not Found`: produto não encontrado, indisponível ou sem estoque.

**Regras de negócio:**
- A consulta é pública.
- Somente produtos disponíveis e com estoque maior que zero são apresentados.

### 3.7 Atualizar produto

**Método:** PUT  
**Rota:** `/produtos/{produto_id}`  
**Autenticação:** obrigatória — ADMIN.

**Parâmetro de rota:**
- `produto_id`: identificador do produto que será atualizado.

**Corpo da requisição:**
```json id="k5p2mw"
{
  "unidade_id": 1,
  "nome": "Produto atualizado",
  "preco": 15.50,
  "descricao": "Nova descrição do produto",
  "estoque": 20
}
```

**Campos obrigatórios:**

| Campo | Tipo | Validação |
|---|---|---|
| `unidade_id` | inteiro | Identificador da unidade. |
| `nome` | texto | Mínimo de 1 caractere. |
| `preco` | número | Maior que zero. |
| `descricao` | texto ou nulo | Opcional. |
| `estoque` | inteiro | Maior ou igual a zero. |

**Resposta de sucesso — HTTP 200:**
```json id="p8x3nv"
{
  "id": 1,
  "unidade_id": 1,
  "nome": "Produto atualizado",
  "preco": 15.5,
  "descricao": "Nova descrição do produto",
  "disponivel": true
}
```

**Possíveis erros:**
- `404 Not Found`: produto ou unidade não encontrada.
- `400 Bad Request`: unidade associada está desativada.
- `409 Conflict`: já existe produto com o mesmo nome na unidade.
- `422 Unprocessable Entity`: dados inválidos ou campos obrigatórios ausentes.

**Regras de negócio:**
- Somente administradores podem atualizar produtos.
- A unidade associada precisa existir e estar ativa.
- Não pode existir outro produto com o mesmo nome na mesma unidade.
- A rota altera unidade, nome, preço e descrição.
- Estoque e disponibilidade permanecem inalterados.

**Observação sobre o estoque:** Embora o campo `estoque` seja obrigatório no corpo da requisição, seu valor não é atualizado por este endpoint. O estoque existente permanece inalterado. Para modificar a quantidade disponível, utilize a rota específica de atualização de estoque.

### 3.8 Desativar produto

**Método:** DELETE  
**Rota:** `/produtos/{produto_id}`  
**Autenticação:** obrigatória — ADMIN.

**Parâmetro de rota:**
- `produto_id`: identificador do produto que será desativado.

**Corpo da requisição:** não exige corpo JSON.

**Exemplo de requisição:**

`DELETE /produtos/1`

**Resposta de sucesso — HTTP 200:**
```json id="v3n8ka"
{
  "mensagem": "Produto desativado com sucesso!",
  "id": 1,
  "nome": "Produto exemplo",
  "disponivel": false
}
```

**Possíveis erros:**
- `404 Not Found`: produto não encontrado.
- `400 Bad Request`: produto já está indisponível.

**Regras de negócio:**
- Somente administradores podem desativar produtos.
- A operação realiza exclusão lógica, alterando o campo `disponivel` para `false`.
- O registro permanece armazenado no banco de dados.

### 3.9 Atualizar estoque do produto

**Método:** PATCH  
**Rota:** `/produtos/{produto_id}/estoque`  
**Autenticação:** obrigatória — ADMIN.

**Parâmetro de rota:**
- `produto_id`: identificador do produto cujo estoque será atualizado.

**Corpo da requisição:**

```json
{
  "estoque": 30
}
```

O campo `estoque` deve ser um número inteiro maior ou igual a zero.

**Resposta de sucesso — HTTP 200:**

```json
{
  "mensagem": "Estoque do produto atualizado com sucesso!",
  "id": 1,
  "unidade_id": 1,
  "nome": "Produto exemplo",
  "preco": 15.0,
  "descricao": "Descrição do produto",
  "disponivel": true,
  "estoque": 30
}
```

**Possíveis erros:**
- `404 Not Found`: produto não encontrado.
- `422 Unprocessable Entity`: valor de estoque inválido.

**Regras de negócio:**
- Somente administradores podem atualizar o estoque.
- O estoque é substituído pelo valor informado na requisição.
- A operação não altera a disponibilidade do produto.

### 3.10 Alterar disponibilidade do produto

**Método:** PATCH  
**Rota:** `/produtos/{produto_id}/disponibilidade`  
**Autenticação:** obrigatória — ADMIN.

**Parâmetro de rota:**
- `produto_id`: identificador do produto cuja disponibilidade será alterada.

**Corpo da requisição:** não exige corpo JSON.

**Exemplo de requisição:**

`PATCH /produtos/1/disponibilidade`

**Resposta de sucesso — HTTP 200:**

```json
{
  "mensagem": "Disponibilidade do produto alterada com sucesso!",
  "id": 1,
  "nome": "Produto exemplo",
  "disponivel": false
}
```

**Possíveis erros:**
- `404 Not Found`: produto não encontrado.
- `400 Bad Request`: não é possível reativar um produto sem estoque.

**Regras de negócio:**
- Somente administradores podem alterar a disponibilidade.
- A operação alterna o campo `disponivel` entre `true` e `false`.
- Um produto indisponível com estoque igual a zero não pode ser reativado.
- A alteração não modifica a quantidade em estoque.

## 4. Pedidos

### 4.1. Cadastrar pedido

- **Método:** POST
- **Rota:** `/pedidos`
- **Autorização:** Obrigatória — usuário autenticado com JWT.
- **Sucesso:** HTTP 201 Created.

**Corpo da requisição:**

```json
{
  "unidade_id": 1,
  "canal_pedido": "APP",
  "itens": [
    {
      "produto_id": 1,
      "quantidade": 2
    }
  ]
}
```

**Resposta de sucesso (HTTP 201)**

```json
{
  "mensagem": "Pedido cadastrado com sucesso!",
  "id": 15,
  "unidade_id": 1,
  "canal_pedido": "APP",
  "valor_total": 25.0
}
```

**Canais aceitos:** APP, TOTEM, BALCAO, PICKUP e WEB.

**Regras e validações:**
- A unidade deve existir e estar ativa.
- Deve haver pelo menos um item no pedido.
- Os produtos devem existir, estar disponíveis e pertencer à unidade informada.
- Não são permitidos produtos repetidos no mesmo pedido.
- A quantidade de cada item deve ser maior que zero.
- Deve existir estoque suficiente.
- O sistema calcula o valor total e aplica a promoção ativa de maior desconto, quando disponível.
- O estoque é atualizado após o processamento do pedido.
- Erros de integridade no banco de dados provocam rollback da operação e retornam HTTP 400 (Bad Request).

### 4.2. Atualizar status do pedido

- **Método:** PATCH
- **Rota:** `/pedidos/{pedido_id}/status`
- **Autorização:** Obrigatória — perfil ADMIN.
- **Sucesso:** HTTP 200 OK.

**Corpo da requisição:**
```json
{
  "status": "EM_PREPARO"
}
```

**Resposta de sucesso (HTTP 200)**

```json
{
  "mensagem": "Status do pedido atualizado com sucesso!",
  "id": 12,
  "unidade_id": 1,
  "canal_pedido": "APP",
  "valor_total": 45.0,
  "status": "EM_PREPARO",
  "pontos_creditados": false,
  "pontos_ganhos": 0
}
```

**Valores aceitos pelo schema:** PENDENTE, EM_PREPARO, PRONTO, ENTREGUE e CANCELADO.

- Embora CANCELADO esteja definido entre os valores aceitos pelo schema, essa situação não pode ser aplicada pela rota de atualização de status. O cancelamento deve ser realizado pela rota específica /pedidos/{pedido_id}/cancelar.

**Fluxo permitido:**

PENDENTE → EM_PREPARO → PRONTO → ENTREGUE.

**Regras de negócio:**
- Não é permitido atualizar pedidos cancelados ou entregues.
- As transições devem respeitar a sequência definida.
- Ao marcar um pedido como ENTREGUE, o sistema credita os pontos ao cliente.
- Os pontos são calculados pela parte inteira do valor total do pedido.
- O crédito ocorre apenas uma vez por pedido, controlado pelo campo `pontos_creditados`.
- O cancelamento é realizado por uma rota específica.

**Códigos de resposta:**
- HTTP 200: status atualizado.
- HTTP 400: transição inválida ou pedido cancelado/entregue.
- HTTP 404: pedido ou cliente não encontrado.

### 4.3 Cancelar pedido

**Método:** PATCH  
**Rota:** `/pedidos/{pedido_id}/cancelar`  
**Autenticação:** obrigatória — usuário autenticado, proprietário do pedido.

**Parâmetro de rota:**
- `pedido_id`: identificador do pedido que será cancelado.

**Corpo da requisição:** não exige corpo JSON.

**Regras de negócio:**
- O pedido deve pertencer ao usuário autenticado.
- Somente pedidos com status `PENDENTE` podem ser cancelados.
- Ao cancelar, as quantidades dos produtos são devolvidas ao estoque.
- O status do pedido é alterado para `CANCELADO`.

**Resposta de sucesso — HTTP 200:**
```json
{
  "mensagem": "Pedido cancelado com sucesso!",
  "id": 15,
  "unidade_id": 1,
  "canal_pedido": "APP",
  "valor_total": 25.00,
  "status": "CANCELADO"
}
```

**Possíveis erros:**
- `404 Not Found`: pedido não encontrado ou não pertence ao usuário autenticado.
- `400 Bad Request`: pedido não está com status `PENDENTE`.

### 4.4 Listar pedidos do cliente

**Método:** GET  
**Rota:** `/pedidos`  
**Autenticação:** obrigatória — CLIENTE ou ADMIN.

**Parâmetros de consulta (query parameters):**

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `skip` | inteiro | Não | Quantidade de registros ignorados. Padrão: 0. |
| `limit` | inteiro | Não | Quantidade máxima de pedidos retornados. Padrão: 10; máximo: 100. |
| `canal_pedido` | texto | Não | Filtra pedidos por APP, TOTEM, BALCAO, PICKUP ou WEB. |

**Exemplo de requisição:**

`GET /pedidos?skip=0&limit=10&canal_pedido=APP`

**Resposta de sucesso — HTTP 200:**
```json
{
  "pedidos": [
    {
      "id": 15,
      "unidade_id": 1,
      "canal_pedido": "APP",
      "valor_total": 25.00,
      "status": "PENDENTE"
    }
  ]
}
```

**Regras de negócio:**
- Retorna somente os pedidos pertencentes ao usuário autenticado.
- Permite filtrar os pedidos pelo canal de venda.
- Utiliza paginação por meio dos parâmetros `skip` e `limit`, permitindo também filtrar os pedidos pelo parâmetro opcional `canal_pedido`.
- `skip`: quantidade de registros ignorados (padrão: 0).
- `limit`: quantidade máxima de registros retornados (padrão: 10; máximo: 100).
- `canal_pedido`: filtro opcional pelos canais APP, TOTEM, BALCAO, PICKUP ou WEB.

### 4.5 Consultar pedido específico

**Método:** GET  
**Rota:** `/pedidos/{pedido_id}`  
**Autenticação:** obrigatória — CLIENTE ou ADMIN.

**Parâmetro de rota:**
- `pedido_id`: identificador do pedido que será consultado.

**Exemplo de requisição:**

`GET /pedidos/15`

**Resposta de sucesso — HTTP 200:**
```json
{
  "id": 15,
  "unidade_id": 1,
  "canal_pedido": "APP",
  "valor_total": 25.00,
  "status": "PENDENTE",
  "itens": [
    {
      "nome_produto": "Produto exemplo",
      "id": 1,
      "produto_id": 1,
      "quantidade": 2,
      "preco_unitario": 12.5
    }
  ]
}
```

**Possíveis erros:**
- `404 Not Found`: pedido não encontrado ou não pertence ao usuário autenticado.

**Regras de negócio:**
- O usuário só pode consultar pedidos vinculados à própria conta.
- A resposta apresenta os dados do pedido e os respectivos itens.

### 4.6 Listar todos os pedidos (administrativo)

**Método:** GET  
**Rota:** `/admin/pedidos`  
**Autenticação:** obrigatória — ADMIN.

**Parâmetros de consulta:**

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `skip` | inteiro | Não | Quantidade de registros ignorados. Padrão: 0. |
| `limit` | inteiro | Não | Quantidade máxima de pedidos retornados. Padrão: 10; máximo: 100. |

**Exemplo de requisição:**

`GET /admin/pedidos?skip=0&limit=10`

**Resposta de sucesso — HTTP 200:**
```json
{
  "pedidos": [
    {
      "id": 15,
      "unidade_id": 1,
      "usuario_id": 2,
      "canal_pedido": "APP",
      "valor_total": 25.00,
      "status": "PENDENTE",
      "pontos_creditados": false
    }
  ]
}
```

**Regras de negócio:**
- Somente administradores podem acessar essa rota.
- Retorna pedidos de todos os usuários.
- Permite controlar a quantidade de registros por meio da paginação.

## 5. Pagamentos

### 5.1. Registrar pagamento simulado

- **Método:** POST
- **Rota:** `/pagamentos`
- **Autorização:** Obrigatória — usuário autenticado com JWT.
- **Sucesso:** HTTP 201 Created.
- **Gateway:** MOCK.

**Corpo da requisição:**

```json
{
  "pedido_id": 15,
  "simular_recusa": false
}
```

**Resposta de sucesso (HTTP 201)**

```json
{
  "id": 9,
  "pedido_id": 15,
  "valor": 25.0,
  "status": "APROVADO",
  "gateway": "MOCK"
}
```

O campo `simular_recusa` é opcional e assume `false` quando não informado.

**Regras de funcionamento:**
- O pedido deve pertencer ao usuário autenticado.
- O pedido deve existir e estar com status PENDENTE.
- Não pode existir outro pagamento aprovado para o mesmo pedido.
- Com `simular_recusa: false`, o pagamento é APROVADO.
- Com `simular_recusa: true`, o pagamento é RECUSADO.
- A requisição enviada ao gateway simulado e a resposta recebida são armazenadas no banco de dados em formato JSON.
- O registro também armazena o status do pagamento, o valor e o gateway utilizado (MOCK).
- Os pagamentos recusados também são registrados no banco de dados, permitindo que uma nova tentativa seja realizada.
- A existência de um pagamento recusado não impede uma nova tentativa, desde que o pedido permaneça com status PENDENTE.

**Possíveis erros:**
- 401 Unauthorized: token ausente ou inválido.
- 404 Not Found: pedido não encontrado ou não pertence ao usuário autenticado.
- 400 Bad Request: pedido não está pendente ou já possui pagamento aprovado.
- 422 Unprocessable Entity: dados enviados inválidos.



## 6. Fidelidade

### 6.1 Consultar saldo de pontos

**Método:** GET  
**Rota:** `/fidelidade/pontos`  
**Autenticação:** obrigatória — CLIENTE ou ADMIN.

**Parâmetros:** nenhum.

**Corpo da requisição:** não exige corpo JSON.

**Exemplo de requisição:**

`GET /fidelidade/pontos`

**Resposta de sucesso — HTTP 200:**
```json id="m8x2pz"
{
  "id": 2,
  "nome": "Cliente Exemplo",
  "pontos": 18
}
```

**Regras de negócio:**
- A consulta utiliza o usuário identificado pelo token JWT.
- Retorna somente o saldo de pontos da conta autenticada.

### 6.2. Resgatar pontos

- **Método:** POST
- **Rota:** `/fidelidade/resgatar/{pedido_id}`
- **Autorização:** Obrigatória — usuário autenticado com JWT.
- **Sucesso:** HTTP 200 OK.

**Corpo da requisição:**

```json
{
  "pontos_utilizados": 10,
  "consentimento": true
}
```

**Resposta de sucesso (HTTP 200)**

```json
{
  "mensagem": "Pontos resgatados com sucesso!",
  "id": 5,
  "pedido_id": 26,
  "pontos_utilizados": 10,
  "valor_desconto": 1.0,
  "valor_final_pedido": 17.5,
  "saldo_pontos": 84
}
```

**Regras e validações:**
- O pedido deve pertencer ao usuário autenticado.
- O pedido deve estar PENDENTE.
- O pedido não pode possuir pagamento aprovado.
- O consentimento deve ser informado e verdadeiro.
- A quantidade de pontos deve ser maior que zero.
- O cliente deve possuir saldo suficiente.
- Cada pedido permite apenas um resgate.
- O desconto não pode superar o valor total do pedido.
- A conversão utilizada é de 10 pontos para R$ 1,00 de desconto.

**Resposta de sucesso:**
- Retorna o identificador do resgate, pedido, pontos utilizados, valor do desconto, valor final do pedido e saldo atualizado do cliente.

**Erros:**
- HTTP 400 para violações das regras de resgate e HTTP 404 quando o pedido não é encontrado ou não pertence ao usuário.
- HTTP 401 Unauthorized: token ausente ou inválido.
- HTTP 422 Unprocessable Entity: dados inválidos, como quantidade de pontos ausente ou menor ou igual a zero.