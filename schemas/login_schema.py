"""
Schemas JSON para validação de respostas do endpoint /login da ServeRest.

O endpoint /login retorna um Bearer token no campo 'authorization'.
O schema valida que o campo existe, é string e começa com o prefixo "Bearer ".
"""

# ─────────────────────────────────────────────
# POST /login (sucesso)
# ─────────────────────────────────────────────

SCHEMA_LOGIN_SUCESSO = {
    "type": "object",
    "required": ["message", "authorization"],
    "properties": {
        "message": {
            "type": "string",
            "const": "Login realizado com sucesso"
        },
        "authorization": {
            "type": "string",
            "pattern": "^Bearer .+",
            "description": "Token JWT no formato 'Bearer <token>'"
        }
    },
    "additionalProperties": False
}

# ─────────────────────────────────────────────
# POST /login (erro de credenciais)
# ─────────────────────────────────────────────

SCHEMA_LOGIN_ERRO_CREDENCIAIS = {
    "type": "object",
    "required": ["message"],
    "properties": {
        "message": {
            "type": "string",
            "const": "Email e/ou senha inválidos"
        }
    },
    "additionalProperties": False
}
