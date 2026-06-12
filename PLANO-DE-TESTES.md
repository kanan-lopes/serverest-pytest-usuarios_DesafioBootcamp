# Plano de Testes — ServeRest API

**Projeto:** Automação de testes para a API ServeRest  
**Base URL:** `https://compassuol.serverest.dev`  
**Stack:** Python · Pytest · Requests  
**Data de criação:** Junho/2026  

---

## 1. Objetivos

O endpoint `/usuarios` já conta com cobertura sólida: 12 testes automatizados exercitando todos os verbos HTTP (GET, POST, PUT, DELETE), incluindo cenários de sucesso, campos obrigatórios ausentes, IDs inexistentes e email duplicado.

O objetivo desta suíte expandida é **cobrir os demais endpoints da ServeRest** com o mesmo nível de qualidade, garantindo que os fluxos de autenticação, gerenciamento de produtos e operações de carrinho de compras sejam validados de forma automatizada e independente.

**Metas específicas:**

- Validar autenticação via `/login` e o uso do token JWT nos endpoints protegidos
- Cobrir o CRUD completo de `/produtos` com e sem autenticação
- Cobrir o ciclo de vida do carrinho em `/carrinhos`, incluindo regras de negócio (carrinho único por usuário, concluir e cancelar compra)
- Detectar regressões nos fluxos críticos da API a cada execução da suíte

---

## 2. Estratégias de Teste

### 2.1 Tipos de teste aplicados

| Tipo | Descrição | Aplicação neste projeto |
|---|---|---|
| **Funcional (caixa-preta)** | Valida entradas e saídas conforme o contrato da API | Todos os endpoints |
| **Positivo (happy path)** | Fluxo com dados válidos e pré-condições atendidas | Todas as operações bem-sucedidas |
| **Negativo** | Dados inválidos, campos ausentes, IDs inexistentes | Validações de erro (4xx) |
| **Contrato** | Verifica presença e tipo dos campos na resposta | Campos obrigatórios em todos os bodies |
| **Fluxo integrado** | Sequência de chamadas que simula um caso de uso real | Login → criar produto → adicionar ao carrinho → concluir compra |
| **Segurança básica** | Tentativa de acessar recursos protegidos sem token | Endpoints que exigem autenticação |

### 2.2 Camada de teste

Todos os testes operam na **camada de API (integração contra ambiente real)**, sem mocks. A ServeRest é uma API pública de prática, portanto o ambiente de teste é o próprio ambiente disponibilizado.

### 2.3 Ferramentas

| Ferramenta | Uso |
|---|---|
| **Pytest** | Framework principal: execução, fixtures, marcadores, parametrização |
| **Requests** | Biblioteca HTTP para chamadas à API |
| **pytest-html** | Geração de relatório HTML após execução |
| **python-dotenv** | Configuração da `BASE_URL` via variável de ambiente |
| **uuid4** | Geração de dados únicos para isolamento de testes |

### 2.4 Padrões adotados

- **Client pattern:** cada endpoint terá seu próprio client (`LoginClient`, `ProdutosClient`, `CarrinhosClient`) seguindo o modelo já aplicado em `UsuariosClient`
- **Data factory:** funções em `data_factory.py` para geração de payloads válidos por endpoint
- **Fixtures com yield:** pré-condição e limpeza isoladas por teste
- **Marcadores:** cada endpoint terá seu marcador (`login`, `produtos`, `carrinhos`) registrado no `pytest.ini`
- **Independência total:** nenhum teste deve depender de estado deixado por outro

---

## 3. Escopo

### 3.1 O que está coberto (atual)

| Endpoint | Método | Cenários cobertos |
|---|---|---|
| `/usuarios` | GET | Listar todos os usuários |
| `/usuarios` | POST | Cadastro válido, email duplicado, campos obrigatórios ausentes (4 campos) |
| `/usuarios/{id}` | GET | Busca por ID válido, ID inexistente |
| `/usuarios/{id}` | PUT | Atualização com dados válidos |
| `/usuarios/{id}` | DELETE | Exclusão de usuário existente, ID inexistente |

**Total atual: 12 testes**

### 3.2 O que será coberto (expandido)

| Endpoint | Métodos | Prioridade |
|---|---|---|
| `/login` | POST | Alta |
| `/produtos` | GET, POST, GET/{id}, PUT/{id}, DELETE/{id} | Alta |
| `/carrinhos` | GET, POST, GET/{id}, DELETE/concluir-compra, DELETE/cancelar-compra | Alta |

### 3.3 O que ficou fora do escopo

| Item | Justificativa |
|---|---|
| Testes de performance / carga | Fora do objetivo do projeto atual |
| Testes de UI ou E2E com browser | API-only por definição do projeto |
| Testes de segurança avançados (pentest, injection) | Escopo além do contexto de QA funcional |
| Filtros/queries avançados por parâmetro | Cobertura básica contempla os campos mais comuns; filtros combinados podem ser adicionados em iteração futura |
| Testes de contrato formal (ex.: Pact) | Não há consumer separado no projeto |

---

## 4. Cenários a Implementar

### 4.1 `/login`

**Método:** POST

| # | Cenário | Tipo | Status esperado |
|---|---|---|---|
| L-01 | Login com credenciais válidas de administrador | Positivo | 200 + token JWT |
| L-02 | Login com credenciais válidas de não-administrador | Positivo | 200 + token JWT |
| L-03 | Login com email inexistente | Negativo | 401 |
| L-04 | Login com password incorreta | Negativo | 401 |
| L-05 | Login sem campo `email` | Negativo | 400 |
| L-06 | Login sem campo `password` | Negativo | 400 |
| L-07 | Login com body vazio | Negativo | 400 |
| L-08 | Validar que o token retornado é uma string não vazia | Contrato | 200 |

---

### 4.2 `/produtos`

**Métodos:** GET · POST · GET `/{id}` · PUT `/{id}` · DELETE `/{id}`

#### GET /produtos

| # | Cenário | Tipo | Status esperado |
|---|---|---|---|
| P-01 | Listar todos os produtos sem autenticação | Positivo | 200 + lista + campo `quantidade` |
| P-02 | Listar produtos verificando estrutura do item retornado | Contrato | 200 |

#### POST /produtos

| # | Cenário | Tipo | Status esperado |
|---|---|---|---|
| P-03 | Cadastrar produto válido com token de administrador | Positivo | 201 + `_id` |
| P-04 | Cadastrar produto sem token (não autenticado) | Segurança | 401 |
| P-05 | Cadastrar produto com token de não-administrador | Segurança | 403 |
| P-06 | Cadastrar produto com nome duplicado | Negativo | 400 |
| P-07 | Cadastrar produto sem campo `nome` | Negativo | 400 |
| P-08 | Cadastrar produto sem campo `preco` | Negativo | 400 |
| P-09 | Cadastrar produto sem campo `descricao` | Negativo | 400 |
| P-10 | Cadastrar produto sem campo `quantidade` | Negativo | 400 |

#### GET /produtos/{id}

| # | Cenário | Tipo | Status esperado |
|---|---|---|---|
| P-11 | Buscar produto por ID válido | Positivo | 200 + dados do produto |
| P-12 | Buscar produto com ID inexistente | Negativo | 400 |

#### PUT /produtos/{id}

| # | Cenário | Tipo | Status esperado |
|---|---|---|---|
| P-13 | Atualizar produto existente com token de administrador | Positivo | 200 |
| P-14 | Atualizar produto sem autenticação | Segurança | 401 |
| P-15 | Atualizar produto com token de não-administrador | Segurança | 403 |
| P-16 | Atualizar produto com ID inexistente (cria novo produto) | Positivo | 201 |

#### DELETE /produtos/{id}

| # | Cenário | Tipo | Status esperado |
|---|---|---|---|
| P-17 | Excluir produto existente com token de administrador | Positivo | 200 |
| P-18 | Excluir produto sem autenticação | Segurança | 401 |
| P-19 | Excluir produto inexistente | Negativo | 200 (nenhum registro excluído) |
| P-20 | Tentar excluir produto que está em um carrinho | Negativo | 400 |

---

### 4.3 `/carrinhos`

**Métodos:** GET · POST · GET `/{id}` · DELETE `/concluir-compra` · DELETE `/cancelar-compra`

#### GET /carrinhos

| # | Cenário | Tipo | Status esperado |
|---|---|---|---|
| C-01 | Listar todos os carrinhos | Positivo | 200 + lista + campo `quantidade` |
| C-02 | Validar estrutura dos itens retornados | Contrato | 200 |

#### POST /carrinhos

| # | Cenário | Tipo | Status esperado |
|---|---|---|---|
| C-03 | Criar carrinho com produto válido e token | Positivo | 201 + `_id` |
| C-04 | Criar carrinho sem autenticação | Segurança | 401 |
| C-05 | Criar segundo carrinho para o mesmo usuário | Negativo | 400 (usuário já tem carrinho) |
| C-06 | Criar carrinho com produto inexistente | Negativo | 400 |
| C-07 | Criar carrinho com quantidade maior que o estoque | Negativo | 400 |
| C-08 | Criar carrinho sem campo `produtos` | Negativo | 400 |
| C-09 | Criar carrinho com lista de produtos vazia | Negativo | 400 |

#### GET /carrinhos/{id}

| # | Cenário | Tipo | Status esperado |
|---|---|---|---|
| C-10 | Buscar carrinho por ID válido | Positivo | 200 + dados do carrinho |
| C-11 | Buscar carrinho com ID inexistente | Negativo | 400 |

#### DELETE /carrinhos/concluir-compra

| # | Cenário | Tipo | Status esperado |
|---|---|---|---|
| C-12 | Concluir compra com carrinho existente | Positivo | 200 + estoque atualizado |
| C-13 | Concluir compra sem ter carrinho aberto | Negativo | 200 (nenhum registro excluído) |
| C-14 | Concluir compra sem autenticação | Segurança | 401 |

#### DELETE /carrinhos/cancelar-compra

| # | Cenário | Tipo | Status esperado |
|---|---|---|---|
| C-15 | Cancelar compra com carrinho existente (estoque deve ser reposto) | Positivo | 200 + estoque reposto |
| C-16 | Cancelar compra sem ter carrinho aberto | Negativo | 200 (nenhum registro excluído) |
| C-17 | Cancelar compra sem autenticação | Segurança | 401 |

---

### 4.4 Fluxos integrados (end-to-end via API)

| # | Fluxo | Cenário |
|---|---|---|
| F-01 | Ciclo completo de compra | Login → criar produto → criar carrinho → concluir compra → verificar estoque |
| F-02 | Ciclo de cancelamento | Login → criar produto → criar carrinho → cancelar compra → verificar reposição de estoque |
| F-03 | Tentativa de produto em uso | Login → criar produto → adicionar ao carrinho → tentar excluir produto → verificar erro 400 |

---

## 5. Critérios de Qualidade

Um teste é considerado **pronto** quando atende a todos os critérios abaixo:

### 5.1 Critérios funcionais

- [ ] Valida o **status code** esperado para o cenário
- [ ] Valida o **body da resposta**: campos obrigatórios presentes e com tipos corretos
- [ ] Valida a **mensagem** retornada pela API (campo `message`) quando aplicável
- [ ] Para criações: valida que o campo `_id` está presente na resposta

### 5.2 Critérios de independência

- [ ] O teste **não depende** de estado deixado por outro teste
- [ ] Usa **dados únicos** gerados dinamicamente (ex.: email com `uuid4`, nome de produto com sufixo único)
- [ ] Realiza **limpeza** dos recursos criados via fixture com `yield` ou chamada explícita de DELETE ao final

### 5.3 Critérios de estrutura

- [ ] Está em um arquivo `test_*.py` correspondente ao endpoint testado
- [ ] Possui `docstring` descrevendo objetivo, pré-condições e critérios verificados
- [ ] Está marcado com o marcador correto (`@pytest.mark.<endpoint>`) registrado no `pytest.ini`
- [ ] Utiliza o **client** correspondente ao endpoint (sem `requests.*` direto no arquivo de teste)
- [ ] Payloads são gerados via **data factory**, não definidos inline no teste

### 5.4 Critérios de execução

- [ ] Passa de forma consistente em pelo menos **3 execuções consecutivas** (sem flakiness)
- [ ] Executa em isolamento (`pytest tests/test_<endpoint>.py::nome_do_teste`) sem falhar
- [ ] Não deixa dados residuais no ambiente após execução (sucesso ou falha)

### 5.5 Critérios para testes de segurança

- [ ] Testa o endpoint **sem token** e valida status `401`
- [ ] Testa com **token de usuário não-administrador** nos recursos que exigem admin e valida status `403`

---

## 6. Estrutura de Arquivos Esperada (após expansão)

```text
serverest-pytest-usuarios/
│
├── clients/
│   ├── usuarios_client.py       ✅ implementado
│   ├── login_client.py          🔲 a criar
│   ├── produtos_client.py       🔲 a criar
│   ├── carrinhos_client.py      🔲 a criar
│   └── __init__.py
│
├── tests/
│   ├── conftest.py              ✅ atualizar com fixtures de login/token
│   ├── test_usuarios.py         ✅ implementado
│   ├── test_login.py            🔲 a criar
│   ├── test_produtos.py         🔲 a criar
│   └── test_carrinhos.py        🔲 a criar
│
├── utils/
│   ├── data_factory.py          ✅ atualizar com geradores de produto/carrinho
│   └── __init__.py
│
├── .env.example
├── pytest.ini                   ✅ atualizar com novos marcadores
├── requirements.txt
├── README.md
└── PLANO-DE-TESTES.md           ✅ este arquivo
```

---

## 7. Resumo de Cobertura

| Endpoint | Testes atuais | Testes planejados | Total |
|---|---|---|---|
| `/usuarios` | 12 | 0 | **12** |
| `/login` | 0 | 8 | **8** |
| `/produtos` | 0 | 20 | **20** |
| `/carrinhos` | 0 | 17 | **17** |
| Fluxos integrados | 0 | 3 | **3** |
| **Total** | **12** | **48** | **60** |
