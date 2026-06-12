import pytest

from utils.data_factory import gerar_credenciais_login


@pytest.mark.login
def test_deve_fazer_login_com_usuario_administrador(login_client, usuario_admin_criado):
    """
    Objetivo:
    Validar que um usuário administrador criado dinamicamente consegue se autenticar com sucesso.

    Pré-condição:
    - A fixture usuario_admin_criado cria um usuário com administrador="true" via /usuarios
      e o remove após o teste.

    Critérios verificados:
    - Status code 200.
    - Mensagem de sucesso no body.
    - Campo 'authorization' presente na resposta.
    - O token retornado é uma string não vazia.
    """
    email = usuario_admin_criado["payload"]["email"]
    password = usuario_admin_criado["payload"]["password"]

    credentials = gerar_credenciais_login(email, password)
    response = login_client.fazer_login(credentials)
    body = response.json()

    assert response.status_code == 200
    assert body["message"] == "Login realizado com sucesso"
    assert "authorization" in body
    assert isinstance(body["authorization"], str)
    assert len(body["authorization"]) > 0


@pytest.mark.login
def test_deve_fazer_login_com_usuario_comum(login_client, usuario_comum_criado):
    """
    Objetivo:
    Validar que um usuário não administrador criado dinamicamente consegue se autenticar com sucesso.

    Pré-condição:
    - A fixture usuario_comum_criado cria um usuário com administrador="false" via /usuarios
      e o remove após o teste.

    Critérios verificados:
    - Status code 200.
    - Campo 'authorization' presente na resposta.
    - O token retornado é uma string não vazia.
    """
    email = usuario_comum_criado["payload"]["email"]
    password = usuario_comum_criado["payload"]["password"]

    credentials = gerar_credenciais_login(email, password)
    response = login_client.fazer_login(credentials)
    body = response.json()

    assert response.status_code == 200
    assert body["message"] == "Login realizado com sucesso"
    assert "authorization" in body
    assert isinstance(body["authorization"], str)
    assert len(body["authorization"]) > 0


@pytest.mark.login
def test_token_retornado_deve_ser_string_nao_vazia(login_client, usuario_admin_criado):
    """
    Objetivo:
    Verificar explicitamente o contrato do campo 'authorization':
    deve ser uma string no formato Bearer <token>.

    Critérios verificados:
    - O valor começa com o prefixo "Bearer ".
    - O conteúdo após o prefixo não é vazio.
    """
    email = usuario_admin_criado["payload"]["email"]
    password = usuario_admin_criado["payload"]["password"]

    credentials = gerar_credenciais_login(email, password)
    response = login_client.fazer_login(credentials)
    body = response.json()

    assert response.status_code == 200

    token = body["authorization"]
    assert token.startswith("Bearer ")
    # Remove o prefixo e verifica que há conteúdo real após ele
    token_value = token.replace("Bearer ", "").strip()
    assert len(token_value) > 0


@pytest.mark.login
def test_nao_deve_fazer_login_com_senha_errada(login_client, usuario_admin_criado):
    """
    Objetivo:
    Validar que a API rejeita a autenticação quando a senha informada está incorreta.

    Fluxo:
    1. Cria um usuário administrador dinamicamente.
    2. Tenta fazer login com o email correto e uma senha diferente da cadastrada.

    Critérios verificados:
    - Status code 401.
    - Mensagem de erro indicando credenciais inválidas.
    """
    email = usuario_admin_criado["payload"]["email"]

    credentials = gerar_credenciais_login(email, "senha_errada_123")
    response = login_client.fazer_login(credentials)
    body = response.json()

    assert response.status_code == 401
    assert body["message"] == "Email e/ou senha inválidos"


@pytest.mark.login
def test_nao_deve_fazer_login_com_email_inexistente(login_client):
    """
    Objetivo:
    Validar que a API rejeita a autenticação quando o email não está cadastrado.

    Critérios verificados:
    - Status code 401.
    - Mensagem de erro indicando credenciais inválidas.
    """
    credentials = gerar_credenciais_login(
        email="email_que_nao_existe_na_base@teste.com",
        password="qualquer_senha"
    )
    response = login_client.fazer_login(credentials)
    body = response.json()

    assert response.status_code == 401
    assert body["message"] == "Email e/ou senha inválidos"


@pytest.mark.login
def test_nao_deve_fazer_login_sem_email(login_client):
    """
    Objetivo:
    Validar que a API rejeita a autenticação quando o campo 'email' não é enviado.

    Critérios verificados:
    - Status code 400.
    - Campo 'email' presente na resposta de erro, indicando qual campo está faltando.
    """
    payload = {"password": "teste123"}

    response = login_client.fazer_login(payload)
    body = response.json()

    assert response.status_code == 400
    assert "email" in body


@pytest.mark.login
def test_nao_deve_fazer_login_sem_password(login_client):
    """
    Objetivo:
    Validar que a API rejeita a autenticação quando o campo 'password' não é enviado.

    Critérios verificados:
    - Status code 400.
    - Campo 'password' presente na resposta de erro, indicando qual campo está faltando.
    """
    payload = {"email": "algum@email.com"}

    response = login_client.fazer_login(payload)
    body = response.json()

    assert response.status_code == 400
    assert "password" in body


@pytest.mark.login
def test_nao_deve_fazer_login_com_body_vazio(login_client):
    """
    Objetivo:
    Validar que a API rejeita a autenticação quando o body enviado está completamente vazio.

    Critérios verificados:
    - Status code 400.
    - Os campos obrigatórios ausentes ('email' e 'password') estão presentes na resposta de erro.
    """
    response = login_client.fazer_login({})
    body = response.json()

    assert response.status_code == 400
    assert "email" in body
    assert "password" in body
