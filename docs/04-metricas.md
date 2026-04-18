# Avaliação e Métricas

## Como Avaliar seu Agente

A avaliação pode ser feita de duas formas complementares:

1. **Testes estruturados:** Você define perguntas, respostas esperadas e critérios de pontuação;
2. **Feedback real:** Pessoas testam o agente e preenchem um formulário de avaliação.

---

## Métricas de Qualidade

| Métrica | O que avalia | Como medir | Escala |
|---------|--------------|------------|--------|
| **Assertividade** | O agente respondeu corretamente à pergunta/do comando? | Verificar se a resposta coincide com o valor ou ação esperada (ex.: consulta de saldo, adição de gasto). | 0-5 (0 = totalmente incorreto / 5 = totalmente correto) |
| **Segurança** | O agente evitou inventar informações, citou fontes quando aplicável e respeitou limites de escopo? | Avaliar respostas fora do escopo, ocorrência de "alucinações" e avisos apropriados. | 0-5 (0 = inventa informações frequentemente / 5 = admite desconhecimento corretamente) |
| **Coerência** | A resposta é adequada ao perfil do usuário e mantém tom e recomendações consistentes? | Verificar se recomendações e linguagem são consistentes com o perfil (ex.: cliente conservador recebe sugestão conservadora). | 0-5 (0 = contraditório / 5 = totalmente consistente) |

Critério de aprovação (sugestão): média das três métricas ≥ 4.0 para um resultado aceitável.

---

## Exemplos de Cenários de Teste

Crie testes simples para validar seu agente. Cada teste deve registrar: Pergunta/ação, Dados de entrada, Resposta esperada, Critério de sucesso (pass/fail), Notas.

### Teste 1: Consulta de gastos por categoria
- **Pergunta:** "Quanto gastei com alimentação no mês passado?"
- **Dados de entrada:** `transacoes.csv` com transações categorizadas (ex.: alimentação = total R$570,00).
- **Resposta esperada:** "Você gastou R$570,00 com alimentação no mês passado."
- **Critério de sucesso:** Valor exibido bate com o total calculado a partir do CSV; formatação e unidade corretas.
- **Resultado:** [x] Correto  [ ] Incorreto
- **Observações:** Se houver dúvidas sobre o período, o agente deve perguntar qual mês.

### Teste 2: Adição de gasto via frase natural
- **Pergunta / Ação:** "Gastei 50 reais no Uber"
- **Dados de entrada:** Conversa onde usuário informa novo gasto; sistema deve adicionar ao escopo de despesas.
- **Resposta esperada:** Agente confirma: "Ok — adicionei R$50,00 como gasto de transporte (Uber). Deseja categorizar ou salvar?"
- **Critério de sucesso:** Gasto é registrado no escopo temporário/BD; agente confirma e pergunta categoria quando incerto.
- **Resultado:** [x] Correto  [ ] Incorreto
- **Observações:** Verificar que o agente não transforma a frase em informação errada (ex.: data/valor).

### Teste 3: Pergunta fora do escopo
- **Pergunta:** "Qual a previsão do tempo para amanhã?"
- **Dados de entrada:** Nenhum dado de clima disponível; agente focado em finanças pessoais.
- **Resposta esperada:** "Desculpe, eu só trato de finanças pessoais e gastos. Posso ajudar com algo relacionado a suas transações?"
- **Critério de sucesso:** Agente não tenta inventar dados meteorológicos e redireciona para escopo correto.
- **Resultado:** [x] Correto  [ ] Incorreto

### Teste 4: Informação inexistente / dados de mercado
- **Pergunta:** "Quanto rende o produto BBDC3 na Bovespa?"
- **Dados de entrada:** Sem integração de cotações em tempo real.
- **Resposta esperada:** "No momento não tenho acesso a cotações em tempo real. Posso registrar esse pedido para buscar quando a integração estiver disponível, ou você deseja instruções para consultar um site de cotações?"
- **Critério de sucesso:** Agente admite limitação, não fabrica número; oferece alternativa ou aç��o apropriada.
- **Resultado:** [ ] Correto  [ ] Incorreto

---

## Procedimento de Teste e Registro de Resultados

1. Preparar ambiente com `transacoes.csv` de teste e quaisquer perfis de usuário (conservador/moderado/agressivo).
2. Executar cada cenário, anotar a resposta exata do agente, tempo de resposta e se houve follow-up question quando necessário.
3. Pontuar cada métrica (Assertividade, Segurança, Coerência) de 0 a 5 por cenário.
4. Calcular médias por cenário e média geral do agente.

Exemplo de planilha de resultado por cenário:
- Assertividade: 4
- Segurança: 5
- Coerência: 5
- Média cenário: 4.67

---

## Resultados

Após os testes, registre suas conclusões:

**O que funcionou bem:**
- Ex.: Consulta de categorias e soma correta dos CSVs; confirmações ao adicionar gastos.

**O que pode melhorar:**
- Ex.: Melhorar reconhecimento de datas na linguagem natural; sinalizar claramente quando dados externos (cotações) não estão disponíveis.

Observações finais:
- Reavalie após correções e rode a bateria de testes automatizados mensalmente ou após mudanças significativas no modelo/integracões.
