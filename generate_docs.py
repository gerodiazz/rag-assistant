#!/usr/bin/env python3
"""Genera la documentación técnica del proyecto RAG Assistant en PDF."""

from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable, Preformatted
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

W, H = A4
M = 2.2 * cm
CW = W - 2 * M

DARK    = colors.HexColor("#0f172a")
PRIMARY = colors.HexColor("#1e293b")
ACCENT  = colors.HexColor("#2563eb")
MUTED   = colors.HexColor("#64748b")
CBG     = colors.HexColor("#f8fafc")
CBR     = colors.HexColor("#e2e8f0")
IBG     = colors.HexColor("#eff6ff")
IBR     = colors.HexColor("#bfdbfe")
WBG     = colors.HexColor("#fffbeb")
WBR     = colors.HexColor("#fde68a")
GBG     = colors.HexColor("#f0fdf4")
GBR     = colors.HexColor("#86efac")

def mk_styles():
    s = getSampleStyleSheet()
    for ps in [
        ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=22, leading=28,
            textColor=PRIMARY, spaceBefore=20, spaceAfter=10),
        ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=16, leading=22,
            textColor=PRIMARY, spaceBefore=16, spaceAfter=8),
        ParagraphStyle('H3', fontName='Helvetica-Bold', fontSize=13, leading=18,
            textColor=ACCENT, spaceBefore=12, spaceAfter=6),
        ParagraphStyle('H4', fontName='Helvetica-BoldOblique', fontSize=11, leading=16,
            textColor=PRIMARY, spaceBefore=8, spaceAfter=4),
        ParagraphStyle('Bod', fontName='Helvetica', fontSize=11, leading=17,
            textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=8),
        ParagraphStyle('BL', fontName='Helvetica', fontSize=11, leading=16,
            textColor=DARK, leftIndent=16, spaceAfter=3),
        ParagraphStyle('BL2', fontName='Helvetica', fontSize=10, leading=15,
            textColor=DARK, leftIndent=36, spaceAfter=2),
        ParagraphStyle('Cd', fontName='Courier', fontSize=8.5, leading=12.5, textColor=DARK),
        ParagraphStyle('Cap', fontName='Helvetica-Oblique', fontSize=9, leading=13,
            textColor=MUTED, alignment=TA_CENTER, spaceAfter=6),
        ParagraphStyle('CovT', fontName='Helvetica-Bold', fontSize=34, leading=42,
            textColor=colors.white, alignment=TA_CENTER),
        ParagraphStyle('CovS', fontName='Helvetica', fontSize=15, leading=22,
            textColor=colors.HexColor("#93c5fd"), alignment=TA_CENTER),
        ParagraphStyle('CovM', fontName='Helvetica', fontSize=11, leading=16,
            textColor=colors.HexColor("#cbd5e1"), alignment=TA_CENTER),
        ParagraphStyle('TOC1', fontName='Helvetica-Bold', fontSize=12, leading=22, textColor=DARK),
        ParagraphStyle('TOC2', fontName='Helvetica', fontSize=11, leading=19, textColor=MUTED, leftIndent=24),
        ParagraphStyle('GT', fontName='Helvetica-Bold', fontSize=11, leading=16, textColor=ACCENT, spaceAfter=2),
        ParagraphStyle('GD', fontName='Helvetica', fontSize=11, leading=16, textColor=DARK, leftIndent=20, spaceAfter=10),
    ]:
        s.add(ps)
    return s

def cdblk(code, s):
    t = Table([[Preformatted(code.strip(), s['Cd'])]], colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),CBG), ('BOX',(0,0),(-1,-1),1,CBR),
        ('LEFTPADDING',(0,0),(-1,-1),10), ('RIGHTPADDING',(0,0),(-1,-1),10),
        ('TOPPADDING',(0,0),(-1,-1),8),   ('BOTTOMPADDING',(0,0),(-1,-1),8),
    ]))
    return t

def ibox(txt, s):
    t = Table([[Paragraph(txt, s['Bod'])]], colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),IBG), ('BOX',(0,0),(-1,-1),1.5,IBR),
        ('LEFTPADDING',(0,0),(-1,-1),12), ('RIGHTPADDING',(0,0),(-1,-1),12),
        ('TOPPADDING',(0,0),(-1,-1),10),  ('BOTTOMPADDING',(0,0),(-1,-1),10),
    ]))
    return t

def wbox(txt, s):
    t = Table([[Paragraph(txt, s['Bod'])]], colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),WBG), ('BOX',(0,0),(-1,-1),1.5,WBR),
        ('LEFTPADDING',(0,0),(-1,-1),12), ('RIGHTPADDING',(0,0),(-1,-1),12),
        ('TOPPADDING',(0,0),(-1,-1),10),  ('BOTTOMPADDING',(0,0),(-1,-1),10),
    ]))
    return t

def gbox(txt, s):
    t = Table([[Paragraph(txt, s['Bod'])]], colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),GBG), ('BOX',(0,0),(-1,-1),1.5,GBR),
        ('LEFTPADDING',(0,0),(-1,-1),12), ('RIGHTPADDING',(0,0),(-1,-1),12),
        ('TOPPADDING',(0,0),(-1,-1),10),  ('BOTTOMPADDING',(0,0),(-1,-1),10),
    ]))
    return t

def pp(txt, sn, s): return Paragraph(txt, s[sn])
def sp(n=1): return Spacer(1, n * 0.4 * cm)
def hr(): return HRFlowable(width="100%", thickness=1, color=CBR, spaceAfter=6, spaceBefore=6)

def bul(items, s, lv=0):
    sn, mk = ('BL2', '◦') if lv else ('BL', '•')
    return [Paragraph(f"{mk}  {i}", s[sn]) for i in items]

def hf(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setFillColor(MUTED); canvas.setFont("Helvetica", 8)
        canvas.drawString(M, H - 1.4*cm, "RAG Document Assistant — Documentación Técnica")
        canvas.drawRightString(W - M, H - 1.4*cm, f"Página {doc.page}")
        canvas.setStrokeColor(CBR); canvas.setLineWidth(0.5)
        canvas.line(M, H - 1.6*cm, W - M, H - 1.6*cm)
        canvas.drawString(M, 1.2*cm, "Python · FastAPI · LangChain · ChromaDB · OpenAI")
        canvas.drawRightString(W - M, 1.2*cm, datetime.now().strftime("%B %Y"))
        canvas.line(M, 1.6*cm, W - M, 1.6*cm)
    canvas.restoreState()


# ═══════════════════════════════════════════════════════════
# SECCIONES
# ═══════════════════════════════════════════════════════════

def sec_cover(s):
    return [
        sp(2),
        Table([
            [pp("RAG Document Assistant", 'CovT', s)],
            [pp("Documentación Técnica Completa", 'CovS', s)],
            [pp(" ", 'CovM', s)],
            [pp("Python · FastAPI · LangChain · ChromaDB · OpenAI", 'CovM', s)],
            [pp(" ", 'CovM', s)],
            [pp(f"Versión 1.0  ·  {datetime.now().strftime('%B %Y')}", 'CovM', s)],
        ], colWidths=[CW], style=TableStyle([
            ('BACKGROUND',(0,0),(-1,-1),PRIMARY),
            ('LEFTPADDING',(0,0),(-1,-1),40), ('RIGHTPADDING',(0,0),(-1,-1),40),
            ('TOPPADDING',(0,0),(0,0),40),
            ('TOPPADDING',(0,1),(-1,-1),14),
            ('BOTTOMPADDING',(0,-1),(-1,-1),40),
        ])),
        sp(2),
        ibox(
            "Este documento cubre en profundidad cada componente del sistema RAG: "
            "arquitectura completa, código fuente comentado línea por línea, conceptos "
            "técnicos fundamentales con analogías, decisiones de diseño justificadas "
            "y glosario. Escrito para quien quiere entender no solo el qué, sino el cómo y el por qué.", s),
        PageBreak(),
    ]


def sec_toc(s):
    fl = [pp("Índice de Contenidos", 'H1', s), hr(), sp()]
    entries = [
        ("1.", "Introducción al sistema RAG", False),
        ("1.1", "¿Qué es RAG?", True),
        ("1.2", "El problema que resuelve", True),
        ("1.3", "Cómo funciona conceptualmente", True),
        ("1.4", "RAG vs. alternativas", True),
        ("2.", "Arquitectura general del proyecto", False),
        ("2.1", "Diagrama de flujo de datos", True),
        ("2.2", "Las dos fases del sistema", True),
        ("2.3", "Componentes y tecnologías", True),
        ("3.", "Análisis detallado — archivo por archivo", False),
        ("3.1", "app/config.py — Configuración", True),
        ("3.2", "app/ingest.py — Ingesta de documentos", True),
        ("3.3", "app/query.py — Consulta RAG", True),
        ("3.4", "app/main.py — API FastAPI", True),
        ("4.", "Flujo completo de una request", False),
        ("4.1", "Fase 1: de PDF a vector (ingesta)", True),
        ("4.2", "Fase 2: de pregunta a respuesta (consulta)", True),
        ("5.", "Conceptos clave en profundidad", False),
        ("5.1", "Embeddings y representación vectorial", True),
        ("5.2", "Similarity search y cosine similarity", True),
        ("5.3", "Chunking y overlap", True),
        ("5.4", "Prompt engineering", True),
        ("5.5", "LCEL: LangChain Expression Language", True),
        ("6.", "Dependencias y librerías", False),
        ("7.", "Decisiones de diseño", False),
        ("8.", "Glosario de términos técnicos", False),
    ]
    for num, title, sub in entries:
        sn = 'TOC2' if sub else 'TOC1'
        fl.append(pp(f"{num}&nbsp;&nbsp;&nbsp;{title}", sn, s))
    fl.append(PageBreak())
    return fl


def sec_intro(s):
    fl = [pp("1. Introducción al sistema RAG", 'H1', s), hr()]

    fl += [pp("1.1 ¿Qué es RAG?", 'H2', s)]
    fl += [pp(
        "RAG (Retrieval-Augmented Generation — Generación Aumentada por Recuperación) "
        "es una arquitectura de inteligencia artificial que combina dos capacidades: "
        "buscar información relevante en una base de datos (retrieval) y generar texto "
        "coherente y contextualizado usando un modelo de lenguaje (generation).", 'Bod', s)]
    fl += [ibox(
        "<b>Analogía fundamental:</b> Imaginá un estudiante universitario extremadamente "
        "inteligente (el LLM). Sabe todo lo que estudió durante su carrera, pero no puede "
        "saber el contenido de un libro que nunca leyó. RAG es equivalente a darle ese libro "
        "antes del examen: primero lo hojea (retrieval), encuentra los párrafos relevantes, "
        "y luego responde la pregunta con esa información fresca (generation).", s), sp()]

    fl += [pp("1.2 El problema que resuelve", 'H2', s)]
    fl += [pp(
        "Los Modelos de Lenguaje Grande (LLMs) como GPT tienen dos limitaciones estructurales "
        "que RAG resuelve directamente:", 'Bod', s)]
    fl += bul([
        "<b>Conocimiento estático:</b> el modelo solo sabe lo que aprendió durante su entrenamiento "
        "(generalmente hasta una fecha de corte). No puede responder preguntas sobre eventos recientes "
        "ni sobre información que no estaba disponible públicamente.",
        "<b>Sin acceso a documentos privados:</b> el modelo nunca vio tu documentación interna, "
        "tus contratos, tus manuales técnicos, ni tus PDFs corporativos. No puede responder "
        "preguntas sobre ellos.",
        "<b>Alucinaciones:</b> cuando el modelo no sabe algo, tiende a inventar respuestas "
        "que suenan plausibles pero son incorrectas. RAG lo ancla a fuentes reales.",
    ], s)
    fl += [sp(), wbox(
        "<b>Ejemplo concreto:</b> Si le preguntás a GPT '¿Cuál es la política de vacaciones de mi empresa?' "
        "va a inventar una respuesta genérica. Con RAG, primero buscamos en el reglamento interno "
        "de la empresa, encontramos el párrafo exacto, y GPT responde con esa información real.", s), sp()]

    fl += [pp("1.3 Cómo funciona conceptualmente", 'H2', s)]
    fl += [pp("El sistema opera en dos fases completamente separadas:", 'Bod', s)]
    fl += [pp("FASE 1 — Ingesta (se ejecuta una vez por documento):", 'H4', s)]
    fl += bul([
        "Leer el documento PDF completo",
        "Dividirlo en fragmentos de texto manejables (chunks)",
        "Convertir cada fragmento en un vector numérico (embedding)",
        "Guardar esos vectores en una base de datos vectorial (ChromaDB)",
    ], s)
    fl += [sp(), pp("FASE 2 — Consulta (se ejecuta ante cada pregunta del usuario):", 'H4', s)]
    fl += bul([
        "Recibir la pregunta del usuario en lenguaje natural",
        "Convertir la pregunta en un vector numérico (con el mismo modelo de embeddings)",
        "Buscar en ChromaDB los fragmentos cuyo vector es más similar al de la pregunta",
        "Construir un prompt que incluye esos fragmentos como contexto",
        "Enviar el prompt al LLM (GPT) para que genere la respuesta final",
        "Retornar la respuesta junto con las fuentes utilizadas",
    ], s)

    fl += [sp(), pp("1.4 RAG vs. alternativas", 'H2', s)]
    tabla = Table([
        [pp("<b>Técnica</b>", 'Bod', s), pp("<b>Ventajas</b>", 'Bod', s), pp("<b>Desventajas</b>", 'Bod', s)],
        [pp("RAG", 'Bod', s),
         pp("Económico, actualizable, fuentes explícitas, sin reentrenamiento", 'Bod', s),
         pp("Depende de la calidad del retrieval", 'Bod', s)],
        [pp("Fine-tuning", 'Bod', s),
         pp("El modelo 'incorpora' el conocimiento", 'Bod', s),
         pp("Costoso, lento, difícil de actualizar, puede olvidar", 'Bod', s)],
        [pp("Context stuffing", 'Bod', s),
         pp("Simple de implementar", 'Bod', s),
         pp("Limitado por el context window, muy caro en tokens", 'Bod', s)],
    ], colWidths=[CW*0.2, CW*0.45, CW*0.35])
    tabla.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),PRIMARY), ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'), ('FONTSIZE',(0,0),(-1,0),10),
        ('BACKGROUND',(0,1),(-1,1),IBG), ('BACKGROUND',(0,2),(-1,2),WBG),
        ('BACKGROUND',(0,3),(-1,3),GBG),
        ('GRID',(0,0),(-1,-1),0.5,CBR),
        ('LEFTPADDING',(0,0),(-1,-1),8), ('RIGHTPADDING',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),6),  ('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    fl += [tabla, sp(), PageBreak()]
    return fl


def sec_arquitectura(s):
    fl = [pp("2. Arquitectura General del Proyecto", 'H1', s), hr()]

    fl += [pp("2.1 Diagrama de flujo de datos", 'H2', s)]
    fl += [pp("El siguiente diagrama muestra el flujo completo de datos del sistema, "
              "desde que el usuario sube un PDF hasta que recibe una respuesta:", 'Bod', s)]
    fl += [cdblk("""
  USUARIO
     │
     │  POST /ingest (PDF)
     ▼
  ┌─────────────────────────────────────────────────────────┐
  │                    FastAPI (main.py)                    │
  │  Recibe el archivo · Lo valida · Lo guarda en /uploads  │
  └──────────────────────────┬──────────────────────────────┘
                             │ llama a ingest_pdf()
                             ▼
  ┌─────────────────────────────────────────────────────────┐
  │                   ingest.py                             │
  │  PyPDFLoader → páginas                                  │
  │  RecursiveCharacterTextSplitter → chunks (1000 chars)   │
  │  OpenAIEmbeddings → vectores (1536 dimensiones)         │
  │  Chroma.from_documents() → persiste en chroma_db/       │
  └──────────────────────────┬──────────────────────────────┘
                             │
                             ▼
  ┌─────────────────────────────────────────────────────────┐
  │               ChromaDB (chroma_db/)                     │
  │  Base de datos vectorial local y persistente            │
  └─────────────────────────────────────────────────────────┘
                             │
             ┌───────────────┘
             │  POST /query (question + collection_name)
             ▼
  ┌─────────────────────────────────────────────────────────┐
  │                   query.py                              │
  │  Carga colección ChromaDB                               │
  │  similarity_search(question, k=4) → top 4 chunks        │
  │  ChatPromptTemplate → prompt con contexto               │
  │  ChatOpenAI (GPT) → genera respuesta                    │
  │  Retorna { answer, sources }                            │
  └──────────────────────────┬──────────────────────────────┘
                             │
                             ▼
                          USUARIO
                   (respuesta + fuentes)
""", s), sp()]

    fl += [pp("2.2 Las dos fases del sistema", 'H2', s)]
    fl += [pp(
        "Es fundamental entender que el sistema opera en dos momentos distintos y separados. "
        "La fase de ingesta puede ocurrir horas o días antes de la primera consulta, y solo "
        "necesita ejecutarse una vez por documento. La fase de consulta es la que el usuario "
        "experimenta en tiempo real.", 'Bod', s)]
    fl += [ibox(
        "<b>Analogía de la biblioteca:</b> La ingesta es como el trabajo del bibliotecario que "
        "ficha y ordena los libros cuando llegan. La consulta es cuando un estudiante llega, "
        "pide información, el bibliotecario sabe exactamente qué páginas buscar y se las entrega. "
        "El estudiante (GPT) lee esas páginas y responde la pregunta.", s), sp()]

    fl += [pp("2.3 Componentes y tecnologías", 'H2', s)]
    tabla = Table([
        [pp("<b>Componente</b>", 'Bod', s), pp("<b>Tecnología</b>", 'Bod', s), pp("<b>Rol</b>", 'Bod', s)],
        [pp("API REST", 'Bod', s), pp("FastAPI", 'Bod', s), pp("Expone endpoints HTTP al frontend", 'Bod', s)],
        [pp("Carga de PDFs", 'Bod', s), pp("PyPDFLoader", 'Bod', s), pp("Lee y extrae texto página por página", 'Bod', s)],
        [pp("Chunking", 'Bod', s), pp("RecursiveCharacterTextSplitter", 'Bod', s), pp("Divide texto en fragmentos manejables", 'Bod', s)],
        [pp("Embeddings", 'Bod', s), pp("OpenAI text-embedding-ada-002", 'Bod', s), pp("Convierte texto a vectores de 1536 dims", 'Bod', s)],
        [pp("Vector DB", 'Bod', s), pp("ChromaDB", 'Bod', s), pp("Almacena y busca vectores localmente", 'Bod', s)],
        [pp("LLM", 'Bod', s), pp("GPT-3.5-turbo / GPT-4", 'Bod', s), pp("Genera la respuesta final en lenguaje natural", 'Bod', s)],
        [pp("Orquestación", 'Bod', s), pp("LangChain (LCEL)", 'Bod', s), pp("Conecta y encadena todos los componentes", 'Bod', s)],
    ], colWidths=[CW*0.22, CW*0.30, CW*0.48])
    tabla.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),PRIMARY), ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'), ('FONTSIZE',(0,0),(-1,0),10),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, CBG]),
        ('GRID',(0,0),(-1,-1),0.5,CBR),
        ('LEFTPADDING',(0,0),(-1,-1),8), ('RIGHTPADDING',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),6),  ('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ]))
    fl += [tabla, sp(), PageBreak()]
    return fl


def sec_config(s):
    fl = [pp("3. Análisis Detallado — Archivo por Archivo", 'H1', s), hr(),
          pp("3.1 app/config.py — Configuración del Sistema", 'H2', s)]

    fl += [pp(
        "Este módulo cumple una función aparentemente simple pero crítica: centralizar "
        "toda la configuración del sistema en un único lugar. Sin este archivo, cada módulo "
        "tendría que importar <b>python-dotenv</b> y gestionar sus propias variables, lo que "
        "generaría duplicación de código y haría el sistema frágil.", 'Bod', s)]

    fl += [pp("Código completo del módulo:", 'H4', s)]
    fl += [cdblk("""
# Carga y expone la configuración de la aplicación desde variables de entorno.
# OpenAI se usa tanto para embeddings como para generación de respuestas.

import os                      # Módulo estándar: acceso a variables de entorno del SO
from dotenv import load_dotenv # Lee el archivo .env y carga sus pares CLAVE=valor

load_dotenv()  # Ejecuta la lectura del .env. Si no existe, no lanza error (modo silencioso)

def _require(name: str) -> str:
    value = os.getenv(name)    # Busca la variable en el entorno del proceso actual
    if value is None:          # None significa que no fue encontrada (distinto de cadena vacía)
        raise ValueError(
            f"Variable de entorno requerida no encontrada: '{name}'. "
            f"Asegúrate de definirla en tu archivo .env o en el entorno del sistema."
        )
    return value               # Si existe, retorna su valor como string

OPENAI_API_KEY    = _require("OPENAI_API_KEY")    # Falla inmediatamente si no está definida
CHROMA_PERSIST_DIR = _require("CHROMA_PERSIST_DIR") # Ruta donde ChromaDB guarda los datos
UPLOAD_DIR        = _require("UPLOAD_DIR")         # Ruta donde se guardan los PDFs subidos
OPENAI_MODEL      = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")  # Opcional: default gpt-3.5-turbo
""", s), sp()]

    fl += [pp("Análisis línea por línea:", 'H3', s)]
    fl += [pp("<b>import os</b>", 'H4', s)]
    fl += [pp("El módulo <b>os</b> de Python provee acceso al sistema operativo. En este caso "
              "usamos <b>os.getenv(name)</b>, que busca una variable de entorno por nombre. "
              "Las variables de entorno son pares clave-valor que el sistema operativo mantiene "
              "para cada proceso. Cuando ejecutás uvicorn, hereda las variables de entorno de tu "
              "terminal, incluyendo las que load_dotenv() inyectó desde .env.", 'Bod', s)]

    fl += [pp("<b>from dotenv import load_dotenv</b>", 'H4', s)]
    fl += [pp("python-dotenv lee el archivo .env (si existe) y agrega cada par CLAVE=valor "
              "al entorno del proceso usando os.environ. Esto permite que os.getenv() "
              "las encuentre normalmente. Sin esta línea, solo funcionaría si el sistema operativo "
              "ya tuviera esas variables definidas (como en producción con variables de servidor).", 'Bod', s)]

    fl += [pp("<b>La función _require()</b>", 'H4', s)]
    fl += [pp("El prefijo <b>_</b> indica que es una función privada del módulo (convención de Python). "
              "Su propósito es el principio DRY (Don't Repeat Yourself): en lugar de escribir la misma "
              "validación cuatro veces, la encapsulamos una vez. "
              "Usa <b>ValueError</b> y no <b>KeyError</b> porque ValueError comunica mejor "
              "que el problema es de configuración del usuario, no un error de programación.", 'Bod', s)]

    fl += [pp("<b>¿Por qué OPENAI_MODEL usa os.getenv() con default y no _require()?</b>", 'H4', s)]
    fl += [ibox(
        "OPENAI_MODEL es opcional porque tiene un valor sensato por defecto: gpt-3.5-turbo. "
        "El usuario puede no definirla y el sistema funciona igual. En cambio, OPENAI_API_KEY "
        "no tiene default posible — sin ella, ninguna llamada a OpenAI puede funcionar. "
        "Esta distinción entre 'obligatorio' y 'opcional con default' es un patrón de diseño "
        "de configuración muy común.", s), sp()]

    fl += [pp("<b>¿Por qué las constantes están a nivel de módulo y no dentro de funciones?</b>", 'H4', s)]
    fl += [pp("Al estar a nivel de módulo, la validación ocurre en el momento del import. "
              "Si falta una variable, el servidor falla al arrancar con un mensaje claro, "
              "en lugar de fallar silenciosamente en la primera request que llegue. "
              "Esto implementa el principio 'fail fast': fallar pronto y con claridad.", 'Bod', s)]

    fl += [PageBreak()]
    return fl


def sec_ingest(s):
    fl = [pp("3.2 app/ingest.py — Ingesta de Documentos PDF", 'H2', s)]

    fl += [pp(
        "Este módulo implementa el pipeline completo de ingesta: toma un archivo PDF del disco, "
        "lo convierte en fragmentos de texto, genera embeddings para cada fragmento y los "
        "almacena en ChromaDB. Es el corazón de la fase de preparación del sistema RAG.", 'Bod', s)]

    fl += [cdblk("""
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from app.config import OPENAI_API_KEY, CHROMA_PERSIST_DIR

def ingest_pdf(file_path: str) -> dict:
    # PASO 1: extraer el nombre del archivo sin extensión (será el nombre de la colección)
    filename = os.path.splitext(os.path.basename(file_path))[0]

    # PASO 2: cargar el PDF (una página = un Document de LangChain)
    loader = PyPDFLoader(file_path)
    pages = loader.load()           # Lista de objetos Document, uno por página
    total_pages = len(pages)

    # PASO 3: dividir en fragmentos con solapamiento
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,            # Máximo 1000 caracteres por fragmento
        chunk_overlap=200,          # Los últimos 200 chars de un chunk se repiten al inicio del siguiente
    )
    chunks = splitter.split_documents(pages)
    total_chunks = len(chunks)

    # PASO 4: inicializar el modelo de embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    # PASO 5: vectorizar y persistir en ChromaDB
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=filename,
        persist_directory=CHROMA_PERSIST_DIR,
    )

    return {
        "filename": filename,
        "total_pages": total_pages,
        "total_chunks": total_chunks,
        "collection_name": filename,
    }
""", s), sp()]

    fl += [pp("PyPDFLoader — Cargador de PDFs", 'H3', s)]
    fl += [pp("PyPDFLoader usa la librería <b>pypdf</b> internamente para leer el archivo PDF. "
              "Retorna una lista de objetos <b>Document</b> de LangChain, donde cada Document "
              "contiene el texto de una página y un diccionario de metadata con información como "
              "número de página, nombre del archivo, autor, fecha de creación, etc. "
              "Esta metadata viaja junto al texto durante todo el pipeline y aparece en "
              "la respuesta final como 'fuentes'.", 'Bod', s)]

    fl += [pp("RecursiveCharacterTextSplitter — El chunking", 'H3', s)]
    fl += [pp("Este es el componente más crítico para la calidad del sistema. Su función es "
              "dividir textos largos en fragmentos más pequeños que puedan ser vectorizados "
              "y recuperados individualmente.", 'Bod', s)]

    fl += [pp("¿Por qué chunk_size=1000?", 'H4', s)]
    fl += [ibox(
        "<b>1000 caracteres ≈ 150-200 palabras ≈ 1-2 párrafos de texto normal.</b><br/><br/>"
        "Este tamaño es el resultado de balancear tres factores:<br/>"
        "1. <b>Contexto suficiente:</b> un fragmento de 1000 chars contiene suficiente información "
        "para que el LLM pueda responder preguntas sobre él.<br/>"
        "2. <b>Precisión del retrieval:</b> fragmentos más pequeños son más específicos y el "
        "similarity search los encuentra mejor. Fragmentos de 5000 chars contienen tantas ideas "
        "que su vector es un promedio difuso.<br/>"
        "3. <b>Costo de tokens:</b> recuperar 4 chunks de 1000 chars = ~4000 chars = ~1000 tokens "
        "de contexto. Manageable y económico.", s), sp()]

    fl += [pp("¿Por qué chunk_overlap=200?", 'H4', s)]
    fl += [ibox(
        "<b>El overlap del 20% previene la pérdida de información en los bordes.</b><br/><br/>"
        "Imaginá un párrafo que dice: '...la temperatura debe mantenerse entre 20° y 25°C "
        "para garantizar la estabilidad del compuesto.' Si esta oración queda partida entre "
        "dos chunks (la primera mitad al final del chunk 1, la segunda al inicio del chunk 2), "
        "ninguno de los dos contiene la información completa. El overlap de 200 chars garantiza "
        "que esos 200 últimos caracteres del chunk 1 también aparecen al inicio del chunk 2.", s), sp()]

    fl += [pp("'Recursive' en el nombre — estrategia de división", 'H4', s)]
    fl += [pp("El splitter intenta dividir primero por párrafos (doble salto de línea), "
              "luego por oraciones (punto), luego por palabras, y finalmente por caracteres. "
              "Esto respeta la estructura natural del texto: prefiere no cortar en medio de "
              "una oración si puede evitarlo.", 'Bod', s)]

    fl += [pp("OpenAIEmbeddings — De texto a vector", 'H3', s)]
    fl += [pp("Llama a la API de OpenAI con el modelo <b>text-embedding-ada-002</b> "
              "(el default al momento de escritura). Por cada fragmento de texto, retorna "
              "un vector de <b>1536 números decimales</b> que representa el significado "
              "semántico del texto en un espacio de alta dimensión. "
              "Textos con significados similares tendrán vectores similares (cercanos en el espacio).", 'Bod', s)]

    fl += [pp("Chroma.from_documents() — Vectorizar y persistir", 'H3', s)]
    fl += [pp("Este método realiza dos operaciones en una llamada:<br/>"
              "1. Llama a OpenAIEmbeddings para generar el vector de cada chunk (una llamada a la API por chunk).<br/>"
              "2. Guarda los pares (texto, vector, metadata) en ChromaDB usando SQLite y "
              "archivos de segmento binarios en el directorio CHROMA_PERSIST_DIR.", 'Bod', s)]

    fl += [wbox(
        "<b>Costo de la ingesta:</b> Ingestar un PDF de 168 chunks implica 168 llamadas al "
        "endpoint de embeddings de OpenAI. Con text-embedding-ada-002, el costo es "
        "aproximadamente $0.0001 por 1000 tokens, lo que hace que ingestar documentos "
        "promedio cueste fracciones de centavo.", s), sp(), PageBreak()]
    return fl


def sec_query(s):
    fl = [pp("3.3 app/query.py — Consulta RAG", 'H2', s)]
    fl += [pp(
        "Este módulo implementa el pipeline de consulta: recibe una pregunta, la busca "
        "en ChromaDB, recupera contexto relevante, construye un prompt y genera la respuesta. "
        "Es donde ocurre la 'magia' del RAG.", 'Bod', s)]

    fl += [cdblk("""
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config import OPENAI_API_KEY, CHROMA_PERSIST_DIR, OPENAI_MODEL

PROMPT_TEMPLATE = \"\"\"
Eres un asistente experto en análisis de documentos.
Usa únicamente el siguiente contexto extraído del documento para responder la pregunta.
Si la respuesta no se encuentra en el contexto, indícalo claramente en español.

Contexto:
{context}

Pregunta:
{question}

Responde de forma clara y concisa en español.
\"\"\"

def query_documents(question: str, collection_name: str) -> dict:
    try:
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

        vectorstore = Chroma(
            collection_name=collection_name,
            persist_directory=CHROMA_PERSIST_DIR,
            embedding_function=embeddings,
        )

        results = vectorstore.similarity_search(question, k=4)

        if not results:
            return {"answer": "No se encontraron resultados...", "sources": []}

        context = "\\n\\n".join([doc.page_content for doc in results])

        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model=OPENAI_MODEL)
        chain = prompt | llm | StrOutputParser()

        answer = chain.invoke({"context": context, "question": question})

        sources = [{"page_content": doc.page_content, "metadata": doc.metadata}
                   for doc in results]

        return {"answer": answer, "sources": sources}

    except Exception as e:
        return {"answer": f"Error: {str(e)}", "sources": []}
""", s), sp()]

    fl += [pp("similarity_search(question, k=4) — La búsqueda vectorial", 'H3', s)]
    fl += [pp("Este método convierte la pregunta en un vector usando el mismo modelo de embeddings "
              "y busca los k fragmentos más cercanos en el espacio vectorial. La similitud se "
              "mide con cosine similarity (ver Sección 5.2).", 'Bod', s)]
    fl += [ibox(
        "<b>¿Por qué k=4?</b><br/><br/>"
        "k=4 chunks × ~1000 chars/chunk = ~4000 chars ≈ 1000 tokens de contexto. "
        "Es el balance óptimo entre:<br/>"
        "• <b>Suficiente contexto:</b> con k=1 podría faltar información si la respuesta "
        "está distribuida en varios párrafos.<br/>"
        "• <b>Sin ruido excesivo:</b> con k=10, el contexto incluiría fragmentos poco "
        "relevantes que confunden al LLM y elevan el costo.<br/>"
        "• <b>Costo de tokens:</b> 1000 tokens de contexto a GPT-3.5 cuesta ~$0.001 por consulta.", s), sp()]

    fl += [pp("El PROMPT_TEMPLATE — Ingeniería de prompts", 'H3', s)]
    fl += [pp("El prompt tiene tres instrucciones críticas:<br/>"
              "1. <b>'Eres un asistente experto en análisis de documentos'</b> — establece el rol del modelo.<br/>"
              "2. <b>'Usa únicamente el siguiente contexto'</b> — evita que el modelo use su conocimiento "
              "previo y se invente respuestas no fundamentadas en el documento.<br/>"
              "3. <b>'Si la respuesta no se encuentra en el contexto, indícalo'</b> — fuerza honestidad "
              "ante preguntas que el documento no responde.", 'Bod', s)]

    fl += [pp("LCEL: El operador pipe (|)", 'H3', s)]
    fl += [cdblk("chain = prompt | llm | StrOutputParser()", s)]
    fl += [pp("LCEL (LangChain Expression Language) usa el operador <b>|</b> (pipe) de Python para "
              "encadenar componentes. Cada componente recibe la salida del anterior como entrada. "
              "El flujo es:<br/>"
              "1. <b>prompt</b>: recibe {context, question} → retorna un ChatPromptValue<br/>"
              "2. <b>llm</b>: recibe el prompt formateado → retorna un AIMessage (objeto de LangChain)<br/>"
              "3. <b>StrOutputParser</b>: recibe el AIMessage → extrae el texto como string Python", 'Bod', s)]
    fl += [ibox(
        "<b>¿Por qué LCEL en lugar de RetrievalQA?</b><br/><br/>"
        "RetrievalQA es la versión antigua de LangChain para hacer RAG. Funciona pero es una "
        "'caja negra': oculta lo que pasa internamente. LCEL es explícito — cada paso es visible "
        "en el código. Esto hace el sistema más fácil de depurar, modificar y entender. "
        "Es el approach moderno recomendado por LangChain desde v0.2.", s), sp(), PageBreak()]
    return fl


def sec_main(s):
    fl = [pp("3.4 app/main.py — API FastAPI", 'H2', s)]
    fl += [pp(
        "main.py es el punto de entrada del backend. Define la aplicación FastAPI, "
        "configura el middleware de CORS, y expone los cuatro endpoints que el frontend "
        "utiliza para interactuar con el sistema.", 'Bod', s)]

    fl += [pp("Configuración inicial de FastAPI:", 'H3', s)]
    fl += [cdblk("""
app = FastAPI(
    title="RAG Document Assistant",
    description="API para ingestar documentos PDF y consultarlos mediante RAG.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # Acepta peticiones de cualquier origen (localhost:3000, etc.)
    allow_credentials=True,
    allow_methods=["*"],     # GET, POST, PUT, DELETE, OPTIONS, etc.
    allow_headers=["*"],     # Authorization, Content-Type, etc.
)

os.makedirs(UPLOAD_DIR, exist_ok=True)     # Crea /uploads si no existe
os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)  # Crea /chroma_db si no existe
""", s), sp()]

    fl += [pp("¿Por qué FastAPI y no Flask o Django?", 'H4', s)]
    fl += bul([
        "<b>Async nativo:</b> FastAPI está construido sobre ASGI (Asynchronous Server Gateway Interface). "
        "Las operaciones de I/O (leer archivos, llamar a APIs externas) no bloquean el servidor.",
        "<b>Validación automática con Pydantic:</b> al declarar QueryRequest(BaseModel), FastAPI "
        "valida automáticamente que el JSON entrante tiene los campos correctos y los tipos correctos.",
        "<b>Documentación automática:</b> FastAPI genera /docs (Swagger UI) y /redoc sin código adicional.",
        "<b>Type hints nativos:</b> usa las anotaciones de tipo de Python para todo lo anterior.",
    ], s)

    fl += [pp("¿Qué es CORS y por qué habilitarlo?", 'H4', s)]
    fl += [ibox(
        "<b>CORS (Cross-Origin Resource Sharing)</b> es un mecanismo de seguridad de los navegadores "
        "que bloquea peticiones HTTP desde un origen (ej: http://localhost:3000) hacia otro origen "
        "(ej: http://localhost:8000) a menos que el servidor lo permita explícitamente.<br/><br/>"
        "Sin CORS habilitado, cuando el frontend Next.js intente hacer fetch() a la API de FastAPI, "
        "el navegador bloqueará la petición. Con allow_origins=['*'] lo permitimos desde cualquier origen. "
        "En producción, se debería restringir al dominio real del frontend.", s), sp()]

    fl += [pp("Los cuatro endpoints:", 'H3', s)]

    fl += [pp("GET /health", 'H4', s)]
    fl += [cdblk("""
@app.get("/health")
async def health_check():
    return {"status": "ok"}
""", s)]
    fl += [pp("El endpoint más simple. Su único propósito es verificar que el servidor está corriendo. "
              "Es útil para sistemas de monitoreo, load balancers y para depuración rápida.", 'Bod', s)]

    fl += [pp("POST /ingest", 'H4', s)]
    fl += [cdblk("""
@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solo se aceptan archivos PDF.")
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)  # Streaming: no carga todo en memoria
    result = ingest_pdf(file_path)
    return result
""", s)]
    fl += [pp("<b>UploadFile</b> es el tipo de FastAPI para archivos subidos via multipart/form-data. "
              "<b>shutil.copyfileobj()</b> copia el stream del archivo directamente al disco en "
              "bloques (streaming), lo que permite manejar PDFs grandes sin agotar la memoria RAM.", 'Bod', s)]

    fl += [pp("POST /query", 'H4', s)]
    fl += [cdblk("""
class QueryRequest(BaseModel):
    question: str
    collection_name: str

@app.post("/query")
async def query_document(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía.")
    return query_documents(request.question, request.collection_name)
""", s)]
    fl += [pp("<b>BaseModel de Pydantic</b> actúa como esquema: si el cliente envía JSON sin 'question' "
              "o con un tipo incorrecto, FastAPI retorna automáticamente un error 422 descriptivo "
              "antes de llegar al código de la función.", 'Bod', s)]

    fl += [pp("GET /collections", 'H4', s)]
    fl += [cdblk("""
@app.get("/collections")
async def list_collections():
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    collections = client.list_collections()
    names = [col.name for col in collections]
    return {"collections": names}
""", s)]
    fl += [pp("Usa el cliente nativo de ChromaDB para listar las colecciones existentes. "
              "Más confiable que inspeccionar el sistema de archivos, porque ChromaDB no "
              "guarda una carpeta por colección con el nombre legible — usa IDs internos.", 'Bod', s)]
    fl += [sp(), PageBreak()]
    return fl


def sec_flujo(s):
    fl = [pp("4. Flujo Completo de una Request", 'H1', s), hr()]

    fl += [pp("4.1 Fase de Ingesta: de PDF a Vector", 'H2', s)]
    pasos = [
        ("Paso 1: El usuario sube el PDF", "El frontend hace POST /ingest con el archivo en multipart/form-data. FastAPI recibe el stream y lo delega al endpoint ingest_document()."),
        ("Paso 2: Validación", "FastAPI verifica que el archivo termina en .pdf. Si no, retorna HTTP 400."),
        ("Paso 3: Guardado en disco", "shutil.copyfileobj() escribe el PDF en /uploads/nombre.pdf de forma streaming."),
        ("Paso 4: Carga de páginas", "PyPDFLoader lee el PDF y retorna una lista de Documents, uno por página, cada uno con su metadata."),
        ("Paso 5: Chunking", "RecursiveCharacterTextSplitter divide las páginas en fragmentos de máximo 1000 chars con 200 de overlap. Un PDF de 67 páginas genera ~168 chunks."),
        ("Paso 6: Embedding", "Para cada chunk, OpenAIEmbeddings llama a la API de OpenAI y obtiene un vector de 1536 dimensiones. Son 168 llamadas API en secuencia."),
        ("Paso 7: Persistencia", "Chroma.from_documents() guarda los 168 pares (chunk, vector) en ChromaDB bajo la colección 'nombre-del-pdf'."),
        ("Paso 8: Respuesta", "FastAPI retorna {filename, total_pages, total_chunks, collection_name} al frontend."),
    ]
    for titulo, desc in pasos:
        fl += [pp(f"<b>{titulo}</b>", 'BL', s), pp(desc, 'BL2', s)]
    fl += [sp()]

    fl += [pp("4.2 Fase de Consulta: de Pregunta a Respuesta", 'H2', s)]
    pasos2 = [
        ("Paso 1: El usuario escribe una pregunta", "El frontend hace POST /query con {question: '¿De qué trata?', collection_name: 'Resumen-Libro'}."),
        ("Paso 2: Validación Pydantic", "FastAPI deserializa el JSON y valida el esquema QueryRequest automáticamente."),
        ("Paso 3: Vectorización de la pregunta", "OpenAIEmbeddings convierte la pregunta en un vector de 1536 dimensiones. Una sola llamada API."),
        ("Paso 4: Similarity search", "ChromaDB calcula la cosine similarity entre el vector de la pregunta y los 168 vectores almacenados. Retorna los 4 más cercanos (k=4)."),
        ("Paso 5: Construcción del contexto", "Los page_content de los 4 chunks se unen con doble salto de línea para formar el bloque de contexto."),
        ("Paso 6: Formateo del prompt", "ChatPromptTemplate rellena {context} y {question} en la plantilla PROMPT_TEMPLATE."),
        ("Paso 7: Generación con GPT", "ChatOpenAI envía el prompt a GPT-3.5-turbo (o el modelo configurado). GPT lee el contexto y genera la respuesta."),
        ("Paso 8: Parsing", "StrOutputParser extrae el texto plano del AIMessage que retorna GPT."),
        ("Paso 9: Construcción de fuentes", "Se construye la lista de sources con page_content y metadata de cada uno de los 4 chunks recuperados."),
        ("Paso 10: Respuesta", "FastAPI retorna {answer: '...', sources: [{page_content, metadata}, ...]} al frontend."),
    ]
    for titulo, desc in pasos2:
        fl += [pp(f"<b>{titulo}</b>", 'BL', s), pp(desc, 'BL2', s)]
    fl += [sp(), PageBreak()]
    return fl


def sec_conceptos(s):
    fl = [pp("5. Conceptos Clave en Profundidad", 'H1', s), hr()]

    fl += [pp("5.1 Embeddings y Representación Vectorial", 'H2', s)]
    fl += [pp("Un embedding es una representación numérica de un texto en forma de vector. "
              "Un vector es simplemente una lista de números decimales.", 'Bod', s)]
    fl += [cdblk("""
# Un embedding de la frase "el perro corre" podría verse así (simplificado a 8 dims):
embedding = [0.234, -0.891, 0.445, 0.012, -0.334, 0.789, -0.123, 0.567]

# En realidad, text-embedding-ada-002 genera vectores de 1536 dimensiones:
embedding_real = [0.002, -0.045, 0.123, ..., 0.089]  # 1536 números
""", s)]
    fl += [ibox(
        "<b>Analogía de las coordenadas:</b> Así como GPS usa 3 números (latitud, longitud, altitud) "
        "para ubicar cualquier punto en el planeta, un embedding usa 1536 números para ubicar "
        "cualquier texto en un 'planeta del significado'. Textos con significados similares "
        "tienen coordenadas cercanas. 'El perro corre' y 'El can galopa' están cerca. "
        "'El perro corre' y 'La economía global' están lejos.", s), sp()]

    fl += [pp("¿Cómo aprende el modelo a asignar coordenadas?", 'H4', s)]
    fl += [pp("El modelo de embeddings fue entrenado con enormes cantidades de texto. "
              "Aprendió que palabras que aparecen en los mismos contextos tienen significados "
              "similares. 'Rey' y 'Reina' aparecen en contextos parecidos, así que sus "
              "vectores son similares. Esta propiedad permite operaciones algebraicas "
              "famosas: vector(Rey) - vector(Hombre) + vector(Mujer) ≈ vector(Reina).", 'Bod', s)]

    fl += [pp("5.2 Similarity Search y Cosine Similarity", 'H2', s)]
    fl += [pp("Cuando buscamos los chunks más relevantes para una pregunta, calculamos qué tan "
              "similares son sus vectores. La métrica más usada es la <b>cosine similarity</b>.", 'Bod', s)]
    fl += [cdblk("""
# Cosine similarity mide el ángulo entre dos vectores (no su distancia)
# Resultado entre -1 y 1:
#   1.0  = vectores idénticos (misma dirección)
#   0.0  = vectores perpendiculares (sin relación semántica)
#  -1.0  = vectores opuestos (significados opuestos)

cosine_similarity(vector_pregunta, vector_chunk_1) = 0.87  # Muy relevante
cosine_similarity(vector_pregunta, vector_chunk_2) = 0.23  # Poco relevante
cosine_similarity(vector_pregunta, vector_chunk_3) = 0.79  # Bastante relevante
cosine_similarity(vector_pregunta, vector_chunk_4) = 0.81  # Relevante
""", s)]
    fl += [ibox(
        "<b>¿Por qué el ángulo y no la distancia euclidiana?</b> La distancia euclidiana "
        "depende de la magnitud (longitud) del vector, que en embeddings de texto varía según "
        "el largo del texto. El coseno mide solo la dirección, que corresponde al significado. "
        "Dos textos idénticos pero uno más largo que el otro tendrán el mismo coseno (1.0) "
        "pero diferente distancia euclidiana.", s), sp()]

    fl += [pp("5.3 Chunking y Overlap", 'H2', s)]
    fl += [pp("Chunking es la división del texto en fragmentos. Es necesario porque:", 'Bod', s)]
    fl += bul([
        "Los modelos de embeddings tienen límites de tokens por llamada (~8000 para ada-002).",
        "Fragmentos más pequeños tienen vectores más precisos y específicos, lo que mejora el retrieval.",
        "La búsqueda es más granular: encontramos el párrafo exacto, no el capítulo entero.",
        "Reducimos el costo: enviamos al LLM solo los fragmentos relevantes, no el documento completo.",
    ], s)

    fl += [sp(), pp("El overlap (solapamiento) en detalle:", 'H4', s)]
    fl += [cdblk("""
Texto original:
"...El protocolo TCP garantiza la entrega ordenada. Por ello se usa en HTTP y FTP.
UDP, en cambio, no garantiza el orden pero es más rápido..."

Sin overlap (chunk_overlap=0):
  Chunk 1: "...El protocolo TCP garantiza la entrega ordenada. Por ello se usa en HTTP y FTP."
  Chunk 2: "UDP, en cambio, no garantiza el orden pero es más rápido..."

Con overlap (chunk_overlap=200, ~40 chars en este ejemplo):
  Chunk 1: "...El protocolo TCP garantiza la entrega ordenada. Por ello se usa en HTTP y FTP."
  Chunk 2: "Por ello se usa en HTTP y FTP. UDP, en cambio, no garantiza el orden pero es más rápido..."
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
             Esta parte se repite → ningún chunk pierde contexto
""", s), sp()]

    fl += [pp("5.4 Prompt Engineering", 'H2', s)]
    fl += [pp("El prompt es la instrucción que le damos al LLM. Su estructura determina la "
              "calidad de las respuestas. Nuestro prompt tiene tres secciones:", 'Bod', s)]
    fl += bul([
        "<b>System context:</b> 'Eres un asistente experto en análisis de documentos' — define el rol.",
        "<b>Restricción:</b> 'Usa únicamente el siguiente contexto' — evita alucinaciones.",
        "<b>Escape hatch:</b> 'Si no está en el contexto, indícalo' — honestidad ante preguntas sin respuesta.",
        "<b>Contexto dinámico:</b> los 4 chunks recuperados, insertados como {context}.",
        "<b>Pregunta:</b> la consulta del usuario, insertada como {question}.",
    ], s)

    fl += [sp(), pp("5.5 LCEL: LangChain Expression Language", 'H2', s)]
    fl += [pp("LCEL es la forma moderna de componer pipelines en LangChain. Usa el operador "
              "<b>|</b> (pipe) de Python para encadenar componentes:", 'Bod', s)]
    fl += [cdblk("""
# Pipeline RAG en LCEL:
chain = prompt | llm | StrOutputParser()

# Equivale a:
prompt_value  = prompt.invoke({"context": context, "question": question})
ai_message    = llm.invoke(prompt_value)
answer_string = StrOutputParser().invoke(ai_message)

# LCEL también soporta streaming, async, y batch con la misma sintaxis:
async for chunk in chain.astream({"context": ctx, "question": q}):
    print(chunk, end="", flush=True)
""", s)]
    fl += [ibox(
        "<b>Ventajas de LCEL sobre RetrievalQA (el approach antiguo):</b><br/>"
        "• Explícito: cada paso es visible en el código, sin magia oculta.<br/>"
        "• Composable: podés insertar pasos intermedios (logging, transformación) con un | adicional.<br/>"
        "• Consistente: la misma API para invoke, stream, batch y async.<br/>"
        "• Debuggeable: si algo falla, sabés exactamente en qué paso.", s),
          sp(), PageBreak()]
    return fl


def sec_deps(s):
    fl = [pp("6. Dependencias y Librerías", 'H1', s), hr()]
    fl += [pp("Cada dependencia del archivo requirements.txt cumple un rol específico e "
              "irremplazable en el sistema:", 'Bod', s), sp()]

    deps = [
        ("fastapi", "Framework web async para Python. Construye la API REST con validación automática, documentación Swagger y soporte para WebSockets. Elegido sobre Flask por su tipado nativo y rendimiento."),
        ("uvicorn[standard]", "Servidor ASGI que ejecuta la aplicación FastAPI. El extra [standard] incluye watchfiles (recarga automática en dev) y httptools (parser HTTP más rápido). Sin uvicorn, FastAPI no puede recibir peticiones HTTP."),
        ("langchain", "Framework de orquestación para aplicaciones de IA. Provee abstracciones para LLMs, embeddings, vectorstores y chains. Actúa como 'pegamento' entre los componentes."),
        ("langchain-openai", "Paquete de LangChain específico para OpenAI. Provee OpenAIEmbeddings (genera vectores) y ChatOpenAI (llama al chat model). Separado del core para reducir dependencias."),
        ("langchain-community", "Contiene integraciones de la comunidad: PyPDFLoader (carga PDFs) y Chroma (vectorstore). Separado porque estas integraciones tienen sus propias dependencias."),
        ("langchain-text-splitters", "Paquete independiente con los splitters de texto. Incluye RecursiveCharacterTextSplitter. Fue separado de langchain core en v0.2 para reducir el tamaño del paquete base."),
        ("chromadb", "Base de datos vectorial embebida y persistente. Funciona sin servidor externo (todo local), lo que la hace ideal para proyectos de aprendizaje y prototipos. Alternativas: Pinecone (cloud), Weaviate, Qdrant."),
        ("pypdf", "Librería Python para leer archivos PDF. PyPDFLoader de LangChain la usa internamente. Extrae texto página por página y metadata del documento."),
        ("python-dotenv", "Lee archivos .env y carga los pares CLAVE=valor en el entorno del proceso. Permite separar la configuración del código sin hardcodear secretos."),
        ("openai", "SDK oficial de OpenAI para Python. LangChain lo usa internamente para llamar a los endpoints de embeddings y chat completion. Sin este paquete, langchain-openai no funciona."),
        ("python-multipart", "Necesario para que FastAPI procese uploads de archivos en formato multipart/form-data. Sin este paquete, el endpoint POST /ingest falla al intentar recibir el PDF."),
    ]

    for nombre, desc in deps:
        fl += [pp(f"<b>{nombre}</b>", 'H4', s)]
        fl += [pp(desc, 'Bod', s)]

    fl += [PageBreak()]
    return fl


def sec_decisiones(s):
    fl = [pp("7. Decisiones de Diseño", 'H1', s), hr()]
    fl += [pp("Cada decisión técnica del proyecto tiene una justificación. Esta sección "
              "documenta las principales alternativas consideradas y por qué se eligió cada approach.", 'Bod', s)]

    decisiones = [
        ("ChromaDB vs. Pinecone / Weaviate / Qdrant",
         "Se eligió ChromaDB por ser completamente local (sin servidor externo, sin API key adicional, sin costo), "
         "persistente en disco mediante SQLite, y sencilla de configurar. Para un proyecto de aprendizaje, "
         "eliminar la dependencia de un servicio cloud externo reduce la fricción. "
         "Pinecone sería la elección correcta en producción por su escalabilidad."),

        ("OpenAI para embeddings y LLM vs. modelos locales",
         "OpenAI ofrece la mejor relación calidad/facilidad de uso. text-embedding-ada-002 produce embeddings "
         "de alta calidad con una sola llamada API. GPT-3.5-turbo es económico y capaz. "
         "La alternativa sería usar modelos locales (llama3, mistral via Ollama) que eliminarían "
         "el costo de API pero requerirían hardware potente y setup complejo."),

        ("FastAPI vs. Flask vs. Django",
         "FastAPI fue elegido por async nativo (crítico para no bloquear el servidor durante llamadas a OpenAI "
         "que pueden tardar varios segundos), validación automática con Pydantic, y documentación Swagger "
         "incluida. Flask requeriría plugins adicionales para async. Django sería excesivo para una API simple."),

        ("LCEL vs. RetrievalQA de LangChain",
         "LCEL (LangChain Expression Language) es el approach moderno y explícito. RetrievalQA es legacy: "
         "oculta los pasos intermedios y hace difícil la depuración. Con LCEL, cada componente del pipeline "
         "es visible: prompt | llm | parser. Más código, pero mucho más comprensible."),

        ("chunk_size=1000 vs. otros tamaños",
         "1000 chars es el balance entre contexto (suficiente para una idea completa) y precisión del retrieval "
         "(un chunk muy largo tiene un embedding 'difuso' que mezcla muchos temas). "
         "Para documentos técnicos densos podría reducirse a 500. Para narrativa podría subirse a 1500."),

        ("Nombre del PDF como collection_name",
         "Usar el nombre del archivo (sin extensión) como nombre de colección en ChromaDB tiene una "
         "ventaja práctica: es predecible y legible. El usuario sabe que subió 'manual.pdf' y la "
         "colección se llama 'manual'. La alternativa (UUID) sería más robusta pero requeriría "
         "una capa de mapeo nombre→uuid."),

        ("shutil.copyfileobj vs. file.read()",
         "shutil.copyfileobj() copia el stream del archivo en bloques (chunks de 16KB por defecto). "
         "file.read() cargaría todo el PDF en memoria RAM antes de guardarlo. Para PDFs grandes "
         "(100MB+), file.read() puede agotar la memoria. copyfileobj es la práctica correcta."),
    ]

    for titulo, desc in decisiones:
        fl += [pp(titulo, 'H3', s), pp(desc, 'Bod', s)]

    fl += [PageBreak()]
    return fl


def sec_glosario(s):
    fl = [pp("8. Glosario de Términos Técnicos", 'H1', s), hr(), sp()]

    terminos = [
        ("API (Application Programming Interface)",
         "Interfaz que permite que dos sistemas de software se comuniquen. En este proyecto, FastAPI expone una API REST que el frontend usa para subir PDFs y hacer consultas."),
        ("Async / Await",
         "Modelo de programación que permite ejecutar operaciones de I/O (llamadas HTTP, lectura de archivos) sin bloquear el hilo principal del servidor. FastAPI lo usa nativamente."),
        ("Chunk",
         "Fragmento de texto resultante de dividir un documento largo. En este proyecto, chunks de máximo 1000 caracteres con 200 de solapamiento con el chunk anterior."),
        ("ChromaDB",
         "Base de datos vectorial embebida. Almacena pares (texto, vector) y permite búsqueda por similitud semántica. Persiste en disco usando SQLite y archivos binarios."),
        ("CORS (Cross-Origin Resource Sharing)",
         "Mecanismo de seguridad de navegadores que controla qué orígenes pueden hacer peticiones HTTP a un servidor. Debe habilitarse para que el frontend pueda llamar al backend."),
        ("Cosine Similarity",
         "Métrica que mide el ángulo entre dos vectores. Resultado entre -1 y 1. En RAG se usa para encontrar chunks cuyo embedding es más similar al embedding de la pregunta."),
        ("Embedding",
         "Representación numérica (vector) de un texto. Textos semánticamente similares tienen embeddings similares (vectores cercanos). text-embedding-ada-002 genera vectores de 1536 dimensiones."),
        ("FastAPI",
         "Framework web moderno para Python basado en ASGI. Provee validación automática con Pydantic, documentación Swagger y soporte async nativo."),
        ("Fine-tuning",
         "Proceso de reentrenar un modelo de lenguaje con datos específicos para que aprenda nuevos conocimientos. Más costoso y complejo que RAG, pero útil para cambiar el estilo o personalidad del modelo."),
        ("LangChain",
         "Framework de orquestación para aplicaciones de IA. Conecta LLMs, embeddings, vectorstores y otras herramientas mediante abstracciones reutilizables."),
        ("LCEL (LangChain Expression Language)",
         "Sintaxis moderna de LangChain para construir pipelines usando el operador |. Permite encadenar componentes de forma explícita y composable."),
        ("LLM (Large Language Model)",
         "Modelo de lenguaje de gran escala. En este proyecto, GPT-3.5-turbo o GPT-4 de OpenAI. Genera texto coherente y contextualizado en lenguaje natural."),
        ("Multipart/form-data",
         "Formato de encoding HTTP usado para subir archivos. El frontend envía el PDF en este formato; FastAPI lo recibe como UploadFile."),
        ("OpenAI Embeddings",
         "Servicio de OpenAI (modelo text-embedding-ada-002) que convierte texto en vectores de 1536 dimensiones. Costo: ~$0.0001 por 1000 tokens."),
        ("Overlap",
         "Solapamiento entre chunks consecutivos. Garantiza que ideas que cruzan el borde entre dos chunks no se pierdan en ninguno."),
        ("Pydantic",
         "Librería Python de validación de datos mediante type hints. FastAPI la usa para validar automáticamente los cuerpos JSON de las requests."),
        ("PyPDFLoader",
         "Cargador de PDFs de LangChain que usa la librería pypdf internamente. Retorna una lista de Documents con el texto y metadata de cada página."),
        ("RAG (Retrieval-Augmented Generation)",
         "Arquitectura de IA que combina búsqueda semántica (retrieval) con generación de texto (generation). Permite a un LLM responder preguntas sobre documentos privados."),
        ("RecursiveCharacterTextSplitter",
         "Splitter de texto de LangChain que divide por párrafos, luego oraciones, luego palabras, respetando la estructura natural del texto."),
        ("Similarity Search",
         "Búsqueda de los vectores más cercanos a uno dado. ChromaDB la implementa calculando cosine similarity entre el vector de la pregunta y todos los vectors de la colección."),
        ("Vector / Vector Space",
         "Un vector es una lista de números. Un espacio vectorial es el 'universo' donde viven todos esos vectores. En RAG, cada texto tiene un vector que lo ubica en ese espacio."),
        ("Vectorstore",
         "Base de datos especializada en almacenar y buscar vectores. ChromaDB es el vectorstore de este proyecto."),
        ("uvicorn",
         "Servidor ASGI para Python. Ejecuta la aplicación FastAPI y maneja las conexiones HTTP entrantes. Se arranca con 'uvicorn app.main:app --reload'."),
    ]

    for term, defn in terminos:
        fl += [pp(term, 'GT', s), pp(defn, 'GD', s)]

    return fl


def main():
    output = "RAG_Assistant_Documentacion_Tecnica.pdf"
    doc = SimpleDocTemplate(
        output,
        pagesize=A4,
        leftMargin=M, rightMargin=M,
        topMargin=2.4*cm, bottomMargin=2.4*cm,
    )

    s = mk_styles()
    story = []
    story += sec_cover(s)
    story += sec_toc(s)
    story += sec_intro(s)
    story += sec_arquitectura(s)
    story += sec_config(s)
    story += sec_ingest(s)
    story += sec_query(s)
    story += sec_main(s)
    story += sec_flujo(s)
    story += sec_conceptos(s)
    story += sec_deps(s)
    story += sec_decisiones(s)
    story += sec_glosario(s)

    doc.build(story, onFirstPage=hf, onLaterPages=hf)
    print(f"PDF generado: {output}")


if __name__ == "__main__":
    main()
