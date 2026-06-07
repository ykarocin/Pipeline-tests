import os
from litellm import completion # Instale usando: pip install litellm

# --- CONFIGURAÇÃO DAS CHAVES DAS IAS ---
# Você pode testar com qualquer IA apenas trocando o nome da variável no código!
os.environ["OPENAI_API_KEY"] = "sua-chave-gpt"
os.environ["GEMINI_API_KEY"] = "sua-chave-gemini"
os.environ["ANTHROPIC_API_KEY"] = "sua-chave-claude"

# Variável para você testar diferentes modelos facilmente
MODELO_ESCOLHIDO = "gemini/gemini-2.5-pro" # ou "gpt-4o", "claude-3-opus", etc.

# --- FUNÇÕES AUXILIARES ---
def ler_prompt(nome_arquivo):
    with open(f"./prompts/{nome_arquivo}", "r", encoding="utf-8") as f:
        return f.read()

def ler_codigo_fonte():
    # Aqui você leria os arquivos do seu repositório para entregar ao oráculo
    return "Conteúdo simulado do repositório: Rotas express, banco PostgreSQL..."

def agente_fala(papel, instrucao_sistema, mensagem_usuario):
    """Envia a mensagem para a IA e retorna a resposta"""
    print(f"\n[{papel} PENSANDO...]")
    
    resposta = completion(
        model=MODELO_ESCOLHIDO,
        messages=[
            {"role": "system", "content": instrucao_sistema},
            {"role": "user", "content": mensagem_usuario}
        ]
    )
    
    texto_resposta = resposta.choices[0].message.content
    print(f"\n================ {papel} ================\n")
    print(texto_resposta)
    print("\n==========================================")
    
    return texto_resposta

# --- O MOTOR DA ESTEIRA (O LOOP) ---
def iniciar_esteira():
    print("Iniciando Pipeline Autônomo de Testes...")
    
    # 1. Carrega os arquivos
    prompt_oraculo = ler_prompt("oracle-prompt.md")
    codigo_fonte = ler_codigo_fonte()
    
    # 2. Instancia o Oráculo passando o código fonte para ele ler
    mensagem_inicial = f"Aqui está o código do repositório para você indexar:\n\n{codigo_fonte}"
    resposta_oraculo = agente_fala("ORÁCULO", prompt_oraculo, mensagem_inicial)
    
    # 3. O Script avalia o que o Oráculo mandou fazer
    if "[SYS_INVOKE: DOCUMENTER]" in resposta_oraculo:
        
        # O Oráculo mandou chamar o Documentador!
        prompt_documentador = ler_prompt("document-prompt.md")
        
        # O Documentador é iniciado e recebe o histórico (o resumo do Oráculo)
        mensagem_doc = f"O Oráculo concluiu a indexação. Aqui está o resumo dele:\n{resposta_oraculo}\nFaça suas perguntas ao Oráculo."
        resposta_doc = agente_fala("DOCUMENTADOR", prompt_documentador, mensagem_doc)
        
        # 4. A conversa entre eles (Loop de Entrevista)
        # O Oráculo responde à pergunta do Documentador
        replica_oraculo = agente_fala("ORÁCULO", prompt_oraculo, f"O Documentador perguntou: {resposta_doc}\nResponda com base no código.")
        
        # O script continua interceptando os comandos...
        # Se a replica_oraculo contiver [SYS_INVOKE: FUZZ_GENERATOR], ele carrega o Papel 3, e assim por diante.

# --- EXECUÇÃO ---
if __name__ == "__main__":
    iniciar_esteira()