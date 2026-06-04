"""
Punto de entrada de la aplicación RAG.
Define la instancia de FastAPI, configura CORS y expone todos los endpoints de la API:
/health, /ingest, /query y /collections.
"""

import os  # Módulo estándar para operaciones con rutas y directorios
import shutil  # Módulo estándar para guardar archivos en disco de forma eficiente

import chromadb  # Cliente de ChromaDB para listar colecciones existentes
from fastapi import FastAPI, File, HTTPException, UploadFile  # Componentes principales de FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Middleware para habilitar CORS en la API
from pydantic import BaseModel  # Clase base para definir esquemas de datos del cuerpo JSON

from app.config import CHROMA_PERSIST_DIR, UPLOAD_DIR  # Directorios de persistencia cargados desde .env
from app.ingest import ingest_pdf  # Función que procesa e ingesta un PDF en ChromaDB
from app.query import query_documents  # Función que consulta ChromaDB y genera una respuesta con OpenAI

app = FastAPI(  # Crea la instancia principal de la aplicación FastAPI
    title="RAG Document Assistant",  # Título que aparece en la documentación automática (/docs)
    description="API para ingestar documentos PDF y consultarlos mediante RAG con OpenAI.",  # Descripción de la API
    version="0.1.0",  # Versión actual de la API
)

app.add_middleware(  # Registra el middleware de CORS en la aplicación
    CORSMiddleware,  # Clase del middleware que gestiona las cabeceras de CORS
    allow_origins=["*"],  # Permite peticiones desde cualquier origen (necesario para el frontend)
    allow_credentials=True,  # Permite el envío de cookies y cabeceras de autenticación
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todas las cabeceras HTTP en las peticiones
)

os.makedirs(UPLOAD_DIR, exist_ok=True)  # Crea el directorio de uploads si no existe, sin error si ya existe
os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)  # Crea el directorio de ChromaDB si no existe, sin error si ya existe


class QueryRequest(BaseModel):  # Esquema Pydantic que valida el cuerpo JSON del endpoint /query
    """Modelo de datos para la petición de consulta RAG."""

    question: str  # Pregunta en lenguaje natural que el usuario quiere responder
    collection_name: str  # Nombre de la colección de ChromaDB a consultar (nombre del PDF sin extensión)


@app.get("/health")  # Registra el endpoint GET en la ruta /health
async def health_check():  # Función asíncrona que maneja las peticiones a /health
    """Verifica que la API está en funcionamiento."""
    return {"status": "ok"}  # Devuelve un JSON simple que confirma que el servidor responde


@app.post("/ingest")  # Registra el endpoint POST en la ruta /ingest
async def ingest_document(file: UploadFile = File(...)):  # Recibe un archivo PDF como form-data obligatorio
    """
    Recibe un archivo PDF, lo guarda en disco y lo ingesta en ChromaDB.

    Parámetros:
        file: Archivo PDF enviado como multipart/form-data.

    Retorna:
        dict con filename, total_pages, total_chunks y collection_name.
    """

    if not file.filename.endswith(".pdf"):  # Valida que el archivo tenga extensión .pdf
        raise HTTPException(  # Lanza un error HTTP 400 si el archivo no es un PDF
            status_code=400,
            detail="Solo se aceptan archivos en formato PDF.",  # Mensaje de error en español
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)  # Construye la ruta completa donde se guardará el archivo

    with open(file_path, "wb") as buffer:  # Abre el archivo en modo escritura binaria
        shutil.copyfileobj(file.file, buffer)  # Copia el contenido del archivo subido al disco de forma eficiente

    try:  # Intenta procesar el PDF; captura errores para devolver una respuesta clara
        result = ingest_pdf(file_path)  # Llama a la función de ingesta que chunkea y vectoriza el PDF
    except Exception as e:  # Si ocurre cualquier error durante la ingesta...
        raise HTTPException(  # ...lanza un error HTTP 500 con el detalle del problema
            status_code=500,
            detail=f"Error al procesar el archivo '{file.filename}': {str(e)}",
        )

    return result  # Devuelve el dict con el resumen de la ingesta (páginas, chunks, colección)


@app.post("/query")  # Registra el endpoint POST en la ruta /query
async def query_document(request: QueryRequest):  # Recibe y valida el cuerpo JSON con el esquema QueryRequest
    """
    Recibe una pregunta y el nombre de una colección, y devuelve una respuesta generada por el LLM.

    Parámetros:
        request: Objeto JSON con 'question' y 'collection_name'.

    Retorna:
        dict con 'answer' (respuesta del LLM) y 'sources' (fragmentos usados como contexto).
    """

    if not request.question.strip():  # Verifica que la pregunta no sea una cadena vacía o solo espacios
        raise HTTPException(  # Lanza un error HTTP 400 si la pregunta está vacía
            status_code=400,
            detail="La pregunta no puede estar vacía.",
        )

    result = query_documents(  # Llama a la función RAG con la pregunta y el nombre de la colección
        question=request.question,  # Pregunta del usuario
        collection_name=request.collection_name,  # Colección de ChromaDB a consultar
    )

    return result  # Devuelve el dict con la respuesta generada y las fuentes utilizadas


@app.get("/collections")  # Registra el endpoint GET en la ruta /collections
async def list_collections():  # Función asíncrona que maneja las peticiones a /collections
    """
    Lista todas las colecciones disponibles en ChromaDB.

    Retorna:
        dict con 'collections', una lista de nombres de colecciones ingestadas.
    """

    try:  # Intenta conectar con ChromaDB para leer las colecciones disponibles
        client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)  # Crea un cliente ChromaDB apuntando al directorio persistido
        collections = client.list_collections()  # Obtiene la lista de todas las colecciones almacenadas
        names = [col.name for col in collections]  # Extrae solo el nombre de cada colección
    except Exception as e:  # Si ChromaDB no puede abrirse o hay otro error...
        raise HTTPException(  # ...lanza un error HTTP 500 con el detalle del problema
            status_code=500,
            detail=f"Error al leer las colecciones de ChromaDB: {str(e)}",
        )

    return {"collections": names}  # Devuelve la lista de nombres de colecciones disponibles
