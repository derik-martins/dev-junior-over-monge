# PRD

## Visao geral

O projeto representa um mini painel de tarefas usado como base para um teste tecnico de desenvolvimento junior.
O repositorio precisa oferecer uma experiencia simples para rodar, ler e evoluir.

## Problema

Times tecnicos frequentemente precisam avaliar fundamentos de backend, frontend, integracao e organizacao de projeto.
Muitos testes ficam abstratos demais ou dependem de contexto de negocio grande demais para um nivel junior.

## Objetivo

Entregar uma base funcional que permita avaliar:

- consumo de API em frontend simples
- organizacao de backend Flask
- capacidade de evoluir endpoints com seguranca
- uso de testes automatizados
- clareza de documentacao e setup

## Usuario alvo

- recrutador tecnico
- lider tecnico
- dev junior participante do teste

## Escopo do MVP

- API Flask para gestao de tarefas
- frontend simples em Bootstrap e JavaScript puro
- listagem, cadastro, atualizacao de status e remocao
- resumo por status e prioridade
- setup com Docker Compose
- estrutura de testes unitarios e de integracao

## Fora de escopo nesta versao

- autenticacao
- banco relacional em producao
- paginacao
- upload de arquivos
- multiusuario

## Requisitos funcionais

- o usuario deve conseguir visualizar a lista de tarefas
- o usuario deve conseguir cadastrar uma nova tarefa
- o usuario deve conseguir alterar o status de uma tarefa
- o usuario deve conseguir remover uma tarefa
- o usuario deve visualizar um resumo consolidado do painel

## Requisitos nao funcionais

- o projeto deve subir com um unico comando em Docker
- a API deve responder em JSON de forma consistente
- a base deve ser simples o suficiente para um teste de 3 a 5 horas
- a estrutura deve incentivar TDD e testes pequenos

## Criterios de sucesso

- um candidato consegue subir o projeto sem ajuda externa
- o avaliador consegue testar a API e a integracao visual rapidamente
- a base permite adicionar novas features sem refatoracao grande
