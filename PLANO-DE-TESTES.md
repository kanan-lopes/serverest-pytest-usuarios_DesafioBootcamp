# Plano de Testes — ServeRest API

**Projeto:** Automação de testes para a API ServeRest
**Base URL:** `https://compassuol.serverest.dev`
**Stack:** Python · Pytest · Requests
**Data de criação:** Junho/2026
**Última atualização:** Junho/2026

---

## 1. Objetivos

O endpoint `/usuarios` já conta com cobertura sólida: 12 testes automatizados exercitando todos os verbos HTTP (GET, POST, PUT, DELETE), incluindo cenários de sucesso, campos obrigatórios ausentes, IDs inexistentes e email duplicado.

O objetivo desta suíte expandida é **cobrir os demais endpoints da ServeRest** com o mesmo nível de qualidade, garantindo que os fluxos de autenticação, gerenciamento de produtos e operações de carrinho de compras sejam validados de forma automatizada e independente.

**Metas específicas:**

- Validar autenticação via `/login` e o uso do token JWT nos endpoints protegidos ✅
- Cobrir o CRUD completo de `/produtos` com e sem autenticação ✅
- Cobrir o ciclo de vida do carrinho em `/carrinhos`, incluindo regras de negócio (carrinho único por usuário, concluir e cancelar compra) ✅
- Detectar regressões nos fluxos críticos da API a cada execução da suíte

---

## 2. Estratégias de Teste

### 2.1 Tipos de teste aplicados

| Tipo | Descrição | Aplicação neste projeto |
| --- | --- | --- |
| **Funcional (caixa-preta)** | Valida entradas e saídas conforme o contrato da API | Todos os endpoints |
| **Positivo (happy path)** | Fluxo com dados válidos e pré-condições atendidas | Todas as operações bem-sucedidas |
| **Negativo** | Dados inválidos, campos ausentes, IDs inexistentes | Validações de erro (4xx) |
| **Contrato** | Verifica presença e tipo dos campos na resposta | Campos obrigatórios em todos os bodies |
| **Regra de negócio** | Valida restrições específicas do domínio | Carrinho único por usuário, estoque insuficiente, decremento/reposição de estoque |
| **Segurança básica** | Tentativa de excluir produto com carrinho aberto | Não foi automatizada nesta etapa; pode ser adicionada em investigação futura por envolver estado compartilhado entre produto e carrinho |

### 2.2 Camada de teste

Todos os testes operam na **camada de API (integração contra ambiente real)**, sem mocks. A ServeRest é uma API pública de prática, portanto o ambiente de teste é o próprio ambiente disponibilizado.

> **Observação sobre instabilidade:** por ser uma API pública compartilhada, respostas `503 Service Unavailable` podem ocorrer esporadicamente. Nesses casos, a falha é de infraestrutura e não do teste. Reexecutar o teste isolado confirma se foi instabilidade pontual.

### 2.3 Ferramentas

| Ferramenta | Uso |
| --- | --- |
| **Pytest** | Framework principal: execução, fixtures, marcadores |
| **Requests** | Biblioteca HTTP para chamadas à API |
| **pytest-html** | Geração de relatório HTML após execução |
| **python-dotenv** | Configuração da `BASE_URL` via variável de ambiente |
| **uuid4** | Geração de dados únicos para isolamento de testes |
| **Postman** | Investigação exploratória manual e validação de contratos |

### 2.4 Padrões adotados

- **Client pattern:** cada endpoint tem seu próprio client (`UsuariosClient`, `LoginClient`, `ProdutosClient`, `CarrinhosClient`), centralizando as chamadas HTTP e evitando `requests.*` direto nos testes
- **Data factory:** funções em `data_factory.py` para geração de payloads válidos por endpoint, todos com dados únicos via `uuid4`
- **Fixtures com yield:** pré-condição antes do `yield`, limpeza depois — garantindo isolamento mesmo em caso de falha do teste
- **Marcadores:** cada endpoint tem seu marcador registrado no `pytest.ini` (`usuarios`, `login`, `produtos`, `carrinhos`)
- **Independência total:** nenhum teste depende de estado deixado por outro; cada um cria e limpa seus próprios dados
- **Tokens dinâmicos:** as fixtures `token_admin` e `token_usuario_comum` criam usuários, fazem login e entregam o token Bearer ao teste, sem depender de credenciais fixas da base
- **Estoque original capturado na fixture:** a fixture `carrinho_criado` captura o estoque antes de criar o carrinho, permitindo validar efeitos de concluir e cancelar compra de forma precisa

---

## 3. Escopo

### 3.1 O que está coberto (implementado)

| Endpoint | Método | Cenários cobertos | Testes |
| --- | --- | --- | --- |
| `/usuarios` | GET | Listar todos os usuários | 1 |
| `/usuarios` | POST | Cadastro válido, email duplicado, campos obrigatórios ausentes (4 campos) | 6 |
| `/usuarios/{id}` | GET | Busca por ID válido, ID inexistente | 2 |
| `/usuarios/{id}` | PUT | Atualização com dados válidos | 1 |
| `/usuarios/{id}` | DELETE | Exclusão de existente, ID inexistente | 2 |
| `/login` | POST | Credenciais válidas (admin), credenciais válidas (comum), token como string Bearer, senha errada, email inexistente, sem email, sem password, body vazio | 8 |
| `/produtos` | GET | Listagem sem autenticação | 1 |
| `/produtos` | POST | Cadastro válido (admin), sem token, token de não-admin, nome duplicado, campos obrigatórios ausentes (4 campos) | 8 |
| `/produtos/{id}` | GET | Busca por ID válido, ID inexistente | 2 |
| `/produtos/{id}` | PUT | Atualização válida (admin), sem token, token de não-admin | 3 |
| `/produtos/{id}` | DELETE | Exclusão válida (admin), sem token, ID inexistente | 3 |
| `/carrinhos` | GET | Listagem sem autenticação | 1 |
| `/carrinhos` | POST | Criação válida, sem token, segundo carrinho (regra de negócio), produto inexistente, quantidade acima do estoque | 5 |
| `/carrinhos/{id}` | GET | Busca por ID válido, ID inexistente | 2 |
| `/carrinhos/concluir-compra` | DELETE | Concluir compra (estoque decrementado), sem carrinho aberto, sem token | 3 |
| `/carrinhos/cancelar-compra` | DELETE | Cancelar compra (estoque reposto), sem carrinho aberto, sem token | 3 |

**Total atual: 51 testes**

### 3.2 O que ficou fora do escopo

| Item | Justificativa |
| --- | --- |
| Testes de performance / carga | Fora do objetivo do projeto atual |
| Testes de UI ou E2E com browser | API-only por definição do projeto |
| Testes de segurança avançados (pentest, injection) | Escopo além do contexto de QA funcional |
| Filtros/queries avançados por parâmetro | Cobertura básica contempla os campos mais comuns; filtros combinados podem ser adicionados em iteração futura |
| Testes de contrato formal (ex.: Pact) | Não há consumer separado no projeto |
| Tentativa de excluir produto com carrinho aberto | Exige estado compartilhado entre módulos; coberto como observação no bug report |
| Fluxos integrados multi-endpoint (F-01, F-02, F-03) | Os cenários essenciais já estão cobertos nos testes de concluir/cancelar; fluxos completos podem ser adicionados em iteração futura |

---

## 4. Cenários Implementados

### 4.1 `/login` — ✅ Implementado

**Arquivo:** `tests/test_login.py` | **Marker:** `@pytest.mark.login`

| # | Função de teste | Tipo | Status esperado |
| --- | --- | --- | --- |
| L-01 | `test_deve_fazer_login_com_usuario_administrador` | Positivo | 200 + token Bearer |
| L-02 | `test_deve_fazer_login_com_usuario_comum` | Positivo | 200 + token Bearer |
| L-03 | `test_token_retornado_deve_ser_string_nao_vazia` | Contrato | 200 + formato `Bearer <jwt>` |
| L-04 | `test_nao_deve_fazer_login_com_senha_errada` | Negativo | 401 |
| L-05 | `test_nao_deve_fazer_login_com_email_inexistente` | Negativo | 401 |
| L-06 | `test_nao_deve_fazer_login_sem_email` | Negativo | 400 |
| L-07 | `test_nao_deve_fazer_login_sem_password` | Negativo | 400 |
| L-08 | `test_nao_deve_fazer_login_com_body_vazio` | Negativo | 400 |

**Fixtures utilizadas:** `login_client`, `usuario_admin_criado`, `usuario_comum_criado`

---

### 4.2 `/produtos` — ✅ Implementado

**Arquivo:** `tests/test_produtos.py` | **Marker:** `@pytest.mark.produtos`

#### GET /produtos

| # | Função de teste | Tipo | Status esperado |
| --- | --- | --- | --- |
| P-01 | `test_deve_listar_produtos_sem_autenticacao` | Positivo | 200 + lista + campo `quantidade` |

#### POST /produtos

| # | Função de teste | Tipo | Status esperado |
| --- | --- | --- | --- |
| P-02 | `test_deve_cadastrar_produto_com_token_admin` | Positivo | 201 + `_id` |
| P-03 | `test_nao_deve_cadastrar_produto_sem_autenticacao` | Segurança | 401 |
| P-04 | `test_nao_deve_cadastrar_produto_com_token_de_usuario_comum` | Segurança | 403 |
| P-05 | `test_nao_deve_cadastrar_produto_com_nome_duplicado` | Negativo | 400 |
| P-06 | `test_nao_deve_cadastrar_produto_sem_nome` | Negativo | 400 |
| P-07 | `test_nao_deve_cadastrar_produto_sem_preco` | Negativo | 400 |
| P-08 | `test_nao_deve_cadastrar_produto_sem_descricao` | Negativo | 400 |
| P-09 | `test_nao_deve_cadastrar_produto_sem_quantidade` | Negativo | 400 |

#### GET /produtos/{id}

| # | Função de teste | Tipo | Status esperado |
| --- | --- | --- | --- |
| P-10 | `test_deve_buscar_produto_por_id_valido` | Positivo | 200 + dados do produto |
| P-11 | `test_nao_deve_buscar_produto_com_id_inexistente` | Negativo | 400 |

#### PUT /produtos/{id}

| # | Função de teste | Tipo | Status esperado |
| --- | --- | --- | --- |
| P-12 | `test_deve_atualizar_produto_com_token_admin` | Positivo | 200 + GET confirma dados atualizados |
| P-13 | `test_nao_deve_atualizar_produto_sem_autenticacao` | Segurança | 401 |
| P-14 | `test_nao_deve_atualizar_produto_com_token_de_usuario_comum` | Segurança | 403 |

#### DELETE /produtos/{id}

| # | Função de teste | Tipo | Status esperado |
| --- | --- | --- | --- |
| P-15 | `test_deve_excluir_produto_com_token_admin` | Positivo | 200 + GET confirma 400 |
| P-16 | `test_nao_deve_excluir_produto_sem_autenticacao` | Segurança | 401 |
| P-17 | `test_deve_retornar_mensagem_ao_excluir_produto_inexistente` | Negativo | 200 + "Nenhum registro excluído" |

**Fixtures utilizadas:** `produtos_client`, `token_admin`, `token_usuario_comum`, `produto_payload`, `produto_criado`

> **Descoberta durante implementação:** a ServeRest valida o formato do ID antes de buscar na base. IDs fora do padrão de 16 caracteres alfanuméricos retornam 400 de validação de formato. Com IDs no formato correto mas inexistentes, o comportamento é o mesmo de `/usuarios`: status 200 com "Nenhum registro excluído". Esse comportamento foi documentado na [Issue #1](https://github.com/kanan-lopes/serverest-pytest-usuarios_DesafioBootcamp/issues/1) após investigação com Postman.

---

### 4.3 `/carrinhos` — ✅ Implementado

**Arquivo:** `tests/test_carrinhos.py` | **Marker:** `@pytest.mark.carrinhos`

#### GET /carrinhos

| # | Função de teste | Tipo | Status esperado |
| --- | --- | --- | --- |
| C-01 | `test_deve_listar_carrinhos_sem_autenticacao` | Positivo | 200 + lista + campo `quantidade` |

#### POST /carrinhos

| # | Função de teste | Tipo | Status esperado |
| --- | --- | --- | --- |
| C-02 | `test_deve_criar_carrinho_com_produto_valido` | Positivo | 201 + `_id` |
| C-03 | `test_nao_deve_criar_carrinho_sem_autenticacao` | Segurança | 401 |
| C-04 | `test_nao_deve_criar_segundo_carrinho_para_mesmo_usuario` | Regra de negócio | 400 |
| C-05 | `test_nao_deve_criar_carrinho_com_produto_inexistente` | Negativo | 400 |
| C-06 | `test_nao_deve_criar_carrinho_com_quantidade_maior_que_estoque` | Negativo | 400 |

#### GET /carrinhos/{id}

| # | Função de teste | Tipo | Status esperado |
| --- | --- | --- | --- |
| C-07 | `test_deve_buscar_carrinho_por_id_valido` | Positivo | 200 + dados do carrinho |
| C-08 | `test_nao_deve_buscar_carrinho_com_id_inexistente` | Negativo | 400 |

#### DELETE /carrinhos/concluir-compra

| # | Função de teste | Tipo | Status esperado |
| --- | --- | --- | --- |
| C-09 | `test_deve_concluir_compra_e_decrementar_estoque` | Positivo | 200 + estoque decrementado |
| C-10 | `test_deve_retornar_mensagem_ao_concluir_compra_sem_carrinho` | Negativo | 200 + "Não foi encontrado carrinho" |
| C-11 | `test_nao_deve_concluir_compra_sem_autenticacao` | Segurança | 401 |

#### DELETE /carrinhos/cancelar-compra

| # | Função de teste | Tipo | Status esperado |
| --- | --- | --- | --- |
| C-12 | `test_deve_cancelar_compra_e_repor_estoque` | Positivo | 200 + estoque reposto |
| C-13 | `test_deve_retornar_mensagem_ao_cancelar_compra_sem_carrinho` | Negativo | 200 + "Não foi encontrado carrinho" |
| C-14 | `test_nao_deve_cancelar_compra_sem_autenticacao` | Segurança | 401 |

**Fixtures utilizadas:** `carrinhos_client`, `produtos_client`, `usuario_com_token_e_produto`, `carrinho_criado`

> **Detalhe de implementação:** a fixture `carrinho_criado` captura o estoque original do produto *antes* de criar o carrinho (que decrementa o estoque ao ser criado). Isso permite que os testes de concluir e cancelar validem a variação correta usando o estoque de referência.

---

## 5. Investigação Exploratória e Bug Report

Além dos testes automatizados, foi realizada uma **investigação manual exploratória** usando o Postman para verificar comportamentos da API.

**Comportamento identificado:** ao tentar excluir um recurso por um ID válido (16 chars alfanuméricos) mas inexistente na base, os endpoints `/usuarios` e `/produtos` retornam **200 OK** com "Nenhum registro excluído", em vez de um código 4xx que indicaria explicitamente a ausência do recurso.

**Resultado:** documentado na Issue #1 do repositório:
[DELETE retorna 200 OK ao tentar excluir recurso inexistente](https://github.com/kanan-lopes/serverest-pytest-usuarios_DesafioBootcamp/issues/1)

---

## 6. Critérios de Qualidade

Um teste é considerado **pronto** quando atende a todos os critérios abaixo:

### 6.1 Critérios funcionais

- [ ] Valida o **status code** esperado para o cenário
- [ ] Valida o **body da resposta**: campos obrigatórios presentes e com tipos corretos
- [ ] Valida a **mensagem** retornada pela API (campo `message`) quando aplicável
- [ ] Para criações: valida que o campo `_id` está presente na resposta

### 6.2 Critérios de independência

- [ ] O teste não depende de estado deixado por outro teste
- [ ] Usa dados únicos gerados dinamicamente (`uuid4` para emails, nomes de produto, etc.)
- [ ] Realiza limpeza dos recursos criados via fixture com `yield` ou chamada explícita de DELETE ao final

### 6.3 Critérios de estrutura

- [ ] Está em um arquivo `test_*.py` correspondente ao endpoint testado
- [ ] Possui `docstring` descrevendo objetivo, pré-condições e critérios verificados
- [ ] Está marcado com o marcador correto (`@pytest.mark.<endpoint>`) registrado no `pytest.ini`
- [ ] Utiliza o **client** correspondente ao endpoint (sem `requests.*` direto no arquivo de teste)
- [ ] Payloads são gerados via **data factory**, não definidos inline no teste

### 6.4 Critérios de execução

- [ ] Passa de forma consistente em pelo menos 3 execuções consecutivas (sem flakiness)
- [ ] Executa em isolamento (`pytest tests/test_<endpoint>.py::nome_do_teste`) sem falhar
- [ ] Não deixa dados residuais no ambiente após execução (sucesso ou falha)

### 6.5 Critérios para testes de segurança

- [ ] Testa o endpoint **sem token** e valida status `401`
- [ ] Testa com **token de usuário não-administrador** nos recursos que exigem admin e valida status `403`

---

## 7. Estrutura de Arquivos

```text
serverest-pytest-usuarios/
│
├── clients/
│   ├── usuarios_client.py       ✅ implementado
│   ├── login_client.py          ✅ implementado
│   ├── produtos_client.py       ✅ implementado
│   ├── carrinhos_client.py      ✅ implementado
│   └── __init__.py
│
├── tests/
│   ├── conftest.py              ✅ fixtures de infra, usuários, tokens, produtos e carrinhos
│   ├── test_usuarios.py         ✅ 12 testes
│   ├── test_login.py            ✅ 8 testes
│   ├── test_produtos.py         ✅ 17 testes
│   └── test_carrinhos.py        ✅ 14 testes
│
├── utils/
│   ├── data_factory.py          ✅ geradores de usuário, credenciais, produto e carrinho
│   └── __init__.py
│
├── .env.example
├── pytest.ini                   ✅ markers: usuarios, login, produtos, carrinhos
├── requirements.txt
├── README.md
└── PLANO-DE-TESTES.md           ✅ este arquivo
```

---

## 8. Resumo de Cobertura

| Endpoint | Implementados | Pendentes | Total |
| --- | --- | --- | --- |
| `/usuarios` | 12 | 0 | **12** |
| `/login` | 8 | 0 | **8** |
| `/produtos` | 17 | 0 | **17** |
| `/carrinhos` | 14 | 0 | **14** |
| **Total** | **51** | **0** | **51** |
