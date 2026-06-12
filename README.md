# Testes Automatizados - ServeRest Usuários

Projeto de automação de testes para o endpoint de **Usuários** da API ServeRest, utilizando **Python**, **Requests** e **Pytest**.

API utilizada:

```text
https://compassuol.serverest.dev
```

Endpoint testado:

```text
/usuarios
```

---

## Tecnologias utilizadas

* Python
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
│   └── usuarios_client.py
│
├── tests/
│   ├── conftest.py
│   └── test_usuarios.py
│
├── utils/
│   └── data_factory.py
│
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Como instalar

Clone o repositório:

```bash
git clone git clone https://github.com/kanan-lopes/serverest-pytest-usuarios_DesafioBootcamp.git
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

Executar apenas o arquivo de testes de usuários:

```bash
pytest tests/test_usuarios.py
```

Executar testes pelo marcador `usuarios`:

```bash
pytest -m usuarios
```

Executar um teste específico:

```bash
pytest tests/test_usuarios.py::test_deve_listar_usuarios_com_sucesso -vv
```

Executar testes filtrando pelo nome:

```bash
pytest -k "cadastrar" -vv
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

## Cenários mínimos solicitados

| Cenário mínimo                        | Teste implementado                                    | Método HTTP | Endpoint         |
| ------------------------------------- | ----------------------------------------------------- | ----------- | ---------------- |
| Listar usuários                       | `test_deve_listar_usuarios_com_sucesso`               | GET         | `/usuarios`      |
| Cadastrar usuário válido              | `test_deve_cadastrar_usuario_valido_com_sucesso`      | POST        | `/usuarios`      |
| Cadastrar usuário com email duplicado | `test_nao_deve_cadastrar_usuario_com_email_duplicado` | POST        | `/usuarios`      |
| Cadastrar usuário com campos faltando | `test_nao_deve_cadastrar_usuario_sem_nome`            | POST        | `/usuarios`      |
| Cadastrar usuário com campos faltando | `test_nao_deve_cadastrar_usuario_sem_email`           | POST        | `/usuarios`      |
| Cadastrar usuário com campos faltando | `test_nao_deve_cadastrar_usuario_sem_password`        | POST        | `/usuarios`      |
| Cadastrar usuário com campos faltando | `test_nao_deve_cadastrar_usuario_sem_administrador`   | POST        | `/usuarios`      |
| Buscar usuário por ID                 | `test_deve_buscar_usuario_por_id_valido`              | GET         | `/usuarios/{id}` |
| Atualizar usuário                     | `test_deve_atualizar_usuario_existente_com_sucesso`   | PUT         | `/usuarios/{id}` |
| Excluir usuário                       | `test_deve_excluir_usuario_existente_com_sucesso`     | DELETE      | `/usuarios/{id}` |

---

## Cenários adicionais

| Cenário adicional                 | Teste implementado                                           | Método HTTP | Endpoint         |
| --------------------------------- | ------------------------------------------------------------ | ----------- | ---------------- |
| Buscar usuário com ID inexistente | `test_nao_deve_buscar_usuario_com_id_inexistente`            | GET         | `/usuarios/{id}` |
| Excluir usuário inexistente       | `test_deve_retornar_mensagem_ao_excluir_usuario_inexistente` | DELETE      | `/usuarios/{id}` |

---

## Total de testes

Foram implementados **12 testes automatizados** para o endpoint `/usuarios`.

Os testes utilizam emails dinâmicos para evitar conflitos e foram estruturados para serem independentes entre si.
