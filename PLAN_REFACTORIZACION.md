# Plan de Refactorización: LogScope

## 1. Arquitectura Actual
Actualmente, LogScope es una aplicación monolítica pequeña:
- `main.py`: Contiene la configuración de Flask, las rutas (`/`, `/upload`, `/upload_text`) y la lógica de creación de archivos temporales.
- `analyzer.py`: Mezcla la extracción de datos (Regex) con la validación de negocio (comprobación de fechas y reglas lógicas) y la lectura de archivos con silenciamiento de excepciones.
- `models.py`: Define los Dataclasses (`ResultadoLinea`, `ResumenAnalisis`).
- `tests/`: Pruebas de unidad para el analizador.

## 2. Problemas Encontrados (Auditoría)
1. **Acoplamiento de responsabilidades**:
   - `analyzer.py -> analizar_archivo`: Lee el archivo, silencia excepciones indiscriminadamente (`except Exception: pass`) y mezcla iteración con lógica de análisis.
   - `analyzer.py -> analizar_linea`: Mezcla parsing (regex) con validación (fechas lógicas).
2. **Uso ineficiente de recursos**:
   - `main.py -> upload_text`: Convierte texto pegado en la UI a un archivo temporal para poder invocar `analizar_archivo`, lo cual es ineficiente y riesgoso si falla la limpieza de temporales.
3. **Manejo de excepciones deficiente**:
   - Bloques `except Exception: pass` en `analyzer.py` que pueden ocultar errores críticos de I/O o codificación.
4. **Falta de arquitectura modular**:
   - `main.py` contiene todo el enrutamiento y setup de Flask (ausencia de App Factory), dificultando las pruebas aisladas.

## 3. Arquitectura Propuesta
Adoptaremos una arquitectura por capas y orientada a dominios:

- **Núcleo (Core)**:
  - `core/models.py` (Dataclasses)
  - `core/parser.py` (Regex y extracción)
  - `core/validator.py` (Reglas de validación pura)
  - `core/exceptions.py` (Excepciones propias)
- **Aplicación**:
  - `application/analysis_service.py` (Servicio que coordina análisis de texto o archivo)
- **Web**:
  - `web/__init__.py` (App Factory)
  - `web/routes.py` (Endpoints)
- **Agente**:
  - `agent/config.py`, `agent/prompt.py`
  - `agent/router.py` (Decisión de qué skill usar)
  - `agent/adapter.py` (Conexión al LLM)
  - `agent/agent.py` (`LogScopeAgent`)
- **Skills**:
  - `skills/validation/`, `skills/explanation/`, `skills/triage/` (Con `SKILL.md` y `resources/`)

## 4. Archivos Modificados, Creados o Movidos
- **Borrados/Movidos**: `analyzer.py` se dividirá en `core/parser.py` y `core/validator.py`. `main.py` se simplificará.
- **Modificados**: `static/script.js` y `templates/index.html` (para agregar el Diagnóstico del Agente de forma segura y evitar innerHTML con data no confiable).
- **Creados**: Estructura `core/`, `application/`, `web/`, `agent/`, `skills/`.

## 5. Riesgos de la Refactorización
- Romper la compatibilidad del frontend si cambian los nombres de las propiedades en el JSON devuelto.
- Errores de importación (circular imports) al mover los modelos.
- Modificar accidentalmente el comportamiento determinista de la validación.

## 6. Estrategia de Compatibilidad
- Las clases `ResumenAnalisis` y `ResultadoLinea` mantendrán la misma estructura serializable para no romper el frontend.
- Los endpoints `/upload` y `/upload_text` devolverán exactamente el mismo contrato JSON.
- Se correrá la batería de pruebas existente *antes* de borrar `analyzer.py` (adaptando los imports) para asegurar que la funcionalidad original se mantiene.

## 7. Relación con la Rúbrica
- **Refactorización del Núcleo**: Cumplido al separar parser, validator y exceptions, y creando análisis directo de texto sin archivos temporales.
- **Skills Propias**: 3 skills creadas con responsabilidades específicas y sin usar LLM para validación.
- **Agente Personalizado**: `LogScopeAgent` con routing explícito y adaptador desacoplado.
- **Integración Web**: Inclusión de "Diagnóstico del agente" renderizado de forma segura usando textContent.
- **Pruebas**: Amplia cobertura (unittest) usando mocks para el LLM.
- **Documentación**: Generación de `NOTA_TECNICA.md`, `USO_IA.md` y actualización del `README.md`.
