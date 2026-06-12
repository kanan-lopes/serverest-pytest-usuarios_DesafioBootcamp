from uuid import uuid4


def gerar_email_unico():
    """
    Gera um email único para evitar conflito com usuários já cadastrados na API.

    A ServeRest não permite cadastrar dois usuários com o mesmo email.
    Por isso, cada teste que cria usuário deve usar um email diferente.
    """
    return f"teste_{uuid4().hex[:8]}@email.com"


def gerar_usuario_valido(administrador="false"):
    """
    Gera uma massa de dados válida para cadastro de usuário.

    O campo 'administrador' na ServeRest deve ser enviado como string:
    - "true"
    - "false"
    """
    return {
        "nome": "Usuario Teste Pytest",
        "email": gerar_email_unico(),
        "password": "teste123",
        "administrador": administrador
    }


def gerar_credenciais_login(email, password):
    """
    Gera um payload de login a partir de email e password fornecidos.

    Separa a construção do payload de login da criação do usuário,
    permitindo reutilizar credenciais já cadastradas.
    """
    return {
        "email": email,
        "password": password
    }
