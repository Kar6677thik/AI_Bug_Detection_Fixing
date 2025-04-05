import unittest
from fastapi.testclient import TestClient
from backend.api.app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "healthy"})

    def test_analyze_endpoint(self):
        test_code = "def test():\n    return 1 / 0"
        response = self.client.post(
            "/analyze",
            json={"code": test_code, "language": "python"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])

    def test_detect_endpoint(self):
        test_code = "def test():\n    return 1 / 0"
        response = self.client.post(
            "/detect",
            json={"code": test_code, "language": "python"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])

    def test_fix_endpoint(self):
        test_code = "def test():\n    return 1 / 0"
        response = self.client.post(
            "/fix",
            json={"code": test_code, "language": "python"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])

if __name__ == '__main__':
    unittest.main()