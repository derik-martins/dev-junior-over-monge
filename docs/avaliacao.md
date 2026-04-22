# Criterios de Avaliacao

## Pontos para analisar

- o candidato entendeu o contrato atual e evoluiu sem quebrar o que ja existia
- os endpoints novos estao corretos e validam entradas ruins
- a organizacao do codigo continuou simples e consistente
- a cobertura de testes cresceu junto com as features
- a integracao frontend e backend funciona sem gambiarra
- a integracao com PostgreSQL continua funcional e previsivel
- o Docker continua funcional e previsivel
- a documentacao ajuda a executar e revisar a entrega
- se houve uso de IA, o registro de uso esta claro, honesto e auditavel

## Sinais de uma boa entrega

- testes pequenos, claros e com foco no comportamento
- mensagens de erro coerentes e em JSON
- mudancas localizadas, sem espalhar regra de negocio pelo projeto inteiro
- frontend com estado minimo, mas bem tratado
- README atualizado com passos reais de execucao
- uso de IA documentado com contexto, criterio e evidencias

## Alertas

- logica importante duplicada entre rota e service
- validacoes faltando ou inconsistentes
- codigo excessivamente complexo para um escopo simples
- frontend dependente de valores hardcoded sem justificativa
- ausencia de testes para o que foi alterado
- uso de IA sem transparencia ou sem evidencias minimas do processo

## Resultado esperado

Ao final do teste, a pessoa avaliadora deve conseguir responder:

- a solucao funciona de ponta a ponta
- o candidato consegue trabalhar com TDD ou ao menos com mentalidade orientada a testes
- o candidato tem base para manter uma API Flask simples
- o candidato entende integracao basica entre frontend e backend

## Sugestao de peso por criterio

- corretude funcional: 35%
- qualidade de codigo: 25%
- testes: 20%
- integracao e UX basica: 10%
- documentacao: 10%
