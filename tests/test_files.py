import unittest
import os
import tempfile
from core.exceptions import FileEncodingError, InvalidFileExtensionError
from application.analysis_service import analizar_archivo

class TestFilesEdgeCases(unittest.TestCase):
    def test_ruta_inexistente(self):
        resumen = analizar_archivo("ruta/falsa/inexistente.txt")
        self.assertEqual(resumen.total_lineas, 0)

    def test_archivo_sin_extension_txt(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.pdf') as f:
            nombre = f.name
        try:
            with self.assertRaises(InvalidFileExtensionError):
                analizar_archivo(nombre)
        finally:
            os.remove(nombre)
            
    def test_codificacion_invalida(self):
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.txt') as f:
            f.write(b'\xff\xfe\x00\x00')
            nombre = f.name
        try:
            with self.assertRaises(FileEncodingError):
                analizar_archivo(nombre)
        finally:
            os.remove(nombre)
