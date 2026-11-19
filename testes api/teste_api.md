# Registro de Testes de API — Raízes do Nordeste

## Teste 1 — Login válido de cliente

- **Objetivo:** Verificar se um cliente consegue realizar login com credenciais válidas.
- **Endpoint:** POST /login
- **Autenticação:** Não exige token.
- **Dados utilizados:** E-mail e senha válidos de uma conta CLIENTE.
- **Resultado esperado:** HTTP 200 e retorno de um token de acesso.
- **Resultado obtido:** HTTP 200 e retorno dos campos access_token e token_type.
- **Status:** APROVADO.
- **Evidência:**

 ![Login Cliente.png](resultados%20api/Login%20Cliente.png)

## Teste 2 — Consulta aos dados do cliente

- **Objetivo:** Verificar se o cliente autenticado consegue consultar seus próprios dados.
- **Endpoint:** GET /usuarios/me
- **Autenticação:** Token CLIENTE.
- **Dados utilizados:** Token válido de uma conta CLIENTE.
- **Resultado esperado:** HTTP 200 e retorno dos dados do usuário autenticado.
- **Resultado obtido:** HTTP 200.
- **Status:** APROVADO.
- **Evidência:** 

![Consulta do cliente.png](resultados%20api/Consulta%20do%20cliente.png)

## Teste 3 — Consulta às unidades

- **Objetivo:** Verificar se qualquer usuário consegue consultar as unidades cadastradas.
- **Endpoint:** GET /unidades
- **Autenticação:** Pública, sem token.
- **Dados utilizados:** Requisição sem parâmetros obrigatórios.
- **Resultado esperado:** HTTP 200 e lista de unidades cadastradas.
- **Resultado obtido:** HTTP 200.
- **Status:** APROVADO.
- **Evidência:** 

![Consulta as unidades.png](resultados%20api/Consulta%20as%20unidades.png)

## Teste 4 — Consulta aos produtos

- **Objetivo:** Verificar se qualquer usuário consegue consultar os produtos de uma unidade.
- **Endpoint:** GET /produtos
- **Autenticação:** Pública, sem token.
- **Dados utilizados:** ID de uma unidade cadastrada.
- **Resultado esperado:** HTTP 200 e lista de produtos da unidade.
- **Resultado obtido:** HTTP 200.
- **Status:** APROVADO.
- **Evidência:** 

![Lista de produtos.png](resultados%20api/Lista%20de%20produtos.png)

## Teste 5 — Consulta aos detalhes de um produto

- **Objetivo:** Verificar se qualquer usuário consegue consultar os detalhes de um produto cadastrado.
- **Endpoint:** GET /produtos/{produto_id}
- **Autenticação:** Pública, sem token.
- **Dados utilizados:** ID de um produto cadastrado.
- **Resultado esperado:** HTTP 200 e os dados do produto selecionado.
- **Resultado obtido:** HTTP 200.
- **Status:** APROVADO.
- **Evidência:** 

![Busca de produtos.png](resultados%20api/Busca%20de%20produtos.png)

## Teste 6 — Cadastro de pedido válido

- **Objetivo:** Verificar se um cliente autenticado consegue registrar um pedido com produto disponível e estoque suficiente.
- **Endpoint:** POST /pedidos
- **Autenticação:** Token CLIENTE.
- **Dados utilizados:** Unidade 1, produto 1, quantidade 1 e canal APP.
- **Resultado esperado:** HTTP 201 e confirmação da criação do pedido.
- **Resultado obtido:** HTTP 201.
- **Status:** APROVADO.
- **Evidência:** 

![Cadastro de pedido.png](resultados%20api/Cadastro%20de%20pedido.png)

## Teste 7 — Login de cliente com senha incorreta

- **Objetivo:** Verificar se a API rejeita tentativas de login com senha inválida.
- **Endpoint:** POST /login
- **Autenticação:** Pública, sem token.
- **Dados utilizados:** E-mail válido de cliente e senha incorreta.
- **Resultado esperado:** HTTP 401, indicando credenciais inválidas.
- **Resultado obtido:** HTTP 401.
- **Status:** APROVADO.
- **Evidência:**

 ![Login cliente com senha incorreta.png](resultados%20api/Login%20cliente%20com%20senha%20incorreta.png)

## Teste 8 — Acesso sem token de autenticação

- **Objetivo:** Verificar se a API bloqueia o acesso de usuários não autenticados a uma rota protegida.
- **Endpoint:** GET /usuarios/me
- **Autenticação:** Nenhum token enviado.
- **Dados utilizados:** Requisição sem credenciais de autenticação.
- **Resultado esperado:** HTTP 401, indicando acesso não autorizado.
- **Resultado obtido:** HTTP 401.
- **Status:** APROVADO.
- **Evidência:** 

![Acesso sem token.png](resultados%20api/Acesso%20sem%20token.png)

## Teste 9 — Cliente tentando acessar rota administrativa

- **Objetivo:** Verificar se um usuário CLIENTE é impedido de acessar recursos exclusivos do ADMIN.
- **Endpoint:** GET /admin/pedidos
- **Autenticação:** Token CLIENTE.
- **Dados utilizados:** Token válido de uma conta CLIENTE.
- **Resultado esperado:** HTTP 403, indicando acesso proibido.
- **Resultado obtido:** HTTP 403.
- **Status:** APROVADO.
- **Evidência:**

 ![Acesso admin com cliente.png](resultados%20api/Acesso%20admin%20com%20cliente.png)

## Teste 10 — Cadastro de pedido com quantidade inválida

- **Objetivo:** Verificar se a API rejeita pedidos com quantidade igual a zero.
- **Endpoint:** POST /pedidos
- **Autenticação:** Token CLIENTE.
- **Dados utilizados:** Unidade 1, produto 1, quantidade 0 e canal APP.
- **Resultado esperado:** HTTP 422, indicando erro de validação.
- **Resultado obtido:** HTTP 422.
- **Status:** APROVADO.
- **Evidência:**

 ![Quantidade invalida.png](resultados%20api/Quantidade%20invalida.png)

## Teste 11 — Pedido com produto inexistente

- **Objetivo:** Verificar se a API rejeita pedidos com a id de um produto inexistente.
- **Endpoint:** POST /pedidos
- **Autenticação:** Token CLIENTE.
- **Dados utilizados:** Unidade 1, produto 99999, quantidade 1 e canal APP.
- **Resultado esperado:** HTTP 404, indicando produto não encontrado.
- **Resultado obtido:** HTTP 404.
- **Status:** APROVADO.
- **Evidência:**

 ![Pedido com produto inexistente.png](resultados%20api/Pedido%20com%20produto%20inexistente.png)

## Teste 12 — Pedido com unidade inexistente

- **Objetivo:** Verificar se a API rejeita pedidos com a id de uma unidade inexistente.
- **Endpoint:** POST /pedidos
- **Autenticação:** Token CLIENTE.
- **Dados utilizados:** Unidade 99999, produto 1, quantidade 1 e canal APP.
- **Resultado esperado:** HTTP 404, indicando unidade não encontrada.
- **Resultado obtido:** HTTP 404.
- **Status:** APROVADO.
- **Evidência:** 

![Pedido com unidade inexistente.png](resultados%20api/Pedido%20com%20unidade%20inexistente.png)

## Teste 13 — Pedido com estoque insuficiente

- **Objetivo:** Verificar se a API rejeita pedidos com estoque insuficiente.
- **Endpoint:** POST /pedidos
- **Autenticação:** Token CLIENTE.
- **Dados utilizados:** Unidade 1, produto 1, quantidade 99999 e canal APP.
- **Resultado esperado:** HTTP 409, indicando que não há estoque suficiente.
- **Resultado obtido:** HTTP 409.
- **Status:** APROVADO.
- **Evidência:**

 ![Estoque insuficiente.png](resultados%20api/Estoque%20insuficiente.png)

## T14 — Pagamento simulado aprovado e conclusão do pedido

- **Objetivo:** Verificar se um pagamento simulado pode ser aprovado e se o pedido percorre corretamente as etapas até a entrega, com o crédito dos pontos de fidelidade.
- **Endpoints utilizados:**
  - `POST /pedidos`
  - `POST /pagamentos`
  - `PATCH /pedidos/{pedido_id}/status`
- **Autenticação:**
  - Token CLIENTE para criar o pedido e realizar o pagamento.
  - Token ADMIN para atualizar o status do pedido.
- **Dados utilizados:** Pedido ID 18, unidade 1, produto 1, quantidade 1, canal APP e `simular_recusa: false`.
- **Resultado esperado:** Criação do pedido com HTTP 201, pagamento aprovado, atualização dos status para EM_PREPARO, PRONTO e ENTREGUE, com crédito dos pontos de fidelidade ao cliente.
- **Resultado obtido:**
  - Pedido criado: HTTP 201.
  - Pagamento aprovado: HTTP 201.
  - Atualização para EM_PREPARO: HTTP 200.
  - Atualização para PRONTO: HTTP 200.
  - Atualização para ENTREGUE: HTTP 200.
  - Pontos creditados: 12 pontos.
- **Status:** Aprovado.

**Evidências:**

 ![Pagamento simulado e conclusão do pedido.png](resultados%20api/Pagamento%20simulado%20e%20conclusão%20do%20pedido.png)

## T15 — Pagamento simulado recusado

- **Objetivo:** Verificar se a API consegue simular uma recusa de pagamento e registrar o resultado.
- **Endpoint:** `POST /pagamentos`
- **Autenticação:** Token CLIENTE.
- **Pré-condição:** Pedido 19 cadastrado e com status PENDENTE.
- **Dados utilizados:** `pedido_id = 19` e `simular_recusa = true`.
- **Resultado esperado:** HTTP 201 Created, com o pagamento registrado como RECUSADO.
- **Resultado obtido:** HTTP 201 Created.
- **Resposta:** Pagamento ID 11, pedido ID 19, valor R$ 12,75, status RECUSADO e gateway MOCK.
- **Status:** Aprovado.

**Evidências:**

 ![Pagamento simulado recusado.png](resultados%20api/Pagamento%20simulado%20recusado.png)

## T16 — Pedido sem campo obrigatório

- **Objetivo:** Verificar se a API rejeita pedidos sem o preenchimento de campos obrigatórios.
- **Endpoint:** `POST /pedidos`
- **Autenticação:** Token CLIENTE.
- **Dados utilizados:** Unidade 1, produto 1, quantidade 1, sem informar o campo `canal_pedido`.
- **Resultado esperado:** HTTP 422 Unprocessable Entity, indicando a ausência de um campo obrigatório.
- **Resultado obtido:** HTTP 422 Unprocessable Entity.
- **Mensagem:** Campo `canal_pedido` obrigatório não informado (`Field required`).
- **Status:** Aprovado.

**Evidências:** 

![Pedido sem campo obrigatorio.png](resultados%20api/Pedido%20sem%20campo%20obrigatorio.png)

## T17 — Pedido com tipo de dado inválido

- **Objetivo:** Verificar se a API rejeita dados com tipos incompatíveis com os campos definidos.
- **Endpoint:** `POST /pedidos`
- **Autenticação:** Token CLIENTE.
- **Dados utilizados:** Unidade 1, canal APP, produto 1 e quantidade informada como texto (`"abc"`).
- **Resultado esperado:** HTTP 422 Unprocessable Entity, indicando incompatibilidade no tipo de dado.
- **Resultado obtido:** HTTP 422 Unprocessable Entity.
- **Mensagem:** O campo `quantidade` deveria receber um número inteiro (`int_parsing`).
- **Status:** Aprovado.

**Evidências:** 

![Pedido com tipo de dado invalido.png](resultados%20api/Pedido%20com%20tipo%20de%20dado%20invalido.png)

## T18 — Consulta administrativa de pedidos

- **Objetivo:** Verificar se um usuário com perfil ADMIN consegue consultar todos os pedidos cadastrados.
- **Endpoint:** `GET /admin/pedidos`
- **Autenticação:** Token ADMIN.
- **Pré-condição:** Usuário autenticado com perfil ADMIN e existência de pedidos cadastrados.
- **Dados utilizados:** Consulta da lista de pedidos registrados no sistema.
- **Resultado esperado:** HTTP 200 OK, com a lista de pedidos cadastrados.
- **Resultado obtido:** retornando uma lista de pedidos com seus respectivos IDs, unidades, usuários, canais, valores, status e informações de fidelidade.
- **Status:** Aprovado.
- **Evidências:**

 ![Consulta administrativa de pedidos.png](resultados%20api/Consulta%20administrativa%20de%20pedidos.png)