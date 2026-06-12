import requests


class LoginClient:
    """
    Cliente responsável por centralizar as chamadas HTTP
    relacionadas ao endpoint /login da ServeRest.
    """

    def __init__(self, base_url):
        self.base_url = base_url
        self.endpoint = f"{self.base_url}/login"

    def fazer_login(self, payload):
        """
        Realiza uma requisição POST para autenticar um usuário.

        Retorna 200 com o token Bearer em caso de sucesso,
        ou 400/401 em caso de credenciais inválidas ou campos ausentes.
        """
        return requests.post(self.endpoint, json=payload)
