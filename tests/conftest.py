import os
import pytest
from dotenv import load_dotenv

# cliente para o endpoint /usuarios
from clients.usuarios_client import UsuariosClient
# cliente para o endpoint /login
from clients.login_client import LoginClient
# cliente para o endpoint /produtos
from clients.produtos_client import ProdutosClient
from utils.data_factory import (
    gerar_usuario_valido,
    gerar_credenciais_login,
    gerar_produto_valido,
)

"""
Lembrando que este arquivo é carregado automaticamente pelo pytest, daí podemos usar
def test_alguma_coisa(usuarios_client), sem precisar importar manualmente.
"""

load_dotenv()  # carregando variáveis do arquivo .env


# ─────────────────────────────────────────────
# Fixtures de infraestrutura
# ─────────────────────────────────────────────

# session → fixture criada uma vez por execução completa
@pytest.fixture(scope="session")
def base_url():
    """
    Define a URL base da API.
    Caso exista uma variável BASE_URL no ambiente, ela será usada.
    Caso contrário, será usada a URL da Compass informada no projeto.
    """
    return os.getenv("BASE_URL", "https://compassuol.serverest.dev")


# ─────────────────────────────────────────────
# Fixtures de clients
# ─────────────────────────────────────────────

@pytest.fixture
def usuarios_client(base_url):
    """
    Fixture que fornece uma instância do cliente de usuários.
    """
    return UsuariosClient(base_url)


@pytest.fixture
def login_client(base_url):
    """
    Fixture que fornece uma instância do cliente de login.
    """
    return LoginClient(base_url)


@pytest.fixture
def produtos_client(base_url):
    """
    Fixture que fornece uma instância do cliente de produtos.
    """
    return ProdutosClient(base_url)


# ─────────────────────────────────────────────
# Fixtures de usuários
# ─────────────────────────────────────────────

@pytest.fixture
def usuario_payload():
    """
    Fixture que retorna um payload válido para cadastro de usuário.
    Cada chamada gera um email único, garantindo independência entre testes.
    Isso evita o problema de "email já está sendo usado".
    """
    return gerar_usuario_valido()


@pytest.fixture
def usuario_criado(usuarios_client):
    """
    Cria um usuário antes do teste e tenta removê-lo depois.
    Essa fixture é útil para testes que precisam de um usuário existente,
    como buscar por ID, atualizar e excluir.
    """
    payload = gerar_usuario_valido()

    response = usuarios_client.cadastrar_usuario(payload)  # cadastro na API
    assert response.status_code == 201  # requisição bem sucedida

    # id utilizado pelos testes de busca, att, exclusão
    usuario_id = response.json()["_id"]

    yield {
        "id": usuario_id,
        "payload": payload
    }
    """
    Tudo antes do yield  → acontece antes do teste
    O valor do yield     → é entregue para o teste
    Tudo depois do yield → acontece depois do teste (limpeza)
    """
    # Caso o próprio teste já tenha excluído o usuário, a chamada pode retornar 200 ou 400.
    usuarios_client.excluir_usuario(usuario_id)


@pytest.fixture
def usuario_admin_criado(usuarios_client):
    """
    Cria um usuário administrador antes do teste e o remove depois.

    Útil para testes que precisam de um administrador real criado dinamicamente,
    evitando dependência de dados fixos da base.
    """
    payload = gerar_usuario_valido(administrador="true")

    response = usuarios_client.cadastrar_usuario(payload)
    assert response.status_code == 201

    usuario_id = response.json()["_id"]

    yield {
        "id": usuario_id,
        "payload": payload
    }

    usuarios_client.excluir_usuario(usuario_id)


@pytest.fixture
def usuario_comum_criado(usuarios_client):
    """
    Cria um usuário não-administrador antes do teste e o remove depois.

    Útil para testes que precisam de um usuário comum criado dinamicamente,
    evitando dependência de dados fixos da base.
    """
    payload = gerar_usuario_valido(administrador="false")

    response = usuarios_client.cadastrar_usuario(payload)
    assert response.status_code == 201

    usuario_id = response.json()["_id"]

    yield {
        "id": usuario_id,
        "payload": payload
    }

    usuarios_client.excluir_usuario(usuario_id)


# ─────────────────────────────────────────────
# Fixtures de tokens de autenticação
# ─────────────────────────────────────────────

@pytest.fixture
def token_admin(usuarios_client, login_client):
    """
    Cria um usuário administrador, realiza login e retorna o token Bearer.
    Remove o usuário ao final do teste.

    Essa fixture é usada pelos testes de produtos que exigem permissão de admin
    para cadastrar, atualizar e excluir produtos.
    """
    payload = gerar_usuario_valido(administrador="true")

    # Cria o usuário admin
    response_cadastro = usuarios_client.cadastrar_usuario(payload)
    assert response_cadastro.status_code == 201
    usuario_id = response_cadastro.json()["_id"]

    # Faz login para obter o token
    credentials = gerar_credenciais_login(
        payload["email"], payload["password"])
    response_login = login_client.fazer_login(credentials)
    assert response_login.status_code == 200
    token = response_login.json()["authorization"]

    yield token

    # Limpeza: remove o usuário admin criado para este teste
    usuarios_client.excluir_usuario(usuario_id)


@pytest.fixture
def token_usuario_comum(usuarios_client, login_client):
    """
    Cria um usuário não-administrador, realiza login e retorna o token Bearer.
    Remove o usuário ao final do teste.

    Essa fixture é usada pelos testes de produtos que verificam que
    um usuário comum NÃO tem permissão para cadastrar, atualizar e excluir produtos.
    """
    payload = gerar_usuario_valido(administrador="false")

    # Cria o usuário comum
    response_cadastro = usuarios_client.cadastrar_usuario(payload)
    assert response_cadastro.status_code == 201
    usuario_id = response_cadastro.json()["_id"]

    # Faz login para obter o token
    credentials = gerar_credenciais_login(
        payload["email"], payload["password"])
    response_login = login_client.fazer_login(credentials)
    assert response_login.status_code == 200
    token = response_login.json()["authorization"]

    yield token

    # Limpeza: remove o usuário comum criado para este teste
    usuarios_client.excluir_usuario(usuario_id)


# ─────────────────────────────────────────────
# Fixtures de produtos
# ─────────────────────────────────────────────

@pytest.fixture
def produto_payload():
    """
    Fixture que retorna um payload válido para cadastro de produto.
    Cada chamada gera um nome único com uuid4, evitando conflito de nome duplicado.
    """
    return gerar_produto_valido()


@pytest.fixture
def produto_criado(produtos_client, token_admin):
    """
    Cria um produto antes do teste (usando token de admin) e o remove depois.

    Essa fixture é útil para testes que precisam de um produto já existente,
    como buscar por ID, atualizar e excluir.
    """
    payload = gerar_produto_valido()

    response = produtos_client.cadastrar_produto(payload, token=token_admin)
    assert response.status_code == 201

    produto_id = response.json()["_id"]

    yield {
        "id": produto_id,
        "payload": payload
    }

    # Limpeza pós-teste. Se o próprio teste já excluiu o produto,
    # a chamada pode retornar 200 (nenhum registro excluído) sem problemas.
    produtos_client.excluir_produto(produto_id, token=token_admin)
