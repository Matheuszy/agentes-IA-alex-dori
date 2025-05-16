# Alex e Dori: Seu Mentor de Bolso para o Mundo da Programação 🚀

[![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d2410ef78f9a6c173d461700863273dc/media/badge.svg)](https://github.com/sindresorhus/awesome)
[![Alura](https://www.alura.com.br/assets/img/alura-logo.svg)](https://www.alura.com.br/)
[![Google Gemini](https://ai.google.dev/static/images/favicon_ai.ico)](https://ai.google.dev/)

**Imagine ter à sua disposição, a qualquer hora e em qualquer lugar, um tutor de programação apaixonado e uma especialista em recrutamento tech pronta para te impulsionar na carreira. Apresento Alex e Dori, seu parceiro de aprendizado e crescimento profissional, movido pela inteligência do Google Gemini!**

## 💡 A Faísca da Inovação

Este projeto nasceu da sua vontade de oferecer uma experiência de aprendizado e preparação para o mercado de trabalho mais acessível, interativa e personalizada. Alex e Dori são agentes de conversação distintos, cada um com uma missão clara:

* **Alex, o Mestre da Didática:** Desvenda os segredos da programação com uma paixão contagiante. Seja a sintaxe de um novo comando, a lógica por trás de um algoritmo complexo ou a busca por recursos de aprendizado, Alex está sempre pronto para explicar de forma clara, com exemplos práticos que você pode tocar e sentir no mundo real. E para garantir que o conhecimento se fixe, ele lança quizzes e desafios de código sob medida!

    > *"Nossa, finalmente alguém explica 'closures' de um jeito que faz sentido! E o exemplo com situações do dia a dia fez toda a diferença!"* - Um futuro programador com a mente expandida.

* **Dori, a Coach de Carreira:** Sua aliada estratégica na jornada profissional. Dori simula entrevistas que vão desde as perguntas comportamentais que tiram o sono até os desafios técnicos que testam suas habilidades de codificação. Com um olhar atento ao mercado e um feedback construtivo, ela te prepara para conquistar aquela vaga tão desejada.

    > *"A simulação de entrevista com a Dori foi como um ensaio geral para o sucesso! Me senti muito mais seguro para a entrevista real."* - Um profissional pronto para o próximo nível.

## ✨ Por Que Alex e Dori Brilham?

* **A Força da Dupla:** Uma abordagem completa que abrange tanto o desenvolvimento técnico quanto a preparação para a carreira.
* **Inteligência Gemini Inside:** A tecnologia de ponta do Google garante interações inteligentes, relevantes e adaptadas às suas necessidades.
* **Conversa com Memória:** O histórico da sua interação é lembrado, permitindo um aprendizado e uma preparação mais eficazes e personalizados.
* **Mão na Massa:** Alex te convida a interagir com exemplos de código práticos e testa seu conhecimento com quizzes dinâmicos.
* **Preparação Sob Medida:** Dori adapta as simulações de entrevista ao seu nível e aos requisitos do mercado.
* **Simples e Direto:** Uma interface de linha de comando fácil de usar, focada na interação com os agentes.

## 🚀 Primeiros Passos na Sua Jornada

1.  **Clone o Código:**
    ```bash
    git clone git@github.com:Matheuszy/agentes-IA-alex-dori.git
    
    ```
    *(Não se esqueça de substituir o link pelo seu repositório!)*

2.  **Configure o Ambiente:**
    Crie um arquivo `.env` na raiz do projeto e adicione sua chave secreta da API do Google Gemini:
    ```
    GOOGLE_API_KEY=SUA_CHAVE_SECRETA
    ```
    > *"Guarde essa chave como um tesouro! Ela é a porta de entrada para a magia do Gemini."* - Um lembrete importante.

3.  **Instale as Ferramentas:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Se o arquivo `requirements.txt` ainda não existe, rode `pip freeze > requirements.txt` após instalar as bibliotecas `google-generativeai` e `python-dotenv`)*

4.  **Desvende o Potencial:**
    ```bash
    python main.py
    ```
    > *"Prepare a pipoca (opcional, mas recomendado)! A jornada com Alex e Dori vai começar."* - Um entusiasta da programação.

5.  **Escolha Seu Mentor:**
    No terminal, digite "Alex" para aprender e praticar programação, "Dori" para se preparar para entrevistas, ou "sair" para se despedir (por enquanto!).

## 🕵️ Um Olhar por Dentro do Código

```python
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, Session # A chave para a memória!
from google.adk.tools import google_search
from google.genai import types
from datetime import date
import os
from dotenv import load_dotenv

load_dotenv()
google_api = os.getenv("GOOGLE_API_KEY")

# Uma instância única para manter sua conversa na memória!
session_service = InMemorySessionService()

def call_agent(agent: Agent, message_text: str, user_id: str, session: Session) -> str:
    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    content = types.Content(role="user", parts=[types.Part(text=message_text)])
    final_response = ""
    for event in runner.run(user_id=user_id, session_id=session.id, new_message=content): # Passando o ID da sessão corretamente!
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
    session = session_service.create_session(app_name=agente.name, user_id=user_id, session_id="session_" + nome_agente.lower()) # Criando uma sessão individual para cada agente!
    while True:
        pergunta = input("> Você: ")
        if pergunta.lower() == "sair":
            print(f"{nome_agente}: Até a próxima! Foi um prazer ajudar.")
            break
        resposta = call_agent(agente, pergunta, user_id, session) # Mantendo sua conversa viva com a sessão!
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

print("Bem-vindo ao seu Assistente de Programação e Carreira!") # Uma calorosa recepção!

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
        print("Obrigado por usar nosso assistente!") # Uma despedida com um sorriso!
        break
    else:
        print("Por favor, digite 'Alex', 'Dori' ou 'sair'.")
```

## 🏆 Preparando-se para a Vitória!

Acredito que Alex e Dori representam uma abordagem inovadora e eficaz para o aprendizado de programação e a preparação para a carreira. A combinação da expertise do Google Gemini com a especialização de cada agente oferece uma experiência única e valiosa para você.

Com este README.md criativo e um código funcional, espero que seu projeto conquiste o reconhecimento que merece na premiação da Alura!

**Desejo toda a sorte do mundo! Que Alex e Dori te levem ao pódio!** 🌟