import type { Metadata } from "next"; // Tipo para definir los metadatos de la página
import { Geist, Geist_Mono } from "next/font/google"; // Fuentes de Google optimizadas por Next.js
import "./globals.css"; // Estilos globales con Tailwind

// Configura la fuente sans-serif principal como variable CSS
const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

// Configura la fuente monoespaciada como variable CSS
const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

// Metadatos que aparecen en la pestaña del navegador y en SEO
export const metadata: Metadata = {
  title: "RAG Document Assistant",
  description: "Subí un PDF y consultalo con inteligencia artificial.",
};

// Componente raíz que envuelve toda la aplicación
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode; // Contenido de cada página que se renderiza dentro del layout
}>) {
  return (
    <html
      lang="es" // Idioma español para accesibilidad y SEO
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`} // Variables de fuente + altura completa + suavizado
    >
      <body className="min-h-full flex flex-col bg-zinc-50">{children}</body>
    </html>
  );
}
