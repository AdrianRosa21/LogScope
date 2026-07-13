class LogScopeError(Exception):
    """Excepción base para errores de LogScope."""
    pass

class LogParsingError(LogScopeError):
    """Lanzada cuando hay un error crítico parseando una línea."""
    pass

class FileEncodingError(LogScopeError):
    """Lanzada cuando el archivo tiene un formato de codificación no soportado (e.g. no es UTF-8)."""
    pass

class InvalidFileExtensionError(LogScopeError):
    """Lanzada cuando se intenta analizar un archivo que no sea .txt."""
    pass
