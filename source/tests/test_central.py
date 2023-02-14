import unittest
from source.modules.requests.central import Central

class TestCentralMethods(unittest.TestCase):
    def setUp(self):
        self.central = Central(base_url="https://ctlreq-api-qas.telemedicinaeinstein.com.br/core", username="", password="")

    def test_login(self):
        self.central.login()
        self.assertIsNotNone(self.central.access_token)
        self.assertIsNotNone(self.central.user_id)

    def test_search_attendance_records(self):
        self.central.login()
        records = self.central.search_attendance_records(start_date="01-01-2023", end_date="10-01-2023")
        self.assertIsNotNone(records)

    def test_search_activity_records(self):
        self.central.login()
        records = self.central.search_activity_records(start_date="01-01-2023", end_date="10-01-2023")
        self.assertIsNotNone(records)

if __name__ == '__main__':
    unittest.main()
