from uuid import uuid4

import pytest

from utils.data_factory import gerar_usuario_valido


@pytest.mark.usuarios
def test_deve_listar_usuarios_com_sucesso(usuarios_client):
    """
    Objetivo:
    Validar que o endpoint GET /usuarios retorna a listagem de usuários com sucesso.

    Critérios verificados:
    - Status code 200.
    - Resposta possui o campo 'quantidade'.
    - Resposta possui o campo 'usuarios'.
    - O campo 'usuarios' é uma lista.
    """
    response = usuarios_client.listar_usuarios()
    body = response.json()

    assert response.status_code == 200
    assert "quantidade" in body
    assert "usuarios" in body
    assert isinstance(body["usuarios"], list)


@pytest.mark.usuarios
def test_deve_cadastrar_usuario_valido_com_sucesso(usuarios_client, usuario_payload):
    """
    Objetivo:
    Validar que a API permite cadastrar um usuário com dados válidos.

    Critérios verificados:
    - Status code 201.
    - Mensagem de sucesso.
    - Retorno do campo '_id'.
    """
    response = usuarios_client.cadastrar_usuario(usuario_payload)
    body = response.json()

    assert response.status_code == 201
    assert body["message"] == "Cadastro realizado com sucesso"
    assert "_id" in body

    # Limpeza: remove o usuário criado para manter o teste independente.
    usuarios_client.excluir_usuario(body["_id"])


@pytest.mark.usuarios
def test_nao_deve_cadastrar_usuario_com_email_duplicado(usuarios_client, usuario_payload):
    """
    Objetivo:
    Validar que a API não permite cadastrar dois usuários com o mesmo email.

    Fluxo:
    1. Cadastra um usuário com email único.
    2. Tenta cadastrar outro usuário usando o mesmo payload.
    3. Verifica que a API retorna erro de email já utilizado.
    """
    primeiro_cadastro = usuarios_client.cadastrar_usuario(usuario_payload)
    body_primeiro_cadastro = primeiro_cadastro.json()

    assert primeiro_cadastro.status_code == 201
    assert "_id" in body_primeiro_cadastro

    usuario_id = body_primeiro_cadastro["_id"]

    segundo_cadastro = usuarios_client.cadastrar_usuario(usuario_payload)
    body_segundo_cadastro = segundo_cadastro.json()

    assert segundo_cadastro.status_code == 400
    assert body_segundo_cadastro["message"] == "Este email já está sendo usado"

    # Limpeza do usuário criado no primeiro cadastro.
    usuarios_client.excluir_usuario(usuario_id)


@pytest.mark.usuarios
def test_nao_deve_cadastrar_usuario_sem_nome(usuarios_client):
    """
    Objetivo:
    Validar que a API rejeita o cadastro quando o campo obrigatório 'nome' não é enviado.
    """
    payload = gerar_usuario_valido()
    payload.pop("nome")

    response = usuarios_client.cadastrar_usuario(payload)
    body = response.json()

    assert response.status_code == 400
    assert "nome" in body


@pytest.mark.usuarios
def test_nao_deve_cadastrar_usuario_sem_email(usuarios_client):
    """
    Objetivo:
    Validar que a API rejeita o cadastro quando o campo obrigatório 'email' não é enviado.
    """
    payload = gerar_usuario_valido()
    payload.pop("email")

    response = usuarios_client.cadastrar_usuario(payload)
    body = response.json()

    assert response.status_code == 400
    assert "email" in body


@pytest.mark.usuarios
def test_nao_deve_cadastrar_usuario_sem_password(usuarios_client):
    """
    Objetivo:
    Validar que a API rejeita o cadastro quando o campo obrigatório 'password' não é enviado.
    """
    payload = gerar_usuario_valido()
    payload.pop("password")

    response = usuarios_client.cadastrar_usuario(payload)
    body = response.json()

    assert response.status_code == 400
    assert "password" in body


@pytest.mark.usuarios
def test_nao_deve_cadastrar_usuario_sem_administrador(usuarios_client):
    """
    Objetivo:
    Validar que a API rejeita o cadastro quando o campo obrigatório 'administrador' não é enviado.
    """
    payload = gerar_usuario_valido()
    payload.pop("administrador")

    response = usuarios_client.cadastrar_usuario(payload)
    body = response.json()

    assert response.status_code == 400
    assert "administrador" in body


@pytest.mark.usuarios
def test_deve_buscar_usuario_por_id_valido(usuarios_client, usuario_criado):
    """
    Objetivo:
    Validar que a API permite buscar um usuário existente pelo seu ID.

    Pré-condição:
    - Um usuário é criado pela fixture usuario_criado.

    Critérios verificados:
    - Status code 200.
    - ID retornado corresponde ao ID buscado.
    - Dados principais do usuário correspondem aos dados cadastrados.
    """
    usuario_id = usuario_criado["id"]
    payload_original = usuario_criado["payload"]

    response = usuarios_client.buscar_usuario_por_id(usuario_id)
    body = response.json()

    assert response.status_code == 200
    assert body["_id"] == usuario_id
    assert body["nome"] == payload_original["nome"]
    assert body["email"] == payload_original["email"]
    assert body["password"] == payload_original["password"]
    assert body["administrador"] == payload_original["administrador"]


@pytest.mark.usuarios
def test_nao_deve_buscar_usuario_com_id_inexistente(usuarios_client):
    """
    Objetivo:
    Validar que a API retorna erro ao buscar um usuário com ID inexistente.
    """
    usuario_id_inexistente = uuid4().hex[:16]

    response = usuarios_client.buscar_usuario_por_id(usuario_id_inexistente)
    body = response.json()

    #print(response.status_code)
    #print(body)

    assert response.status_code == 400
    assert body["message"] == "Usuário não encontrado"


@pytest.mark.usuarios
def test_deve_atualizar_usuario_existente_com_sucesso(usuarios_client, usuario_criado):
    """
    Objetivo:
    Validar que a API permite atualizar um usuário existente.

    Fluxo:
    1. Cria um usuário pela fixture usuario_criado.
    2. Atualiza os dados desse usuário.
    3. Busca o usuário novamente.
    4. Confirma que os dados foram alterados.
    """
    usuario_id = usuario_criado["id"]

    #print("ID criado:", usuario_id)

    busca_antes = usuarios_client.buscar_usuario_por_id(usuario_id)
    #print("GET antes do PUT:", busca_antes.status_code, busca_antes.json())

    payload_atualizado = gerar_usuario_valido()
    payload_atualizado["nome"] = "Usuario Atualizado Pytest"

    response = usuarios_client.atualizar_usuario(usuario_id, payload_atualizado)
    body = response.json()
    #print("PUT:", response.status_code, body)

    assert response.status_code == 200
    assert body["message"] == "Registro alterado com sucesso"

    busca_usuario_atualizado = usuarios_client.buscar_usuario_por_id(usuario_id)
    #print("GET depois do PUT:", busca_usuario_atualizado.status_code, busca_usuario_atualizado.json())
    body_busca = busca_usuario_atualizado.json()

    assert busca_usuario_atualizado.status_code == 200
    assert body_busca["_id"] == usuario_id
    assert body_busca["nome"] == payload_atualizado["nome"]
    assert body_busca["email"] == payload_atualizado["email"]
    assert body_busca["password"] == payload_atualizado["password"]
    assert body_busca["administrador"] == payload_atualizado["administrador"]


@pytest.mark.usuarios
def test_deve_excluir_usuario_existente_com_sucesso(usuarios_client, usuario_criado):
    """
    Objetivo:
    Validar que a API permite excluir um usuário existente.

    Fluxo:
    1. Cria um usuário pela fixture usuario_criado.
    2. Exclui o usuário.
    3. Tenta buscar o usuário excluído.
    4. Confirma que ele não existe mais.
    """
    usuario_id = usuario_criado["id"]

    response = usuarios_client.excluir_usuario(usuario_id)
    body = response.json()

    assert response.status_code == 200
    assert body["message"] == "Registro excluído com sucesso"

    busca_usuario_excluido = usuarios_client.buscar_usuario_por_id(usuario_id)
    body_busca = busca_usuario_excluido.json()

    assert busca_usuario_excluido.status_code == 400
    assert body_busca["message"] == "Usuário não encontrado"


@pytest.mark.usuarios
def test_deve_retornar_mensagem_ao_excluir_usuario_inexistente(usuarios_client):
    """
    Objetivo:
    Validar o comportamento da API ao tentar excluir um usuário que não existe.

    Esse cenário é importante porque nem toda exclusão inexistente retorna erro.
    Na ServeRest, a API responde com sucesso, mas informa que nenhum registro foi excluído.
    """
    usuario_id_inexistente = f"id_inexistente_{uuid4().hex[:8]}"

    response = usuarios_client.excluir_usuario(usuario_id_inexistente)
    body = response.json()

    assert response.status_code == 200
    assert body["message"] == "Nenhum registro excluído"