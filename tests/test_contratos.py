"""
Testes de contrato via JSON Schema — ServeRest API

Esses testes validam a ESTRUTURA das respostas da API, verificando que
os campos obrigatórios estão presentes e com os tipos corretos.

São complementares aos testes funcionais: enquanto estes verificam valores
específicos (status code, mensagens), os testes de contrato garantem que
o formato da resposta não mudou de forma inesperada — útil para detectar
quebras de contrato em atualizações da API.

Todos os testes usam jsonschema.validate(instance=body, schema=schema).
Caso a estrutura da resposta não corresponda ao schema, a validação lança
jsonschema.ValidationError com detalhes precisos do campo problemático.
"""

import pytest
import jsonschema

from schemas.usuarios_schema import (
    SCHEMA_LISTAR_USUARIOS,
    SCHEMA_CADASTRAR_USUARIO,
    SCHEMA_BUSCAR_USUARIO_POR_ID,
)
from schemas.login_schema import (
    SCHEMA_LOGIN_SUCESSO,
    SCHEMA_LOGIN_ERRO_CREDENCIAIS,
)
from schemas.produtos_schema import (
    SCHEMA_LISTAR_PRODUTOS,
    SCHEMA_CADASTRAR_PRODUTO,
    SCHEMA_BUSCAR_PRODUTO_POR_ID,
)
from schemas.carrinhos_schema import (
    SCHEMA_LISTAR_CARRINHOS,
    SCHEMA_BUSCAR_CARRINHO_POR_ID,
    SCHEMA_CRIAR_CARRINHO,
)
from utils.data_factory import gerar_credenciais_login


# ─────────────────────────────────────────────
# Contratos de /usuarios
# ─────────────────────────────────────────────

@pytest.mark.usuarios
@pytest.mark.contrato
def test_schema_listar_usuarios(usuarios_client):
    """
    Objetivo:
    Validar que a resposta de GET /usuarios está em conformidade com o schema
    esperado: objeto com 'quantidade' (integer) e 'usuarios' (array de objetos
    com campos obrigatórios nome, email, password, administrador e _id).

    Critérios verificados:
    - Status code 200.
    - jsonschema.validate() não lança exceção com SCHEMA_LISTAR_USUARIOS.
    """
    response = usuarios_client.listar_usuarios()
    body = response.json()

    assert response.status_code == 200
    jsonschema.validate(instance=body, schema=SCHEMA_LISTAR_USUARIOS)


@pytest.mark.usuarios
@pytest.mark.contrato
def test_schema_cadastrar_usuario(usuarios_client, usuario_payload):
    """
    Objetivo:
    Validar que a resposta de POST /usuarios (cadastro bem-sucedido) contém
    os campos 'message' e '_id' com os tipos e valores esperados.

    Critérios verificados:
    - Status code 201.
    - jsonschema.validate() não lança exceção com SCHEMA_CADASTRAR_USUARIO.

    Limpeza:
    - O usuário criado é removido ao final.
    """
    response = usuarios_client.cadastrar_usuario(usuario_payload)
    body = response.json()

    assert response.status_code == 201
    jsonschema.validate(instance=body, schema=SCHEMA_CADASTRAR_USUARIO)

    # Limpeza
    usuarios_client.excluir_usuario(body["_id"])


@pytest.mark.usuarios
@pytest.mark.contrato
def test_schema_buscar_usuario_por_id(usuarios_client, usuario_criado):
    """
    Objetivo:
    Validar que a resposta de GET /usuarios/{id} contém todos os campos
    esperados com os tipos corretos.

    Critérios verificados:
    - Status code 200.
    - jsonschema.validate() não lança exceção com SCHEMA_BUSCAR_USUARIO_POR_ID.
    """
    usuario_id = usuario_criado["id"]

    response = usuarios_client.buscar_usuario_por_id(usuario_id)
    body = response.json()

    assert response.status_code == 200
    jsonschema.validate(instance=body, schema=SCHEMA_BUSCAR_USUARIO_POR_ID)


# ─────────────────────────────────────────────
# Contratos de /login
# ─────────────────────────────────────────────

@pytest.mark.login
@pytest.mark.contrato
def test_schema_login_sucesso(login_client, usuario_admin_criado):
    """
    Objetivo:
    Validar que a resposta de POST /login (sucesso) contém 'message' com o valor
    correto e 'authorization' no formato 'Bearer <token>'.

    Critérios verificados:
    - Status code 200.
    - jsonschema.validate() não lança exceção com SCHEMA_LOGIN_SUCESSO.
    - O campo 'authorization' começa com 'Bearer ' (validado pelo pattern do schema).
    """
    email = usuario_admin_criado["payload"]["email"]
    password = usuario_admin_criado["payload"]["password"]

    credentials = gerar_credenciais_login(email, password)
    response = login_client.fazer_login(credentials)
    body = response.json()

    assert response.status_code == 200
    jsonschema.validate(instance=body, schema=SCHEMA_LOGIN_SUCESSO)


@pytest.mark.login
@pytest.mark.contrato
def test_schema_login_erro_credenciais(login_client):
    """
    Objetivo:
    Validar que a resposta de POST /login com credenciais inválidas
    contém apenas o campo 'message' com a mensagem de erro esperada.

    Critérios verificados:
    - Status code 401.
    - jsonschema.validate() não lança exceção com SCHEMA_LOGIN_ERRO_CREDENCIAIS.
    """
    credentials = gerar_credenciais_login(
        email="nao_existe@teste.com",
        password="senha_invalida"
    )
    response = login_client.fazer_login(credentials)
    body = response.json()

    assert response.status_code == 401
    jsonschema.validate(instance=body, schema=SCHEMA_LOGIN_ERRO_CREDENCIAIS)


# ─────────────────────────────────────────────
# Contratos de /produtos
# ─────────────────────────────────────────────

@pytest.mark.produtos
@pytest.mark.contrato
def test_schema_listar_produtos(produtos_client):
    """
    Objetivo:
    Validar que a resposta de GET /produtos está em conformidade com o schema:
    objeto com 'quantidade' (integer) e 'produtos' (array de objetos com
    nome, preco, descricao, quantidade e _id).

    Critérios verificados:
    - Status code 200.
    - jsonschema.validate() não lança exceção com SCHEMA_LISTAR_PRODUTOS.
    """
    response = produtos_client.listar_produtos()
    body = response.json()

    assert response.status_code == 200
    jsonschema.validate(instance=body, schema=SCHEMA_LISTAR_PRODUTOS)


@pytest.mark.produtos
@pytest.mark.contrato
def test_schema_cadastrar_produto(produtos_client, produto_payload, token_admin):
    """
    Objetivo:
    Validar que a resposta de POST /produtos (cadastro bem-sucedido) contém
    os campos 'message' e '_id' com os tipos e valores esperados.

    Critérios verificados:
    - Status code 201.
    - jsonschema.validate() não lança exceção com SCHEMA_CADASTRAR_PRODUTO.

    Limpeza:
    - O produto criado é removido ao final.
    """
    response = produtos_client.cadastrar_produto(
        produto_payload, token=token_admin)
    body = response.json()

    assert response.status_code == 201
    jsonschema.validate(instance=body, schema=SCHEMA_CADASTRAR_PRODUTO)

    # Limpeza
    produtos_client.excluir_produto(body["_id"], token=token_admin)


@pytest.mark.produtos
@pytest.mark.contrato
def test_schema_buscar_produto_por_id(produtos_client, produto_criado):
    """
    Objetivo:
    Validar que a resposta de GET /produtos/{id} contém todos os campos
    esperados com os tipos corretos.

    Critérios verificados:
    - Status code 200.
    - jsonschema.validate() não lança exceção com SCHEMA_BUSCAR_PRODUTO_POR_ID.
    """
    produto_id = produto_criado["id"]

    response = produtos_client.buscar_produto_por_id(produto_id)
    body = response.json()

    assert response.status_code == 200
    jsonschema.validate(instance=body, schema=SCHEMA_BUSCAR_PRODUTO_POR_ID)


# ─────────────────────────────────────────────
# Contratos de /carrinhos
# ─────────────────────────────────────────────

@pytest.mark.carrinhos
@pytest.mark.contrato
def test_schema_listar_carrinhos(carrinhos_client, carrinho_criado):
    """
    Objetivo:
    Validar que a resposta de GET /carrinhos está em conformidade com o schema:
    objeto com 'quantidade' e 'carrinhos' (array com campos calculados como
    precoTotal e quantidadeTotal).

    Pré-condição:
    - A fixture carrinho_criado garante que pelo menos 1 carrinho existe no momento
      da chamada, tornando a listagem não vazia e os itens validáveis.

    Critérios verificados:
    - Status code 200.
    - jsonschema.validate() não lança exceção com SCHEMA_LISTAR_CARRINHOS.
    """
    response = carrinhos_client.listar_carrinhos()
    body = response.json()

    assert response.status_code == 200
    jsonschema.validate(instance=body, schema=SCHEMA_LISTAR_CARRINHOS)


@pytest.mark.carrinhos
@pytest.mark.contrato
def test_schema_criar_carrinho(carrinhos_client, usuario_com_token_e_produto):
    """
    Objetivo:
    Validar que a resposta de POST /carrinhos (criação bem-sucedida) contém
    os campos 'message' e '_id' com os tipos e valores esperados.

    Critérios verificados:
    - Status code 201.
    - jsonschema.validate() não lança exceção com SCHEMA_CRIAR_CARRINHO.

    Limpeza:
    - O carrinho criado é cancelado ao final.
    """
    from utils.data_factory import gerar_carrinho_valido

    token = usuario_com_token_e_produto["token"]
    produto_id = usuario_com_token_e_produto["produto_id"]

    payload = gerar_carrinho_valido(produto_id, quantidade=1)
    response = carrinhos_client.criar_carrinho(payload, token=token)
    body = response.json()

    assert response.status_code == 201
    jsonschema.validate(instance=body, schema=SCHEMA_CRIAR_CARRINHO)

    # Limpeza
    carrinhos_client.cancelar_compra(token=token)


@pytest.mark.carrinhos
@pytest.mark.contrato
def test_schema_buscar_carrinho_por_id(carrinhos_client, carrinho_criado):
    """
    Objetivo:
    Validar que a resposta de GET /carrinhos/{id} contém todos os campos
    esperados, incluindo produtos com precoUnitario, precoTotal e quantidadeTotal.

    Critérios verificados:
    - Status code 200.
    - jsonschema.validate() não lança exceção com SCHEMA_BUSCAR_CARRINHO_POR_ID.
    """
    carrinho_id = carrinho_criado["carrinho_id"]

    response = carrinhos_client.buscar_carrinho_por_id(carrinho_id)
    body = response.json()

    assert response.status_code == 200
    jsonschema.validate(instance=body, schema=SCHEMA_BUSCAR_CARRINHO_POR_ID)
