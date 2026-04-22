# Desafio Dev Junior

## Contexto

Voce recebeu um projeto base com API Flask, frontend simples, PostgreSQL e setup Docker.
O objetivo agora e evoluir a aplicacao mantendo clareza, qualidade de codigo e testes.

## Tempo sugerido

3 a 5 horas.

## O que ja existe

- CRUD parcial de tarefas
- frontend integrado ao backend
- testes unitarios e de integracao
- ambiente com Docker Compose e PostgreSQL ja integrado

## Entregas obrigatorias

1. Implementar `PUT /api/tasks/<task_id>` para permitir editar `title`, `description` e `priority`.
2. Implementar filtros em `GET /api/tasks` com query params `status` e `priority`.
3. Refletir os filtros e a edicao no frontend.
4. Adicionar testes automatizados cobrindo os novos cenarios.
5. Atualizar a documentacao com as decisoes tecnicas tomadas.
6. Entregar um documento descrevendo o uso de ferramentas de IA, quando houver.

## Extras opcionais

- adicionar migracao/versionamento simples do schema PostgreSQL
- adicionar ordenacao por data ou prioridade
- melhorar feedback visual de loading e erro
- incluir cobertura de testes maior

## Regras

- manter Flask no backend
- manter Bootstrap ou CSS simples no frontend
- nao remover o fluxo que ja funciona
- priorizar legibilidade e simplicidade
- e permitido usar ferramentas de IA
- se usar IA, entregar um documento com o que foi usado, objetivo de cada uso e o que foi aproveitado ou descartado
- anexar evidencias no documento, como prints de conversas, prompts, skills, agents ou ferramentas equivalentes

## O que esperamos ver

- commits ou entregas pequenas e coerentes
- validacao de entrada consistente
- codigo facil de ler
- separacao razoavel entre regra de negocio e HTTP
- testes que realmente protegem o comportamento

## Como validar

- `docker compose up --build`
- `pytest backend`
- validar o frontend em `http://localhost:8080`

## Entrega sobre IA

Se houver uso de IA, inclua um arquivo como `docs/uso-de-ia.md` com:

- ferramentas utilizadas
- contexto ou problema resolvido com cada ferramenta
- prompts ou instrucoes principais
- o que foi aceito, ajustado ou descartado
- prints ou registros das conversas, skills, agents ou recursos semelhantes
