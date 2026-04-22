# Flask Junior Challenge

Projeto base para um teste tecnico com backend em Flask, frontend estatico com Bootstrap, persistencia em PostgreSQL e orquestracao com Docker.

## O que esta pronto

- API REST simples para tarefas
- Frontend basico consumindo a API
- Persistencia de tarefas em PostgreSQL quando executado via Docker Compose
- Estrutura inicial de TDD com `pytest`
- Dockerfiles separados para frontend e backend
- `docker-compose.yml` para subir tudo junto
- Documentacao do PRD, design, desafio e criterios de avaliacao

## Estrutura

```text
backend/
  app/
  tests/
frontend/
  public/
docs/
docker-compose.yml
README.md
```

## Executar com Docker

```bash
docker compose up --build
```

URLs:

- Frontend: `http://localhost:8080`
- API: `http://localhost:5000/api/health`
- PostgreSQL: `localhost:5432`

Credenciais padrao do banco no ambiente Docker:

- Banco: `junior_challenge`
- Usuario: `junior`
- Senha: `junior`

## Executar backend localmente

```bash
python -m venv backend/.venv
backend/.venv/Scripts/python -m pip install -r backend/requirements.txt
backend/.venv/Scripts/python -m pytest backend
backend/.venv/Scripts/python backend/wsgi.py
```

Por padrao, a execucao local sem `DATABASE_URL` usa repositorio em memoria para manter o setup leve.
Para rodar localmente com PostgreSQL, defina:

```bash
set TASKS_REPOSITORY=postgres
set DATABASE_URL=postgresql://junior:junior@localhost:5432/junior_challenge
backend/.venv/Scripts/python backend/wsgi.py
```

## Endpoints atuais

- `GET /api/health`
- `GET /api/tasks`
- `GET /api/tasks/summary`
- `GET /api/tasks/<task_id>`
- `POST /api/tasks`
- `PATCH /api/tasks/<task_id>/status`
- `DELETE /api/tasks/<task_id>`

## Documentacao

- [PRD](./docs/prd.md)
- [Design](./docs/design.md)
- [Desafio do dev junior](./docs/desafio-junior.md)
- [Criterios de avaliacao](./docs/avaliacao.md)
