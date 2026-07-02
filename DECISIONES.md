# Decisiones técnicas
## 1. Severidades permitidas

Solamente se aceptarán:

- INFO
- WARNING
- ERROR

La severidad podrá escribirse en mayúsculas o minúsculas, pero será
normalizada a mayúsculas.

Ejemplo:

[error] se interpretará como ERROR.

DEBUG, TRACE, CRITICAL y otras severidades serán consideradas inválidas.

## 2. Fecha

La fecha será opcional.

Una línea puede ser válida sin fecha cuando contiene una severidad
permitida y un mensaje no vacío.

Cuando una fecha esté presente deberá:

- Utilizar el formato YYYY-MM-DD.
- Encontrarse después de la severidad.
- Representar una fecha real del calendario.

La expresión regular solamente comprobará la forma de la fecha.

La existencia real de la fecha será validada utilizando datetime.strptime.

## 3. Mensaje

El mensaje será obligatorio.

Una línea que tenga severidad y fecha, pero no tenga mensaje, será
considerada incompleta.

## 4. Línea malformada

Se considerará malformada una línea cuando:

- Esté vacía.
- No tenga severidad.
- Tenga una severidad no permitida.
- No tenga mensaje.
- Contenga una fecha inválida.
- Contenga una fecha imposible.
- Tenga una estructura que no pueda ser interpretada.

## 5. Conteos

Total de líneas incluirá todas las líneas leídas, incluyendo líneas vacías.

Total de eventos válidos incluirá solamente las líneas correctamente
interpretadas.

Las líneas inválidas no se sumarán a INFO, WARNING o ERROR.

## 6. Archivos

Solamente se analizarán archivos con extensión .txt.

Los archivos se leerán utilizando UTF-8.

## 7. Interfaz gráfica

La interfaz solamente mostrará los resultados producidos por el núcleo
del analizador.

La interfaz no decidirá si una línea es válida o inválida.

Todas las reglas estarán centralizadas en el módulo de análisis.

## 8. Casos borde incluidos

- Ruta inexistente.
- Ruta vacía.
- Archivo sin extensión .txt.
- Archivo vacío.
- Línea vacía.
- Severidad en minúsculas.
- Fecha imposible.
- Fecha con formato incorrecto.
- Mensaje vacío.
- Archivo con caracteres UTF-8.
- Rutas de Windows rodeadas de comillas.

## 9. Casos no incluidos

- Fechas con hora.
- Zonas horarias.
- Registros de varias líneas.
- Archivos JSON.
- Archivos CSV.
- Archivos extremadamente grandes.
- Procesamiento en tiempo real.