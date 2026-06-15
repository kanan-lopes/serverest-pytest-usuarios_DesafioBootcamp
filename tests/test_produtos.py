from uuid import uuid4

import pytest

from utils.data_factory import gerar_produto_valido


# ─────────────────────────────────────────────
# GET /produtos
# ─────────────────────────────────────────────

@pytest.mark.produtos
def test_deve_listar_produtos_sem_autenticacao(produtos_client):
    """
    Objetivo:
    Validar que o endpoint GET /produtos retorna a listagem de produtos com sucesso,
    sem necessidade de autenticação.

    Critérios verificados:
    - Status code 200.
    - Resposta possui o campo 'quantidade'.
    - Resposta possui o campo 'produtos'.
    - O campo 'produtos' é uma lista.
    """
    response = produtos_client.listar_produtos()
    body = response.json()

    assert response.status_code == 200
    assert "quantidade" in body
    assert "produtos" in body
    assert isinstance(body["produtos"], list)


# ─────────────────────────────────────────────
# POST /produtos
# ─────────────────────────────────────────────

@pytest.mark.produtos
def test_deve_cadastrar_produto_com_token_admin(produtos_client, produto_payload, token_admin):
    """
    Objetivo:
    Validar que a API permite cadastrar um produto quando o token de administrador
    é fornecido corretamente.

    Pré-condição:
    - A fixture token_admin cria um usuário admin dinamicamente e retorna o token Bearer.
    - A fixture produto_payload gera um payload com nome único via uuid4.

    Critérios verificados:
    - Status code 201.
    - Mensagem de sucesso no body.
    - Campo '_id' presente na resposta.

    Limpeza:
    - O produto criado é excluído ao final para manter o teste independente.
    """
    response = produtos_client.cadastrar_produto(
        produto_payload, token=token_admin)
    body = response.json()

    assert response.status_code == 201
    assert body["message"] == "Cadastro realizado com sucesso"
    assert "_id" in body

    # Limpeza: remove o produto criado para manter isolamento entre testes.
    produtos_client.excluir_produto(body["_id"], token=token_admin)


@pytest.mark.produtos
def test_nao_deve_cadastrar_produto_sem_autenticacao(produtos_client, produto_payload):
    """
    Objetivo:
    Validar que a API rejeita o cadastro de produto quando nenhum token é enviado.

    Critérios verificados:
    - Status code 401.
    - Mensagem de erro indicando ausência de token.
    """
    # Nenhum token é passado → requisição sem cabeçalho Authorization
    response = produtos_client.cadastrar_produto(produto_payload, token=None)
    body = response.json()

    assert response.status_code == 401
    assert body["message"] == "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"


@pytest.mark.produtos
def test_nao_deve_cadastrar_produto_com_token_de_usuario_comum(
    produtos_client, produto_payload, token_usuario_comum
):
    """
    Objetivo:
    Validar que a API rejeita o cadastro de produto quando o token pertence a
    um usuário não-administrador.

    Pré-condição:
    - A fixture token_usuario_comum cria um usuário com administrador="false" e retorna o token.

    Critérios verificados:
    - Status code 403.
    - Mensagem de erro indicando falta de permissão de administrador.
    """
    response = produtos_client.cadastrar_produto(
        produto_payload, token=token_usuario_comum)
    body = response.json()

    assert response.status_code == 403
    assert body["message"] == "Rota exclusiva para administradores"


@pytest.mark.produtos
def test_nao_deve_cadastrar_produto_com_nome_duplicado(produtos_client, token_admin):
    """
    Objetivo:
    Validar que a API não permite cadastrar dois produtos com o mesmo nome.

    Fluxo:
    1. Cadastra um produto com nome único.
    2. Tenta cadastrar outro produto com o mesmo nome.
    3. Verifica que a API retorna erro de nome já cadastrado.

    Critérios verificados:
    - Primeiro cadastro retorna status code 201.
    - Segundo cadastro retorna status code 400.
    - Mensagem de erro indica que o nome já está em uso.

    Limpeza:
    - O produto do primeiro cadastro é excluído ao final.
    """
    payload = gerar_produto_valido()

    # Primeiro cadastro deve ter sucesso
    primeiro = produtos_client.cadastrar_produto(payload, token=token_admin)
    body_primeiro = primeiro.json()
    assert primeiro.status_code == 201
    produto_id = body_primeiro["_id"]

    # Segundo cadastro com o mesmo nome deve falhar
    segundo = produtos_client.cadastrar_produto(payload, token=token_admin)
    body_segundo = segundo.json()

    assert segundo.status_code == 400
    assert body_segundo["message"] == "Já existe produto com esse nome"

    # Limpeza
    produtos_client.excluir_produto(produto_id, token=token_admin)


@pytest.mark.produtos
def test_nao_deve_cadastrar_produto_sem_nome(produtos_client, token_admin):
    """
    Objetivo:
    Validar que a API rejeita o cadastro quando o campo obrigatório 'nome' não é enviado.

    Critérios verificados:
    - Status code 400.
    - Campo 'nome' presente na resposta de erro, indicando qual campo está faltando.
    """
    payload = gerar_produto_valido()
    payload.pop("nome")

    response = produtos_client.cadastrar_produto(payload, token=token_admin)
    body = response.json()

    assert response.status_code == 400
    assert "nome" in body


@pytest.mark.produtos
def test_nao_deve_cadastrar_produto_sem_preco(produtos_client, token_admin):
    """
    Objetivo:
    Validar que a API rejeita o cadastro quando o campo obrigatório 'preco' não é enviado.

    Critérios verificados:
    - Status code 400.
    - Campo 'preco' presente na resposta de erro, indicando qual campo está faltando.
    """
    payload = gerar_produto_valido()
    payload.pop("preco")

    response = produtos_client.cadastrar_produto(payload, token=token_admin)
    body = response.json()

    assert response.status_code == 400
    assert "preco" in body


@pytest.mark.produtos
def test_nao_deve_cadastrar_produto_sem_descricao(produtos_client, token_admin):
    """
    Objetivo:
    Validar que a API rejeita o cadastro quando o campo obrigatório 'descricao' não é enviado.

    Critérios verificados:
    - Status code 400.
    - Campo 'descricao' presente na resposta de erro, indicando qual campo está faltando.
    """
    payload = gerar_produto_valido()
    payload.pop("descricao")

    response = produtos_client.cadastrar_produto(payload, token=token_admin)
    body = response.json()

    assert response.status_code == 400
    assert "descricao" in body


@pytest.mark.produtos
def test_nao_deve_cadastrar_produto_sem_quantidade(produtos_client, token_admin):
    """
    Objetivo:
    Validar que a API rejeita o cadastro quando o campo obrigatório 'quantidade' não é enviado.

    Critérios verificados:
    - Status code 400.
    - Campo 'quantidade' presente na resposta de erro, indicando qual campo está faltando.
    """
    payload = gerar_produto_valido()
    payload.pop("quantidade")

    response = produtos_client.cadastrar_produto(payload, token=token_admin)
    body = response.json()

    assert response.status_code == 400
    assert "quantidade" in body


# ─────────────────────────────────────────────
# GET /produtos/{id}
# ─────────────────────────────────────────────

@pytest.mark.produtos
def test_deve_buscar_produto_por_id_valido(produtos_client, produto_criado):
    """
    Objetivo:
    Validar que a API retorna os dados corretos ao buscar um produto pelo ID.

    Pré-condição:
    - A fixture produto_criado cria um produto via POST e o remove após o teste.

    Critérios verificados:
    - Status code 200.
    - O '_id' retornado corresponde ao ID buscado.
    - Os campos 'nome', 'preco', 'descricao' e 'quantidade' correspondem ao payload original.
    """
    produto_id = produto_criado["id"]
    payload_original = produto_criado["payload"]

    response = produtos_client.buscar_produto_por_id(produto_id)
    body = response.json()

    assert response.status_code == 200
    assert body["_id"] == produto_id
    assert body["nome"] == payload_original["nome"]
    assert body["preco"] == payload_original["preco"]
    assert body["descricao"] == payload_original["descricao"]
    assert body["quantidade"] == payload_original["quantidade"]


@pytest.mark.produtos
def test_nao_deve_buscar_produto_com_id_inexistente(produtos_client):
    """
    Objetivo:
    Validar que a API retorna erro ao buscar um produto com ID que não existe na base.

    Critérios verificados:
    - Status code 400.
    - Mensagem de erro indicando que o produto não foi encontrado.
    """
    produto_id_inexistente = uuid4().hex[:16]

    response = produtos_client.buscar_produto_por_id(produto_id_inexistente)
    body = response.json()

    assert response.status_code == 400
    assert body["message"] == "Produto não encontrado"


# ─────────────────────────────────────────────
# PUT /produtos/{id}
# ─────────────────────────────────────────────

@pytest.mark.produtos
def test_deve_atualizar_produto_com_token_admin(produtos_client, produto_criado, token_admin):
    """
    Objetivo:
    Validar que a API permite atualizar um produto existente com token de administrador.

    Fluxo:
    1. A fixture produto_criado cria um produto existente.
    2. Um novo payload é gerado com nome único para substituir os dados anteriores.
    3. O PUT é feito com o token de admin.
    4. Um GET é feito para confirmar que os dados foram alterados na base.

    Critérios verificados:
    - Status code 200 no PUT.
    - Mensagem de sucesso no body do PUT.
    - Os dados retornados pelo GET subsequente correspondem ao payload atualizado.
    """
    produto_id = produto_criado["id"]
    payload_atualizado = gerar_produto_valido()
    payload_atualizado["preco"] = 999
    payload_atualizado["quantidade"] = 10

    response = produtos_client.atualizar_produto(
        produto_id, payload_atualizado, token=token_admin)
    body = response.json()

    assert response.status_code == 200
    assert body["message"] == "Registro alterado com sucesso"

    # Confirma que os dados foram persistidos corretamente
    busca = produtos_client.buscar_produto_por_id(produto_id)
    body_busca = busca.json()

    assert busca.status_code == 200
    assert body_busca["_id"] == produto_id
    assert body_busca["nome"] == payload_atualizado["nome"]
    assert body_busca["preco"] == payload_atualizado["preco"]
    assert body_busca["descricao"] == payload_atualizado["descricao"]
    assert body_busca["quantidade"] == payload_atualizado["quantidade"]


@pytest.mark.produtos
def test_nao_deve_atualizar_produto_sem_autenticacao(produtos_client, produto_criado):
    """
    Objetivo:
    Validar que a API rejeita a atualização de produto quando nenhum token é enviado.

    Critérios verificados:
    - Status code 401.
    - Mensagem de erro indicando ausência de token.
    """
    produto_id = produto_criado["id"]
    payload_atualizado = gerar_produto_valido()

    response = produtos_client.atualizar_produto(
        produto_id, payload_atualizado, token=None)
    body = response.json()

    assert response.status_code == 401
    assert body["message"] == "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"


@pytest.mark.produtos
def test_nao_deve_atualizar_produto_com_token_de_usuario_comum(
    produtos_client, produto_criado, token_usuario_comum
):
    """
    Objetivo:
    Validar que a API rejeita a atualização de produto quando o token pertence a
    um usuário não-administrador.

    Critérios verificados:
    - Status code 403.
    - Mensagem de erro indicando falta de permissão de administrador.
    """
    produto_id = produto_criado["id"]
    payload_atualizado = gerar_produto_valido()

    response = produtos_client.atualizar_produto(
        produto_id, payload_atualizado, token=token_usuario_comum)
    body = response.json()

    assert response.status_code == 403
    assert body["message"] == "Rota exclusiva para administradores"


# ─────────────────────────────────────────────
# DELETE /produtos/{id}
# ─────────────────────────────────────────────

@pytest.mark.produtos
def test_deve_excluir_produto_com_token_admin(produtos_client, produto_criado, token_admin):
    """
    Objetivo:
    Validar que a API permite excluir um produto existente com token de administrador.

    Fluxo:
    1. A fixture produto_criado cria um produto existente.
    2. O DELETE é feito com token de admin.
    3. Um GET subsequente confirma que o produto não existe mais.

    Critérios verificados:
    - Status code 200 no DELETE.
    - Mensagem de sucesso no body.
    - GET subsequente retorna status 400 com mensagem de produto não encontrado.

    Observação:
    - Como o teste já exclui o produto, a limpeza da fixture produto_criado
      tentará excluir novamente, o que é seguro (retornará "Nenhum registro excluído").
    """
    produto_id = produto_criado["id"]

    response = produtos_client.excluir_produto(produto_id, token=token_admin)
    body = response.json()

    assert response.status_code == 200
    assert body["message"] == "Registro excluído com sucesso"

    # Confirma que o produto foi removido da base
    busca = produtos_client.buscar_produto_por_id(produto_id)
    body_busca = busca.json()

    assert busca.status_code == 400
    assert body_busca["message"] == "Produto não encontrado"


@pytest.mark.produtos
def test_nao_deve_excluir_produto_sem_autenticacao(produtos_client, produto_criado):
    """
    Objetivo:
    Validar que a API rejeita a exclusão de produto quando nenhum token é enviado.

    Critérios verificados:
    - Status code 401.
    - Mensagem de erro indicando ausência de token.
    """
    produto_id = produto_criado["id"]

    response = produtos_client.excluir_produto(produto_id, token=None)
    body = response.json()

    assert response.status_code == 401
    assert body["message"] == "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"


@pytest.mark.produtos
def test_deve_retornar_mensagem_ao_excluir_produto_inexistente(produtos_client, token_admin):
    """
    Objetivo:
    Validar o comportamento da API ao tentar excluir um produto com ID que não existe na base.

    Observação sobre formato do ID:
    A ServeRest valida que o ID tenha exatamente 16 caracteres alfanuméricos antes de
    realizar a busca. IDs em formato inválido retornam 400 com erro de validação,
    e não chegam a consultar a base. Por isso usamos uuid4().hex[:16], que garante
    um ID no formato válido mas com probabilidade astronomicamente baixa de
    coincidir com um ID real.

    Observação sobre comportamento:
    Assim como em /usuarios, excluir um produto por ID válido mas inexistente
    retorna 200 informando que nenhum registro foi excluído — em vez de 404.

    Critérios verificados:
    - Status code 200.
    - Mensagem informando que nenhum registro foi excluído.
    """
    produto_id_inexistente = uuid4().hex[:16]

    response = produtos_client.excluir_produto(
        produto_id_inexistente, token=token_admin)
    body = response.json()

    assert response.status_code == 200
    assert body["message"] == "Nenhum registro excluído"
