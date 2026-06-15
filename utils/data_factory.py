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


def gerar_nome_produto_unico():
    """
    Gera um nome de produto único usando uuid4.

    A ServeRest não permite cadastrar dois produtos com o mesmo nome.
    Por isso, cada teste que cria produto deve usar um nome diferente,
    evitando conflito de nome duplicado entre execuções.
    """
    return f"Produto Teste {uuid4().hex[:8]}"


def gerar_produto_valido():
    """
    Gera uma massa de dados válida para cadastro de produto.

    Campos obrigatórios na ServeRest:
    - nome: string única (usa uuid4 para evitar duplicatas)
    - preco: número inteiro positivo
    - descricao: string descritiva
    - quantidade: número inteiro não negativo
    """
    return {
        "nome": gerar_nome_produto_unico(),
        "preco": 100,
        "descricao": "Produto gerado automaticamente pelo Pytest",
        "quantidade": 50
    }
