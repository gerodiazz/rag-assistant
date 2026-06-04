"""
Módulo de consulta RAG (Retrieval-Augmented Generation).
Recupera los fragmentos más relevantes de ChromaDB y genera una respuesta
contextualizada usando el modelo de chat de OpenAI.
"""

from langchain_openai import OpenAIEmbeddings, ChatOpenAI  # Clases de OpenAI para embeddings y modelo de chat
from langchain_community.vectorstores import Chroma  # Clase para cargar y consultar colecciones de ChromaDB
from langchain_core.prompts import ChatPromptTemplate  # Clase para construir plantillas de prompt estructuradas
from langchain_core.output_parsers import StrOutputParser  # Parser que convierte la respuesta del LLM a string plano
from app.config import OPENAI_API_KEY, CHROMA_PERSIST_DIR, OPENAI_MODEL  # Configuración cargada desde .env

# Plantilla del prompt que se enviará al modelo de chat
PROMPT_TEMPLATE = """
Eres un asistente experto en análisis de documentos.
Usa únicamente el siguiente contexto extraído del documento para responder la pregunta.
Si la respuesta no se encuentra en el contexto, indícalo claramente en español.

Contexto:
{context}

Pregunta:
{question}

Responde de forma clara y concisa en español.
"""  # Texto de la plantilla con marcadores {context} y {question} que se rellenan en cada consulta


def query_documents(question: str, collection_name: str) -> dict:
    """
    Recupera fragmentos relevantes de una colección ChromaDB y genera una respuesta con OpenAI.

    Parámetros:
        question (str): Pregunta del usuario en lenguaje natural.
        collection_name (str): Nombre de la colección en ChromaDB (generalmente el nombre del PDF sin extensión).

    Retorna:
        dict: Diccionario con 'answer' (respuesta generada) y 'sources' (lista de fragmentos usados como contexto).
    """

    try:  # Envuelve todo en try/except para capturar errores de colección inexistente u otros fallos

        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)  # Inicializa el modelo de embeddings con la clave de OpenAI

        vectorstore = Chroma(  # Carga la colección existente en ChromaDB (no crea una nueva)
            collection_name=collection_name,  # Nombre de la colección a consultar
            persist_directory=CHROMA_PERSIST_DIR,  # Directorio donde está guardada la base vectorial
            embedding_function=embeddings,  # Función de embeddings para vectorizar la pregunta antes de buscar
        )

        results = vectorstore.similarity_search(question, k=4)  # Recupera los 4 fragmentos más similares a la pregunta

        if not results:  # Si no se encontraron fragmentos relevantes...
            return {  # ...devuelve un error explicativo sin llamar al LLM
                "answer": (
                    f"No se encontraron resultados en la colección '{collection_name}'. "
                    f"Asegúrate de haber ingestado el documento antes de consultarlo."
                ),
                "sources": [],  # Lista vacía porque no hay fragmentos que mostrar
            }

        context = "\n\n".join([doc.page_content for doc in results])  # Une los fragmentos recuperados en un solo bloque de texto

        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)  # Crea el prompt a partir de la plantilla definida arriba

        llm = ChatOpenAI(  # Inicializa el modelo de chat de OpenAI
            openai_api_key=OPENAI_API_KEY,  # Clave de autenticación para la API
            model=OPENAI_MODEL,  # Modelo a usar, definido en config.py (por defecto gpt-3.5-turbo)
        )

        chain = prompt | llm | StrOutputParser()  # Encadena: prompt → LLM → parser de texto plano

        answer = chain.invoke({  # Ejecuta la cadena con el contexto y la pregunta del usuario
            "context": context,  # Fragmentos recuperados de ChromaDB
            "question": question,  # Pregunta original del usuario
        })

        sources = [  # Construye la lista de fuentes para devolver junto a la respuesta
            {
                "page_content": doc.page_content,  # Texto del fragmento usado como contexto
                "metadata": doc.metadata,  # Metadatos del fragmento (número de página, nombre de archivo, etc.)
            }
            for doc in results  # Itera sobre cada fragmento recuperado
        ]

        return {  # Devuelve la respuesta generada y las fuentes utilizadas
            "answer": answer,  # Texto de la respuesta generada por el LLM
            "sources": sources,  # Lista de fragmentos que sirvieron como contexto
        }

    except Exception as e:  # Captura cualquier error inesperado (colección inexistente, fallo de red, etc.)
        return {  # Devuelve un mensaje de error claro en lugar de lanzar una excepción
            "answer": (
                f"Error al consultar la colección '{collection_name}': {str(e)}. "
                f"Verifica que el documento haya sido ingestado correctamente."
            ),
            "sources": [],  # Lista vacía porque no se pudo completar la búsqueda
        }
