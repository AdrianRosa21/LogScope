# CHANGELOG REFACTORIZACION

## [v2.0.0] - Refactorización de Arquitectura y Skills Agénticas

### Añadido
- **App Factory Pattern**: `web/__init__.py` y `web/routes.py` separan la configuración de Flask de las rutas de negocio, permitiendo un testing robusto con el test client.
- **Service Layer**: `application/analysis_service.py` procesa los archivos o textos en RAM usando el core. Se elimina la necesidad de crear archivos `.txt` temporales al analizar texto.
- **Agent Orchestration**: `agent/agent.py` añade un `LogScopeAgent` que coordina a un router y a un adaptador LLM simulado para mantener autonomía de dependencias externas en desarrollo local.
- **Skills Directory**: 
  - `skills/validation/`: Encapsula reglas Regex deterministas que rechazan fallas de estructura (ej: fechas en el futuro como `2025-02-30`).
  - `skills/explanation/`: Sugiere motivos e ideas para solucionar logs mal formados.
  - `skills/triage/`: Define umbrales de severidad críticos usando un JSON de recursos.
- **Tests Unitarios Completos**: 30 pruebas unitarias con una cobertura del 100% (incluye casos límite como inyección de código y simulación de caída de agente).
- **Exportador**: Endpoint `/export` y métodos JS que permiten descargar JSON o TXT generados bajo demanda.
- **Límite Carga Archivos**: Definido `MAX_CONTENT_LENGTH = 16MB` para evitar ataques de DDoS mediante archivos gigantes.
- **Protección contra inyecciones XSS**: El frontend asigna el contenido mediante `textContent` en vez de `innerHTML`.

### Modificado
- `README.md`: Incorporación de Diagrama Mermaid explicando la relación Router-Skill y las instrucciones de testeo.
- `static/script.js`: Reestructuración total para aceptar la conexión al agente inteligente (`/agent_triage`) y mapeo asíncrono para prevenir interfaces congeladas.
- `templates/index.html`: Se integraron paneles en estilo glassmorphism.

### Eliminado (Código Muerto/Anti-patrones)
- `analyzer.py`: Archivo monolítico original borrado de raíz.
- `models.py`: Suprimido de la base para nacer en `core/models.py`.
- Bloques `except Exception: pass` suprimidos en favor del manejo apropiado con excepciones de dominio como `InvalidFileExtensionError` y `FileEncodingError`.
