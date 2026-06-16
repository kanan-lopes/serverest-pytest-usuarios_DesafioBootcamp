# Plano de Testes — ServeRest API

**Projeto:** Automação de testes para a API ServeRest
**Base URL:** `https://compassuol.serverest.dev`
**Stack:** Python · Pytest · Requests · jsonschema · GitHub Actions
**Data de criação:** Junho/2026
**Última atualização:** Junho/2026

---

## 1. Objetivos

O endpoint `/usuarios` já contava inicialmente com cobertura sólida: 12 testes automatizados exercitando os principais verbos HTTP do endpoint (GET, POST, PUT, DELETE), incluindo cenários de sucesso, campos obrigatórios ausentes, IDs inexistentes e email duplicado.

O objetivo da expansão da suíte foi cobrir os demais endpoints da ServeRest com o mesmo nível de qualidade, garantindo que os fluxos de autenticação, gerenciamento de produtos e operações de carrinho fossem validados de forma automatizada, independente e rastreável.

A suíte também passou a contemplar dois desafios extras: validação estrutural das respostas com **JSON Schema** e execução automática dos testes via **GitHub Actions**.

### Metas específicas

* Validar autenticação via `/login` e o uso do token Bearer nos endpoints protegidos. ✅
* Cobrir o CRUD de `/produtos` com e sem autenticação. ✅
* Cobrir o ciclo de vida do carrinho em `/carrinhos`, incluindo regras de negócio. ✅
* Validar a estrutura das respostas via JSON Schema em pelo menos 3 endpoints. ✅
* Configurar GitHub Actions para execução automática a cada push/pull request. ✅
* Detectar regressões nos fluxos críticos da API a cada execução da suíte. ✅
* Registrar comportamentos suspeitos por meio de investigação exploratória e bug report. ✅

---

## 2. Estratégias de Teste

### 2.1 Tipos de teste aplicados

| Tipo                      | Descrição                                                                  | Aplicação neste projeto                                                 |
| ------------------------- | -------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Funcional caixa-preta     | Valida entradas e saídas conforme o comportamento esperado da API          | Todos os endpoints                                                      |
| Positivo                  | Fluxos com dados válidos e pré-condições atendidas                         | Criação, listagem, busca, atualização, exclusão, login e carrinho       |
| Negativo                  | Dados inválidos, campos ausentes, IDs inexistentes ou regras violadas      | Validações 4xx e comportamentos não permitidos                          |
| Contrato / JSON Schema    | Verifica estrutura da resposta: campos obrigatórios e tipos                | `tests/test_contratos.py`                                               |
| Regra de negócio          | Valida restrições específicas do domínio                                   | Carrinho único, estoque insuficiente, decremento e reposição de estoque |
| Segurança básica          | Verifica acesso a recursos protegidos sem token ou com token sem permissão | Produtos e carrinhos                                                    |
| Investigação exploratória | Explora comportamentos suspeitos fora da automação principal               | Postman e Issue #1                                                      |

### 2.2 Camada de teste

Todos os testes operam na **camada de API**, realizando chamadas reais contra o ambiente público da ServeRest. Não foram utilizados mocks.

A ServeRest é uma API pública de prática; portanto, o ambiente testado é compartilhado e pode apresentar instabilidades pontuais. Respostas como `503 Service Unavailable` devem ser investigadas e o teste deve ser reexecutado isoladamente para diferenciar instabilidade de infraestrutura de falha funcional.

### 2.3 Ferramentas

| Ferramenta     | Uso                                                                    |
| -------------- | ---------------------------------------------------------------------- |
| Pytest         | Framework principal de testes                                          |
| Requests       | Biblioteca HTTP para chamadas à API                                    |
| jsonschema     | Validação estrutural de respostas via JSON Schema                      |
| pytest-html    | Geração de relatório HTML após execução                                |
| python-dotenv  | Configuração da `BASE_URL` via variável de ambiente                    |
| uuid4          | Geração de dados únicos para isolamento de testes                      |
| GitHub Actions | Execução automática da suíte a cada push/pull request                  |
| Postman        | Investigação exploratória manual e validação de comportamento suspeito |

### 2.4 Padrões adotados

* **Client pattern:** cada endpoint possui seu próprio client (`UsuariosClient`, `LoginClient`, `ProdutosClient`, `CarrinhosClient`), centralizando chamadas HTTP e evitando `requests.*` diretamente nos testes.
* **Data factory:** payloads são gerados por funções em `utils/data_factory.py`, reduzindo duplicação e evitando dados fixos.
* **Fixtures com `yield`:** pré-condições são criadas antes do teste e limpezas são executadas depois do teste.
* **Dados dinâmicos:** emails, nomes de produtos e IDs inexistentes válidos são gerados dinamicamente com `uuid4`.
* **Markers por endpoint:** os testes são organizados com `@pytest.mark.usuarios`, `@pytest.mark.login`, `@pytest.mark.produtos`, `@pytest.mark.carrinhos` e `@pytest.mark.contrato`.
* **Independência dos testes:** nenhum teste depende do estado deixado por outro.
* **Limpeza de dados:** usuários, produtos e carrinhos criados durante os testes são removidos ou cancelados ao final da execução.
* **Tokens dinâmicos:** os tokens são obtidos por fixtures que criam usuários, realizam login e retornam o Bearer token.
* **JSON Schema:** schemas ficam organizados em `schemas/` e são validados com `jsonschema.validate(instance=body, schema=schema)`.
* **CI/CD:** GitHub Actions executa a suíte completa automaticamente a cada push e pull request.

---

## 3. Escopo

### 3.1 Escopo implementado

| Endpoint                     | Método | Cenários cobertos                                                                       | Testes funcionais | Testes de contrato |
| ---------------------------- | ------ | --------------------------------------------------------------------------------------- | ----------------: | -----------------: |
| `/usuarios`                  | GET    | Listar usuários                                                                         |                 1 |                  1 |
| `/usuarios`                  | POST   | Cadastro válido, email duplicado, campos obrigatórios ausentes                          |                 6 |                  1 |
| `/usuarios/{id}`             | GET    | Busca por ID válido e ID inexistente                                                    |                 2 |                  1 |
| `/usuarios/{id}`             | PUT    | Atualização de usuário existente                                                        |                 1 |                  0 |
| `/usuarios/{id}`             | DELETE | Exclusão de usuário existente e ID inexistente                                          |                 2 |                  0 |
| `/login`                     | POST   | Login válido, login inválido, campos ausentes e validação de token                      |                 8 |                  2 |
| `/produtos`                  | GET    | Listagem de produtos                                                                    |                 1 |                  1 |
| `/produtos`                  | POST   | Cadastro válido, autenticação, autorização, nome duplicado e campos ausentes            |                 8 |                  1 |
| `/produtos/{id}`             | GET    | Busca por ID válido e ID inexistente                                                    |                 2 |                  1 |
| `/produtos/{id}`             | PUT    | Atualização válida, sem autenticação e usuário sem permissão                            |                 3 |                  0 |
| `/produtos/{id}`             | DELETE | Exclusão válida, sem autenticação e ID inexistente                                      |                 3 |                  0 |
| `/carrinhos`                 | GET    | Listagem de carrinhos                                                                   |                 1 |                  1 |
| `/carrinhos`                 | POST   | Criação válida, sem token, segundo carrinho, produto inexistente e estoque insuficiente |                 5 |                  1 |
| `/carrinhos/{id}`            | GET    | Busca por ID válido e ID inexistente                                                    |                 2 |                  1 |
| `/carrinhos/concluir-compra` | DELETE | Concluir compra, concluir sem carrinho e concluir sem token                             |                 3 |                  0 |
| `/carrinhos/cancelar-compra` | DELETE | Cancelar compra, cancelar sem carrinho e cancelar sem token                             |                 3 |                  0 |

**Total implementado:** 51 testes funcionais/regra/segurança + 11 testes de contrato = **62 testes automatizados**.

### 3.2 Cenários pendentes em relação à matriz inicial

A primeira versão do plano previa 60 cenários no total. Ao final da implementação funcional, 51 testes haviam sido implementados. Com a inclusão dos testes de contrato, dois cenários inicialmente pendentes passaram a ser cobertos:

* validação estrutural da listagem de produtos;
* validação estrutural da listagem de carrinhos.

Assim, a suíte passou a cobrir **53 dos 60 cenários da matriz inicial**, restando **7 cenários pendentes**.

| Cenário pendente                                          | Justificativa                                                                                                           |
| --------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Atualizar produto com ID inexistente criando novo produto | Cenário específico da regra de `PUT`; pode gerar criação residual e exige investigação isolada.                         |
| Tentar excluir produto que está em um carrinho            | Depende de estado compartilhado entre produto e carrinho; permanece como investigação futura.                           |
| Criar carrinho sem campo `produtos`                       | Cenário negativo válido, mas não automatizado nesta versão.                                                             |
| Criar carrinho com lista de produtos vazia                | Cenário negativo válido, mas não automatizado nesta versão.                                                             |
| Fluxo integrado F-01 — ciclo completo de compra           | Parte do comportamento foi coberta nos testes de carrinho, mas o fluxo E2E completo não foi isolado como teste próprio. |
| Fluxo integrado F-02 — ciclo de cancelamento              | Parte do comportamento foi coberta nos testes de carrinho, mas o fluxo E2E completo não foi isolado como teste próprio. |
| Fluxo integrado F-03 — produto em uso                     | Relacionado à tentativa de excluir produto vinculado a carrinho; permanece como investigação futura.                    |

### 3.3 Fora do escopo geral do projeto

| Item                                            | Justificativa                             |
| ----------------------------------------------- | ----------------------------------------- |
| Testes de performance/carga                     | Fora do objetivo do desafio atual.        |
| Testes de UI ou E2E com browser                 | Projeto focado em testes de API.          |
| Testes de segurança avançados                   | Fora do escopo de QA funcional proposto.  |
| Testes de contrato formal com Pact              | Não há consumer separado no projeto.      |
| Filtros e combinações avançadas de query params | Podem ser adicionados em iteração futura. |

---

## 4. Cenários Implementados

### 4.1 `/usuarios` — Implementado

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

---

### 4.2 `/login` — Implementado

**Arquivo:** `tests/test_login.py`
**Marker:** `@pytest.mark.login`

| #    | Função de teste                                   | Tipo            | Status esperado       |
| ---- | ------------------------------------------------- | --------------- | --------------------- |
| L-01 | `test_deve_fazer_login_com_usuario_administrador` | Positivo        | 200 + token Bearer    |
| L-02 | `test_deve_fazer_login_com_usuario_comum`         | Positivo        | 200 + token Bearer    |
| L-03 | `test_token_retornado_deve_ser_string_nao_vazia`  | Contrato básico | 200 + token não vazio |
| L-04 | `test_nao_deve_fazer_login_com_senha_errada`      | Negativo        | 401                   |
| L-05 | `test_nao_deve_fazer_login_com_email_inexistente` | Negativo        | 401                   |
| L-06 | `test_nao_deve_fazer_login_sem_email`             | Negativo        | 400                   |
| L-07 | `test_nao_deve_fazer_login_sem_password`          | Negativo        | 400                   |
| L-08 | `test_nao_deve_fazer_login_com_body_vazio`        | Negativo        | 400                   |

---

### 4.3 `/produtos` — Implementado

**Arquivo:** `tests/test_produtos.py`
**Marker:** `@pytest.mark.produtos`

| #    | Função de teste                                              | Tipo      | Status esperado |
| ---- | ------------------------------------------------------------ | --------- | --------------- |
| P-01 | `test_deve_listar_produtos_sem_autenticacao`                 | Positivo  | 200             |
| P-02 | `test_deve_cadastrar_produto_com_token_admin`                | Positivo  | 201             |
| P-03 | `test_nao_deve_cadastrar_produto_sem_autenticacao`           | Segurança | 401             |
| P-04 | `test_nao_deve_cadastrar_produto_com_token_de_usuario_comum` | Segurança | 403             |
| P-05 | `test_nao_deve_cadastrar_produto_com_nome_duplicado`         | Negativo  | 400             |
| P-06 | `test_nao_deve_cadastrar_produto_sem_nome`                   | Negativo  | 400             |
| P-07 | `test_nao_deve_cadastrar_produto_sem_preco`                  | Negativo  | 400             |
| P-08 | `test_nao_deve_cadastrar_produto_sem_descricao`              | Negativo  | 400             |
| P-09 | `test_nao_deve_cadastrar_produto_sem_quantidade`             | Negativo  | 400             |
| P-10 | `test_deve_buscar_produto_por_id_valido`                     | Positivo  | 200             |
| P-11 | `test_nao_deve_buscar_produto_com_id_inexistente`            | Negativo  | 400             |
| P-12 | `test_deve_atualizar_produto_com_token_admin`                | Positivo  | 200             |
| P-13 | `test_nao_deve_atualizar_produto_sem_autenticacao`           | Segurança | 401             |
| P-14 | `test_nao_deve_atualizar_produto_com_token_de_usuario_comum` | Segurança | 403             |
| P-15 | `test_deve_excluir_produto_com_token_admin`                  | Positivo  | 200             |
| P-16 | `test_nao_deve_excluir_produto_sem_autenticacao`             | Segurança | 401             |
| P-17 | `test_deve_retornar_mensagem_ao_excluir_produto_inexistente` | Negativo  | 200             |

---

### 4.4 `/carrinhos` — Implementado

**Arquivo:** `tests/test_carrinhos.py`
**Marker:** `@pytest.mark.carrinhos`

| #    | Função de teste                                                 | Tipo             | Status esperado |
| ---- | --------------------------------------------------------------- | ---------------- | --------------- |
| C-01 | `test_deve_listar_carrinhos_sem_autenticacao`                   | Positivo         | 200             |
| C-02 | `test_deve_criar_carrinho_com_produto_valido`                   | Positivo         | 201             |
| C-03 | `test_nao_deve_criar_carrinho_sem_autenticacao`                 | Segurança        | 401             |
| C-04 | `test_nao_deve_criar_segundo_carrinho_para_mesmo_usuario`       | Regra de negócio | 400             |
| C-05 | `test_nao_deve_criar_carrinho_com_produto_inexistente`          | Negativo         | 400             |
| C-06 | `test_nao_deve_criar_carrinho_com_quantidade_maior_que_estoque` | Negativo         | 400             |
| C-07 | `test_deve_buscar_carrinho_por_id_valido`                       | Positivo         | 200             |
| C-08 | `test_nao_deve_buscar_carrinho_com_id_inexistente`              | Negativo         | 400             |
| C-09 | `test_deve_concluir_compra_e_decrementar_estoque`               | Positivo/regra   | 200             |
| C-10 | `test_deve_retornar_mensagem_ao_concluir_compra_sem_carrinho`   | Negativo         | 200             |
| C-11 | `test_nao_deve_concluir_compra_sem_autenticacao`                | Segurança        | 401             |
| C-12 | `test_deve_cancelar_compra_e_repor_estoque`                     | Positivo/regra   | 200             |
| C-13 | `test_deve_retornar_mensagem_ao_cancelar_compra_sem_carrinho`   | Negativo         | 200             |
| C-14 | `test_nao_deve_cancelar_compra_sem_autenticacao`                | Segurança        | 401             |

---

### 4.5 Testes de contrato com JSON Schema — Extra 1 Implementado

**Arquivo:** `tests/test_contratos.py`
**Markers:** `@pytest.mark.<endpoint>` + `@pytest.mark.contrato`

Os schemas ficam em `schemas/`, organizados por endpoint. A validação usa:

```python
jsonschema.validate(instance=body, schema=SCHEMA_X)
```

| #    | Função de teste                      | Endpoint validado     | Schema utilizado                |
| ---- | ------------------------------------ | --------------------- | ------------------------------- |
| S-01 | `test_schema_listar_usuarios`        | GET `/usuarios`       | `SCHEMA_LISTAR_USUARIOS`        |
| S-02 | `test_schema_cadastrar_usuario`      | POST `/usuarios`      | `SCHEMA_CADASTRAR_USUARIO`      |
| S-03 | `test_schema_buscar_usuario_por_id`  | GET `/usuarios/{id}`  | `SCHEMA_BUSCAR_USUARIO_POR_ID`  |
| S-04 | `test_schema_login_sucesso`          | POST `/login`         | `SCHEMA_LOGIN_SUCESSO`          |
| S-05 | `test_schema_login_erro_credenciais` | POST `/login`         | `SCHEMA_LOGIN_ERRO_CREDENCIAIS` |
| S-06 | `test_schema_listar_produtos`        | GET `/produtos`       | `SCHEMA_LISTAR_PRODUTOS`        |
| S-07 | `test_schema_cadastrar_produto`      | POST `/produtos`      | `SCHEMA_CADASTRAR_PRODUTO`      |
| S-08 | `test_schema_buscar_produto_por_id`  | GET `/produtos/{id}`  | `SCHEMA_BUSCAR_PRODUTO_POR_ID`  |
| S-09 | `test_schema_listar_carrinhos`       | GET `/carrinhos`      | `SCHEMA_LISTAR_CARRINHOS`       |
| S-10 | `test_schema_criar_carrinho`         | POST `/carrinhos`     | `SCHEMA_CRIAR_CARRINHO`         |
| S-11 | `test_schema_buscar_carrinho_por_id` | GET `/carrinhos/{id}` | `SCHEMA_BUSCAR_CARRINHO_POR_ID` |

**Endpoints validados por JSON Schema:** `/usuarios`, `/login`, `/produtos`, `/carrinhos`.

---

## 5. GitHub Actions — Extra 2 Implementado

**Arquivo:** `.github/workflows/tests.yml`

O workflow executa automaticamente a suíte completa em dois gatilhos:

* `push` em qualquer branch;
* `pull_request` em qualquer branch.

### Passos do job

1. Checkout do repositório com `actions/checkout@v4`.
2. Configuração do Python 3.13 com `actions/setup-python@v5`.
3. Instalação das dependências com `pip install -r requirements.txt`.
4. Execução dos testes com:

```bash
pytest -vv --html=reports/relatorio.html --self-contained-html
```

5. Upload do relatório HTML como artefato com `actions/upload-artifact@v4`.

Nenhum secret ou credencial é necessário, pois a ServeRest é uma API pública.

---

## 6. Investigação Exploratória e Bug Report

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

Resultado documentado na Issue #1 do repositório:

[DELETE retorna 200 OK ao tentar excluir recurso inexistente](https://github.com/kanan-lopes/serverest-pytest-usuarios_DesafioBootcamp/issues/1)

---

## 7. Análise de Cobertura

A análise de cobertura foi feita com base na matriz inicial de cenários planejados no próprio plano de testes.

### 7.1 Matriz inicial

A primeira versão do plano previa:

| Grupo             | Cenários planejados inicialmente |
| ----------------- | -------------------------------: |
| `/usuarios`       |                               12 |
| `/login`          |                                8 |
| `/produtos`       |                               20 |
| `/carrinhos`      |                               17 |
| Fluxos integrados |                                3 |
| **Total**         |                           **60** |

### 7.2 Cobertura após implementação funcional

Após a implementação dos testes funcionais, de regra de negócio e de segurança básica, foram cobertos 51 cenários da matriz inicial.

| Grupo                      | Cenários cobertos |
| -------------------------- | ----------------: |
| `/usuarios`                |                12 |
| `/login`                   |                 8 |
| `/produtos`                |                17 |
| `/carrinhos`               |                14 |
| Fluxos integrados isolados |                 0 |
| **Total**                  |            **51** |

### 7.3 Impacto dos testes de contrato

Com a inclusão dos testes de contrato via JSON Schema, dois cenários que estavam previstos na matriz inicial passaram a ser cobertos:

| Cenário da matriz inicial                                  | Teste que passou a cobrir      |
| ---------------------------------------------------------- | ------------------------------ |
| Validar estrutura do item retornado em `GET /produtos`     | `test_schema_listar_produtos`  |
| Validar estrutura dos itens retornados em `GET /carrinhos` | `test_schema_listar_carrinhos` |

Os demais testes de contrato são considerados reforço de qualidade e robustez do contrato, mas não aumentam diretamente a contagem de cenários da matriz inicial, pois validam estruturalmente respostas de cenários já cobertos funcionalmente.

### 7.4 Cobertura final da matriz inicial

```text
Cobertura = (cenários da matriz inicial cobertos / cenários planejados inicialmente) × 100
Cobertura = (53 / 60) × 100
Cobertura = 88,33%
```

| Métrica                              | Resultado |
| ------------------------------------ | --------: |
| Cenários planejados inicialmente     |        60 |
| Cenários da matriz inicial cobertos  |        53 |
| Cenários pendentes da matriz inicial |         7 |
| Cobertura da matriz inicial          |    88,33% |
| Testes funcionais/regra/segurança    |        51 |
| Testes de contrato JSON Schema       |        11 |
| Total de testes automatizados        |        62 |

### 7.5 Cobertura por grupo

| Grupo             | Cenários planejados | Cenários cobertos da matriz inicial | Pendentes |  Cobertura |
| ----------------- | ------------------: | ----------------------------------: | --------: | ---------: |
| `/usuarios`       |                  12 |                                  12 |         0 |       100% |
| `/login`          |                   8 |                                   8 |         0 |       100% |
| `/produtos`       |                  20 |                                  18 |         2 |        90% |
| `/carrinhos`      |                  17 |                                  15 |         2 |     88,24% |
| Fluxos integrados |                   3 |                                   0 |         3 |         0% |
| **Total**         |              **60** |                              **53** |     **7** | **88,33%** |

### 7.6 Cenários pendentes

| Cenário pendente                                          | Justificativa                                                                                                         |
| --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Atualizar produto com ID inexistente criando novo produto | Cenário específico da regra de `PUT`; pode gerar criação residual e exige investigação isolada.                       |
| Tentar excluir produto que está em um carrinho            | Depende de estado compartilhado entre produto e carrinho; permanece como investigação futura.                         |
| Criar carrinho sem campo `produtos`                       | Cenário negativo válido, mas não automatizado nesta versão.                                                           |
| Criar carrinho com lista de produtos vazia                | Cenário negativo válido, mas não automatizado nesta versão.                                                           |
| Fluxo integrado F-01 — ciclo completo de compra           | Parte do comportamento foi coberta nos testes de carrinho, mas o fluxo E2E completo não foi isolado em teste próprio. |
| Fluxo integrado F-02 — ciclo de cancelamento              | Parte do comportamento foi coberta nos testes de carrinho, mas o fluxo E2E completo não foi isolado em teste próprio. |
| Fluxo integrado F-03 — produto em uso                     | Relacionado à tentativa de excluir produto vinculado a carrinho; permanece como investigação futura.                  |

---

## 8. Critérios de Qualidade

Um teste é considerado pronto quando atende aos critérios abaixo.

### 8.1 Critérios funcionais

* [ ] Valida o status code esperado para o cenário.
* [ ] Valida o body da resposta quando aplicável.
* [ ] Valida mensagens de erro ou sucesso quando relevantes.
* [ ] Para criações, valida presença do campo `_id`.

### 8.2 Critérios de independência

* [ ] Não depende de estado deixado por outro teste.
* [ ] Usa dados únicos gerados dinamicamente.
* [ ] Realiza limpeza dos recursos criados.
* [ ] Pode ser executado isoladamente.

### 8.3 Critérios de estrutura

* [ ] Está em arquivo `test_*.py` correspondente ao endpoint.
* [ ] Possui docstring explicando objetivo e critérios verificados.
* [ ] Usa o marker correto do endpoint.
* [ ] Usa o client correspondente ao endpoint.
* [ ] Usa payloads gerados por data factory.

### 8.4 Critérios de execução

* [ ] Passa na execução individual.
* [ ] Passa na execução por marker.
* [ ] Passa na execução da suíte completa.
* [ ] Não deixa dados residuais no ambiente após a execução.

### 8.5 Critérios para testes de contrato

* [ ] Schema definido em `schemas/<endpoint>_schema.py`.
* [ ] Validação feita com `jsonschema.validate(instance=body, schema=SCHEMA_X)`.
* [ ] Schema cobre campos obrigatórios e tipos esperados.
* [ ] Schema evita valores fixos em campos dinâmicos.
* [ ] Teste usa client e fixture do projeto, sem `requests.*` diretamente.

### 8.6 Critérios para CI/CD

* [ ] Workflow localizado em `.github/workflows/tests.yml`.
* [ ] Execução automática em `push` e `pull_request`.
* [ ] Instala dependências via `requirements.txt`.
* [ ] Executa a suíte completa com Pytest.
* [ ] Gera relatório HTML como artefato.

---

## 9. Estrutura de Arquivos

```text
serverest-pytest-usuarios/
│
├── .github/
│   └── workflows/
│       └── tests.yml            ✅ CI/CD GitHub Actions
│
├── clients/
│   ├── usuarios_client.py       ✅
│   ├── login_client.py          ✅
│   ├── produtos_client.py       ✅
│   ├── carrinhos_client.py      ✅
│   └── __init__.py
│
├── schemas/
│   ├── usuarios_schema.py       ✅ schemas de /usuarios
│   ├── login_schema.py          ✅ schemas de /login
│   ├── produtos_schema.py       ✅ schemas de /produtos
│   ├── carrinhos_schema.py      ✅ schemas de /carrinhos
│   └── __init__.py
│
├── tests/
│   ├── conftest.py              ✅ fixtures de infra, usuários, tokens, produtos e carrinhos
│   ├── test_usuarios.py         ✅ 12 testes funcionais
│   ├── test_login.py            ✅ 8 testes funcionais
│   ├── test_produtos.py         ✅ 17 testes funcionais
│   ├── test_carrinhos.py        ✅ 14 testes funcionais
│   └── test_contratos.py        ✅ 11 testes de contrato JSON Schema
│
├── utils/
│   ├── data_factory.py          ✅ geradores de usuário, credenciais, produto e carrinho
│   └── __init__.py
│
├── .env.example
├── .gitignore
├── pytest.ini                   ✅ markers: usuarios, login, produtos, carrinhos, contrato
├── requirements.txt             ✅ inclui jsonschema==4.23.0
├── README.md
└── PLANO-DE-TESTES.md           ✅ este arquivo
```

---

## 10. Resumo Final

| Indicador                                 | Resultado                                        |
| ----------------------------------------- | ------------------------------------------------ |
| Total de cenários planejados inicialmente | 60                                               |
| Cenários da matriz inicial cobertos       | 53                                               |
| Cenários pendentes da matriz inicial      | 7                                                |
| Cobertura da matriz inicial               | 88,33%                                           |
| Testes funcionais/regra/segurança         | 51                                               |
| Testes de contrato JSON Schema            | 11                                               |
| Total de testes automatizados             | 62                                               |
| Endpoints automatizados                   | `/usuarios`, `/login`, `/produtos`, `/carrinhos` |
| Endpoints validados por JSON Schema       | `/usuarios`, `/login`, `/produtos`, `/carrinhos` |
| Bug report aberto                         | Issue #1                                         |
| Ferramenta de investigação manual         | Postman                                          |
| CI/CD                                     | GitHub Actions                                   |
| Relatório de execução                     | Pytest HTML                                      |
