from uuid import uuid4

import pytest

from utils.data_factory import gerar_carrinho_valido


# ─────────────────────────────────────────────
# GET /carrinhos
# ─────────────────────────────────────────────

@pytest.mark.carrinhos
def test_deve_listar_carrinhos_sem_autenticacao(carrinhos_client):
    """
    Objetivo:
    Validar que o endpoint GET /carrinhos retorna a listagem de carrinhos
    com sucesso, sem necessidade de autenticação.

    Critérios verificados:
    - Status code 200.
    - Resposta possui o campo 'quantidade'.
    - Resposta possui o campo 'carrinhos'.
    - O campo 'carrinhos' é uma lista.
    """
    response = carrinhos_client.listar_carrinhos()
    body = response.json()

    assert response.status_code == 200
    assert "quantidade" in body
    assert "carrinhos" in body
    assert isinstance(body["carrinhos"], list)


# ─────────────────────────────────────────────
# POST /carrinhos
# ─────────────────────────────────────────────

@pytest.mark.carrinhos
def test_deve_criar_carrinho_com_produto_valido(carrinhos_client, usuario_com_token_e_produto):
    """
    Objetivo:
    Validar que a API permite criar um carrinho com um produto válido e token de usuário.

    Pré-condição:
    - A fixture usuario_com_token_e_produto cria dinamicamente um usuário autenticado
      e um produto disponível no estoque.

    Critérios verificados:
    - Status code 201.
    - Mensagem de sucesso no body.
    - Campo '_id' presente na resposta.

    Limpeza:
    - O carrinho é cancelado ao final para repor o estoque e remover o carrinho.
    """
    token = usuario_com_token_e_produto["token"]
    produto_id = usuario_com_token_e_produto["produto_id"]

    payload = gerar_carrinho_valido(produto_id, quantidade=2)
    response = carrinhos_client.criar_carrinho(payload, token=token)
    body = response.json()

    assert response.status_code == 201
    assert body["message"] == "Cadastro realizado com sucesso"
    assert "_id" in body

    # Limpeza: cancela para repor estoque e remover o carrinho.
    carrinhos_client.cancelar_compra(token=token)


@pytest.mark.carrinhos
def test_nao_deve_criar_carrinho_sem_autenticacao(carrinhos_client, usuario_com_token_e_produto):
    """
    Objetivo:
    Validar que a API rejeita a criação de carrinho quando nenhum token é enviado.

    Critérios verificados:
    - Status code 401.
    - Mensagem de erro indicando ausência de token.
    """
    produto_id = usuario_com_token_e_produto["produto_id"]
    payload = gerar_carrinho_valido(produto_id, quantidade=1)

    # Nenhum token → requisição sem cabeçalho Authorization
    response = carrinhos_client.criar_carrinho(payload, token=None)
    body = response.json()

    assert response.status_code == 401
    assert body["message"] == "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"


@pytest.mark.carrinhos
def test_nao_deve_criar_segundo_carrinho_para_mesmo_usuario(
    carrinhos_client, usuario_com_token_e_produto
):
    """
    Objetivo:
    Validar a regra de negócio que impede um usuário de ter mais de 1 carrinho aberto.

    Fluxo:
    1. Cria o primeiro carrinho para o usuário.
    2. Tenta criar um segundo carrinho para o mesmo usuário.
    3. Verifica que a API retorna erro.

    Critérios verificados:
    - Primeiro POST retorna status 201.
    - Segundo POST retorna status 400.
    - Mensagem de erro indica que não é permitido mais de 1 carrinho.

    Limpeza:
    - O primeiro carrinho é cancelado ao final.
    """
    token = usuario_com_token_e_produto["token"]
    produto_id = usuario_com_token_e_produto["produto_id"]

    payload = gerar_carrinho_valido(produto_id, quantidade=1)

    # Primeiro carrinho deve ser criado com sucesso
    primeiro = carrinhos_client.criar_carrinho(payload, token=token)
    assert primeiro.status_code == 201

    # Segundo carrinho para o mesmo usuário deve falhar
    segundo = carrinhos_client.criar_carrinho(payload, token=token)
    body_segundo = segundo.json()

    assert segundo.status_code == 400
    assert body_segundo["message"] == "Não é permitido ter mais de 1 carrinho"

    # Limpeza
    carrinhos_client.cancelar_compra(token=token)


@pytest.mark.carrinhos
def test_nao_deve_criar_carrinho_com_produto_inexistente(
    carrinhos_client, usuario_com_token_e_produto
):
    """
    Objetivo:
    Validar que a API rejeita a criação de carrinho quando o produto informado não existe.

    Critérios verificados:
    - Status code 400.
    - Mensagem de erro indicando que o produto não foi encontrado.
    """
    token = usuario_com_token_e_produto["token"]

    # ID no formato válido (16 chars hex) mas inexistente na base
    produto_id_inexistente = uuid4().hex[:16]
    payload = gerar_carrinho_valido(produto_id_inexistente, quantidade=1)

    response = carrinhos_client.criar_carrinho(payload, token=token)
    body = response.json()

    assert response.status_code == 400
    assert body["message"] == "Produto não encontrado"


@pytest.mark.carrinhos
def test_nao_deve_criar_carrinho_com_quantidade_maior_que_estoque(
    carrinhos_client, usuario_com_token_e_produto
):
    """
    Objetivo:
    Validar que a API rejeita a criação de carrinho quando a quantidade solicitada
    é maior que o estoque disponível do produto.

    Pré-condição:
    - O produto criado pela fixture tem estoque de 50 unidades.
    - A requisição solicita mais do que o estoque disponível.

    Critérios verificados:
    - Status code 400.
    - Mensagem de erro indica estoque insuficiente.
    """
    token = usuario_com_token_e_produto["token"]
    produto_id = usuario_com_token_e_produto["produto_id"]
    estoque = usuario_com_token_e_produto["produto_quantidade_estoque"]

    quantidade_acima_do_estoque = estoque + 9999
    payload = gerar_carrinho_valido(
        produto_id, quantidade=quantidade_acima_do_estoque)

    response = carrinhos_client.criar_carrinho(payload, token=token)
    body = response.json()

    assert response.status_code == 400
    assert body["message"] == "Produto não possui quantidade suficiente"


# ─────────────────────────────────────────────
# GET /carrinhos/{id}
# ─────────────────────────────────────────────

@pytest.mark.carrinhos
def test_deve_buscar_carrinho_por_id_valido(carrinhos_client, carrinho_criado):
    """
    Objetivo:
    Validar que a API retorna os dados corretos ao buscar um carrinho pelo ID.

    Pré-condição:
    - A fixture carrinho_criado cria um carrinho com produto e o cancela após o teste.

    Critérios verificados:
    - Status code 200.
    - O '_id' retornado corresponde ao ID buscado.
    - Campos obrigatórios do carrinho presentes: 'produtos', 'precoTotal',
      'quantidadeTotal', 'idUsuario'.
    - O produto adicionado está na lista de produtos do carrinho.
    """
    carrinho_id = carrinho_criado["carrinho_id"]
    produto_id = carrinho_criado["produto_id"]

    response = carrinhos_client.buscar_carrinho_por_id(carrinho_id)
    body = response.json()

    assert response.status_code == 200
    assert body["_id"] == carrinho_id
    assert "produtos" in body
    assert "precoTotal" in body
    assert "quantidadeTotal" in body
    assert "idUsuario" in body

    # Verifica que o produto adicionado está presente no carrinho
    ids_no_carrinho = [p["idProduto"] for p in body["produtos"]]
    assert produto_id in ids_no_carrinho


@pytest.mark.carrinhos
def test_nao_deve_buscar_carrinho_com_id_inexistente(carrinhos_client):
    """
    Objetivo:
    Validar que a API retorna erro ao buscar um carrinho com ID que não existe na base.

    Critérios verificados:
    - Status code 400.
    - Mensagem de erro indicando que o carrinho não foi encontrado.
    """
    carrinho_id_inexistente = uuid4().hex[:16]

    response = carrinhos_client.buscar_carrinho_por_id(carrinho_id_inexistente)
    body = response.json()

    assert response.status_code == 400
    assert body["message"] == "Carrinho não encontrado"


# ─────────────────────────────────────────────
# DELETE /carrinhos/concluir-compra
# ─────────────────────────────────────────────

@pytest.mark.carrinhos
def test_deve_concluir_compra_e_decrementar_estoque(
    carrinhos_client, produtos_client, carrinho_criado
):
    """
    Objetivo:
    Validar que ao concluir a compra o carrinho é removido e o estoque dos produtos
    é decrementado corretamente.

    Fluxo:
    1. A fixture carrinho_criado captura o estoque original do produto e depois
       cria um carrinho com 2 unidades — o estoque já decrementou ao abrir o carrinho.
    2. A compra é concluída via DELETE /carrinhos/concluir-compra.
    3. O produto é buscado para confirmar que o estoque final reflete o decremento.

    Critérios verificados:
    - Status code 200 no DELETE.
    - Mensagem de sucesso indicando que o registro foi excluído.
    - O estoque final é igual ao estoque original menos a quantidade do carrinho.

    Observação:
    - Como o teste já conclui a compra, a limpeza da fixture carrinho_criado
      tentará cancelar uma compra inexistente, o que é seguro (retorna 200
      com "Não foi encontrado carrinho para esse usuário").
    """
    token = carrinho_criado["token"]
    produto_id = carrinho_criado["produto_id"]
    quantidade_no_carrinho = carrinho_criado["quantidade_no_carrinho"]
    estoque_original = carrinho_criado["estoque_original"]

    # Conclui a compra
    response = carrinhos_client.concluir_compra(token=token)
    body = response.json()

    assert response.status_code == 200
    assert body["message"] == "Registro excluído com sucesso"

    # Verifica que o estoque final = estoque original - quantidade do carrinho
    estoque_depois = produtos_client.buscar_produto_por_id(produto_id).json()[
        "quantidade"]
    assert estoque_depois == estoque_original - quantidade_no_carrinho


@pytest.mark.carrinhos
def test_deve_retornar_mensagem_ao_concluir_compra_sem_carrinho(
    carrinhos_client, usuario_com_token_e_produto
):
    """
    Objetivo:
    Validar o comportamento da API ao tentar concluir a compra quando o usuário
    não possui carrinho aberto.

    Critérios verificados:
    - Status code 200.
    - Mensagem informando que não foi encontrado carrinho para o usuário.
    """
    token = usuario_com_token_e_produto["token"]

    response = carrinhos_client.concluir_compra(token=token)
    body = response.json()

    assert response.status_code == 200
    assert body["message"] == "Não foi encontrado carrinho para esse usuário"


@pytest.mark.carrinhos
def test_nao_deve_concluir_compra_sem_autenticacao(carrinhos_client):
    """
    Objetivo:
    Validar que a API rejeita a conclusão de compra quando nenhum token é enviado.

    Critérios verificados:
    - Status code 401.
    - Mensagem de erro indicando ausência de token.
    """
    response = carrinhos_client.concluir_compra(token=None)
    body = response.json()

    assert response.status_code == 401
    assert body["message"] == "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"


# ─────────────────────────────────────────────
# DELETE /carrinhos/cancelar-compra
# ─────────────────────────────────────────────

@pytest.mark.carrinhos
def test_deve_cancelar_compra_e_repor_estoque(
    carrinhos_client, produtos_client, carrinho_criado
):
    """
    Objetivo:
    Validar que ao cancelar a compra o carrinho é removido e o estoque dos produtos
    é reposto corretamente (reabastecido).

    Fluxo:
    1. A fixture carrinho_criado captura o estoque original e cria um carrinho com
       2 unidades — o estoque já está decrementado ao início do teste.
    2. A compra é cancelada via DELETE /carrinhos/cancelar-compra.
    3. O produto é buscado para verificar se o estoque voltou ao valor original.

    Critérios verificados:
    - Status code 200 no DELETE.
    - Mensagem de sucesso informando que o estoque foi reabastecido.
    - O estoque final volta ao valor original antes do carrinho ser criado.

    Observação:
    - Como o teste já cancela a compra, a limpeza da fixture carrinho_criado
      tentará cancelar novamente, o que é seguro (retorna 200 com
      "Não foi encontrado carrinho para esse usuário").
    """
    token = carrinho_criado["token"]
    produto_id = carrinho_criado["produto_id"]
    estoque_original = carrinho_criado["estoque_original"]

    # Cancela a compra
    response = carrinhos_client.cancelar_compra(token=token)
    body = response.json()

    assert response.status_code == 200
    assert body["message"] == "Registro excluído com sucesso. Estoque dos produtos reabastecido"

    # Verifica que o estoque voltou ao valor original
    estoque_depois = produtos_client.buscar_produto_por_id(produto_id).json()[
        "quantidade"]
    assert estoque_depois == estoque_original


@pytest.mark.carrinhos
def test_deve_retornar_mensagem_ao_cancelar_compra_sem_carrinho(
    carrinhos_client, usuario_com_token_e_produto
):
    """
    Objetivo:
    Validar o comportamento da API ao tentar cancelar a compra quando o usuário
    não possui carrinho aberto.

    Critérios verificados:
    - Status code 200.
    - Mensagem informando que não foi encontrado carrinho para o usuário.
    """
    token = usuario_com_token_e_produto["token"]

    response = carrinhos_client.cancelar_compra(token=token)
    body = response.json()

    assert response.status_code == 200
    assert body["message"] == "Não foi encontrado carrinho para esse usuário"


@pytest.mark.carrinhos
def test_nao_deve_cancelar_compra_sem_autenticacao(carrinhos_client):
    """
    Objetivo:
    Validar que a API rejeita o cancelamento de compra quando nenhum token é enviado.

    Critérios verificados:
    - Status code 401.
    - Mensagem de erro indicando ausência de token.
    """
    response = carrinhos_client.cancelar_compra(token=None)
    body = response.json()

    assert response.status_code == 401
    assert body["message"] == "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"
