"use client"; // Marca este componente como Client Component para usar estado y efectos

import { useEffect, useRef, useState } from "react"; // Hooks de React para estado, efectos y referencias
import {
  getCollections,
  queryDocument,
  QueryResult,
  uploadPDF,
  UploadResult,
} from "@/lib/api"; // Funciones de comunicación con el backend

// Componente principal de la aplicación
export default function Home() {
  // --- Estado del panel de ingesta ---
  const fileInputRef = useRef<HTMLInputElement>(null);         // Referencia al input de archivo para resetearlo tras la subida
  const [selectedFile, setSelectedFile] = useState<File | null>(null); // Archivo PDF seleccionado por el usuario
  const [uploading, setUploading] = useState(false);          // Indica si la subida está en progreso
  const [uploadResult, setUploadResult] = useState<UploadResult | null>(null); // Resultado de la última ingesta exitosa
  const [uploadError, setUploadError] = useState<string | null>(null); // Mensaje de error de ingesta

  // --- Estado del panel de consulta ---
  const [collections, setCollections] = useState<string[]>([]);          // Lista de colecciones disponibles en ChromaDB
  const [selectedCollection, setSelectedCollection] = useState("");       // Colección seleccionada para consultar
  const [question, setQuestion] = useState("");                           // Pregunta escrita por el usuario
  const [querying, setQuerying] = useState(false);                        // Indica si la consulta está en progreso
  const [queryResult, setQueryResult] = useState<QueryResult | null>(null); // Resultado de la última consulta
  const [queryError, setQueryError] = useState<string | null>(null);      // Mensaje de error de consulta

  // Carga las colecciones disponibles al montar el componente
  useEffect(() => {
    fetchCollections(); // Llama a la función que obtiene las colecciones del backend
  }, []); // Array vacío: solo se ejecuta una vez al cargar la página

  // Obtiene la lista de colecciones desde el backend y actualiza el estado
  async function fetchCollections() {
    try {
      const cols = await getCollections(); // Llama a la API y obtiene el array de nombres
      setCollections(cols);                // Actualiza el estado con las colecciones recibidas
      if (cols.length > 0) setSelectedCollection(cols[0]); // Selecciona la primera colección por defecto si hay alguna
    } catch {
      // Si falla la carga de colecciones se ignora silenciosamente (no es crítico al iniciar)
    }
  }

  // Maneja la selección de un archivo PDF desde el input
  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0] || null; // Obtiene el primer archivo seleccionado o null si no hay ninguno
    setSelectedFile(file);   // Actualiza el estado con el archivo seleccionado
    setUploadResult(null);   // Limpia el resultado anterior al seleccionar un nuevo archivo
    setUploadError(null);    // Limpia el error anterior al seleccionar un nuevo archivo
  }

  // Sube el PDF seleccionado al backend y actualiza las colecciones disponibles
  async function handleUpload() {
    if (!selectedFile) return; // No hace nada si no hay archivo seleccionado

    setUploading(true);    // Activa el indicador de carga
    setUploadError(null);  // Limpia errores previos antes de intentar la subida
    setUploadResult(null); // Limpia el resultado previo antes de intentar la subida

    try {
      const result = await uploadPDF(selectedFile); // Envía el PDF al backend y espera el resultado
      setUploadResult(result);                       // Guarda el resultado de la ingesta en el estado
      setSelectedFile(null);                         // Limpia el archivo seleccionado tras la subida exitosa
      if (fileInputRef.current) fileInputRef.current.value = ""; // Resetea el input de archivo visualmente
      await fetchCollections();                      // Recarga las colecciones para incluir la nueva
    } catch (err) {
      setUploadError(err instanceof Error ? err.message : "Error desconocido"); // Muestra el error si la subida falla
    } finally {
      setUploading(false); // Desactiva el indicador de carga siempre, tanto si hubo éxito como error
    }
  }

  // Envía la pregunta al backend y muestra la respuesta generada
  async function handleQuery() {
    if (!question.trim() || !selectedCollection) return; // No hace nada si la pregunta está vacía o no hay colección seleccionada

    setQuerying(true);    // Activa el indicador de carga
    setQueryError(null);  // Limpia errores previos antes de consultar
    setQueryResult(null); // Limpia el resultado previo antes de consultar

    try {
      const result = await queryDocument(question, selectedCollection); // Envía la pregunta al backend
      setQueryResult(result); // Guarda la respuesta y las fuentes en el estado
    } catch (err) {
      setQueryError(err instanceof Error ? err.message : "Error desconocido"); // Muestra el error si la consulta falla
    } finally {
      setQuerying(false); // Desactiva el indicador de carga siempre, tanto si hubo éxito como error
    }
  }

  // Permite enviar la pregunta presionando Enter en el campo de texto
  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) { // Enter solo (sin Shift) envía; Shift+Enter hace salto de línea
      e.preventDefault(); // Previene el salto de línea por defecto al presionar Enter
      handleQuery();       // Ejecuta la consulta
    }
  }

  return (
    <main className="flex flex-col flex-1 max-w-6xl mx-auto w-full px-4 py-8 gap-6">

      {/* Título de la aplicación */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-zinc-800">RAG Document Assistant</h1>
        <p className="text-zinc-500 mt-1">Subí un PDF y consultalo con inteligencia artificial</p>
      </div>

      {/* Contenedor de dos paneles */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 flex-1">

        {/* ── Panel izquierdo: Ingesta ── */}
        <section className="bg-white rounded-2xl shadow-sm border border-zinc-200 p-6 flex flex-col gap-4">
          <h2 className="text-lg font-semibold text-zinc-700">Subir documento</h2>

          {/* Input de archivo */}
          <div className="flex flex-col gap-2">
            <label className="text-sm text-zinc-500">Seleccioná un archivo PDF</label>
            <input
              ref={fileInputRef}              // Referencia para resetear el input tras la subida
              type="file"
              accept=".pdf"                   // Solo permite seleccionar archivos PDF
              onChange={handleFileChange}     // Actualiza el estado al seleccionar un archivo
              className="block w-full text-sm text-zinc-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-zinc-100 file:text-zinc-700 file:cursor-pointer hover:file:bg-zinc-200"
            />
          </div>

          {/* Botón de subida */}
          <button
            onClick={handleUpload}                           // Ejecuta la subida al hacer click
            disabled={!selectedFile || uploading}            // Deshabilitado si no hay archivo o está subiendo
            className="w-full py-2 px-4 rounded-lg bg-zinc-800 text-white font-medium hover:bg-zinc-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            {uploading ? "Procesando..." : "Subir e ingestar"} {/* Texto dinámico según el estado */}
          </button>

          {/* Resultado exitoso de ingesta */}
          {uploadResult && (
            <div className="rounded-lg bg-green-50 border border-green-200 p-4 text-sm text-green-800 flex flex-col gap-1">
              <span className="font-semibold">✓ {uploadResult.filename}</span>
              <span>{uploadResult.total_pages} páginas · {uploadResult.total_chunks} fragmentos</span>
              <span className="text-green-600">Colección: {uploadResult.collection_name}</span>
            </div>
          )}

          {/* Error de ingesta */}
          {uploadError && (
            <div className="rounded-lg bg-red-50 border border-red-200 p-4 text-sm text-red-700">
              {uploadError}
            </div>
          )}

          {/* Lista de colecciones disponibles */}
          {collections.length > 0 && (
            <div className="mt-auto flex flex-col gap-2">
              <span className="text-sm text-zinc-500 font-medium">Documentos disponibles</span>
              <ul className="flex flex-col gap-1">
                {collections.map((col) => ( // Itera sobre cada colección disponible
                  <li
                    key={col} // Clave única para React
                    className="text-sm text-zinc-700 bg-zinc-50 rounded-lg px-3 py-2 border border-zinc-100"
                  >
                    {col}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </section>

        {/* ── Panel derecho: Consulta ── */}
        <section className="bg-white rounded-2xl shadow-sm border border-zinc-200 p-6 flex flex-col gap-4">
          <h2 className="text-lg font-semibold text-zinc-700">Consultar documento</h2>

          {/* Selector de colección */}
          <div className="flex flex-col gap-2">
            <label className="text-sm text-zinc-500">Documento a consultar</label>
            {collections.length === 0 ? ( // Si no hay colecciones muestra un mensaje
              <p className="text-sm text-zinc-400 italic">No hay documentos ingestados todavía</p>
            ) : (
              <select
                value={selectedCollection}                          // Valor controlado por el estado
                onChange={(e) => setSelectedCollection(e.target.value)} // Actualiza la colección seleccionada
                className="w-full border border-zinc-200 rounded-lg px-3 py-2 text-sm text-zinc-700 bg-white focus:outline-none focus:ring-2 focus:ring-zinc-300"
              >
                {collections.map((col) => ( // Renderiza una opción por cada colección disponible
                  <option key={col} value={col}>{col}</option>
                ))}
              </select>
            )}
          </div>

          {/* Campo de pregunta */}
          <div className="flex flex-col gap-2">
            <label className="text-sm text-zinc-500">Tu pregunta</label>
            <textarea
              value={question}                   // Valor controlado por el estado
              onChange={(e) => setQuestion(e.target.value)} // Actualiza la pregunta al escribir
              onKeyDown={handleKeyDown}           // Enter envía la pregunta
              placeholder="¿De qué trata el documento? (Enter para enviar)"
              rows={3}                            // Altura inicial del textarea en líneas
              className="w-full border border-zinc-200 rounded-lg px-3 py-2 text-sm text-zinc-700 resize-none focus:outline-none focus:ring-2 focus:ring-zinc-300"
            />
          </div>

          {/* Botón de consulta */}
          <button
            onClick={handleQuery}                                         // Ejecuta la consulta al hacer click
            disabled={!question.trim() || !selectedCollection || querying} // Deshabilitado si faltan datos o está consultando
            className="w-full py-2 px-4 rounded-lg bg-zinc-800 text-white font-medium hover:bg-zinc-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            {querying ? "Consultando..." : "Preguntar"} {/* Texto dinámico según el estado */}
          </button>

          {/* Error de consulta */}
          {queryError && (
            <div className="rounded-lg bg-red-50 border border-red-200 p-4 text-sm text-red-700">
              {queryError}
            </div>
          )}

          {/* Resultado de la consulta */}
          {queryResult && (
            <div className="flex flex-col gap-3 overflow-y-auto">

              {/* Respuesta del LLM */}
              <div className="rounded-lg bg-zinc-50 border border-zinc-200 p-4 text-sm text-zinc-800 leading-relaxed">
                <span className="font-semibold text-zinc-600 block mb-1">Respuesta</span>
                {queryResult.answer} {/* Texto de la respuesta generada por el modelo */}
              </div>

              {/* Fuentes utilizadas */}
              <div className="flex flex-col gap-2">
                <span className="text-xs font-semibold text-zinc-400 uppercase tracking-wide">
                  Fuentes ({queryResult.sources.length}) {/* Cantidad de fragmentos usados como contexto */}
                </span>
                {queryResult.sources.map((source, index) => ( // Itera sobre cada fragmento fuente
                  <div
                    key={index} // Índice como clave ya que las fuentes no tienen ID propio
                    className="rounded-lg bg-zinc-50 border border-zinc-100 p-3 text-xs text-zinc-600"
                  >
                    <span className="font-medium text-zinc-400">
                      Pág. {String(source.metadata.page_label ?? (Number(source.metadata.page) + 1))} {/* Número de página, con fallback al índice +1 */}
                    </span>
                    <p className="mt-1 line-clamp-3">{source.page_content}</p> {/* Muestra hasta 3 líneas del fragmento */}
                  </div>
                ))}
              </div>
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
