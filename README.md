# Testes Automatizados - ServeRest API

Projeto de automação de testes para a API **ServeRest**, cobrindo os endpoints de Usuários, Login e Produtos, utilizando **Python**, **Requests** e **Pytest**.

API utilizada:

```text
https://compassuol.serverest.dev
```

Endpoints cobertos:

```text
/usuarios
/login
/produtos
```

---

## Tecnologias utilizadas

* Python 3.13
* Pytest
* Requests
* Python Dotenv
* Pytest HTML

---

## Estrutura do projeto

```text
serverest-pytest-usuarios/
│
├── clients/
│   ├── usuarios_client.py      # chamadas HTTP para /usuarios
│   ├── login_client.py         # chamadas HTTP para /login
│   ├── produtos_client.py      # chamadas HTTP para /produtos
│   └── __init__.py
│
├── tests/
│   ├── conftest.py             # fixtures compartilhadas (clients, tokens, dados)
│   ├── test_usuarios.py        # 12 testes do endpoint /usuarios
│   ├── test_login.py           # 8 testes do endpoint /login
│   └── test_produtos.py        # 17 testes do endpoint /produtos
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

Executar um arquivo específico:

```bash
pytest tests/test_usuarios.py
pytest tests/test_login.py
pytest tests/test_produtos.py
```

Executar por marcador:

```bash
pytest -m usuarios
pytest -m login
pytest -m produtos
```

Executar um teste específico:

```bash
pytest tests/test_login.py::test_deve_fazer_login_com_usuario_administrador -vv
```

Executar testes filtrando pelo nome:

```bash
pytest -k "cadastrar" -vv
pytest -k "admin" -vv
```

Exibir prints durante a execução:

```bash
pytest -s
```

Gerar relatório HTML:

```bash
pytest --html=reports/relatorio.html --self-contained-html
```

---

## Testes implementados

### `/usuarios` — 12 testes

| Cenário | Teste | Método | Endpoint |
| --- | --- | --- | --- |
| Listar usuários | `test_deve_listar_usuarios_com_sucesso` | GET | `/usuarios` |
| Cadastrar usuário válido | `test_deve_cadastrar_usuario_valido_com_sucesso` | POST | `/usuarios` |
| Email duplicado | `test_nao_deve_cadastrar_usuario_com_email_duplicado` | POST | `/usuarios` |
| Campo `nome` ausente | `test_nao_deve_cadastrar_usuario_sem_nome` | POST | `/usuarios` |
| Campo `email` ausente | `test_nao_deve_cadastrar_usuario_sem_email` | POST | `/usuarios` |
| Campo `password` ausente | `test_nao_deve_cadastrar_usuario_sem_password` | POST | `/usuarios` |
| Campo `administrador` ausente | `test_nao_deve_cadastrar_usuario_sem_administrador` | POST | `/usuarios` |
| Buscar por ID válido | `test_deve_buscar_usuario_por_id_valido` | GET | `/usuarios/{id}` |
| Buscar por ID inexistente | `test_nao_deve_buscar_usuario_com_id_inexistente` | GET | `/usuarios/{id}` |
| Atualizar usuário | `test_deve_atualizar_usuario_existente_com_sucesso` | PUT | `/usuarios/{id}` |
| Excluir usuário existente | `test_deve_excluir_usuario_existente_com_sucesso` | DELETE | `/usuarios/{id}` |
| Excluir usuário inexistente | `test_deve_retornar_mensagem_ao_excluir_usuario_inexistente` | DELETE | `/usuarios/{id}` |

---

### `/login` — 8 testes

| Cenário | Teste | Método | Endpoint |
| --- | --- | --- | --- |
| Login com administrador | `test_deve_fazer_login_com_usuario_administrador` | POST | `/login` |
| Login com usuário comum | `test_deve_fazer_login_com_usuario_comum` | POST | `/login` |
| Token no formato Bearer | `test_token_retornado_deve_ser_string_nao_vazia` | POST | `/login` |
| Senha errada | `test_nao_deve_fazer_login_com_senha_errada` | POST | `/login` |
| Email inexistente | `test_nao_deve_fazer_login_com_email_inexistente` | POST | `/login` |
| Campo `email` ausente | `test_nao_deve_fazer_login_sem_email` | POST | `/login` |
| Campo `password` ausente | `test_nao_deve_fazer_login_sem_password` | POST | `/login` |
| Body vazio | `test_nao_deve_fazer_login_com_body_vazio` | POST | `/login` |

> Os testes de login válido criam usuários dinamicamente via `/usuarios` e os removem ao final, sem depender de dados fixos da base.

---

### `/produtos` — 17 testes

| Cenário | Teste | Método | Endpoint |
| --- | --- | --- | --- |
| Listar produtos | `test_deve_listar_produtos_sem_autenticacao` | GET | `/produtos` |
| Cadastrar com token admin | `test_deve_cadastrar_produto_com_token_admin` | POST | `/produtos` |
| Cadastrar sem token | `test_nao_deve_cadastrar_produto_sem_autenticacao` | POST | `/produtos` |
| Cadastrar com token de não-admin | `test_nao_deve_cadastrar_produto_com_token_de_usuario_comum` | POST | `/produtos` |
| Nome duplicado | `test_nao_deve_cadastrar_produto_com_nome_duplicado` | POST | `/produtos` |
| Campo `nome` ausente | `test_nao_deve_cadastrar_produto_sem_nome` | POST | `/produtos` |
| Campo `preco` ausente | `test_nao_deve_cadastrar_produto_sem_preco` | POST | `/produtos` |
| Campo `descricao` ausente | `test_nao_deve_cadastrar_produto_sem_descricao` | POST | `/produtos` |
| Campo `quantidade` ausente | `test_nao_deve_cadastrar_produto_sem_quantidade` | POST | `/produtos` |
| Buscar por ID válido | `test_deve_buscar_produto_por_id_valido` | GET | `/produtos/{id}` |
| Buscar por ID inexistente | `test_nao_deve_buscar_produto_com_id_inexistente` | GET | `/produtos/{id}` |
| Atualizar com token admin | `test_deve_atualizar_produto_com_token_admin` | PUT | `/produtos/{id}` |
| Atualizar sem token | `test_nao_deve_atualizar_produto_sem_autenticacao` | PUT | `/produtos/{id}` |
| Atualizar com token de não-admin | `test_nao_deve_atualizar_produto_com_token_de_usuario_comum` | PUT | `/produtos/{id}` |
| Excluir com token admin | `test_deve_excluir_produto_com_token_admin` | DELETE | `/produtos/{id}` |
| Excluir sem token | `test_nao_deve_excluir_produto_sem_autenticacao` | DELETE | `/produtos/{id}` |
| Excluir ID inexistente | `test_deve_retornar_mensagem_ao_excluir_produto_inexistente` | DELETE | `/produtos/{id}` |

> Os tokens de admin e de usuário comum são obtidos dinamicamente: cada fixture cria um usuário via `/usuarios`, faz login em `/login` para obter o Bearer token e remove o usuário ao final do teste.

---

## Total de testes

**37 testes automatizados** distribuídos em 3 endpoints.

| Endpoint | Testes |
| --- | --- |
| `/usuarios` | 12 |
| `/login` | 8 |
| `/produtos` | 17 |
| **Total** | **37** |

---

## Padrões do projeto

- **Client pattern** — cada endpoint tem um client dedicado; nenhum `requests.*` é usado diretamente nos testes
- **Data factory** — todos os payloads são gerados dinamicamente com `uuid4`, evitando conflitos entre execuções
- **Fixtures com yield** — pré-condição antes do `yield`, limpeza depois, garantindo isolamento mesmo em falhas
- **Independência total** — cada teste cria e limpa seus próprios dados; nenhum depende de outro
- **Marcadores** — `@pytest.mark.usuarios`, `@pytest.mark.login`, `@pytest.mark.produtos`
