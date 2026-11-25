from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = FastAPI()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class MensagemRequest(BaseModel):
    mensagem: str

@app.post("/classificar")
async def classificar(body: MensagemRequest):
    prompt = f"""Você é um classificador de mensagens de clientes.

Analise a mensagem abaixo e retorne APENAS um JSON válido, sem explicações, sem markdown, sem texto extra.

Categorias possíveis:
- "duvida": cliente tem uma pergunta ou quer informação
- "reclamacao": cliente está insatisfeito ou relatando um problema
- "solicitacao": cliente está pedindo algo (cancelamento, troca, etc)

Formato obrigatório:
{{
  "categoria": "<duvida|reclamacao|solicitacao>",
  "confianca": "<alta|media|baixa>",
  "resumo": "<resumo curto da mensagem em 1 frase>"
}}

Mensagem: {body.mensagem}"""

    response = client.models.generate_content(
       model="gemini-3.1-flash-lite",
        contents=prompt
    )

    resultado = json.loads(response.text)
    return resultado