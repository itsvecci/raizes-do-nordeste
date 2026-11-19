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

A documentação dos testes está em `documentacao_testes.md`, e os registros dos resultados estão organizados em `testes api/resultados api/`.

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
│
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