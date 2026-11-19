# Raízes do Nordeste

## Descrição do Projeto

Raízes do Nordeste é uma API Backend REST desenvolvida em Python, utilizando o framework FastAPI, voltada ao gerenciamento de operações de uma plataforma de comercialização de produtos alimentícios regionais.

## Tecnologias utilizadas

- **Python:** linguagem de programação.
- **FastAPI:** framework para desenvolvimento da API.
- **SQLAlchemy:** ORM para comunicação com o banco de dados.
- **SQLite:** banco de dados relacional.
- **Pydantic:** validação dos dados.
- **JWT:** autenticação por tokens.
- **Uvicorn:** servidor ASGI para executar a aplicação.
- **Postman:** testes das requisições da API.

## Funcionalidades implementadas

1. Cadastro e autenticação de usuários.
2. Gerenciamento de unidades e produtos.
3. Criação, consulta e acompanhamento de pedidos.
4. Controle de pagamentos com simulação de aprovação e recusa.
5. Programa de fidelidade com acúmulo e resgate de pontos.
6. Controle de acesso por perfil CLIENTE e ADMIN.
7. Gerenciamento de promoções.

## Como executar o projeto

### 1. Clonar o repositório

```powershell
git clone https://github.com/itsvecci/raizes-do-nordeste.git
```

Acesse a pasta do projeto:

```powershell
cd raizes-do-nordeste
```

### 2. Criar e ativar o ambiente virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```powershell
pip install -r requirements.txt
```

Esse comando instala as bibliotecas necessárias para executar o projeto.

### 4. Configurar as variáveis de ambiente

O projeto utiliza um arquivo `.env` para armazenar configurações sensíveis, como a chave secreta usada na autenticação JWT.

Para criar o arquivo local a partir do modelo disponibilizado, execute:

```powershell
Copy-Item .env.example .env
```

Configure a variável `SECRET_KEY` no arquivo `.env`, conforme necessário para a execução da aplicação.

O arquivo `.env` não deve ser compartilhado publicamente nem enviado ao GitHub.

### 5. Executar a aplicação

Com o ambiente virtual ativado e as dependências instaladas, execute:

```powershell
python -m uvicorn app.main:app --reload
```

Após iniciar o servidor, a documentação interativa da API estará disponível em:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Testes da API

Os testes da API foram realizados utilizando o Postman, contemplando cenários de sucesso e de erro para verificar o comportamento dos endpoints, a autenticação, as permissões de acesso e as regras de negócio.

A coleção de requisições está disponível em `testes api/colecao_postman_raizes.json`.

A documentação dos testes está disponível em `documentacao_testes.md`. As evidências ilustradas estão organizadas em `testes api/teste_api.md`, com as capturas de tela armazenadas na pasta `testes api/resultados api/`.

## Autenticação e controle de acesso

1. A autenticação é realizada por meio de tokens JWT.
2. O perfil CLIENTE acessa as funcionalidades destinadas aos consumidores.
3. O perfil ADMIN possui acesso às operações administrativas, como gerenciamento de produtos e atualização de status dos pedidos.

## Banco de dados

O projeto utiliza SQLite para armazenar os dados da aplicação e SQLAlchemy para o mapeamento e a interação entre as classes Python e as tabelas do banco.

- **SQLite:** armazenamento persistente dos dados.
- **SQLAlchemy:** mapeamento das classes Python para as tabelas e operações de consulta e alteração dos registros.

## Estrutura do projeto

```text
raizes-do-nordeste/
│
├── app/
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── security.py
│
├── DER/
├── Diagramas/
├── testes api/
│   ├── colecao_postman_raizes.json
│   └── resultados api/
│   └── teste_api.md/
├── documentacao_api.md
├── documentacao_testes.md
├── promover_admin.py
├── resetar_senha.py
├── verificar_banco.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Arquitetura e organização do projeto

O projeto utiliza uma organização modular, com separação de responsabilidades entre os componentes da aplicação.
- Camada de API: concentrada principalmente no arquivo main.py, responsável pela definição dos endpoints REST, recebimento das requisições e retorno das respostas.
- Modelagem de dados: realizada em models.py, que define as entidades utilizadas para representar os dados persistidos no banco.
- Validação de dados: realizada em schemas.py, utilizando Pydantic para validar e estruturar as informações recebidas e retornadas pela API.
- Persistência: organizada em database.py, responsável pela configuração da conexão com o banco de dados e pelo gerenciamento das sessões do SQLAlchemy.
- Segurança: dividida entre security.py, responsável pelo tratamento seguro das senhas, e auth.py, responsável pela autenticação baseada em tokens JWT.

## Endpoints principais

A API disponibiliza endpoints REST para gerenciamento das principais funcionalidades da aplicação.

| Funcionalidade | Endpoint | Método HTTP |
|---|---|---|
| Autenticação de usuários | `/login` | POST |
| Consulta do usuário autenticado | `/usuarios/me` | GET |
| Consulta de unidades | `/unidades` | GET |
| Consulta de produtos | `/produtos` | GET |
| Cadastro de pedidos | `/pedidos` | POST |
| Consulta de pedidos | `/pedidos` | GET |
| Consulta de pedido por ID | `/pedidos/{pedido_id}` | GET |
| Registro de pagamentos | `/pagamentos` | POST |
| Consulta de pontos de fidelidade | `/fidelidade/pontos` | GET |
| Resgate de pontos | `/fidelidade/resgatar/{pedido_id}` | POST |

Alguns endpoints exigem autenticação JWT e permissões específicas conforme o perfil do usuário.

A documentação interativa completa dos endpoints está disponível por meio do Swagger UI, no endereço `http://127.0.0.1:8000/docs`, após iniciar a aplicação.

## Regras de negócio

A API implementa regras para controlar o fluxo de pedidos, os pagamentos, o estoque e o programa de fidelidade.

- **Pedidos:** os pedidos são associados a uma unidade e a um usuário autenticado. A API verifica a disponibilidade dos produtos e a quantidade em estoque antes de registrar a solicitação.
- **Estoque:** a quantidade disponível é reduzida após a criação de um pedido válido. O cancelamento de um pedido pendente permite restaurar os itens ao estoque.
- **Status dos pedidos:** o fluxo de atendimento contempla os estados PENDENTE, EM_PREPARO, PRONTO e ENTREGUE, com regras para atualização e cancelamento.
- **Pagamentos:** os pagamentos são simulados por um gateway MOCK, permitindo registrar operações aprovadas ou recusadas.
- **Fidelidade:** pedidos entregues geram pontos para o cliente. Os pontos podem ser utilizados para obter descontos em pedidos pendentes, seguindo a conversão de 10 pontos para R$ 1,00.
- **Promoções:** descontos promocionais podem ser aplicados aos produtos conforme as condições e os períodos de validade cadastrados.

## Segurança e validação

A API utiliza mecanismos de autenticação, autorização e validação de dados para controlar o acesso às funcionalidades.

- **Autenticação JWT:** os usuários autenticados recebem tokens de acesso com validade de 30 minutos.
- **Proteção de senhas:** as senhas são armazenadas utilizando hashes gerados com bcrypt.
- **Controle de acesso:** as operações administrativas são restritas aos usuários com perfil ADMIN.
- **Validação de dados:** o Pydantic valida os dados recebidos, verificando tipos, campos obrigatórios e restrições definidas nos esquemas.
- **Tratamento de erros:** a API utiliza respostas JSON padronizadas para erros HTTP e falhas de validação.
- **Variáveis de ambiente:** a chave secreta utilizada na autenticação JWT é configurada localmente por meio do arquivo `.env`, que não deve ser incluído no repositório público.

Esses mecanismos compõem a segurança básica do protótipo e não representam uma auditoria completa de segurança ou conformidade com a LGPD.

## Diagramas e documentação

O projeto conta com documentação técnica e diagramas que representam a estrutura, os componentes e os processos da aplicação.

- **Documentação da API:** `documentacao_api.md`, contendo informações sobre os endpoints, os dados utilizados e as regras de funcionamento.
- **Documentação dos testes:** `documentacao_testes.md`, com os cenários de testes, resultados esperados e resultados obtidos.
- **Evidências dos testes:** `testes api/teste_api.md`, com capturas de tela dos testes realizados.
- **Diagramas UML:** pasta `Diagramas/`, contendo as representações dos casos de uso, classes e fluxos da aplicação.
- **Diagrama Entidade-Relacionamento (DER):** pasta `DER/`, contendo a representação das entidades do banco de dados e seus relacionamentos.

Esses materiais complementam o código-fonte e ajudam a compreender a organização e o funcionamento da API.

## Limitações do projeto

O Raízes do Nordeste foi desenvolvido como um protótipo acadêmico para demonstrar conceitos e práticas de desenvolvimento back-end.

Atualmente, o projeto apresenta algumas limitações:

- **Pagamentos:** as operações são simuladas por meio de um gateway MOCK, sem integração com instituições financeiras ou serviços reais de pagamento.
- **Banco de dados:** utiliza SQLite, adequado ao desenvolvimento e aos testes locais, sem configuração específica para ambientes de produção de grande escala.
- **Interface:** as funcionalidades são disponibilizadas por meio de endpoints REST, sem uma interface gráfica própria para clientes ou administradores.
- **Ambiente de execução:** a aplicação foi desenvolvida e testada localmente, sem implantação em infraestrutura de produção.
- **Segurança e privacidade:** foram implementados mecanismos básicos de autenticação e controle de acesso, mas não foi realizada uma auditoria completa de segurança ou conformidade com a LGPD.

Essas limitações delimitam o escopo do protótipo e representam possibilidades de evolução futura.

## Créditos

**Desenvolvimento:** Hudson Bueno  
**Instituição:** Centro Universitário Internacional UNINTER  
**Curso:** Análise e Desenvolvimento de Sistemas  
**Projeto acadêmico:** Projeto Multidisciplinar — Trilha Back-End  
**Ano:** 2026

Projeto desenvolvido como parte das atividades acadêmicas do curso de Análise e Desenvolvimento de Sistemas, com foco na aplicação prática de conceitos de desenvolvimento back-end, APIs REST, banco de dados, autenticação e testes de software.