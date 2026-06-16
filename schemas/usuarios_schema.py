"""
Schemas JSON para validação de respostas do endpoint /usuarios da ServeRest.

Cada schema define a estrutura esperada (campos obrigatórios e tipos)
de uma resposta. A validação é feita com jsonschema.validate().

Os schemas usam o draft padrão do jsonschema (Draft 7 / 2020-12),
com foco em garantir que campos críticos do contrato estejam presentes
e com os tipos corretos, sem ser frágil a dados dinâmicos da API pública.
"""

# ─────────────────────────────────────────────
# GET /usuarios
# ─────────────────────────────────────────────

SCHEMA_LISTAR_USUARIOS = {
    "type": "object",
    "required": ["quantidade", "usuarios"],
    "properties": {
        "quantidade": {
            "type": "integer",
            "description": "Total de usuários retornados na listagem"
        },
        "usuarios": {
            "type": "array",
            "description": "Lista de usuários",
            "items": {
                "type": "object",
                "required": ["nome", "email", "password", "administrador", "_id"],
                "properties": {
                    "nome": {"type": "string"},
                    "email": {"type": "string", "format": "email"},
                    "password": {"type": "string"},
                    "administrador": {
                        "type": "string",
                        "enum": ["true", "false"],
                        "description": "Na ServeRest, administrador é string 'true' ou 'false'"
                    },
                    "_id": {"type": "string"}
                },
                "additionalProperties": False
            }
        }
    },
    "additionalProperties": False
}

# ─────────────────────────────────────────────
# POST /usuarios (resposta de cadastro)
# ─────────────────────────────────────────────

SCHEMA_CADASTRAR_USUARIO = {
    "type": "object",
    "required": ["message", "_id"],
    "properties": {
        "message": {
            "type": "string",
            "const": "Cadastro realizado com sucesso"
        },
        "_id": {
            "type": "string",
            "description": "ID gerado para o novo usuário"
        }
    },
    "additionalProperties": False
}

# ─────────────────────────────────────────────
# GET /usuarios/{id} (busca por ID)
# ─────────────────────────────────────────────

SCHEMA_BUSCAR_USUARIO_POR_ID = {
    "type": "object",
    "required": ["nome", "email", "password", "administrador", "_id"],
    "properties": {
        "nome": {"type": "string"},
        "email": {"type": "string"},
        "password": {"type": "string"},
        "administrador": {
            "type": "string",
            "enum": ["true", "false"]
        },
        "_id": {"type": "string"}
    },
    "additionalProperties": False
}
