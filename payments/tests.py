from django.test import TestCase, Client
import json

class STKPushTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_stk_push(self):
        response = self.client.post(
            '/stk-push/',
            data=json.dumps({
                "phone": "2547XXXXXXXX",
                "amount": 10,
                "description": "Test Payment"
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('MerchantRequestID', response.json())

