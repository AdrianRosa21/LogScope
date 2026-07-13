import unittest
import os
import tempfile
from datetime import datetime
from core.validator import analizar_linea
from application.analysis_service import analizar_archivo, analizar_texto

class TestCoreAnalyzer(unittest.TestCase):
    def test_01_info_con_fecha_valida(self):
        res = analizar_linea("[INFO] 2025-10-15 Todo bien", 1)
        self.assertTrue(res.es_valida)
        self.assertEqual(res.severidad, "INFO")
        self.assertTrue(res.tiene_fecha)
        self.assertEqual(res.fecha, datetime(2025, 10, 15))
        self.assertEqual(res.mensaje, "Todo bien")

    def test_02_warning_sin_fecha(self):
        res = analizar_linea("WARNING Cuidado", 2)
        self.assertTrue(res.es_valida)
        self.assertEqual(res.severidad, "WARNING")
        self.assertFalse(res.tiene_fecha)
        self.assertEqual(res.mensaje, "Cuidado")

    def test_03_error_en_minusculas(self):
        res = analizar_linea("[error] Fallo fatal", 3)
        self.assertTrue(res.es_valida)
        self.assertEqual(res.severidad, "ERROR")

    def test_04_fecha_imposible(self):
        res = analizar_linea("[INFO] 2025-02-30 Imposible", 4)
        self.assertFalse(res.es_valida)
        self.assertIn("imposible", res.motivo_error.lower())

    def test_05_fecha_con_barras(self):
        res = analizar_linea("[INFO] 2025/02/10 Barras", 5)
        self.assertFalse(res.es_valida)
        self.assertIn("formato", res.motivo_error.lower())

    def test_06_severidad_debug(self):
        res = analizar_linea("[DEBUG] 2025-10-15 Fallo", 6)
        self.assertFalse(res.es_valida)

    def test_07_linea_sin_severidad(self):
        res = analizar_linea("2025-10-15 Hola", 7)
        self.assertFalse(res.es_valida)

    def test_08_linea_sin_mensaje(self):
        res = analizar_linea("[ERROR] 2025-10-15", 8)
        self.assertFalse(res.es_valida)
        
        res2 = analizar_linea("[ERROR] 2025-10-15   ", 9)
        self.assertFalse(res2.es_valida)

    def test_09_linea_vacia(self):
        res = analizar_linea("   \n", 10)
        self.assertFalse(res.es_valida)

    def test_10_mensaje_con_espacios(self):
        res = analizar_linea("[INFO]    Mensaje   con  espacios   ", 11)
        self.assertTrue(res.es_valida)
        self.assertIn("Mensaje   con  espacios", res.mensaje)

    def test_11_archivo_vacio(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            nombre = f.name
        
        try:
            resumen = analizar_archivo(nombre)
            self.assertEqual(resumen.total_lineas, 0)
            self.assertEqual(resumen.eventos_validos, 0)
        finally:
            os.remove(nombre)

    def test_12_a_15_archivo_completo(self):
        contenido = (
            "[INFO] 2025-01-01 Inicio\n"           # 1 (Válido, INFO)
            "WARNING Sin fecha\n"                  # 2 (Válido, WARNING)
            "[DEBUG] Algo\n"                       # 3 (Inválido, severidad)
            "   \n"                                # 4 (Inválido, vacía)
            "[error] 2025-02-30 Falla\n"           # 5 (Inválido, fecha imposible)
            "[ERROR] Fuego\n"                      # 6 (Válido, ERROR)
        )
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            f.write(contenido)
            nombre = f.name
            
        try:
            resumen = analizar_archivo(nombre)
            
            # Conteos correctos
            self.assertEqual(resumen.total_lineas, 6)
            self.assertEqual(resumen.eventos_validos, 3)
            self.assertEqual(resumen.total_info, 1)
            self.assertEqual(resumen.total_warning, 1)
            self.assertEqual(resumen.total_error, 1)
            
            # Número de línea correcto en errores
            self.assertEqual(resumen.resultados[2].numero_linea, 3)
            self.assertFalse(resumen.resultados[2].es_valida)
            
            self.assertEqual(resumen.resultados[4].numero_linea, 5)
            self.assertFalse(resumen.resultados[4].es_valida)
            
        finally:
            os.remove(nombre)
            
    def test_16_analisis_texto_directo(self):
        texto = "[INFO] 2025-01-01 Ok\nERROR Fuego"
        resumen = analizar_texto(texto)
        self.assertEqual(resumen.total_lineas, 2)
        self.assertEqual(resumen.eventos_validos, 2)

    def test_17_html_injection(self):
        # Verifica que el parseo no se rompa con caracteres de inyección
        texto = "[INFO] 2025-01-01 <script>alert(1)</script>"
        res = analizar_linea(texto, 1)
        self.assertTrue(res.es_valida)
        self.assertEqual(res.mensaje, "<script>alert(1)</script>")
