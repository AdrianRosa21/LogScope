import unittest
from skills.explanation.skill import explain_malformed_line
from skills.triage.skill import summarize_incidents
from skills.validation.skill import validate_logs

class TestSkills(unittest.TestCase):
    def test_explanation_skill(self):
        result = explain_malformed_line("   ", "Línea vacía", 1)
        self.assertEqual(result["numero_linea"], 1)
        self.assertIn("Línea vacía", result["motivo_detectado"])
        self.assertTrue(len(result["explicacion"]) > 0)
        self.assertTrue(len(result["posible_correccion"]) > 0)
        
    def test_triage_skill_empty(self):
        res = summarize_incidents({"total_lineas": 0})
        self.assertTrue(res["falta_evidencia"])
        self.assertEqual(res["prioridad"], "BAJA")
        
    def test_triage_skill_critical(self):
        payload = {
            "total_lineas": 100,
            "eventos_validos": 100,
            "total_error": 51,
            "total_warning": 0,
            "malformados": 0
        }
        res = summarize_incidents(payload)
        self.assertEqual(res["prioridad"], "CRITICA")

    def test_triage_skill_media(self):
        payload = {
            "total_lineas": 100,
            "eventos_validos": 100,
            "total_error": 0,
            "total_warning": 6,
            "malformados": 0
        }
        res = summarize_incidents(payload)
        self.assertEqual(res["prioridad"], "MEDIA")

    def test_validation_skill(self):
        res = validate_logs(text="[INFO] Todo bien")
        self.assertEqual(res["total_lineas"], 1)
        self.assertEqual(res["eventos_validos"], 1)
