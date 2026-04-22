# Design Tecnico

## Arquitetura

O projeto esta dividido em dois servicos:

- `backend`: API Flask com regras de negocio, validacao e testes
- `frontend`: pagina estatica em Bootstrap servida por Nginx

O frontend usa chamadas HTTP para `/api/*`.
No ambiente Docker, o Nginx faz proxy dessas requisicoes para o container `backend`.

## Estrutura do backend

- `app/__init__.py`: app factory, configuracao e tratamento de erros
- `app/api.py`: endpoints HTTP
- `app/service.py`: regras de negocio e validacao
- `app/repository.py`: repositorio em memoria
- `app/models.py`: modelo da entidade `Task`
- `tests/unit`: testes das regras de negocio
- `tests/integration`: testes HTTP usando `FlaskClient`

## Modelo de dados

Entidade `Task`:

- `id`
- `title`
- `description`
- `priority`
- `status`
- `created_at`
- `updated_at`

Valores previstos:

- `priority`: `low`, `medium`, `high`
- `status`: `todo`, `doing`, `done`

## Contrato da API

- `GET /api/health`: status da aplicacao
- `GET /api/tasks`: retorna `{"items": [...]}`
- `GET /api/tasks/summary`: retorna total por status e prioridade
- `GET /api/tasks/<task_id>`: retorna uma tarefa
- `POST /api/tasks`: cria uma tarefa
- `PATCH /api/tasks/<task_id>/status`: atualiza somente status
- `DELETE /api/tasks/<task_id>`: remove uma tarefa

## Estrutura do frontend

- `public/index.html`: layout e pontos de montagem
- `public/app.js`: fetch da API, renderizacao e interacoes
- `public/styles.css`: tema visual simples

## Fluxo principal

- carregar resumo e lista de tarefas
- criar tarefa via formulario
- atualizar status por seletor em cada card
- remover tarefa e recarregar o painel

## Estrategia de testes

- testes unitarios para validacao e regras de negocio
- testes de integracao para o contrato HTTP
- repositorio em memoria para manter testes pequenos e deterministas

## Decisoes de design

- Flask foi escolhido pela simplicidade e boa aderencia a testes pequenos
- JavaScript puro evita acoplamento com frameworks desnecessarios para o desafio
- Bootstrap acelera a camada visual e reduz tempo de setup
- Nginx no frontend simplifica proxy e entrega estatica

## Evolucoes esperadas para o desafio

- edicao completa de tarefa
- filtros por status e prioridade
- testes adicionais guiados por TDD
- opcionalmente persistencia real
