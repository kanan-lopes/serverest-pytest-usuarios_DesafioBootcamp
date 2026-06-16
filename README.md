# Testes Automatizados - ServeRest API

Projeto de automação de testes para a API **ServeRest**, cobrindo os endpoints de **Usuários**, **Login**, **Produtos** e **Carrinhos**, utilizando **Python**, **Requests** e **Pytest**.

A suíte também contempla testes de contrato com **JSON Schema** e execução automática via **GitHub Actions** a cada push ou pull request.

API utilizada:

```text
https://compassuol.serverest.dev
```

Endpoints cobertos:

```text
/usuarios
/login
/produtos
/carrinhos
```

---

## Tecnologias utilizadas

* Python 3.13
* Pytest
* Requests
* Python Dotenv
* Pytest HTML
* jsonschema
* GitHub Actions
* Postman

---

## Estrutura do projeto

```text
serverest-pytest-usuarios/
│
├── .github/
│   └── workflows/
│       └── tests.yml           # pipeline CI/CD — roda a suíte a cada push/PR
│
├── clients/
│   ├── usuarios_client.py      # chamadas HTTP para /usuarios
│   ├── login_client.py         # chamadas HTTP para /login
│   ├── produtos_client.py      # chamadas HTTP para /produtos
│   ├── carrinhos_client.py     # chamadas HTTP para /carrinhos
│   └── __init__.py
│
├── schemas/
│   ├── usuarios_schema.py      # JSON Schemas para /usuarios
│   ├── login_schema.py         # JSON Schemas para /login
│   ├── produtos_schema.py      # JSON Schemas para /produtos
│   ├── carrinhos_schema.py     # JSON Schemas para /carrinhos
│   └── __init__.py
│
├── tests/
│   ├── conftest.py             # fixtures compartilhadas
│   ├── test_usuarios.py        # 12 testes funcionais de /usuarios
│   ├── test_login.py           # 8 testes funcionais de /login
│   ├── test_produtos.py        # 17 testes funcionais de /produtos
│   ├── test_carrinhos.py       # 14 testes funcionais de /carrinhos
│   └── test_contratos.py       # 11 testes de contrato via JSON Schema
│
├── utils/
│   ├── data_factory.py         # geradores de payloads dinâmicos
│   └── __init__.py
│
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
├── PLANO-DE-TESTES.md
└── README.md
```

---

## Como instalar

Clone o repositório:

```bash
git clone https://github.com/kanan-lopes/serverest-pytest-usuarios_DesafioBootcamp.git
```

Acesse a pasta do projeto:

```bash
cd serverest-pytest-usuarios_DesafioBootcamp
```

Crie o ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual no Windows:

```bash
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## Como executar os testes

Executar todos os testes:

```bash
pytest
```

Executar com mais detalhes:

```bash
pytest -v
```

ou:

```bash
pytest -vv
```

Executar um arquivo específico:

```bash
pytest tests/test_usuarios.py
pytest tests/test_login.py
pytest tests/test_produtos.py
pytest tests/test_carrinhos.py
pytest tests/test_contratos.py
```

Executar por marcador:

```bash
pytest -m usuarios
pytest -m login
pytest -m produtos
pytest -m carrinhos
pytest -m contrato
```

Executar um teste específico:

```bash
pytest tests/test_contratos.py::test_schema_listar_produtos -vv
```

Executar testes filtrando pelo nome:

```bash
pytest -k "schema" -vv
pytest -k "cadastrar" -vv
pytest -k "admin" -vv
pytest -k "carrinho" -vv
```

Exibir prints durante a execução:

```bash
pytest -s
```

Gerar relatório HTML:

```bash
pytest -vv --html=reports/relatorio.html --self-contained-html
```

O relatório será gerado em:

```text
reports/relatorio.html
```

---

## Testes implementados

### `/usuarios` — 12 testes funcionais

| Cenário                       | Teste                                                        | Método | Endpoint         |
| ----------------------------- | ------------------------------------------------------------ | ------ | ---------------- |
| Listar usuários               | `test_deve_listar_usuarios_com_sucesso`                      | GET    | `/usuarios`      |
| Cadastrar usuário válido      | `test_deve_cadastrar_usuario_valido_com_sucesso`             | POST   | `/usuarios`      |
| Email duplicado               | `test_nao_deve_cadastrar_usuario_com_email_duplicado`        | POST   | `/usuarios`      |
| Campo `nome` ausente          | `test_nao_deve_cadastrar_usuario_sem_nome`                   | POST   | `/usuarios`      |
| Campo `email` ausente         | `test_nao_deve_cadastrar_usuario_sem_email`                  | POST   | `/usuarios`      |
| Campo `password` ausente      | `test_nao_deve_cadastrar_usuario_sem_password`               | POST   | `/usuarios`      |
| Campo `administrador` ausente | `test_nao_deve_cadastrar_usuario_sem_administrador`          | POST   | `/usuarios`      |
| Buscar por ID válido          | `test_deve_buscar_usuario_por_id_valido`                     | GET    | `/usuarios/{id}` |
| Buscar por ID inexistente     | `test_nao_deve_buscar_usuario_com_id_inexistente`            | GET    | `/usuarios/{id}` |
| Atualizar usuário             | `test_deve_atualizar_usuario_existente_com_sucesso`          | PUT    | `/usuarios/{id}` |
| Excluir usuário existente     | `test_deve_excluir_usuario_existente_com_sucesso`            | DELETE | `/usuarios/{id}` |
| Excluir usuário inexistente   | `test_deve_retornar_mensagem_ao_excluir_usuario_inexistente` | DELETE | `/usuarios/{id}` |

---

### `/login` — 8 testes funcionais

| Cenário                               | Teste                                             | Método | Endpoint |
| ------------------------------------- | ------------------------------------------------- | ------ | -------- |
| Login com administrador               | `test_deve_fazer_login_com_usuario_administrador` | POST   | `/login` |
| Login com usuário comum               | `test_deve_fazer_login_com_usuario_comum`         | POST   | `/login` |
| Token retornado como string não vazia | `test_token_retornado_deve_ser_string_nao_vazia`  | POST   | `/login` |
| Senha errada                          | `test_nao_deve_fazer_login_com_senha_errada`      | POST   | `/login` |
| Email inexistente                     | `test_nao_deve_fazer_login_com_email_inexistente` | POST   | `/login` |
| Campo `email` ausente                 | `test_nao_deve_fazer_login_sem_email`             | POST   | `/login` |
| Campo `password` ausente              | `test_nao_deve_fazer_login_sem_password`          | POST   | `/login` |
| Body vazio                            | `test_nao_deve_fazer_login_com_body_vazio`        | POST   | `/login` |

Os testes de login válido criam usuários dinamicamente via `/usuarios` e os removem ao final, sem depender de dados fixos da base.

---

### `/produtos` — 17 testes funcionais

| Cenário                          | Teste                                                        | Método | Endpoint         |
| -------------------------------- | ------------------------------------------------------------ | ------ | ---------------- |
| Listar produtos                  | `test_deve_listar_produtos_sem_autenticacao`                 | GET    | `/produtos`      |
| Cadastrar com token admin        | `test_deve_cadastrar_produto_com_token_admin`                | POST   | `/produtos`      |
| Cadastrar sem token              | `test_nao_deve_cadastrar_produto_sem_autenticacao`           | POST   | `/produtos`      |
| Cadastrar com token de não-admin | `test_nao_deve_cadastrar_produto_com_token_de_usuario_comum` | POST   | `/produtos`      |
| Nome duplicado                   | `test_nao_deve_cadastrar_produto_com_nome_duplicado`         | POST   | `/produtos`      |
| Campo `nome` ausente             | `test_nao_deve_cadastrar_produto_sem_nome`                   | POST   | `/produtos`      |
| Campo `preco` ausente            | `test_nao_deve_cadastrar_produto_sem_preco`                  | POST   | `/produtos`      |
| Campo `descricao` ausente        | `test_nao_deve_cadastrar_produto_sem_descricao`              | POST   | `/produtos`      |
| Campo `quantidade` ausente       | `test_nao_deve_cadastrar_produto_sem_quantidade`             | POST   | `/produtos`      |
| Buscar por ID válido             | `test_deve_buscar_produto_por_id_valido`                     | GET    | `/produtos/{id}` |
| Buscar por ID inexistente        | `test_nao_deve_buscar_produto_com_id_inexistente`            | GET    | `/produtos/{id}` |
| Atualizar com token admin        | `test_deve_atualizar_produto_com_token_admin`                | PUT    | `/produtos/{id}` |
| Atualizar sem token              | `test_nao_deve_atualizar_produto_sem_autenticacao`           | PUT    | `/produtos/{id}` |
| Atualizar com token de não-admin | `test_nao_deve_atualizar_produto_com_token_de_usuario_comum` | PUT    | `/produtos/{id}` |
| Excluir com token admin          | `test_deve_excluir_produto_com_token_admin`                  | DELETE | `/produtos/{id}` |
| Excluir sem token                | `test_nao_deve_excluir_produto_sem_autenticacao`             | DELETE | `/produtos/{id}` |
| Excluir ID inexistente           | `test_deve_retornar_mensagem_ao_excluir_produto_inexistente` | DELETE | `/produtos/{id}` |

Os tokens de admin e de usuário comum são obtidos dinamicamente: cada fixture cria um usuário via `/usuarios`, faz login em `/login` para obter o Bearer token e remove o usuário ao final do teste.

---

### `/carrinhos` — 14 testes funcionais

| Cenário                               | Teste                                                           | Método | Endpoint                     |
| ------------------------------------- | --------------------------------------------------------------- | ------ | ---------------------------- |
| Listar carrinhos                      | `test_deve_listar_carrinhos_sem_autenticacao`                   | GET    | `/carrinhos`                 |
| Criar carrinho com produto válido     | `test_deve_criar_carrinho_com_produto_valido`                   | POST   | `/carrinhos`                 |
| Criar sem token                       | `test_nao_deve_criar_carrinho_sem_autenticacao`                 | POST   | `/carrinhos`                 |
| Segundo carrinho mesmo usuário        | `test_nao_deve_criar_segundo_carrinho_para_mesmo_usuario`       | POST   | `/carrinhos`                 |
| Produto inexistente                   | `test_nao_deve_criar_carrinho_com_produto_inexistente`          | POST   | `/carrinhos`                 |
| Quantidade acima do estoque           | `test_nao_deve_criar_carrinho_com_quantidade_maior_que_estoque` | POST   | `/carrinhos`                 |
| Buscar por ID válido                  | `test_deve_buscar_carrinho_por_id_valido`                       | GET    | `/carrinhos/{id}`            |
| Buscar por ID inexistente             | `test_nao_deve_buscar_carrinho_com_id_inexistente`              | GET    | `/carrinhos/{id}`            |
| Concluir compra e decrementar estoque | `test_deve_concluir_compra_e_decrementar_estoque`               | DELETE | `/carrinhos/concluir-compra` |
| Concluir sem carrinho aberto          | `test_deve_retornar_mensagem_ao_concluir_compra_sem_carrinho`   | DELETE | `/carrinhos/concluir-compra` |
| Concluir sem token                    | `test_nao_deve_concluir_compra_sem_autenticacao`                | DELETE | `/carrinhos/concluir-compra` |
| Cancelar compra e repor estoque       | `test_deve_cancelar_compra_e_repor_estoque`                     | DELETE | `/carrinhos/cancelar-compra` |
| Cancelar sem carrinho aberto          | `test_deve_retornar_mensagem_ao_cancelar_compra_sem_carrinho`   | DELETE | `/carrinhos/cancelar-compra` |
| Cancelar sem token                    | `test_nao_deve_cancelar_compra_sem_autenticacao`                | DELETE | `/carrinhos/cancelar-compra` |

A fixture `carrinho_criado` captura o estoque original do produto antes de criar o carrinho, permitindo validar os efeitos de concluir e cancelar compra sobre o estoque.

---

### Testes de contrato com JSON Schema — 11 testes

Os testes de contrato validam a **estrutura** das respostas usando `jsonschema.validate()`. Eles são complementares aos testes funcionais: enquanto os testes funcionais verificam status code, mensagens e regras de negócio, os testes de contrato verificam se os campos obrigatórios continuam presentes e com os tipos esperados.

Os schemas ficam em `schemas/` e são importados diretamente nos testes.

| Teste                                | Endpoint              | O que valida                                            |
| ------------------------------------ | --------------------- | ------------------------------------------------------- |
| `test_schema_listar_usuarios`        | GET `/usuarios`       | `quantidade` e array `usuarios` com campos obrigatórios |
| `test_schema_cadastrar_usuario`      | POST `/usuarios`      | `message` e `_id`                                       |
| `test_schema_buscar_usuario_por_id`  | GET `/usuarios/{id}`  | estrutura completa de um usuário                        |
| `test_schema_login_sucesso`          | POST `/login`         | `message` e `authorization` no padrão `Bearer .+`       |
| `test_schema_login_erro_credenciais` | POST `/login`         | `message` de erro                                       |
| `test_schema_listar_produtos`        | GET `/produtos`       | `quantidade` e array `produtos` com campos obrigatórios |
| `test_schema_cadastrar_produto`      | POST `/produtos`      | `message` e `_id`                                       |
| `test_schema_buscar_produto_por_id`  | GET `/produtos/{id}`  | estrutura completa de um produto                        |
| `test_schema_listar_carrinhos`       | GET `/carrinhos`      | `quantidade` e array `carrinhos` com campos de carrinho |
| `test_schema_criar_carrinho`         | POST `/carrinhos`     | `message` e `_id`                                       |
| `test_schema_buscar_carrinho_por_id` | GET `/carrinhos/{id}` | estrutura completa de um carrinho                       |

---

## Total de testes

**62 testes automatizados** distribuídos entre testes funcionais, regras de negócio, segurança básica e contrato.

| Categoria               | Arquivo             | Testes |
| ----------------------- | ------------------- | -----: |
| Funcionais `/usuarios`  | `test_usuarios.py`  |     12 |
| Funcionais `/login`     | `test_login.py`     |      8 |
| Funcionais `/produtos`  | `test_produtos.py`  |     17 |
| Funcionais `/carrinhos` | `test_carrinhos.py` |     14 |
| Contrato JSON Schema    | `test_contratos.py` |     11 |
| **Total**               |                     | **62** |

---

## Análise de cobertura

A análise de cobertura foi feita com base na **matriz inicial de cenários planejados** no `PLANO-DE-TESTES.md`.

A matriz inicial previa **60 cenários**:

| Grupo             | Cenários planejados inicialmente |
| ----------------- | -------------------------------: |
| `/usuarios`       |                               12 |
| `/login`          |                                8 |
| `/produtos`       |                               20 |
| `/carrinhos`      |                               17 |
| Fluxos integrados |                                3 |
| **Total**         |                           **60** |

Após a implementação dos testes funcionais e dos testes de contrato, a suíte passou a cobrir **53 dos 60 cenários da matriz inicial**.

O cálculo utilizado foi:

```text
Cobertura = (cenários da matriz inicial cobertos / cenários planejados inicialmente) × 100
Cobertura = (53 / 60) × 100
Cobertura = 88,33%
```

| Métrica                                    | Resultado |
| ------------------------------------------ | --------: |
| Cenários planejados inicialmente           |        60 |
| Cenários da matriz inicial cobertos        |        53 |
| Cenários ainda pendentes da matriz inicial |         7 |
| Cobertura da matriz inicial                |    88,33% |
| Testes funcionais/regra/segurança          |        51 |
| Testes de contrato com JSON Schema         |        11 |
| Total de testes automatizados              |        62 |

### Cenários ainda pendentes da matriz inicial

| Cenário pendente                                          | Justificativa                                                                                                |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Atualizar produto com ID inexistente criando novo produto | Cenário específico da regra de `PUT`; pode gerar criação residual e exige investigação isolada.              |
| Tentar excluir produto vinculado a carrinho               | Depende de estado compartilhado entre produto e carrinho; permanece como investigação futura.                |
| Criar carrinho sem campo `produtos`                       | Cenário negativo válido, mas não automatizado nesta versão.                                                  |
| Criar carrinho com lista de produtos vazia                | Cenário negativo válido, mas não automatizado nesta versão.                                                  |
| Fluxo integrado F-01 — ciclo completo de compra           | Parte do comportamento foi coberta nos testes de carrinho, mas o fluxo E2E não foi isolado em teste próprio. |
| Fluxo integrado F-02 — ciclo de cancelamento              | Parte do comportamento foi coberta nos testes de carrinho, mas o fluxo E2E não foi isolado em teste próprio. |
| Fluxo integrado F-03 — produto em uso                     | Relacionado à tentativa de excluir produto vinculado a carrinho; permanece como investigação futura.         |

Os testes de contrato com JSON Schema cobriram dois cenários da matriz inicial que antes estavam pendentes: a validação estrutural da listagem de produtos e a validação estrutural da listagem de carrinhos. Os demais testes de contrato foram considerados testes adicionais de robustez do contrato, não novos cenários da matriz inicial.

---

## CI/CD com GitHub Actions

O arquivo `.github/workflows/tests.yml` configura a execução automática da suíte completa.

Gatilhos:

* `push` em qualquer branch
* `pull_request` em qualquer branch

Ambiente:

* Ubuntu latest
* Python 3.13

Passos principais:

```text
checkout → configurar Python → instalar dependências → executar pytest → gerar relatório HTML → publicar artefato
```

Comando executado no workflow:

```bash
pytest -vv --html=reports/relatorio.html --self-contained-html
```

O relatório HTML é publicado como artefato da execução e fica disponível na aba **Actions** do GitHub.

---

## Investigação exploratória e bug report

Durante o desenvolvimento, foi realizada uma **investigação manual exploratória** usando o **Postman** para verificar comportamentos da API que os testes automatizados não cobriam diretamente.

Essa investigação identificou um comportamento inconsistente na ServeRest: ao tentar excluir um recurso (`/usuarios` ou `/produtos`) por um ID válido, mas inexistente, a API retorna **200 OK** com `"Nenhum registro excluído"` em vez de um erro 4xx.

O resultado foi documentado na **Issue #1** do repositório:

[DELETE retorna 200 OK ao tentar excluir recurso inexistente](https://github.com/kanan-lopes/serverest-pytest-usuarios_DesafioBootcamp/issues/1)

---

## Padrões do projeto

* **Client pattern** — cada endpoint tem um client dedicado; nenhum `requests.*` é usado diretamente nos testes.
* **JSON Schema** — schemas organizados por endpoint em `schemas/`; validação via `jsonschema.validate()`.
* **Data factory** — payloads são gerados dinamicamente com `uuid4`, evitando conflitos entre execuções.
* **Fixtures com yield** — pré-condição antes do `yield`, limpeza depois, garantindo isolamento mesmo em falhas.
* **Independência total** — cada teste cria e limpa seus próprios dados.
* **Marcadores** — `@pytest.mark.usuarios`, `@pytest.mark.login`, `@pytest.mark.produtos`, `@pytest.mark.carrinhos`, `@pytest.mark.contrato`.
* **Relatório HTML** — geração com `pytest-html` para anexação como evidência.
* **CI/CD** — execução automática da suíte via GitHub Actions.

---

## Extras implementados

| Extra                                                                        | Status       | Evidência                            |
| ---------------------------------------------------------------------------- | ------------ | ------------------------------------ |
| Validar estrutura das respostas usando JSON Schema em pelo menos 3 endpoints | Implementado | 11 testes de contrato em 4 endpoints |
| Configurar GitHub Actions para rodar os testes automaticamente a cada push   | Implementado | `.github/workflows/tests.yml`        |
