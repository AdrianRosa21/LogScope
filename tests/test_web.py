import unittest
import io
from web import create_app

class TestWebEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app({'TESTING': True})
        self.client = self.app.test_client()

    def test_upload_file(self):
        data = {'file': (io.BytesIO(b"[INFO] 2025-01-01 Todo bien\n"), 'test.txt')}
        res = self.client.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['total_lineas'], 1)
        self.assertEqual(res.json['eventos_validos'], 1)

    def test_upload_text(self):
        res = self.client.post('/upload_text', json={'text': '[ERROR] Fuego'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['total_lineas'], 1)
        self.assertEqual(res.json['total_error'], 1)
        
    def test_agent_triage(self):
        payload = {"total_lineas": 10, "eventos_validos": 10, "total_error": 8, "malformados": 0, "total_warning": 0}
        res = self.client.post('/agent_triage', json=payload)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json["diagnostico_agente"]["prioridad"], "CRITICA")

    def test_export_json(self):
        res = self.client.post('/export', json={'resumen': {'total_lineas': 1, 'eventos_validos': 1}, 'formato': 'json'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['total_lineas'], 1)

    def test_export_txt(self):
        res = self.client.post('/export', json={'resumen': {'total_lineas': 1, 'eventos_validos': 1}, 'formato': 'txt'})
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Total: 1, Validos: 1", res.data)
