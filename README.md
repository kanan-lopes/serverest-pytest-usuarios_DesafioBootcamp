# Testes Automatizados - ServeRest API

Projeto de automação de testes para a API **ServeRest**, cobrindo os endpoints de **Usuários**, **Login**, **Produtos** e **Carrinhos**, utilizando **Python**, **Requests** e **Pytest**.

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
* Postman

---

## Estrutura do projeto

```text
serverest-pytest-usuarios/
│
├── clients/
│   ├── usuarios_client.py      # chamadas HTTP para /usuarios
│   ├── login_client.py         # chamadas HTTP para /login
│   ├── produtos_client.py      # chamadas HTTP para /produtos
│   ├── carrinhos_client.py     # chamadas HTTP para /carrinhos
│   └── __init__.py
│
├── tests/
│   ├── conftest.py             # fixtures compartilhadas
│   ├── test_usuarios.py        # 12 testes do endpoint /usuarios
│   ├── test_login.py           # 8 testes do endpoint /login
│   ├── test_produtos.py        # 17 testes do endpoint /produtos
│   └── test_carrinhos.py       # 14 testes do endpoint /carrinhos
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
```

Executar por marcador:

```bash
pytest -m usuarios
pytest -m login
pytest -m produtos
pytest -m carrinhos
```

Executar um teste específico:

```bash
pytest tests/test_carrinhos.py::test_deve_concluir_compra_e_decrementar_estoque -vv
```

Executar testes filtrando pelo nome:

```bash
pytest -k "cadastrar" -vv
pytest -k "admin" -vv
pytest -k "carrinho" -vv
```

Exibir prints durante a execução:

```bash
pytest -s
```

Gerar relatório HTML com Pytest HTML:

```bash
pytest -vv --html=reports/relatorio.html --self-contained-html
```

O relatório será gerado em:

```text
reports/relatorio.html
```

---

## Testes implementados

### `/usuarios` — 12 testes

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

### `/login` — 8 testes

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

### `/produtos` — 17 testes

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

### `/carrinhos` — 14 testes

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

Os testes de carrinho criam dinamicamente um usuário autenticado e um produto disponível. A fixture `carrinho_criado` captura o estoque original do produto antes de criar o carrinho, permitindo validar os efeitos de concluir e cancelar compra sobre o estoque.

---

## Total de testes

**51 testes automatizados** distribuídos em 4 endpoints.

| Endpoint     | Testes |
| ------------ | -----: |
| `/usuarios`  |     12 |
| `/login`     |      8 |
| `/produtos`  |     17 |
| `/carrinhos` |     14 |
| **Total**    | **51** |

---

## Análise de cobertura

A análise de cobertura foi feita com base na matriz inicial de cenários planejados no `PLANO-DE-TESTES.md`.

O método utilizado foi:

```text
Cobertura = (cenários automatizados / cenários planejados) × 100
```

A primeira versão do plano previa **60 cenários** no total:

| Grupo             | Cenários planejados inicialmente |
| ----------------- | -------------------------------: |
| `/usuarios`       |                               12 |
| `/login`          |                                8 |
| `/produtos`       |                               20 |
| `/carrinhos`      |                               17 |
| Fluxos integrados |                                3 |
| **Total**         |                           **60** |

Ao final do projeto, foram implementados **51 testes automatizados**:

| Grupo             | Implementados | Pendentes | Total planejado | Cobertura |
| ----------------- | ------------: | --------: | --------------: | --------: |
| `/usuarios`       |            12 |         0 |              12 |      100% |
| `/login`          |             8 |         0 |               8 |      100% |
| `/produtos`       |            17 |         3 |              20 |       85% |
| `/carrinhos`      |            14 |         3 |              17 |    82,35% |
| Fluxos integrados |             0 |         3 |               3 |        0% |
| **Total**         |        **51** |     **9** |          **60** |   **85%** |

Cálculo da cobertura total:

```text
Cobertura = (51 / 60) × 100
Cobertura = 85%
```

Portanto, a cobertura total atingida pela suíte foi de **85%** em relação à matriz inicial de cenários planejados.

### Cenários que ficaram fora da automação

| Cenário fora da automação                                              | Justificativa                                                                                                         |
| ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Validação formal da estrutura de item retornado em `GET /produtos`     | A listagem de produtos foi testada, mas sem validação detalhada de schema para cada item da lista.                    |
| Atualização de produto com ID inexistente criando novo produto         | Cenário específico da regra de `PUT`; foi deixado para investigação futura para evitar criação residual indevida.     |
| Tentativa de excluir produto vinculado a carrinho                      | Depende de estado compartilhado entre produto e carrinho; pode ser explorado em investigação futura.                  |
| Validação formal da estrutura dos itens retornados em `GET /carrinhos` | A listagem foi testada, mas sem validação detalhada de schema para cada item.                                         |
| Criação de carrinho sem campo `produtos`                               | Cenário negativo válido, mas não automatizado nesta etapa.                                                            |
| Criação de carrinho com lista de produtos vazia                        | Cenário negativo válido, mas não automatizado nesta etapa.                                                            |
| Fluxo integrado F-01 — ciclo completo de compra                        | Parte do comportamento foi coberta nos testes de carrinho, mas o fluxo E2E completo não foi isolado em teste próprio. |
| Fluxo integrado F-02 — ciclo de cancelamento                           | Parte do comportamento foi coberta nos testes de carrinho, mas o fluxo E2E completo não foi isolado em teste próprio. |
| Fluxo integrado F-03 — produto em uso                                  | Cenário relacionado à tentativa de excluir produto vinculado a carrinho; permanece como investigação futura.          |

Embora a cobertura total por cenários seja de **85%**, a suíte cobre os principais endpoints e métodos HTTP definidos no escopo do projeto.

| Endpoint                     | Métodos cobertos |
| ---------------------------- | ---------------- |
| `/usuarios`                  | GET, POST        |
| `/usuarios/{id}`             | GET, PUT, DELETE |
| `/login`                     | POST             |
| `/produtos`                  | GET, POST        |
| `/produtos/{id}`             | GET, PUT, DELETE |
| `/carrinhos`                 | GET, POST        |
| `/carrinhos/{id}`            | GET              |
| `/carrinhos/concluir-compra` | DELETE           |
| `/carrinhos/cancelar-compra` | DELETE           |

---

## Investigação exploratória e bug report

Durante o desenvolvimento do projeto, além dos testes automatizados, foi realizada uma **investigação manual exploratória** usando o **Postman** para verificar comportamentos da API que os testes automatizados não cobriam diretamente.

Essa investigação identificou um comportamento inconsistente na ServeRest: ao tentar excluir um recurso (`/usuarios` ou `/produtos`) por um ID válido, mas inexistente, a API retorna **200 OK** com `"Nenhum registro excluído"` em vez de um erro 4xx. Esse comportamento pode mascarar problemas em integrações que esperam uma indicação explícita de falha ao tentar remover algo que não existe.

O resultado da investigação foi documentado na **Issue #1** do repositório:

[DELETE retorna 200 OK ao tentar excluir recurso inexistente](https://github.com/kanan-lopes/serverest-pytest-usuarios_DesafioBootcamp/issues/1)

---

## Padrões do projeto

* **Client pattern** — cada endpoint tem um client dedicado; nenhum `requests.*` é usado diretamente nos testes.
* **Data factory** — payloads são gerados dinamicamente com `uuid4`, evitando conflitos entre execuções.
* **Fixtures com yield** — pré-condição antes do `yield`, limpeza depois, garantindo isolamento mesmo em falhas.
* **Independência total** — cada teste cria e limpa seus próprios dados; nenhum depende de outro.
* **Marcadores** — `@pytest.mark.usuarios`, `@pytest.mark.login`, `@pytest.mark.produtos`, `@pytest.mark.carrinhos`.

---

## Desafios extras opcionais

Os seguintes desafios extras foram considerados, mas não foram implementados nesta versão:

| Extra                                                                             | Status           |
| --------------------------------------------------------------------------------- | ---------------- |
| Validação de estrutura das respostas usando JSON Schema em pelo menos 3 endpoints | Não implementado |
| Configuração de GitHub Actions para rodar os testes automaticamente a cada push   | Não implementado |
