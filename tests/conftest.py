import os
import pytest
from dotenv import load_dotenv

# objeto que contém os métodos pra chamar a API
from clients.usuarios_client import UsuariosClient
# cliente para o endpoint /login
from clients.login_client import LoginClient
from utils.data_factory import gerar_usuario_valido  # função que cria dados válidos

"""
Lembrando que este arquivo é gerado automaticamente pelo pytest, daí podemos usar
def test_alguma_coisa(usuarios_client), sem precisar importar manualmente.
"""

load_dotenv()  # carregando variáveis do arquivo .env


# session -> fixture criada uma vez por execução completa
@pytest.fixture(scope="session")
def base_url():
    """
    Define a URL base da API.
    Caso exista uma variável BASE_URL no ambiente, ela será usada.
    Caso contrário, será usada a URL da Compass informada no projeto.
    """
    return os.getenv("BASE_URL", "https://compassuol.serverest.dev")


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
def usuario_payload():
    """
    Fixture que retorna um payload válido para cadastro de usuário.
    Cada chamada gera um email único, garantindo independência entre testes. Isso é mt importante para
    o código, pois evita o problema de "email já está sendo usado".
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

    response = usuarios_client.cadastrar_usuario(payload)  # cadastro na api
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
    Tudo depois do yield → acontece depois do teste
    """
    # Limpeza pós-teste. Se fosse um return não teríamos a limpeza.
    # Caso o próprio teste já tenha excluído o usuário, essa chamada pode retornar 200 ou 400.
    usuarios_client.excluir_usuario(usuario_id)


@pytest.fixture
def usuario_admin_criado(usuarios_client):
    """
    Cria um usuário administrador antes do teste e o remove depois.

    Útil para testes de login que precisam de um administrador real
    criado dinamicamente, evitando dependência de dados fixos da base.
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

    Útil para testes de login que precisam de um usuário comum criado
    dinamicamente, evitando dependência de dados fixos da base.
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
