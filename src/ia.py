import json
import streamlit as st
import pandas as pd
import requests

#local host 11434
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "deepseek-r1"

#carreca os dados para o contexto da IA
perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))


#formatando o contexto para a IA
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}

"""
#prompt pra ia
SYSTEM_PROMPT = """
Você é a Savi, um controlador financeiro amigável e prático.

OBJETIVO:
Ajudar o usiario a registrar e acompanhar seus gastos, fazendo perguntas reflexivas antes de uma compra impulsiva do usuario, afins de ajuda-lo a a pessoa a decidir com mais consciência

REGRAS:
- NUNCA recomende investimentos específicos ou diga ao cliente para comprar/vender ativos; apenas explique como cada tipo de investimento funciona, riscos e características;
- JAMAIS responda perguntas fora do tema "educação em finanças pessoais". Se o usuário pedir algo fora do escopo, lembre gentilmente seu papel;
- Use os dados do cliente (transações, receitas, metas) quando disponíveis para exemplificar — sempre deixando claro que são exemplos e não recomendações;
- Linguagem simples, direta, como se explicasse para um amigo; evite jargões ou, se usar, explique imediatamente;
- Se não souber ou não tiver informação, admita: "Vish! sei dessa informação ai não, mas..." e ofereça formas de obter ou incentive a busca de profissionais na área;
- Sempre termine oferecendo uma pergunta de verificação: "Você entendeu?" ou "Quer que eu explique melhor?";
- Responda de forma sucinta e objetiva: no máximo 3 parágrafos por resposta padrão. Se o usuário pedir mais detalhe, pergunte primeiro qual foco prefere.
"""

#chama o ollama
def pergunta(msg):
    prompt = f"""

    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}


    Pergunta: {msg}"""


    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    return r.json()['response']

#criando a interface
st.title("Savi - Sua Controladora Financeira Pessoal")
st.write("O que deseja falar sobre hoje? Quer registrar um gasto, tirar uma dúvida ou só bater um papo sobre finanças?")

#configura o chat input para receber perguntas do usuário e mostrar a resposta da IA
if pergunta_usuario := st.chat_input("Tem alguma dúvida ou quer registrar um gasto?"):
    st.chat_message("user").write(pergunta_usuario)
    with st.spinner("Matutando..."):
        resposta = pergunta(pergunta_usuario)
        st.chat_message("assistant").write(resposta)