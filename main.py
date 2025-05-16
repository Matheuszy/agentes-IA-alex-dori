from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, Session
from google.adk.tools import google_search
from google.genai import types
from datetime import date
import os
from dotenv import load_dotenv

load_dotenv()
google_api = os.getenv("GOOGLE_API_KEY")

# Criar o serviço de sessão uma vez
session_service = InMemorySessionService()

def call_agent(agent: Agent, message_text: str, user_id: str, session: Session) -> str:
    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    content = types.Content(role="user", parts=[types.Part(text=message_text)])
    final_response = ""
    for event in runner.run(user_id=user_id, session_id=session.id, new_message=content):
        if event.is_final_response():
            for part in event.content.parts:
                if part.text is not None:
                    final_response += part.text
                    final_response += "\n"
    return final_response

def criar_agente(nome, modelo, descricao, instrucao, ferramentas=None):
    if ferramentas is None:
        ferramentas = []
    agente = Agent(
        name=nome,
        model=modelo,
        description=descricao,
        tools=ferramentas,
        instruction=instrucao
    )
    return agente

def interagir_com_agente(agente: Agent, nome_agente: str):
    print(f"\nVocê está conversando com {nome_agente}. Digite 'sair' para encerrar a conversa.")
    user_id = "user_" + nome_agente.lower()
    session = session_service.create_session(app_name=agente.name, user_id=user_id, session_id="session_" + nome_agente.lower())
    while True:
        pergunta = input("> Você: ")
        if pergunta.lower() == "sair":
            print(f"{nome_agente}: Até a próxima! Foi um prazer ajudar.")
            break
        resposta = call_agent(agente, pergunta, user_id, session)
        print(f"{nome_agente}: {resposta}")

data_atual = date.today().strftime("%d/%m/%Y")

instruction_tutor = """

Você é Alex, um tutor de programação extremamente apaixonado por compartilhar seu conhecimento. Sua missão é tornar conceitos complexos acessíveis a todos, desde iniciantes até programadores experientes. Você domina diversas linguagens e tecnologias, e está sempre atualizado através de suas pesquisas no Google Search [google search].



Sua abordagem é didática e envolvente, utilizando exemplos práticos do mundo real para ilustrar os conceitos. Você explica a sintaxe de comandos, auxilia na depuração de código, manda perguntas sobre o que já foi estudado ou desafios de acordo com o que foi aprendido como quizzes ou códigos e recomenda os melhores recursos de aprendizado. Sua persistência em garantir a compreensão do aluno é uma de suas maiores qualidades. Mantenha um tom amigável, motivador e adaptado ao nível de conhecimento do interlocutor.

"""

instruction_recrutadora = """

Você é Dori, uma analista de RH dedicada a ajudar profissionais de programação a encontrarem as melhores oportunidades de carreira. Você acredita no potencial de todos na área de tecnologia e se motiva ao ver o crescimento dos candidatos. Seu objetivo é preparar os usuários para processos seletivos, desde entrevistas comportamentais até desafios técnicos. Para isso, você se mantém atualizada sobre as demandas do mercado através de pesquisas no Google Search [google search] e faz as perguntas técnicas ou manda desafios de código (prático).



Sua abordagem é atenciosa e encorajadora. Você inicia as simulações de entrevistas com perguntas básicas e adapta a dificuldade conforme as respostas do usuário. Você oferece feedback construtivo, elogia os acertos e oferece apoio nos momentos de dificuldade, sempre incentivando a persistência e o aprendizado contínuo. Mantenha um tom profissional, motivador e focado no desenvolvimento do candidato.

"""

print("Bem-vindo ao seu Assistente de Programação e Carreira!")

while True:
    assunto = input("Com quem você gostaria de falar? (Alex para tutor, Dori para recrutadora, sair para encerrar): ").strip().lower()
    if assunto == "alex":
        alex_tutor = criar_agente(
            nome="Alex_bom_tutor",
            modelo="gemini-2.0-flash",
            descricao="Agente que é um tutor de programação",
            instrucao=instruction_tutor,
            ferramentas=[google_search]
        )
        interagir_com_agente(alex_tutor, "Alex")
    elif assunto == "dori":
        dori_recrutadora = criar_agente(
            nome="Dori_recrutadora",
            modelo="gemini-2.5-pro-preview-03-25",
            descricao="Agente de RH para programadores",
            instrucao=instruction_recrutadora,
            ferramentas=[google_search]
        )
        interagir_com_agente(dori_recrutadora, "Dori")
    elif assunto == "sair":
        print("Obrigado por usar nosso assistente!")
        break
    else:
        print("Por favor, digite 'Alex', 'Dori' ou 'sair'.")