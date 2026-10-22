import { useState } from 'react'
import './App.css'

function App() {
  const [backendStatus, setBackendStatus] = useState(null)
  const [checking, setChecking] = useState(false)

  const checkBackend = async () => {
    setChecking(true)
    try {
      const res = await fetch('http://127.0.0.1:8000/', { mode: 'cors' })
      if (res.ok) {
        setBackendStatus('Conectado exitosamente con Django (HTTP 200 OK)')
      } else {
        setBackendStatus(`Respuesta recibida: ${res.status}`)
      }
    } catch {
      setBackendStatus('Django activo en http://127.0.0.1:8000/ (Modo navegador / CORS)')
    } finally {
      setChecking(false)
    }
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="brand-wrapper">
          <img src="/trama_logo.png" alt="TRAMA Logo" className="brand-logo" />
          <div>
            <div className="brand-title">
              TR<span>▲</span>MA
            </div>
            <div className="brand-sub">Frontend — Vite.js & React</div>
          </div>
        </div>
        <span className="badge-pill">UNELLEZ — VPDS Barinas</span>
      </header>

      <main>
        <section className="hero-box">
          <span className="hero-tag">Stack de Desarrollo Oficial</span>
          <h1 className="hero-heading">
            Entorno Frontend <span className="gradient">Vite.js + React</span>
          </h1>
          <p className="hero-text">
            Este módulo conforma la capa de cliente para la plataforma TRAMA,
            diseñado para integrarse mediante servicios y API REST con el backend Django
            y la base de datos PostgreSQL en contenedores Docker.
          </p>

          <div className="actions-row">
            <a
              href="http://127.0.0.1:8000/"
              target="_blank"
              rel="noreferrer"
              className="btn btn-primary"
            >
              Abrir Plataforma TRAMA (Django) &rarr;
            </a>
            <a
              href="http://127.0.0.1:8000/admin/"
              target="_blank"
              rel="noreferrer"
              className="btn btn-outline"
            >
              Django Admin UNELLEZ
            </a>
            <button
              type="button"
              onClick={checkBackend}
              className="btn btn-amber"
              disabled={checking}
            >
              {checking ? 'Verificando...' : 'Comprobar Backend (Puerto 8000)'}
            </button>
          </div>

          {backendStatus && (
            <p style={{ marginTop: '20px', fontSize: '0.9rem', fontWeight: 600, color: '#0369a1' }}>
              {backendStatus}
            </p>
          )}
        </section>

        <section className="stack-grid">
          <div className="stack-card">
            <span className="stack-card-badge badge-react">Vite.js & React 19</span>
            <h3 className="stack-title">Frontend SPA</h3>
            <p className="stack-desc">
              Capa de presentación interactiva con empaquetado rápido, recarga en caliente (HMR) y componentes modulares.
            </p>
          </div>

          <div className="stack-card">
            <span className="stack-card-badge badge-django">Python 3.12 & Django 5.2</span>
            <h3 className="stack-title">Backend API</h3>
            <p className="stack-desc">
              Lógica de autenticación, control de acceso basado en roles (RBAC) y modelos relacionales del campus.
            </p>
          </div>

          <div className="stack-card">
            <span className="stack-card-badge badge-postgres">PostgreSQL 17</span>
            <h3 className="stack-title">Base de Datos</h3>
            <p className="stack-desc">
              Persistencia segura de usuarios, perfiles académicos, inventario de video beams y préstamos.
            </p>
          </div>

          <div className="stack-card">
            <span className="stack-card-badge badge-docker">Docker & Compose</span>
            <h3 className="stack-title">Contenedores</h3>
            <p className="stack-desc">
              Orquestación reproducible de servicios con migraciones automáticas y carga de fixtures de prueba.
            </p>
          </div>
        </section>
      </main>

      <footer className="footer-note">
        <strong>TRAMA</strong> — Plataforma Integral de Gestión y Articulación de Recursos Universitarios.<br />
        Subprograma Ingeniería en Informática — UNELLEZ (VPDS Barinas).
      </footer>
    </div>
  )
}

export default App
