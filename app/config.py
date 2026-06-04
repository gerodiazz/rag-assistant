# Carga y expone la configuración de la aplicación desde variables de entorno.
# OpenAI se usa tanto para embeddings como para generación de respuestas.

import os  # Módulo estándar para acceder a las variables de entorno del sistema
from dotenv import load_dotenv  # Función que lee el archivo .env y carga sus valores en el entorno

load_dotenv()  # Carga las variables definidas en el archivo .env al entorno del proceso actual

def _require(name: str) -> str:  # Función auxiliar que obtiene una variable de entorno obligatoria
    value = os.getenv(name)  # Intenta leer el valor de la variable de entorno con el nombre dado
    if value is None:  # Si la variable no existe o no está definida...
        raise ValueError(  # ...lanza un error con un mensaje claro indicando cuál falta
            f"Variable de entorno requerida no encontrada: '{name}'. "
            f"Asegúrate de definirla en tu archivo .env o en el entorno del sistema."
        )
    return value  # Devuelve el valor si la variable existe

OPENAI_API_KEY: str = _require("OPENAI_API_KEY")  # Clave de API de OpenAI, obligatoria para embeddings y generación
CHROMA_PERSIST_DIR: str = _require("CHROMA_PERSIST_DIR")  # Ruta al directorio donde ChromaDB guardará la base vectorial
UPLOAD_DIR: str = _require("UPLOAD_DIR")  # Ruta al directorio donde se almacenarán los PDFs subidos por el usuario
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")  # Modelo de OpenAI a usar; si no está definido, usa gpt-3.5-turbo por defecto