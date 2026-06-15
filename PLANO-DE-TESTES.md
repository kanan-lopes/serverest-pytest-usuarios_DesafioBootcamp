# Plano de Testes — ServeRest API

**Projeto:** Automação de testes para a API ServeRest
**Base URL:** `https://compassuol.serverest.dev`
**Stack:** Python · Pytest · Requests
**Data de criação:** Junho/2026
**Última atualização:** Junho/2026

---

## 1. Objetivos

O endpoint `/usuarios` já conta com cobertura sólida: 12 testes automatizados exercitando todos os verbos HTTP principais do endpoint (GET, POST, PUT, DELETE), incluindo cenários de sucesso, campos obrigatórios ausentes, IDs inexistentes e email duplicado.

O objetivo desta suíte expandida é **cobrir os demais endpoints da ServeRest** com o mesmo nível de qualidade, garantindo que os fluxos de autenticação, gerenciamento de produtos e operações de carrinho de compras sejam validados de forma automatizada, independente e rastreável.

**Metas específicas:**

* Validar autenticação via `/login` e o uso do token Bearer nos endpoints protegidos ✅
* Cobrir o CRUD de `/produtos` com e sem autenticação ✅
* Cobrir o ciclo de vida do carrinho em `/carrinhos`, incluindo regras de negócio como carrinho único por usuário, concluir compra e cancelar compra ✅
* Detectar regressões nos fluxos críticos da API a cada execução da suíte ✅
* Registrar comportamentos suspeitos por meio de investigação exploratória e bug report ✅

---

## 2. Estratégias de Teste

### 2.1 Tipos de teste aplicados

| Tipo                          | Descrição                                                                  | Aplicação neste projeto                                                             |
| ----------------------------- | -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| **Funcional (caixa-preta)**   | Valida entradas e saídas conforme o comportamento esperado da API          | Todos os endpoints                                                                  |
| **Positivo (happy path)**     | Fluxo com dados válidos e pré-condições atendidas                          | Criação, listagem, busca, atualização, exclusão, login e operações de carrinho      |
| **Negativo**                  | Dados inválidos, campos ausentes, IDs inexistentes ou regras violadas      | Validações de erro e comportamentos não permitidos                                  |
| **Contrato**                  | Verifica presença e tipo de campos relevantes nas respostas                | Respostas de listagem, busca, criação e autenticação                                |
| **Regra de negócio**          | Valida restrições específicas do domínio                                   | Carrinho único por usuário, estoque insuficiente, decremento e reposição de estoque |
| **Segurança básica**          | Verifica acesso a recursos protegidos sem token ou com token sem permissão | Produtos e carrinhos                                                                |
| **Investigação exploratória** | Explora comportamentos suspeitos fora da automação principal               | Validação manual com Postman e abertura de Issue                                    |

### 2.2 Camada de teste

Todos os testes automatizados operam na **camada de API**, realizando chamadas reais contra o ambiente público da ServeRest. Não foram utilizados mocks.

A ServeRest é uma API pública de prática; portanto, o ambiente testado é compartilhado e pode apresentar instabilidades pontuais. Em caso de respostas como `503 Service Unavailable`, a falha deve ser investigada e o teste deve ser reexecutado isoladamente para diferenciar instabilidade de infraestrutura de falha funcional.

### 2.3 Ferramentas

| Ferramenta        | Uso                                                                    |
| ----------------- | ---------------------------------------------------------------------- |
| **Python 3.13**   | Linguagem utilizada no projeto                                         |
| **Pytest**        | Framework principal de testes                                          |
| **Requests**      | Biblioteca para chamadas HTTP                                          |
| **pytest-html**   | Geração de relatório HTML de execução                                  |
| **python-dotenv** | Configuração da `BASE_URL` via variável de ambiente                    |
| **uuid4**         | Geração de dados únicos para isolamento dos testes                     |
| **Postman**       | Investigação exploratória manual e validação de comportamento suspeito |

### 2.4 Padrões adotados

* **Client pattern:** cada endpoint possui seu próprio client (`UsuariosClient`, `LoginClient`, `ProdutosClient`, `CarrinhosClient`), centralizando as chamadas HTTP e evitando `requests.*` diretamente nos testes.
* **Data factory:** payloads são gerados por funções em `utils/data_factory.py`, reduzindo duplicação e evitando dados fixos.
* **Fixtures com `yield`:** pré-condições são criadas antes do teste e limpezas são executadas após o teste.
* **Dados dinâmicos:** emails, nomes de produtos e IDs inexistentes válidos são gerados dinamicamente com `uuid4`.
* **Markers por endpoint:** os testes são organizados com `@pytest.mark.usuarios`, `@pytest.mark.login`, `@pytest.mark.produtos` e `@pytest.mark.carrinhos`.
* **Independência dos testes:** nenhum teste depende do estado deixado por outro.
* **Limpeza de dados:** usuários, produtos e carrinhos criados durante os testes são removidos ou cancelados ao final da execução.
* **Tokens dinâmicos:** os tokens são obtidos por fixtures que criam usuários, realizam login e retornam o Bearer token.

---

## 3. Escopo

### 3.1 Escopo implementado

| Endpoint                     | Método | Cenários cobertos                                                                       | Testes |
| ---------------------------- | ------ | --------------------------------------------------------------------------------------- | ------ |
| `/usuarios`                  | GET    | Listar usuários                                                                         | 1      |
| `/usuarios`                  | POST   | Cadastro válido, email duplicado, campos obrigatórios ausentes                          | 6      |
| `/usuarios/{id}`             | GET    | Busca por ID válido e ID inexistente                                                    | 2      |
| `/usuarios/{id}`             | PUT    | Atualização de usuário existente                                                        | 1      |
| `/usuarios/{id}`             | DELETE | Exclusão de usuário existente e ID inexistente                                          | 2      |
| `/login`                     | POST   | Login válido, login inválido, campos ausentes e validação do token                      | 8      |
| `/produtos`                  | GET    | Listagem de produtos                                                                    | 1      |
| `/produtos`                  | POST   | Cadastro válido, autenticação, autorização, nome duplicado e campos ausentes            | 8      |
| `/produtos/{id}`             | GET    | Busca por ID válido e ID inexistente                                                    | 2      |
| `/produtos/{id}`             | PUT    | Atualização válida, sem autenticação e com usuário sem permissão                        | 3      |
| `/produtos/{id}`             | DELETE | Exclusão válida, sem autenticação e ID inexistente                                      | 3      |
| `/carrinhos`                 | GET    | Listagem de carrinhos                                                                   | 1      |
| `/carrinhos`                 | POST   | Criação válida, sem token, segundo carrinho, produto inexistente e estoque insuficiente | 5      |
| `/carrinhos/{id}`            | GET    | Busca por ID válido e ID inexistente                                                    | 2      |
| `/carrinhos/concluir-compra` | DELETE | Concluir compra, concluir sem carrinho e concluir sem token                             | 3      |
| `/carrinhos/cancelar-compra` | DELETE | Cancelar compra, cancelar sem carrinho e cancelar sem token                             | 3      |

**Total implementado: 51 testes automatizados**

### 3.2 Cenários pendentes em relação ao plano inicial

A primeira versão do plano previa **60 cenários** no total. Ao final da implementação, foram automatizados **51 testes**, restando **9 cenários pendentes** ou candidatos a investigação futura.

| Cenário pendente                                           | Justificativa                                                                                                                                      |
| ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Validar estrutura do item retornado em `GET /produtos`     | A listagem de produtos foi testada, mas sem validação formal de schema/estrutura de cada item.                                                     |
| Atualizar produto com ID inexistente criando novo produto  | Cenário específico da regra de `PUT`; não foi automatizado para evitar criação residual e por exigir investigação isolada do comportamento da API. |
| Tentar excluir produto que está em um carrinho             | Depende de estado compartilhado entre produto e carrinho; pode ser adicionado em investigação futura.                                              |
| Validar estrutura dos itens retornados em `GET /carrinhos` | A listagem de carrinhos foi testada, mas sem validação formal de schema/estrutura de cada item.                                                    |
| Criar carrinho sem campo `produtos`                        | Cenário negativo válido, mas não automatizado nesta versão.                                                                                        |
| Criar carrinho com lista de produtos vazia                 | Cenário negativo válido, mas não automatizado nesta versão.                                                                                        |
| Fluxo integrado F-01 — ciclo completo de compra            | Parte do comportamento foi coberta nos testes de carrinho, mas o fluxo E2E completo não foi isolado como teste próprio.                            |
| Fluxo integrado F-02 — ciclo de cancelamento               | Parte do comportamento foi coberta nos testes de carrinho, mas o fluxo E2E completo não foi isolado como teste próprio.                            |
| Fluxo integrado F-03 — produto em uso                      | Cenário relacionado à tentativa de excluir produto vinculado a carrinho; permanece como investigação futura.                                       |

### 3.3 Fora do escopo do projeto

| Item                                            | Justificativa                            |
| ----------------------------------------------- | ---------------------------------------- |
| Testes de performance/carga                     | Fora do objetivo do desafio atual        |
| Testes de UI ou E2E com browser                 | Projeto focado em testes de API          |
| Testes de segurança avançados                   | Fora do escopo de QA funcional proposto  |
| Testes de contrato formal com Pact              | Não há consumer separado no projeto      |
| Filtros e combinações avançadas de query params | Podem ser adicionados em iteração futura |
| JSON Schema                                     | Ficou como desafio extra opcional        |
| GitHub Actions                                  | Ficou como desafio extra opcional        |

---

## 4. Cenários Implementados

### 4.1 `/usuarios` — ✅ Implementado

**Arquivo:** `tests/test_usuarios.py`
**Marker:** `@pytest.mark.usuarios`

| #    | Função de teste                                              | Tipo     | Status esperado |
| ---- | ------------------------------------------------------------ | -------- | --------------- |
| U-01 | `test_deve_listar_usuarios_com_sucesso`                      | Positivo | 200             |
| U-02 | `test_deve_cadastrar_usuario_valido_com_sucesso`             | Positivo | 201             |
| U-03 | `test_nao_deve_cadastrar_usuario_com_email_duplicado`        | Negativo | 400             |
| U-04 | `test_nao_deve_cadastrar_usuario_sem_nome`                   | Negativo | 400             |
| U-05 | `test_nao_deve_cadastrar_usuario_sem_email`                  | Negativo | 400             |
| U-06 | `test_nao_deve_cadastrar_usuario_sem_password`               | Negativo | 400             |
| U-07 | `test_nao_deve_cadastrar_usuario_sem_administrador`          | Negativo | 400             |
| U-08 | `test_deve_buscar_usuario_por_id_valido`                     | Positivo | 200             |
| U-09 | `test_nao_deve_buscar_usuario_com_id_inexistente`            | Negativo | 400             |
| U-10 | `test_deve_atualizar_usuario_existente_com_sucesso`          | Positivo | 200             |
| U-11 | `test_deve_excluir_usuario_existente_com_sucesso`            | Positivo | 200             |
| U-12 | `test_deve_retornar_mensagem_ao_excluir_usuario_inexistente` | Negativo | 200             |

**Fixtures utilizadas:** `usuarios_client`, `usuario_payload`, `usuario_criado`

---

### 4.2 `/login` — ✅ Implementado

**Arquivo:** `tests/test_login.py`
**Marker:** `@pytest.mark.login`

| #    | Função de teste                                   | Tipo     | Status esperado       |
| ---- | ------------------------------------------------- | -------- | --------------------- |
| L-01 | `test_deve_fazer_login_com_usuario_administrador` | Positivo | 200 + token Bearer    |
| L-02 | `test_deve_fazer_login_com_usuario_comum`         | Positivo | 200 + token Bearer    |
| L-03 | `test_token_retornado_deve_ser_string_nao_vazia`  | Contrato | 200 + token não vazio |
| L-04 | `test_nao_deve_fazer_login_com_senha_errada`      | Negativo | 401                   |
| L-05 | `test_nao_deve_fazer_login_com_email_inexistente` | Negativo | 401                   |
| L-06 | `test_nao_deve_fazer_login_sem_email`             | Negativo | 400                   |
| L-07 | `test_nao_deve_fazer_login_sem_password`          | Negativo | 400                   |
| L-08 | `test_nao_deve_fazer_login_com_body_vazio`        | Negativo | 400                   |

**Fixtures utilizadas:** `login_client`, `usuario_admin_criado`, `usuario_comum_criado`

---

### 4.3 `/produtos` — ✅ Implementado

**Arquivo:** `tests/test_produtos.py`
**Marker:** `@pytest.mark.produtos`

#### GET /produtos

| #    | Função de teste                              | Tipo     | Status esperado |
| ---- | -------------------------------------------- | -------- | --------------- |
| P-01 | `test_deve_listar_produtos_sem_autenticacao` | Positivo | 200             |

#### POST /produtos

| #    | Função de teste                                              | Tipo      | Status esperado |
| ---- | ------------------------------------------------------------ | --------- | --------------- |
| P-02 | `test_deve_cadastrar_produto_com_token_admin`                | Positivo  | 201             |
| P-03 | `test_nao_deve_cadastrar_produto_sem_autenticacao`           | Segurança | 401             |
| P-04 | `test_nao_deve_cadastrar_produto_com_token_de_usuario_comum` | Segurança | 403             |
| P-05 | `test_nao_deve_cadastrar_produto_com_nome_duplicado`         | Negativo  | 400             |
| P-06 | `test_nao_deve_cadastrar_produto_sem_nome`                   | Negativo  | 400             |
| P-07 | `test_nao_deve_cadastrar_produto_sem_preco`                  | Negativo  | 400             |
| P-08 | `test_nao_deve_cadastrar_produto_sem_descricao`              | Negativo  | 400             |
| P-09 | `test_nao_deve_cadastrar_produto_sem_quantidade`             | Negativo  | 400             |

#### GET /produtos/{id}

| #    | Função de teste                                   | Tipo     | Status esperado |
| ---- | ------------------------------------------------- | -------- | --------------- |
| P-10 | `test_deve_buscar_produto_por_id_valido`          | Positivo | 200             |
| P-11 | `test_nao_deve_buscar_produto_com_id_inexistente` | Negativo | 400             |

#### PUT /produtos/{id}

| #    | Função de teste                                              | Tipo      | Status esperado |
| ---- | ------------------------------------------------------------ | --------- | --------------- |
| P-12 | `test_deve_atualizar_produto_com_token_admin`                | Positivo  | 200             |
| P-13 | `test_nao_deve_atualizar_produto_sem_autenticacao`           | Segurança | 401             |
| P-14 | `test_nao_deve_atualizar_produto_com_token_de_usuario_comum` | Segurança | 403             |

#### DELETE /produtos/{id}

| #    | Função de teste                                              | Tipo      | Status esperado |
| ---- | ------------------------------------------------------------ | --------- | --------------- |
| P-15 | `test_deve_excluir_produto_com_token_admin`                  | Positivo  | 200             |
| P-16 | `test_nao_deve_excluir_produto_sem_autenticacao`             | Segurança | 401             |
| P-17 | `test_deve_retornar_mensagem_ao_excluir_produto_inexistente` | Negativo  | 200             |

**Fixtures utilizadas:** `produtos_client`, `token_admin`, `token_usuario_comum`, `produto_payload`, `produto_criado`

**Observação:** durante os testes de produtos, foi identificado que a API retorna `200 OK` com `"Nenhum registro excluído"` ao tentar excluir um produto com ID válido, mas inexistente. Esse comportamento também ocorre em `/usuarios` e foi documentado na Issue #1 após investigação manual com Postman.

---

### 4.4 `/carrinhos` — ✅ Implementado

**Arquivo:** `tests/test_carrinhos.py`
**Marker:** `@pytest.mark.carrinhos`

#### GET /carrinhos

| #    | Função de teste                               | Tipo     | Status esperado |
| ---- | --------------------------------------------- | -------- | --------------- |
| C-01 | `test_deve_listar_carrinhos_sem_autenticacao` | Positivo | 200             |

#### POST /carrinhos

| #    | Função de teste                                                 | Tipo             | Status esperado |
| ---- | --------------------------------------------------------------- | ---------------- | --------------- |
| C-02 | `test_deve_criar_carrinho_com_produto_valido`                   | Positivo         | 201             |
| C-03 | `test_nao_deve_criar_carrinho_sem_autenticacao`                 | Segurança        | 401             |
| C-04 | `test_nao_deve_criar_segundo_carrinho_para_mesmo_usuario`       | Regra de negócio | 400             |
| C-05 | `test_nao_deve_criar_carrinho_com_produto_inexistente`          | Negativo         | 400             |
| C-06 | `test_nao_deve_criar_carrinho_com_quantidade_maior_que_estoque` | Negativo         | 400             |

#### GET /carrinhos/{id}

| #    | Função de teste                                    | Tipo     | Status esperado |
| ---- | -------------------------------------------------- | -------- | --------------- |
| C-07 | `test_deve_buscar_carrinho_por_id_valido`          | Positivo | 200             |
| C-08 | `test_nao_deve_buscar_carrinho_com_id_inexistente` | Negativo | 400             |

#### DELETE /carrinhos/concluir-compra

| #    | Função de teste                                               | Tipo      | Status esperado |
| ---- | ------------------------------------------------------------- | --------- | --------------- |
| C-09 | `test_deve_concluir_compra_e_decrementar_estoque`             | Positivo  | 200             |
| C-10 | `test_deve_retornar_mensagem_ao_concluir_compra_sem_carrinho` | Negativo  | 200             |
| C-11 | `test_nao_deve_concluir_compra_sem_autenticacao`              | Segurança | 401             |

#### DELETE /carrinhos/cancelar-compra

| #    | Função de teste                                               | Tipo      | Status esperado |
| ---- | ------------------------------------------------------------- | --------- | --------------- |
| C-12 | `test_deve_cancelar_compra_e_repor_estoque`                   | Positivo  | 200             |
| C-13 | `test_deve_retornar_mensagem_ao_cancelar_compra_sem_carrinho` | Negativo  | 200             |
| C-14 | `test_nao_deve_cancelar_compra_sem_autenticacao`              | Segurança | 401             |

**Fixtures utilizadas:** `carrinhos_client`, `produtos_client`, `usuario_com_token_e_produto`, `carrinho_criado`

**Observação:** os testes de carrinho criam dinamicamente um usuário autenticado e um produto disponível. A fixture `carrinho_criado` captura o estoque original do produto antes da criação do carrinho, permitindo validar os efeitos de concluir e cancelar compra sobre o estoque.

---

## 5. Investigação Exploratória e Bug Report

Além dos testes automatizados, foi realizada uma investigação manual exploratória usando o Postman.

Durante essa investigação, foi identificado um comportamento inconsistente da API: ao tentar excluir um recurso por um ID válido, mas inexistente na base, os endpoints `/usuarios` e `/produtos` retornam `200 OK` com `"Nenhum registro excluído"`, em vez de um status 4xx que indicaria explicitamente que o recurso não foi encontrado.

O comportamento foi verificado nos seguintes casos:

| Requisição                          | Resultado                          |
| ----------------------------------- | ---------------------------------- |
| `GET /produtos/{id_inexistente}`    | 400 + `"Produto não encontrado"`   |
| `DELETE /produtos/{id_inexistente}` | 200 + `"Nenhum registro excluído"` |
| `DELETE /produtos/id_invalido`      | 400 + validação de formato do ID   |
| `GET /usuarios/{id_inexistente}`    | 400 + `"Usuário não encontrado"`   |
| `DELETE /usuarios/{id_inexistente}` | 200 + `"Nenhum registro excluído"` |

**Resultado:** o comportamento foi documentado na Issue #1 do repositório:

[DELETE retorna 200 OK ao tentar excluir recurso inexistente](https://github.com/kanan-lopes/serverest-pytest-usuarios_DesafioBootcamp/issues/1)

---

## 6. Análise de Cobertura

A análise de cobertura foi feita com base na matriz inicial de cenários planejados no próprio plano de testes.

A primeira versão do plano previa:

| Grupo             | Cenários planejados inicialmente |
| ----------------- | -------------------------------: |
| `/usuarios`       |                               12 |
| `/login`          |                                8 |
| `/produtos`       |                               20 |
| `/carrinhos`      |                               17 |
| Fluxos integrados |                                3 |
| **Total**         |                           **60** |

Ao final do projeto, foram implementados:

| Grupo                      | Testes implementados |
| -------------------------- | -------------------: |
| `/usuarios`                |                   12 |
| `/login`                   |                    8 |
| `/produtos`                |                   17 |
| `/carrinhos`               |                   14 |
| Fluxos integrados isolados |                    0 |
| **Total**                  |               **51** |

### 6.1 Método de cálculo

A cobertura total foi calculada pela fórmula:

```text
Cobertura = (cenários automatizados / cenários planejados) × 100
```

Aplicando ao projeto:

```text
Cobertura = (51 / 60) × 100
Cobertura = 85%
```

Portanto, a cobertura total atingida foi de **85%** em relação à matriz inicial de cenários planejados.

### 6.2 Cobertura por grupo

| Grupo             | Implementados | Pendentes | Total planejado | Cobertura |
| ----------------- | ------------: | --------: | --------------: | --------: |
| `/usuarios`       |            12 |         0 |              12 |      100% |
| `/login`          |             8 |         0 |               8 |      100% |
| `/produtos`       |            17 |         3 |              20 |       85% |
| `/carrinhos`      |            14 |         3 |              17 |    82,35% |
| Fluxos integrados |             0 |         3 |               3 |        0% |
| **Total**         |        **51** |     **9** |          **60** |   **85%** |

### 6.3 Cobertura de endpoints e métodos principais

Embora a cobertura total por cenários tenha sido de **85%**, a suíte cobre os principais endpoints e métodos HTTP trabalhados no escopo do projeto:

| Endpoint                     | Métodos cobertos |
| ---------------------------- | ---------------- |
| `/usuarios`                  | GET, POST        |
| `/usuarios/{id}`             | GET, PUT, DELETE |
| `/login`                     | POST             |
| `/produtos`                  | GET, POST        |
| `/produtos/{id}`             | GET, PUT, DELETE |
| `/carrinhos`                 | GET, POST        |
| `/carrinhos/{id}`            | GET              |
| `/carrinhos/concluir-compra` | DELETE           |
| `/carrinhos/cancelar-compra` | DELETE           |

Com isso, os principais fluxos funcionais, negativos, de autenticação, de autorização e de regra de negócio foram exercitados pela suíte.

---

## 7. Critérios de Qualidade

Um teste é considerado pronto quando atende aos critérios abaixo:

### 7.1 Critérios funcionais

* [ ] Valida o status code esperado para o cenário.
* [ ] Valida o body da resposta quando aplicável.
* [ ] Valida mensagens de erro ou sucesso quando relevantes.
* [ ] Para criações, valida presença do campo `_id`.

### 7.2 Critérios de independência

* [ ] Não depende de estado deixado por outro teste.
* [ ] Usa dados únicos gerados dinamicamente.
* [ ] Realiza limpeza dos recursos criados.
* [ ] Pode ser executado isoladamente.

### 7.3 Critérios de estrutura

* [ ] Está em arquivo `test_*.py` correspondente ao endpoint.
* [ ] Possui docstring explicando objetivo e critérios verificados.
* [ ] Usa o marker correto do endpoint.
* [ ] Usa o client correspondente ao endpoint.
* [ ] Usa payloads gerados por data factory.

### 7.4 Critérios de execução

* [ ] Passa na execução individual.
* [ ] Passa na execução por marker.
* [ ] Passa na execução da suíte completa.
* [ ] Não deixa dados residuais no ambiente após a execução.

---

## 8. Estrutura de Arquivos

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
├── .gitignore
├── pytest.ini                   ✅ markers: usuarios, login, produtos, carrinhos
├── requirements.txt
├── README.md
└── PLANO-DE-TESTES.md           ✅ este arquivo
```

---

## 9. Resumo Final

| Indicador                                   | Resultado                                        |
| ------------------------------------------- | ------------------------------------------------ |
| Total de cenários planejados inicialmente   | 60                                               |
| Total de testes automatizados implementados | 51                                               |
| Cenários pendentes                          | 9                                                |
| Cobertura total por cenários                | 85%                                              |
| Endpoints automatizados                     | `/usuarios`, `/login`, `/produtos`, `/carrinhos` |
| Bug report aberto                           | Issue #1                                         |
| Ferramenta de investigação manual           | Postman                                          |
| Relatório de execução                       | Pytest HTML                                      |
