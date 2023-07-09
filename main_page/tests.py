from django.test import TestCase


class TestViews(TestCase):

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('On this page you can explore our rich collection of wall materials',
                      response.content.decode())

    def test_materials(self):
        response = self.client.get('/api/wall/materials/')
        self.assertEqual(response.status_code, 200)
