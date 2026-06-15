import requests


class ProdutosClient:
    """
    Cliente responsável por centralizar as chamadas HTTP
    relacionadas ao endpoint /produtos da ServeRest.

    Endpoints que exigem autenticação (POST, PUT, DELETE) recebem
    o token Bearer via cabeçalho Authorization.
    """

    def __init__(self, base_url):
        self.base_url = base_url
        self.endpoint = f"{self.base_url}/produtos"

    def listar_produtos(self):
        """
        Realiza uma requisição GET para listar todos os produtos.
        Não requer autenticação.
        """
        return requests.get(self.endpoint)

    def cadastrar_produto(self, payload, token=None):
        """
        Realiza uma requisição POST para cadastrar um novo produto.

        Requer token de administrador. Caso token não seja informado,
        a requisição é enviada sem o cabeçalho Authorization,
        permitindo testar o cenário de ausência de autenticação.
        """
        headers = self._montar_headers(token)
        return requests.post(self.endpoint, json=payload, headers=headers)

    def buscar_produto_por_id(self, produto_id):
        """
        Realiza uma requisição GET para buscar um produto específico pelo ID.
        Não requer autenticação.
        """
        return requests.get(f"{self.endpoint}/{produto_id}")

    def atualizar_produto(self, produto_id, payload, token=None):
        """
        Realiza uma requisição PUT para atualizar um produto pelo ID.

        Requer token de administrador. Caso token não seja informado,
        a requisição é enviada sem o cabeçalho Authorization.
        """
        headers = self._montar_headers(token)
        return requests.put(f"{self.endpoint}/{produto_id}", json=payload, headers=headers)

    def excluir_produto(self, produto_id, token=None):
        """
        Realiza uma requisição DELETE para excluir um produto pelo ID.

        Requer token de administrador. Caso token não seja informado,
        a requisição é enviada sem o cabeçalho Authorization.
        """
        headers = self._montar_headers(token)
        return requests.delete(f"{self.endpoint}/{produto_id}", headers=headers)

    def _montar_headers(self, token):
        """
        Monta o dicionário de cabeçalhos HTTP.

        Caso um token seja fornecido, inclui o cabeçalho Authorization.
        Caso contrário, retorna um dicionário vazio, simulando uma
        requisição não autenticada.
        """
        if token:
            return {"Authorization": token}
        return {}
