# Reglas de Validación Aceptadas

1. **Estructura Base**: `[SEVERIDAD] YYYY-MM-DD Mensaje` (los corchetes y la fecha son opcionales según el parser, pero la severidad es obligatoria).
2. **Severidad**: Solo se permite `INFO`, `WARNING` o `ERROR`. (Insensible a mayúsculas/minúsculas).
3. **Fecha**: 
   - Debe tener el formato `YYYY-MM-DD`.
   - DEBE ser una fecha que exista en el calendario real (ej. `2025-02-30` será rechazada).
4. **Mensaje**: Obligatorio.
5. **Líneas malformadas**: Cualquier línea vacía o que no cumpla las reglas será clasificada como malformada.
