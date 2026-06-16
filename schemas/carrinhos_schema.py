"""
Schemas JSON para validação de respostas do endpoint /carrinhos da ServeRest.

O carrinho contém uma lista de produtos com campos calculados (precoTotal,
quantidadeTotal). Os schemas validam a estrutura completa incluindo os itens.
"""

# ─────────────────────────────────────────────
# GET /carrinhos
# ─────────────────────────────────────────────

SCHEMA_LISTAR_CARRINHOS = {
    "type": "object",
    "required": ["quantidade", "carrinhos"],
    "properties": {
        "quantidade": {
            "type": "integer",
            "description": "Total de carrinhos abertos no momento"
        },
        "carrinhos": {
            "type": "array",
            "description": "Lista de carrinhos",
            "items": {
                "type": "object",
                "required": ["produtos", "precoTotal", "quantidadeTotal", "idUsuario", "_id"],
                "properties": {
                    "produtos": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["idProduto", "quantidade", "precoUnitario"],
                            "properties": {
                                "idProduto": {"type": "string"},
                                "quantidade": {"type": "integer"},
                                "precoUnitario": {"type": "number"}
                            },
                            "additionalProperties": False
                        }
                    },
                    "precoTotal": {"type": "number"},
                    "quantidadeTotal": {"type": "integer"},
                    "idUsuario": {"type": "string"},
                    "_id": {"type": "string"}
                },
                "additionalProperties": False
            }
        }
    },
    "additionalProperties": False
}

# ─────────────────────────────────────────────
# GET /carrinhos/{id}
# ─────────────────────────────────────────────

SCHEMA_BUSCAR_CARRINHO_POR_ID = {
    "type": "object",
    "required": ["produtos", "precoTotal", "quantidadeTotal", "idUsuario", "_id"],
    "properties": {
        "produtos": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["idProduto", "quantidade", "precoUnitario"],
                "properties": {
                    "idProduto": {"type": "string"},
                    "quantidade": {"type": "integer"},
                    "precoUnitario": {"type": "number"}
                },
                "additionalProperties": False
            }
        },
        "precoTotal": {"type": "number"},
        "quantidadeTotal": {"type": "integer"},
        "idUsuario": {"type": "string"},
        "_id": {"type": "string"}
    },
    "additionalProperties": False
}

# ─────────────────────────────────────────────
# POST /carrinhos (resposta de criação)
# ─────────────────────────────────────────────

SCHEMA_CRIAR_CARRINHO = {
    "type": "object",
    "required": ["message", "_id"],
    "properties": {
        "message": {
            "type": "string",
            "const": "Cadastro realizado com sucesso"
        },
        "_id": {
            "type": "string",
            "description": "ID gerado para o novo carrinho"
        }
    },
    "additionalProperties": False
}
