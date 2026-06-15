import requests


class CarrinhosClient:
    """
    Cliente responsável por centralizar as chamadas HTTP
    relacionadas ao endpoint /carrinhos da ServeRest.

    Todos os métodos que modificam estado (POST, DELETE) exigem token Bearer.
    A listagem (GET) e a busca por ID (GET /{id}) não requerem autenticação.
    """

    def __init__(self, base_url):
        self.base_url = base_url
        self.endpoint = f"{self.base_url}/carrinhos"

    def listar_carrinhos(self):
        """
        Realiza uma requisição GET para listar todos os carrinhos.
        Não requer autenticação.
        """
        return requests.get(self.endpoint)

    def criar_carrinho(self, payload, token=None):
        """
        Realiza uma requisição POST para criar um novo carrinho.

        Requer token de usuário autenticado (admin ou comum).
        Cada usuário pode ter no máximo 1 carrinho aberto.
        Caso token não seja informado, a requisição é enviada sem
        o cabeçalho Authorization, permitindo testar ausência de autenticação.
        """
        headers = self._montar_headers(token)
        return requests.post(self.endpoint, json=payload, headers=headers)

    def buscar_carrinho_por_id(self, carrinho_id):
        """
        Realiza uma requisição GET para buscar um carrinho específico pelo ID.
        Não requer autenticação.
        """
        return requests.get(f"{self.endpoint}/{carrinho_id}")

    def concluir_compra(self, token=None):
        """
        Realiza uma requisição DELETE para concluir a compra do carrinho do usuário.

        Ao concluir, o carrinho é removido e o estoque dos produtos é decrementado.
        Requer token do usuário dono do carrinho.
        """
        headers = self._montar_headers(token)
        return requests.delete(f"{self.endpoint}/concluir-compra", headers=headers)

    def cancelar_compra(self, token=None):
        """
        Realiza uma requisição DELETE para cancelar a compra do carrinho do usuário.

        Ao cancelar, o carrinho é removido e o estoque dos produtos é reposto.
        Requer token do usuário dono do carrinho.
        """
        headers = self._montar_headers(token)
        return requests.delete(f"{self.endpoint}/cancelar-compra", headers=headers)

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
