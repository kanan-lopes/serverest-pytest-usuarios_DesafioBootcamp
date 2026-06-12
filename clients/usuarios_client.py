import requests


class UsuariosClient:
    """
    Cliente responsável por centralizar as chamadas HTTP
    relacionadas ao endpoint /usuarios da ServeRest.

    Essa separação evita repetir requests.get, requests.post,
    requests.put e requests.delete diretamente em todos os testes.
    """

    def __init__(self, base_url):
        self.base_url = base_url
        self.endpoint = f"{self.base_url}/usuarios"

    def listar_usuarios(self):
        """
        Realiza uma requisição GET para listar todos os usuários.
        """
        return requests.get(self.endpoint)

    def cadastrar_usuario(self, payload):
        """
        Realiza uma requisição POST para cadastrar um novo usuário.
        """
        return requests.post(self.endpoint, json=payload)

    def buscar_usuario_por_id(self, usuario_id):
        """
        Realiza uma requisição GET para buscar um usuário específico pelo ID.
        """
        return requests.get(f"{self.endpoint}/{usuario_id}")

    def atualizar_usuario(self, usuario_id, payload):
        """
        Realiza uma requisição PUT para atualizar um usuário pelo ID.
        """
        return requests.put(f"{self.endpoint}/{usuario_id}", json=payload)

    def excluir_usuario(self, usuario_id):
        """
        Realiza uma requisição DELETE para excluir um usuário pelo ID.
        """
        return requests.delete(f"{self.endpoint}/{usuario_id}")