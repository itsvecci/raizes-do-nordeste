# Documentação de Testes — Raízes do Nordeste

## 1. Objetivo

Este documento apresenta os testes realizados na API do sistema Raízes do Nordeste, desenvolvido com Python, FastAPI, SQLAlchemy e SQLite.

O objetivo é verificar o funcionamento dos principais recursos da aplicação, incluindo autenticação, gerenciamento de unidades e produtos, pedidos, pagamentos e fidelidade.

## 2. Ambiente de testes

- **Linguagem:** Python
- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Banco de dados:** SQLite
- **Ferramenta de testes:** Swagger UI
- **Endereço local:** http://127.0.0.1:8000/docs

## 3. Critérios de avaliação

Os testes são classificados em:

- **Positivos:** verificam se as operações válidas são executadas corretamente.
- **Negativos:** verificam se a API identifica e bloqueia operações inválidas, retornando os códigos HTTP apropriados.

## 4. Testes positivos

### 4.1. Teste positivo 01 — Atualização de unidade

- Funcionalidade: Atualização de unidade.
- Método HTTP: PUT.
- Endpoint:** `/unidades/{unidade_id}`.
- Objetivo: Verificar se o administrador consegue atualizar corretamente os dados de uma unidade existente.
- Autorização: ADMIN.
- Resultado esperado:** Atualização realizada com sucesso.
- **Resultado obtido:** Atualização realizada com sucesso.
- **Código HTTP:** 200.
- **Situação:** APROVADO.

### 4.2. Teste positivo 02 — Cadastro de produto

- **Funcionalidade:** Cadastro de produto.
- **Método HTTP:** POST.
- **Endpoint:** `/produtos`.
- **Objetivo:** Verificar se o administrador consegue cadastrar um produto com dados válidos.
- **Autorização:** ADMIN.
- **Resultado esperado:** Produto cadastrado com sucesso.
- **Resultado obtido:** Produto cadastrado com sucesso.
- **Código HTTP:** 201.
- **Situação:** APROVADO.

### 4.3. Teste positivo 03 — Cadastro de pedido com promoção

- **Funcionalidade:** Cadastro de pedido com aplicação de promoção.
- **Método HTTP:** POST.
- **Endpoint:** `/pedidos`.
- **Objetivo:** Verificar se o cliente consegue realizar um pedido válido e se o sistema aplica corretamente o desconto da promoção vigente.
- **Autorização:** CLIENTE.
- **Resultado esperado:** Pedido cadastrado com sucesso, com desconto promocional aplicado.
- **Resultado obtido:** Pedidos cadastrados com sucesso e descontos promocionais aplicados corretamente.
- **Código HTTP:** 201.
- **Situação:** APROVADO.
- Atenção: para esse endpoint, use o token da conta CLIENTE, não o ADMIN.

### 4.4. Teste positivo 04 — Pagamento aprovado

- **Funcionalidade:** Registro de pagamento aprovado.
- **Método HTTP:** POST.
- **Endpoint:** `/pagamentos`.
- **Objetivo:** Verificar se o sistema registra corretamente um pagamento simulado como aprovado.
- **Autorização:** CLIENTE.
- **Resultado esperado:** Pagamento registrado com status APROVADO.
- **Resultado obtido:** Pagamento registrado com status APROVADO.
- **Código HTTP:** 201.
- **Situação:** APROVADO.
  Autorização: CLIENTE

### 4.5. Teste positivo 05 — Entrega do pedido e crédito de pontos

- **Funcionalidade:** Atualização do status do pedido e crédito de pontos de fidelidade.
- **Método HTTP:** PATCH.
- **Endpoint:** `/pedidos/{pedido_id}/status`.
- **Objetivo:** Verificar se o administrador consegue concluir o fluxo de status do pedido e se o sistema credita os pontos ao cliente somente quando o pedido chega ao status ENTREGUE.
- **Autorização:** ADMIN.
- **Resultado esperado:** Pedido atualizado para ENTREGUE e pontos creditados ao cliente.
- **Resultado obtido:** Pedido 11 atualizado para ENTREGUE, com 15 pontos ganhos e crédito registrado.
- **Código HTTP:** 200.
- **Situação:** APROVADO.

### 4.6. Teste positivo 06 — Resgate de pontos de fidelidade

- **Funcionalidade:** Resgate de pontos de fidelidade.
- **Método HTTP:** POST.
- **Endpoint:** `/fidelidade/resgatar/{pedido_id}`.
- **Objetivo:** Verificar se o cliente consegue utilizar seus pontos para obter desconto em um pedido pendente.
- **Autorização:** CLIENTE.
- **Resultado esperado:** Pontos descontados do saldo do cliente e desconto aplicado ao valor do pedido.
- **Resultado obtido:** Pedido 15 recebeu desconto de R$ 1,00 com utilização de 10 pontos. O saldo do cliente passou para 18 pontos.
- **Código HTTP:** 200.
- **Situação:** APROVADO.
utilize o token CLIENTE ao testar essa rota.


## 5. Testes negativos

### 5.1. Teste negativo 01 — Acesso indevido à rota administrativa

- **Funcionalidade:** Controle de acesso por perfil.
- **Método HTTP:** GET.
- **Endpoint:** `/admin/promocoes`.
- **Objetivo:** Verificar se um cliente sem privilégios administrativos é impedido de acessar uma rota exclusiva para administradores.
- **Autorização:** CLIENTE.
- **Resultado esperado:** Acesso negado.
- **Resultado obtido:** A API bloqueou o acesso do cliente.
- **Código HTTP:** 403.
- **Situação:** APROVADO.

### 5.2. Teste negativo 02 — Tentativa de resgate duplicado

- **Funcionalidade:** Controle de resgates de pontos.
- **Método HTTP:** POST.
- **Endpoint:** `/fidelidade/resgatar/{pedido_id}`.
- **Objetivo:** Verificar se a API impede que um mesmo pedido receba mais de um resgate de pontos.
- **Autorização:** CLIENTE.
- **Resultado esperado:** Operação bloqueada por já existir um resgate associado ao pedido.
- **Resultado obtido:** A API impediu o segundo resgate no pedido 15.
- **Código HTTP:** 400.
- **Situação:** APROVADO.

### 5.3. Teste negativo 03 — Tentativa de resgate sem consentimento

- **Funcionalidade:** Validação do consentimento para resgate de pontos.
- **Método HTTP:** POST.
- **Endpoint:** `/fidelidade/resgatar/{pedido_id}`.
- **Objetivo:** Verificar se a API impede o resgate de pontos quando o cliente não fornece consentimento.
- **Autorização:** CLIENTE.
- **Resultado esperado:** Operação bloqueada por ausência de consentimento.
- **Resultado obtido:** A API bloqueou o resgate e retornou a mensagem de que o consentimento é necessário.
- **Código HTTP:** 400.
- **Situação:** APROVADO.

### 5.4. Teste negativo 04 — Tentativa de resgate com saldo insuficiente

- **Funcionalidade:** Validação do saldo de pontos de fidelidade.
- **Método HTTP:** POST.
- **Endpoint:** `/fidelidade/resgatar/{pedido_id}`.
- **Objetivo:** Verificar se a API impede que o cliente utilize uma quantidade de pontos superior ao saldo disponível.
- **Autorização:** CLIENTE.
- **Resultado esperado:** Operação bloqueada por saldo insuficiente.
- **Resultado obtido:** A API impediu o resgate de 100 pontos, pois o cliente possuía apenas 13 pontos.
- **Código HTTP:** 400.
- **Situação:** APROVADO.

### 5.5. Teste negativo adicional — Requisição sem autenticação

- **Funcionalidade:** Autenticação e proteção de rotas.
- **Método HTTP:** GET.
- **Endpoint:** `/admin/promocoes`.
- **Objetivo:** Verificar se a API impede o acesso de usuários que não forneceram um token de autenticação.
- **Autorização:** Nenhuma.
- **Resultado esperado:** Acesso negado por ausência de autenticação.
- **Resultado obtido:** A API bloqueou a requisição e retornou a mensagem "Not authenticated".
- **Código HTTP:** 401.
- **Situação:** APROVADO.

### 5.6. Teste negativo adicional — Consulta de produto inexistente

- **Funcionalidade:** Consulta de produtos.
- **Método HTTP:** GET.
- **Endpoint:** `/produtos/{produto_id}`.
- **Objetivo:** Verificar se a API retorna erro ao consultar um produto que não existe no banco de dados.
- **Autorização:** Pública, sem necessidade de token.
- **Resultado esperado:** Produto não encontrado.
- **Resultado obtido:** A API retornou a mensagem "Produto não encontrado".
- **Código HTTP:** 404.
- **Situação:** APROVADO.

### 5.7. Teste negativo adicional — Pagamento recusado

- **Funcionalidade:** Registro de tentativa de pagamento recusada.
- **Método HTTP:** POST.
- **Endpoint:** `/pagamentos`.
- **Objetivo:** Verificar o comportamento da API diante de uma tentativa de pagamento recusada.
- **Autorização:** CLIENTE.
- **Dados enviados:**

  ```json
  {
    "pedido_id": 14,
    "simular_recusa": true
  }
  ```

- **Resultado esperado:** Tentativa de pagamento registrada com status RECUSADO.
- **Resultado obtido:** Tentativa registrada com HTTP 201 — Created.
- **Código HTTP:** 201.
- **Status do pagamento:** RECUSADO.
- **Gateway:** MOCK.
- **Verificação adicional no banco de dados:** O pagamento recusado foi persistido com os dados da requisição e da resposta do gateway.
- **Situação do pedido após a recusa:** Permaneceu PENDENTE, com valor de R$ 13,00.
- **Conclusão:** Teste aprovado. A API registrou corretamente a recusa sem alterar indevidamente o status ou o valor do pedido.

### 5.8. Teste de segurança — Cliente tentando acessar rota administrativa

- **Funcionalidade:** Controle de acesso às rotas administrativas.
- **Método HTTP:** GET.
- **Endpoint:** `/admin/pedidos`.
- **Objetivo:** Verificar se um usuário com perfil CLIENTE é impedido de acessar uma rota administrativa.
- **Autorização:** CLIENTE.
- **Resultado obtido:** A API retornou a mensagem "Acesso permitido apenas para administradores".
- **Conclusão:** Teste aprovado. O acesso administrativo foi bloqueado para o usuário CLIENTE.

### 5.9. Teste negativo — Pedido com quantidade inválida

- **Funcionalidade:** Validação da quantidade dos itens do pedido.
- **Método HTTP:** POST.
- **Endpoint:** `/pedidos`.
- **Objetivo:** Verificar se a API rejeita pedidos com quantidade igual a zero.
- **Autorização:** CLIENTE.
- **Dados enviados:** Produto ID 5, quantidade 0.
- **Resultado obtido:** A validação retornou `greater_than`, indicando que a quantidade deve ser maior que zero.
- **Conclusão:** Teste aprovado. A API impediu o processamento de um pedido com quantidade inválida.

### 5.10. Teste negativo — Pedido com produto inexistente

- **Funcionalidade:** Validação da existência dos produtos informados no pedido.
- **Método HTTP:** POST.
- **Endpoint:** `/pedidos`.
- **Objetivo:** Verificar se a API rejeita pedidos que contenham produtos inexistentes.
- **Autorização:** CLIENTE.
- **Dados enviados:** Produto ID 99999, quantidade 1.
- **Resultado obtido:** "Um ou mais produtos não encontrados".
- **Conclusão:** Teste aprovado. A API identificou o produto inexistente e rejeitou o pedido.

### 5.8. Teste de segurança — Cliente tentando acessar rota administrativa

- **Funcionalidade:** Controle de acesso às rotas administrativas.
- **Método HTTP:** GET.
- **Endpoint:** `/admin/pedidos`.
- **Objetivo:** Verificar se um usuário com perfil CLIENTE é impedido de acessar uma rota administrativa.
- **Autorização:** CLIENTE.
- **Resultado obtido:** A API retornou a mensagem "Acesso permitido apenas para administradores".
- **Conclusão:** Teste aprovado. O acesso administrativo foi bloqueado para o usuário CLIENTE.

### 5.9. Teste negativo — Pedido com quantidade inválida

- **Funcionalidade:** Validação da quantidade dos itens do pedido.
- **Método HTTP:** POST.
- **Endpoint:** `/pedidos`.
- **Objetivo:** Verificar se a API rejeita pedidos com quantidade igual a zero.
- **Autorização:** CLIENTE.
- **Dados enviados:** Produto ID 5, quantidade 0.
- **Resultado obtido:** A validação retornou `greater_than`, indicando que a quantidade deve ser maior que zero.
- **Conclusão:** Teste aprovado. A API impediu o processamento de um pedido com quantidade inválida.

### 5.10. Teste negativo — Pedido com produto inexistente

- **Funcionalidade:** Validação da existência dos produtos informados no pedido.
- **Método HTTP:** POST.
- **Endpoint:** `/pedidos`.
- **Objetivo:** Verificar se a API rejeita pedidos que contenham produtos inexistentes.
- **Autorização:** CLIENTE.
- **Dados enviados:** Produto ID 99999, quantidade 1.
- **Resultado obtido:** "Um ou mais produtos não encontrados".
- **Conclusão:** Teste aprovado. A API identificou o produto inexistente e rejeitou o pedido.

### 5.11. Teste negativo — Pedido com estoque insuficiente

- **Funcionalidade:** Validação da disponibilidade de estoque.
- **Método HTTP:** POST.
- **Endpoint:** `/pedidos`.
- **Objetivo:** Verificar se a API impede pedidos cuja quantidade solicitada ultrapasse o estoque disponível.
- **Autorização:** CLIENTE.
- **Dados enviados:** Produto ID 5, quantidade 99999.
- **Resultado obtido:** "Um ou mais produtos não possuem estoque suficiente".
- **Conclusão:** Teste aprovado. A API impediu o pedido acima da disponibilidade de estoque.

### 5.12. Teste negativo — Pedido sem canal informado

- **Funcionalidade:** Validação dos campos obrigatórios do pedido.
- **Método HTTP:** POST.
- **Endpoint:** `/pedidos`.
- **Objetivo:** Verificar se a API rejeita pedidos sem informar o canal de realização.
- **Autorização:** CLIENTE.
- **Dados enviados:** Unidade ID 1 e produto ID 5, sem o campo `canal_pedido`.
- **Resultado obtido:** HTTP 422 — Unprocessable Entity.
- **Conclusão:** Teste aprovado. A API identificou a ausência do campo obrigatório `canal_pedido`.
-**Resultado esperado:** HTTP 422 — Unprocessable Entity, com identificação da ausência do campo obrigatório canal_pedido.
-**Verificação após a padronização:** HTTP 422, com os campos erro.codigo, erro.mensagem e erro.detalhes. O tipo de validação retornado foi missing, -indicando que o campo canal_pedido não foi informado.

### 5.13. Teste negativo — Pedido com tipo de dado inválido

- **Funcionalidade:** Validação do tipo de dado da quantidade.
- **Método HTTP:** POST.
- **Endpoint:** `/pedidos`.
- **Objetivo:** Verificar se a API rejeita valores incompatíveis com o tipo de dado esperado.
- **Autorização:** CLIENTE.
- **Dados enviados:** Produto ID 5, quantidade informada como texto (`"abc"`).
- **Resultado obtido:** HTTP 422 — Unprocessable Entity. A validação retornou `int_parsing`, indicando que o texto não pôde ser convertido em número inteiro.
- **Conclusão:** Teste aprovado. A API rejeitou corretamente o tipo de dado inválido.
-**Resultado esperado:** HTTP 422, com rejeição do valor textual informado no campo quantidade.
-**Verificação após a padronização:** HTTP 422, com os campos erro.codigo, erro.mensagem e erro.detalhes. O tipo de validação retornado foi int_parsing.

### 5.14. Teste administrativo — Consulta de todos os pedidos

- **Funcionalidade:** Consulta administrativa dos pedidos.
- **Método HTTP:** GET.
- **Endpoint:** `/admin/pedidos`.
- **Objetivo:** Verificar se um usuário com perfil ADMIN consegue acessar a listagem administrativa de pedidos.
- **Autorização:** ADMIN.
- **Resultado obtido:** Consulta realizada com sucesso, com retorno da listagem de pedidos.
- **Código HTTP:** 200.
- **Conclusão:** Teste aprovado. O administrador conseguiu acessar a rota de consulta administrativa.

### 5.15. Teste negativo — Pedido com unidade inexistente

- **Funcionalidade:** Validação da existência da unidade associada ao pedido.
- **Método HTTP:** POST.
- **Endpoint:** `/pedidos`.
- **Objetivo:** Verificar se a API rejeita pedidos associados a unidades inexistentes.
- **Autorização:** CLIENTE.
- **Dados enviados:** Unidade ID 99999, canal APP, produto ID 5 e quantidade 1.
- **Resultado esperado:** Rejeição do pedido com HTTP 404 — Not Found.
- **Resultado obtido:** A API retornou a mensagem "Unidade não encontrada".
- **Código HTTP:** 404.
- **Conclusão:** Teste aprovado. A API identificou corretamente a unidade inexistente e impediu a criação do pedido.

### 5.16. Teste de integração — Fluxo completo de pedido, pagamento e entrega (T14)

- **Funcionalidade:** Execução completa do ciclo de vida de um pedido.
- **Objetivo:** Verificar a integração entre cadastro de pedido, pagamento, atualização de status e crédito de pontos de fidelidade.

**1. Cadastro do pedido**
- Método HTTP: POST.
- Endpoint: `/pedidos`.
- Pedido criado: ID 25.
- Unidade: 1.
- Canal: APP.
- Produto: ID 5 — Cuscuz com Queijo.
- Quantidade: 1.
- Valor total: R$ 18,50.
- Resultado: Pedido cadastrado com sucesso.

**2. Realização do pagamento**
- Método HTTP: POST.
- Endpoint: `/pagamentos`.
- Pedido: 25.
- Pagamento: ID 16.
- Valor: R$ 18,50.
- Status: APROVADO.
- Gateway: MOCK.
- Código HTTP: 201 Created.

**3. Atualização para EM_PREPARO**
- Método HTTP: PATCH.
- Endpoint: `/pedidos/25/status`.
- Status atualizado: EM_PREPARO.
- Resultado: Status do pedido atualizado com sucesso.

**4. Atualização para PRONTO**
- Método HTTP: PATCH.
- Endpoint: `/pedidos/25/status`.
- Status atualizado: PRONTO.
- Resultado: Status do pedido atualizado com sucesso.

**5. Atualização para ENTREGUE**
- Método HTTP: PATCH.
- Endpoint: `/pedidos/25/status`.
- Status atualizado: ENTREGUE.
- Pontos creditados: 1.
- Pontos ganhos: 18.
- Resultado: Status do pedido atualizado com sucesso.

**Resultado final:** Fluxo completo executado com sucesso. O pedido passou pelos status EM_PREPARO, PRONTO e ENTREGUE, com pagamento aprovado e crédito de 18 pontos de fidelidade após a entrega.

### 5.17. Teste de consulta de pontos de fidelidade

- **Funcionalidade:** Consulta do saldo de pontos de fidelidade do cliente.
- **Método HTTP:** GET.
- **Endpoint:** `/fidelidade/pontos`.
- **Autenticação:** Cliente.
- **Objetivo:** Verificar se a API retorna corretamente os dados do cliente e seu saldo de pontos acumulados.

**Resultado obtido:**

- Cliente ID: 5.
- Nome: Cliente Teste Permissoes.
- Saldo de pontos: 94.

**Resultado final:** Consulta realizada com sucesso. A API retornou os dados do cliente e seu saldo atualizado de 94 pontos, após o crédito de 18 pontos referente ao pedido 25.

### 5.18. Teste de resgate de pontos de fidelidade (T19)

- **Funcionalidade:** Resgate de pontos de fidelidade para obtenção de desconto em um pedido.
- **Método HTTP:** POST.
- **Endpoint:** `/fidelidade/resgatar/26`.
- **Autenticação:** Cliente.
- **Objetivo:** Verificar se a API permite resgatar pontos em pedidos pendentes e aplica corretamente a conversão de pontos em desconto.

**Dados utilizados:**
- Pedido: 26.
- Status do pedido: PENDENTE.
- Pontos utilizados: 10.
- Saldo anterior: 94 pontos.
- Regra de conversão: 10 pontos equivalem a R$ 1,00 de desconto.

**Resultado obtido:**
- Mensagem: Pontos resgatados com sucesso!
- Valor do desconto: R$ 1,00.
- Valor original do pedido: R$ 18,50.
- Valor final do pedido: R$ 17,50.
- Saldo atualizado: 84 pontos.
- Código HTTP: 200 OK.

**Resultado final:** Teste executado com sucesso. A API permitiu o resgate de 10 pontos, aplicou R$ 1,00 de desconto ao pedido e atualizou corretamente o saldo de fidelidade do cliente.