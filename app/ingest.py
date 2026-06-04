"""
Módulo de ingesta de documentos PDF.
Carga un PDF, lo divide en fragmentos, genera embeddings con OpenAI
y los almacena en una colección de ChromaDB para su posterior consulta.
"""

import os  # Módulo estándar para operaciones con rutas de archivos
from langchain_community.document_loaders import PyPDFLoader  # Cargador de PDFs página por página
from langchain_text_splitters import RecursiveCharacterTextSplitter  # Divisor de texto en fragmentos con solapamiento
from langchain_openai import OpenAIEmbeddings  # Clase para generar embeddings usando la API de OpenAI
from langchain_community.vectorstores import Chroma  # Clase para interactuar con ChromaDB como vector store
from app.config import OPENAI_API_KEY, CHROMA_PERSIST_DIR  # Constantes de configuración cargadas desde .env


def ingest_pdf(file_path: str) -> dict:
    """
    Procesa un archivo PDF y almacena sus fragmentos como embeddings en ChromaDB.

    Parámetros:
        file_path (str): Ruta absoluta o relativa al archivo PDF a procesar.

    Retorna:
        dict: Diccionario con filename, total_pages, total_chunks y collection_name.
    """

    filename = os.path.splitext(os.path.basename(file_path))[0]  # Extrae el nombre del archivo sin extensión ni ruta

    loader = PyPDFLoader(file_path)  # Inicializa el cargador apuntando al PDF recibido
    pages = loader.load()  # Carga el PDF y devuelve una lista de documentos, uno por página
    total_pages = len(pages)  # Cuenta el total de páginas cargadas

    splitter = RecursiveCharacterTextSplitter(  # Inicializa el divisor de texto con la configuración deseada
        chunk_size=1000,  # Tamaño máximo de cada fragmento en caracteres
        chunk_overlap=200,  # Cantidad de caracteres que se solapan entre fragmentos consecutivos
    )
    chunks = splitter.split_documents(pages)  # Divide las páginas en fragmentos más pequeños
    total_chunks = len(chunks)  # Cuenta el total de fragmentos generados

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)  # Inicializa el modelo de embeddings con la clave de OpenAI

    Chroma.from_documents(  # Genera embeddings para cada fragmento y los almacena en ChromaDB
        documents=chunks,  # Lista de fragmentos de texto a vectorizar
        embedding=embeddings,  # Modelo de embeddings que transformará el texto en vectores
        collection_name=filename,  # Nombre de la colección dentro de ChromaDB, basado en el nombre del archivo
        persist_directory=CHROMA_PERSIST_DIR,  # Directorio donde ChromaDB guardará los datos de forma persistente
    )

    return {  # Devuelve un resumen del proceso de ingesta
        "filename": filename,  # Nombre del archivo procesado (sin extensión)
        "total_pages": total_pages,  # Número de páginas que tenía el PDF original
        "total_chunks": total_chunks,  # Número de fragmentos generados y almacenados
        "collection_name": filename,  # Nombre de la colección creada en ChromaDB
    }
