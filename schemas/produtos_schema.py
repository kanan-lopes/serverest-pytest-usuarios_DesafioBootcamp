"""
Schemas JSON para validação de respostas do endpoint /produtos da ServeRest.

Os schemas validam a estrutura dos campos obrigatórios sem ser frágeis
a dados dinâmicos como nomes únicos gerados por uuid4.
"""

# ─────────────────────────────────────────────
# GET /produtos
# ─────────────────────────────────────────────

SCHEMA_LISTAR_PRODUTOS = {
    "type": "object",
    "required": ["quantidade", "produtos"],
    "properties": {
        "quantidade": {
            "type": "integer",
            "description": "Total de produtos retornados na listagem"
        },
        "produtos": {
            "type": "array",
            "description": "Lista de produtos",
            "items": {
                "type": "object",
                "required": ["nome", "preco", "descricao", "quantidade", "_id"],
                "properties": {
                    "nome": {"type": "string"},
                    "preco": {"type": "number"},
                    "descricao": {"type": "string"},
                    "quantidade": {"type": "integer"},
                    "_id": {"type": "string"}
                },
                "additionalProperties": False
            }
        }
    },
    "additionalProperties": False
}

# ─────────────────────────────────────────────
# POST /produtos (resposta de cadastro)
# ─────────────────────────────────────────────

SCHEMA_CADASTRAR_PRODUTO = {
    "type": "object",
    "required": ["message", "_id"],
    "properties": {
        "message": {
            "type": "string",
            "const": "Cadastro realizado com sucesso"
        },
        "_id": {
            "type": "string",
            "description": "ID gerado para o novo produto"
        }
    },
    "additionalProperties": False
}

# ─────────────────────────────────────────────
# GET /produtos/{id}
# ─────────────────────────────────────────────

SCHEMA_BUSCAR_PRODUTO_POR_ID = {
    "type": "object",
    "required": ["nome", "preco", "descricao", "quantidade", "_id"],
    "properties": {
        "nome": {"type": "string"},
        "preco": {"type": "number"},
        "descricao": {"type": "string"},
        "quantidade": {"type": "integer"},
        "_id": {"type": "string"}
    },
    "additionalProperties": False
}
