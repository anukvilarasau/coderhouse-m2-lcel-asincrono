"""Refactorización a LCEL asíncrono · AI Engineering (Coderhouse) · Módulo 2.

Antes (Módulo 1): llamada imperativa al SDK crudo
    client = AsyncAnthropic(api_key=...)
    resp = await client.messages.create(model=..., system=..., messages=[...])
    texto = resp.content[0].text

Ahora: una cadena declarativa con LCEL
    chain = prompt | modelo | StrOutputParser()
    texto = await chain.ainvoke({"pregunta": "..."})
"""
import asyncio
import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


def crear_modelo():
    """Instancia el modelo de LangChain según las claves disponibles.
    Reemplaza la inicialización manual del cliente del SDK."""
    if os.getenv("ANTHROPIC_API_KEY"):
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model=os.getenv("MODELO", "claude-haiku-4-5"), temperature=0.2, max_tokens=400)
    if os.getenv("OPENAI_API_KEY"):
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=os.getenv("MODELO", "gpt-4o-mini"), temperature=0.2, max_tokens=400)
    raise RuntimeError("Falta ANTHROPIC_API_KEY u OPENAI_API_KEY en el entorno o en .env")


# Prompt con roles definidos (System / Human) y dos variables
prompt = ChatPromptTemplate.from_messages([
    ("system", "Sos un tutor de AI Engineering. Respondé en español rioplatense, "
               "en no más de 4 oraciones y con un ejemplo concreto. Nivel del alumno: {nivel}."),
    ("human", "{pregunta}"),
])

modelo = crear_modelo()

# La cadena: Prompt | Modelo | Parser. StrOutputParser extrae el texto plano del AIMessage.
chain = prompt | modelo | StrOutputParser()


async def main() -> None:
    preguntas = [
        {"pregunta": "¿Qué es LCEL y por qué conviene usar el operador |?", "nivel": "principiante"},
        {"pregunta": "¿Para qué sirve ainvoke en una cadena?", "nivel": "principiante"},
    ]
    # Una sola pregunta con ainvoke...
    respuesta = await chain.ainvoke(preguntas[0])
    print(f"¿La salida es texto plano (str)? {isinstance(respuesta, str)}\n")  # no un AIMessage
    print(f"P: {preguntas[0]['pregunta']}\nR: {respuesta}\n")

    # ...y varias en paralelo: la misma cadena es un Runnable y se puede combinar con asyncio
    respuestas = await asyncio.gather(*(chain.ainvoke(p) for p in preguntas[1:]))
    for p, r in zip(preguntas[1:], respuestas):
        print(f"P: {p['pregunta']}\nR: {r}\n")


if __name__ == "__main__":
    asyncio.run(main())
