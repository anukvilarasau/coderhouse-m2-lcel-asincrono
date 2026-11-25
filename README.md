# Refactorización a LCEL asíncrono

Ejercicio del **Módulo 2 · Unidad 1 (Arquitectura de cadenas con LCEL y runnables)** de AI Engineering (Coderhouse).

Migra una llamada imperativa al SDK crudo (lo del Módulo 1) a una cadena declarativa de LangChain:

```python
chain = prompt | modelo | StrOutputParser()
respuesta = await chain.ainvoke({"pregunta": "...", "nivel": "principiante"})
```

## Antes y después

| | Módulo 1 (imperativo) | Módulo 2 (LCEL) |
|---|---|---|
| Modelo | `AsyncAnthropic(api_key=...)` | `ChatAnthropic(model=..., temperature=0.2)` (o `ChatOpenAI`) |
| Prompt | strings armados a mano | `ChatPromptTemplate.from_messages` con roles **system** y **human** |
| Salida | `resp.content[0].text` | `StrOutputParser()` devuelve el texto plano |
| Flujo | pasos encadenados con código | `prompt | modelo | parser` |
| Ejecución | `await client.messages.create(...)` | `await chain.ainvoke({...})` |

## Criterios de aceptación

- Flujo principal armado solo con el operador `|`: `chain = prompt | modelo | StrOutputParser()`.
- Ejecución asíncrona con `await chain.ainvoke(...)` dentro de `async def main()`.
- La salida es un `str`, no un `AIMessage` (el script lo imprime: `¿La salida es texto plano (str)? True`).
- El prompt tiene roles System y Human, y las variables `{pregunta}` y `{nivel}` coinciden con las claves del diccionario.
- Extra: como la cadena es un *Runnable*, se ejecutan varias preguntas en paralelo con `asyncio.gather`.

## Cómo correrlo

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (en Mac/Linux: source .venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env          # y completá tu clave
python main.py
```

Usa Claude si encuentra `ANTHROPIC_API_KEY`; si no, OpenAI con `OPENAI_API_KEY`. El modelo se puede cambiar con la variable `MODELO`.

## Errores comunes que evita

- **Olvidar el `await`:** sin él, `ainvoke` devuelve una corrutina y no el texto.
- **Variables que no coinciden:** las llaves `{pregunta}` y `{nivel}` del prompt son exactamente las claves del diccionario que recibe `ainvoke`.
