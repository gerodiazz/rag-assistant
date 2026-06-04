# RAG Assistant — Instrucciones para Claude Code

## Regla principal
Comentar absolutamente todas las líneas de código en español, sin excepción.
Esto incluye: imports, declaraciones de variables, funciones, decoradores, condicionales, returns, todo.
Los comentarios deben ser concisos pero claros. Este es un proyecto de aprendizaje.

## Stack
- Backend: Python + FastAPI + LangChain
- Vector DB: ChromaDB (persistencia local)
- Embeddings: OpenAI
- LLM: Claude vía Anthropic API
- Frontend: Next.js + Tailwind (fase posterior)

## Estructura del proyecto
- app/config.py — carga de variables de entorno
- app/ingest.py — ingesta de PDFs, chunking y embeddings
- app/query.py — cadena de retrieval y respuesta con fuentes
- app/main.py — API FastAPI con endpoints

## Convenciones
- Español para comentarios y mensajes de error
- Nombres de variables y funciones en inglés
- Cada función debe tener docstring en español
