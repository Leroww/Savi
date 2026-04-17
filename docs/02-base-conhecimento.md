# Base de Conhecimento
## Dados Utilizados

| Arquivo | Formato | Para que serve na Savi? |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores, ou seja, dar continuidade ao atendimento de forma mais eficiente. |
| `perfil_investidor.json` | JSON | Personalizar as explicações sobre as dúvidas e necessidades de aprendizado do cliente. |
| `produtos_financeiros.json` | JSON | Conhecer os produtos disponíveis para que eles possam ser ensinados ao cliente. |
| `transacoes.csv` | CSV | Analisar padrão de gastos do cliente e usar essas informações de forma didática. |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Utilizei a base dos dados mocados, porém alterei os dados pessoais do usuario e as transações para melhorar as respostas e tornar o agente mais assertivo.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Existem duas possibilidades, injetar os dados diretamente no prompt (Ctrl + C, Ctrl + V) ou carregar os arquivos via código, como no exemplo abaixo:

```python
import pandas as pd
import json

perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))
```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Para simplificar, podemos simplesmente "injetar" os dados em nosso prompt, agarantindo que o Agente tenha o melhor contexto possível. Lembrando que, em soluções mais robustas, o ideal é que essas informaçoes sejam carregadas dinamicamente para que possamos ganhar flexibilidade.

```text
DADOS DO CLIENTE E PERFIL (data/perfil_investidor.json):
{
  "nome": "Maria Eduarda",
  "idade": 22,
  "profissao": "Atendente de lanchonete",
  "renda_mensal": 1500.00,
  "perfil_investidor": "baixo",
  "objetivo_principal": "Construir reserva de emergência",
  "patrimonio_total": 5000.00,
  "reserva_emergencia_atual": 100.00,
  "aceita_risco": false,
  "metas": [
    {
      "meta": "Completar reserva de emergência",
      "valor_necessario": 15000.00,
      "prazo": "2027-06"
    },
    {
      "meta": "Entrada do apartamento novo",
      "valor_necessario": 5000.00,
      "prazo": "2027-12"
    },
    {
      "meta": "Comprar um carro",
      "valor_necessario": 52000.00,
      "prazo": "2029-10"
    }
  ]
}

TRANSACOES DO CLIENTE (data/transacoes.csv):
data,descricao,categoria,valor,tipo
2025-10-01,Salário,receita,5000.00,entrada
2025-10-02,Aluguel,moradia,1200.00,saida
2025-10-03,Supermercado,alimentacao,450.00,saida
2025-10-05,Netflix,lazer,55.90,saida
2025-10-07,Farmácia,saude,89.00,saida
2025-10-10,Restaurante,alimentacao,120.00,saida
2025-10-12,Uber,transporte,45.00,saida
2025-10-15,Conta de Luz,moradia,180.00,saida
2025-10-20,Academia,saude,99.00,saida
2025-10-25,Combustível,transporte,250.00,saida
2025-10-26,bis,lazer,5.00,saida
2025-11-29,coca-cola 2l,lazer,25.00,saida

HISTORICO DE ATENDIMENTO DO CLIENTE (data/historico_atendimento.csv):
data,canal,tema,resumo,resolvido
2025-09-15,chat,CDB,Cliente perguntou sobre rentabilidade e prazos,sim
2025-09-22,telefone,Problema no app,Erro ao visualizar extrato foi corrigido,sim
2025-10-01,chat,Tesouro Selic,Cliente pediu explicação sobre o funcionamento do Tesouro Direto,sim
2025-10-12,chat,Metas financeiras,Cliente acompanhou o progresso da reserva de emergência,sim
2025-10-25,email,Atualização cadastral,Cliente atualizou e-mail e telefone,sim

PRODUTOS DISPONIVEIS PARA ENSINO (data/produtos_financeiros.json):
[
  {
    "nome": "Tesouro Selic",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "100% da Selic",
    "aporte_minimo": 30.00,
    "indicado_para": "Reserva de emergência e iniciantes"
  },
  {
    "nome": "CDB Liquidez Diária",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "102% do CDI",
    "aporte_minimo": 100.00,
    "indicado_para": "Quem busca segurança com rendimento diário"
  },
  {
    "nome": "LCI/LCA",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "95% do CDI",
    "aporte_minimo": 1000.00,
    "indicado_para": "Quem pode esperar 90 dias (isento de IR)"
  },
  {
    "nome": "Fundo Imobiliário (FII)",
    "categoria": "fundo",
    "risco": "medio",
    "rentabilidade": "Dividend Yield (DY) costuma ficar entre 6% a 12% ao ano",
    "aporte_minimo": 100.00,
    "indicado_para": "Perfil moderado que busca diversificação e renda recorrente mensal"
  },
  {
    "nome": "Fundo de Ações",
    "categoria": "fundo",
    "risco": "alto",
    "rentabilidade": "Variável",
    "aporte_minimo": 100.00,
    "indicado_para": "Perfil arrojado com foco no longo prazo"
  }
]
```

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

O exemplo de contexto montado abaixo, se baiseia nos dados originais da base de conhecimento, mas os sintetiza deixando apenas as informações mais relevantes, otimizando assim o consumo de tokens. Entretanto, vale lembrar que mais importante do que economizar tokens, é ter todas as informações relevantes disponíveis em seu contexto.

```
DADOS DO CLIENTE:
- Nome: Maria Eduarda
- Idade: 22 anos
- Profissão: Atendente de lanchonete
- Renda Mensal: R$ 1.500,00
- Perfil: Conservador (baixo risco)
- Objetivo: Construir reserva de emergência
- Reserva atual: R$ 100,00 (meta: R$ 15.000,00)
- Patrimônio total: R$ 5.000,00
- Aceita risco: Não
 
METAS FINANCEIRAS:
- Completar reserva de emergência: R$ 15.000,00 (prazo: junho/2027)
- Entrada do apartamento novo: R$ 5.000,00 (prazo: dezembro/2027)
- Comprar um carro: R$ 52.000,00 (prazo: outubro/2029)
 
RESUMO DE GASTOS:
- Moradia: R$ 1.380,00
  * Aluguel: R$ 1.200,00
  * Conta de Luz: R$ 180,00
- Alimentação: R$ 570,00
  * Supermercado: R$ 450,00
  * Restaurante: R$ 120,00
- Transporte: R$ 295,00
  * Combustível: R$ 250,00
  * Uber: R$ 45,00
- Saúde: R$ 188,00
  * Academia: R$ 99,00
  * Farmácia: R$ 89,00
- Lazer: R$ 85,90
  * Netflix: R$ 55,90
  * Coca-Cola 2L: R$ 25,00
  * Bis: R$ 5,00
- Total de saídas: R$ 2.518,90
- Saldo disponível: R$ 2.481,10

PRODUTOS DISPONÍVEIS PARA EXPLICAR:
- Tesouro Selic (risco baixo)
- CDB Liquidez Diária (risco baixo)
- LCI/LCA (risco baixo)
- Fundo Imobiliário - FII (risco médio)
- Fundo de Ações (risco alto)
```
